import asyncio
import html
from unittest import mock

from aiogram import Bot
from aiogram.types import Update
from django.test import SimpleTestCase, TestCase, TransactionTestCase, override_settings

from .handlers import DIAGNOSTIC_QUESTIONS, QuizFSM, SupportFSM, normalize_short_answer
from .views import dp


@override_settings(TELEGRAM_WEBHOOK_SECRET='tg-secret')
class TelegramWebhookSecretTests(TestCase):
    @mock.patch('telegram_bot.views.dp')
    def test_update_without_secret_is_rejected(self, dispatcher):
        response = self.client.post('/bot/webhook/', '{}', content_type='application/json')
        self.assertEqual(response.status_code, 403)
        dispatcher.feed_update.assert_not_called()

    @mock.patch('telegram_bot.views.dp')
    def test_update_with_wrong_secret_is_rejected(self, dispatcher):
        response = self.client.post('/bot/webhook/', '{}', content_type='application/json',
                                    HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN='nope')
        self.assertEqual(response.status_code, 403)

    @mock.patch('telegram_bot.views.dp')
    def test_update_with_secret_is_accepted(self, dispatcher):
        response = self.client.post('/bot/webhook/', '{}', content_type='application/json',
                                    HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN='tg-secret')
        self.assertEqual(response.status_code, 200)


@override_settings(TELEGRAM_ADMIN_ID='999')
class BotHandlerTests(TransactionTestCase):
    """Проганяємо оновлення через справжній диспетчер; запити до Telegram підмінені.
    TransactionTestCase: сховище станів пише в базу з окремого потоку (sync_to_async)."""

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.addCleanup(self.loop.close)
        self.bot = Bot(token='42:TEST')
        self.sent = []

        async def fake_call(method, request_timeout=None):
            self.sent.append(method)
            return True
        patcher = mock.patch.object(Bot, '__call__', side_effect=fake_call)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.update_id = 0

    def run_async(self, coro):
        return self.loop.run_until_complete(coro)

    def state(self):
        return dp.fsm.get_context(bot=self.bot, chat_id=100, user_id=100)

    def message_update(self, **content):
        self.update_id += 1
        return Update.model_validate({'update_id': self.update_id, 'message': {
            'message_id': self.update_id, 'date': 0, 'chat': {'id': 100, 'type': 'private'},
            'from': {'id': 100, 'is_bot': False, 'first_name': '<Хакер & Ко>'}, **content}},
            context={'bot': self.bot})

    def feed(self, update):
        return self.run_async(dp.feed_update(self.bot, update))

    def test_sticker_during_short_answer_does_not_crash(self):
        short_index = next(i for i, q in enumerate(DIAGNOSTIC_QUESTIONS) if q['type'] != 'choice')
        self.run_async(self.state().set_state(QuizFSM.answering_short))
        self.run_async(self.state().update_data(current_q=short_index, score=0, wrong_topics=[]))

        self.feed(self.message_update(sticker={'file_id': 'x', 'file_unique_id': 'y', 'type': 'regular',
                                               'width': 1, 'height': 1, 'is_animated': False, 'is_video': False}))

        self.assertTrue(any('текстом' in getattr(m, 'text', '') for m in self.sent))
        self.assertEqual(self.run_async(self.state().get_state()), QuizFSM.answering_short.state)

    def test_sticker_on_button_question_asks_for_button(self):
        self.run_async(self.state().set_state(QuizFSM.answering_choice))
        self.feed(self.message_update(sticker={'file_id': 'x', 'file_unique_id': 'y', 'type': 'regular',
                                               'width': 1, 'height': 1, 'is_animated': False, 'is_video': False}))
        self.feed(self.message_update(text='8'))
        replies = [m.text for m in self.sent if hasattr(m, 'text')]
        self.assertEqual(len(replies), 2)
        self.assertTrue(all('кнопкою' in r for r in replies))

    def test_service_message_ignored(self):
        self.run_async(self.state().set_state(QuizFSM.answering_short))
        self.feed(self.message_update(new_chat_title='x'))
        self.assertEqual(self.sent, [])

    def test_support_question_escapes_html_for_admin(self):
        self.run_async(self.state().set_state(SupportFSM.waiting_for_question))
        self.feed(self.message_update(text='Чому 2 < 3 & <b>?'))
        admin_messages = [m for m in self.sent if getattr(m, 'chat_id', None) == 999]
        self.assertEqual(len(admin_messages), 1)
        self.assertIn(html.escape('Чому 2 < 3 & <b>?'), admin_messages[0].text)
        self.assertIn(html.escape('<Хакер & Ко>'), admin_messages[0].text)

    def test_quiz_state_survives_restart(self):
        from aiogram import Dispatcher
        from aiogram.fsm.storage.base import StorageKey
        from .storage import DjangoStorage
        self.run_async(self.state().set_state(QuizFSM.answering_short))
        self.run_async(self.state().update_data(current_q=7, score=3))

        # «Перезапуск»: новий диспетчер з новим сховищем бачить той самий стан
        fresh = Dispatcher(storage=DjangoStorage())
        key = StorageKey(bot_id=self.bot.id, chat_id=100, user_id=100)
        self.assertEqual(self.run_async(fresh.storage.get_state(key)), QuizFSM.answering_short.state)
        self.assertEqual(self.run_async(fresh.storage.get_data(key)), {'current_q': 7, 'score': 3})

    def test_enrollment_lead_saved_in_admin(self):
        from .handlers import EnrollFSM
        from .models import BotLead
        self.run_async(self.state().set_state(EnrollFSM.phone))
        self.run_async(self.state().update_data(role='Батьки', subject='Заняття (5-10 класи)', name='Тарас',
                                                grade='7', goal='Підтягнути алгебру'))
        self.feed(self.message_update(text='+380991112233'))
        lead = BotLead.objects.get()
        self.assertEqual((lead.name, lead.grade, lead.contact, lead.telegram_id), ('Тарас', '7', '+380991112233', 100))
        self.assertIsNone(self.run_async(self.state().get_state()))

    def test_all_free_pdf_is_stitched_once(self):
        from .handlers import send_all_free_materials

        sent_doc = mock.Mock(document=mock.Mock(file_id='FILE-ID-1'))
        message = mock.AsyncMock()
        message.answer_document.return_value = sent_doc
        message.answer.return_value = mock.AsyncMock()  # повідомлення «⏳ Завантажую…»
        callback = mock.AsyncMock()
        callback.message = message

        stitched = []

        statuses = iter([503, 200, 200])  # перша спроба — збій Cloudinary

        class FakeResp:
            def __init__(self_inner):
                self_inner.status = next(statuses)
            def raise_for_status(self_inner):
                if self_inner.status != 200:
                    raise RuntimeError(f'HTTP {self_inner.status}')
            async def read(self_inner):
                from pypdf import PdfWriter
                import io
                writer = PdfWriter()
                writer.add_blank_page(width=10, height=10)
                buf = io.BytesIO()
                writer.write(buf)
                stitched.append(1)
                return buf.getvalue()
            async def __aenter__(self_inner):
                return self_inner
            async def __aexit__(self_inner, *a):
                return False

        class FakeSession:
            def get(self_inner, url):
                return FakeResp()
            async def __aenter__(self_inner):
                return self_inner
            async def __aexit__(self_inner, *a):
                return False

        async def fake_urls():
            return ['https://res.cloudinary.com/x/1.pdf'], 'fp1'

        with mock.patch('telegram_bot.handlers.get_free_materials_urls', fake_urls), \
                mock.patch('telegram_bot.handlers.aiohttp.ClientSession', FakeSession):
            self.run_async(send_all_free_materials(callback))  # збій: нічого не надіслано й не закешовано
            self.assertEqual(message.answer_document.call_count, 0)
            self.run_async(send_all_free_materials(callback))  # склеєно і закешовано
            self.run_async(send_all_free_materials(callback))  # готовий файл за file_id

        self.assertEqual(len(stitched), 1)
        self.assertEqual(message.answer_document.call_count, 2)
        self.assertEqual(message.answer_document.call_args.kwargs['document'], 'FILE-ID-1')

    def tearDown(self):
        self.run_async(self.state().clear())


class ShortAnswerNormalizeTests(SimpleTestCase):
    def test_decimal_answers_match(self):
        self.assertEqual(normalize_short_answer(' 2,5 '), normalize_short_answer('2.5'))
        self.assertEqual(normalize_short_answer('10 200'), normalize_short_answer('10200'))
        self.assertEqual(normalize_short_answer('Б А В'), normalize_short_answer('бав'))

    def test_separators_and_trailing_dot_accepted(self):
        for typed in ('Б, А, В', 'Б,А,В', 'б.а.в', 'б-а-в', 'бав.'):
            self.assertEqual(normalize_short_answer(typed), normalize_short_answer('бав'), typed)
        self.assertEqual(normalize_short_answer('14.'), normalize_short_answer('14'))

    def test_wrong_numbers_still_rejected(self):
        self.assertNotEqual(normalize_short_answer('1,4'), normalize_short_answer('14'))
        self.assertNotEqual(normalize_short_answer('2.40'), normalize_short_answer('240'))

    def test_all_quiz_answers_match_themselves_typed_with_commas(self):
        for q in DIAGNOSTIC_QUESTIONS:
            if q['type'] != 'choice' and not str(q['ans']).isdigit():
                typed = ', '.join(str(q['ans']).upper())
                self.assertEqual(normalize_short_answer(typed), normalize_short_answer(q['ans']), typed)
