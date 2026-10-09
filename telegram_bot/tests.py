import asyncio
import html
from unittest import mock

from aiogram import Bot
from aiogram.types import Update
from django.test import SimpleTestCase, TestCase, override_settings

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
class BotHandlerTests(SimpleTestCase):
    """Проганяємо оновлення через справжній диспетчер; запити до Telegram підмінені."""

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

    def test_support_question_escapes_html_for_admin(self):
        self.run_async(self.state().set_state(SupportFSM.waiting_for_question))
        self.feed(self.message_update(text='Чому 2 < 3 & <b>?'))
        admin_messages = [m for m in self.sent if getattr(m, 'chat_id', None) == 999]
        self.assertEqual(len(admin_messages), 1)
        self.assertIn(html.escape('Чому 2 < 3 & <b>?'), admin_messages[0].text)
        self.assertIn(html.escape('<Хакер & Ко>'), admin_messages[0].text)

    def tearDown(self):
        self.run_async(self.state().clear())


class ShortAnswerNormalizeTests(SimpleTestCase):
    def test_decimal_answers_match(self):
        self.assertEqual(normalize_short_answer(' 2,5 '), normalize_short_answer('2.5'))
        self.assertEqual(normalize_short_answer('10 200'), normalize_short_answer('10200'))
        self.assertEqual(normalize_short_answer('Б А В'), normalize_short_answer('бав'))
