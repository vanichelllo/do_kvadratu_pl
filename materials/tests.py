import base64
import datetime
import hashlib
import json
import re
from unittest import mock

import ecdsa
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.utils import timezone
from django.utils.html import escapejs

from django.db import models

from .models import (AnswerOption, Cart, CartItem, CurriculumChapter, DiagnosticOffer, CurriculumGrade, CurriculumSubject,
                     CurriculumTopic, GameMistake, Homework, MatchItem, TeacherLicense, Order, OrderItem, PracticeAttempt, PracticeRun, Question, Review, StudentReport,
                     StudyMaterial, TutorStudentRequest, ClassSubscription)

User = get_user_model()


def make_nmt_topic(name, chapter_order=1):
    """Тема з курсу НМТ (класифікатор: курс → клас → розділ → тема)."""
    subject, _ = CurriculumSubject.objects.get_or_create(name='Підготовка до НМТ / ЗНО', defaults={'order': 5})
    grade, _ = CurriculumGrade.objects.get_or_create(subject=subject, name='Підготовка до НМТ')
    chapter, _ = CurriculumChapter.objects.get_or_create(grade=grade, name=f'Розділ {chapter_order}',
                                                         order=chapter_order)
    return CurriculumTopic.objects.create(chapter=chapter, name=name)

# У тестах не ходимо в Cloudinary і не потребуємо collectstatic
TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


# REMINDERS_DAILY=False: інакше ввечері (16–21 за Києвом) кожен запит у тесті запускав би фонову розсилку нагадувань
@override_settings(STORAGES=TEST_STORAGES, TELEGRAM_BOT_TOKEN='', TELEGRAM_ADMIN_ID='', REMINDERS_DAILY=False)
class BaseTestCase(TestCase):
    def run(self, result=None):
        # Лічильники лімітів живуть у кеші процесу — не переносимо їх між тестами
        cache.clear()
        return super().run(result)

    def make_user(self, email, **extra):
        # Користувачі в тестах уже погодилися з офертою (інакше сторінки ведуть на /accept-terms/)
        extra.setdefault('terms_accepted_at', timezone.now())
        extra.setdefault('terms_version', settings.TERMS_VERSION)
        return User.objects.create_user(username=email, email=email, password='Pass12345!', **extra)


class TeacherAccessTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('student@example.com')
        self.victim = self.make_user('victim@example.com')
        self.victim_request = TutorStudentRequest.objects.create(
            user=self.victim, real_name='Учень', course='grade_7', status='approved')
        self.material = StudyMaterial.objects.create(title='1. Тема')
        self.client.force_login(self.user)

    def test_role_teacher_from_profile_gives_no_teacher_panel(self):
        self.client.post('/cabinet/', {'role': 'teacher', 'first_name': '', 'last_name': '',
                                       'phone_number': '', 'target_grade': ''})
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'teacher')

        response = self.client.get('/cabinet/')
        self.assertNotIn(str(self.victim_request.parent_token), response.content.decode())

        self.client.post('/cabinet/add-nmt-score/', {'student_id': self.victim_request.id,
                                                     'material_id': self.material.id, 'score': 18})
        self.assertFalse(PracticeAttempt.objects.filter(user=self.victim).exists())

    def test_role_teacher_cannot_view_foreign_attempt(self):
        self.user.role = 'teacher'
        self.user.save()
        attempt = PracticeAttempt.objects.create(user=self.victim, material=self.material, score=1,
                                                 answers_json={'question_ids': ''})
        response = self.client.get(f'/attempt/{attempt.id}/')
        self.assertEqual(response.status_code, 404)

    def test_staff_sees_teacher_panel(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get('/cabinet/')
        self.assertIn(str(self.victim_request.parent_token), response.content.decode())


class MonoWebhookBase(BaseTestCase):
    def setUp(self):
        cache.clear()
        self.signing_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        pem = self.signing_key.get_verifying_key().to_pem()
        pubkey_response = mock.Mock(status_code=200)
        pubkey_response.json.return_value = {'key': base64.b64encode(pem).decode()}
        patcher = mock.patch('materials.views.requests.get', return_value=pubkey_response)
        self.pubkey_get = patcher.start()
        self.addCleanup(patcher.stop)

        self.user = self.make_user('payer@example.com')
        self.topup = Order.objects.create(user=self.user, total_amount=500, mono_invoice_id='inv-topup')

    def post_webhook(self, payload, sign=True, signing_key=None):
        body = json.dumps(payload).encode()
        headers = {}
        if sign:
            key = signing_key or self.signing_key
            signature = key.sign(body, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
            headers['HTTP_X_SIGN'] = base64.b64encode(signature).decode()
        return self.client.post('/mono/webhook/', body, content_type='application/json', **headers)


class MonoWebhookTests(MonoWebhookBase):
    def test_unsigned_webhook_is_rejected(self):
        response = self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'}, sign=False)
        self.assertEqual(response.status_code, 403)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 0)

    def test_webhook_signed_by_other_key_is_rejected(self):
        fake_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        response = self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'}, signing_key=fake_key)
        self.assertEqual(response.status_code, 403)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 0)

    def test_signed_topup_credits_balance_once(self):
        for _ in range(2):
            response = self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'})
            self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 500)
        self.topup.refresh_from_db()
        self.assertEqual(self.topup.status, 'paid')
        self.assertIsNotNone(self.topup.paid_at)

    def test_signed_purchase_grants_materials(self):
        material = StudyMaterial.objects.create(title='5. Тема', price=200)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, material=material)
        order = Order.objects.create(user=self.user, total_amount=200, mono_invoice_id='inv-buy')
        OrderItem.objects.create(order=order, material=material, price=200)

        response = self.post_webhook({'invoiceId': 'inv-buy', 'status': 'success'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(material, self.user.purchased_materials.all())
        self.assertFalse(cart.items.exists())
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 0)

    def test_garbage_signature_is_rejected(self):
        body = json.dumps({'invoiceId': 'inv-topup', 'status': 'success'})
        for garbage in ('not base64!', base64.b64encode(b'not a DER signature').decode()):
            response = self.client.post('/mono/webhook/', body, content_type='application/json', HTTP_X_SIGN=garbage)
            self.assertEqual(response.status_code, 403)

    def test_bad_signatures_do_not_refetch_key_every_time(self):
        fake_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        for _ in range(5):
            self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'}, signing_key=fake_key)
        self.assertEqual(self.pubkey_get.call_count, 1)

    def test_rotated_key_is_refetched(self):
        cache.set('monobank_pubkey', base64.b64encode(
            ecdsa.SigningKey.generate(curve=ecdsa.NIST256p).get_verifying_key().to_pem()).decode())
        response = self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.pubkey_get.call_count, 1)

    def test_pubkey_unavailable_returns_503(self):
        self.pubkey_get.side_effect = ConnectionError('down')
        response = self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'})
        self.assertEqual(response.status_code, 503)


class PayFromBalanceTests(BaseTestCase):
    def test_pay_from_balance_deducts_and_grants(self):
        user = self.make_user('buyer@example.com', balance=300)
        material = StudyMaterial.objects.create(title='3. Тема', price=200)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, material=material)
        self.client.force_login(user)

        self.assertRedirects(self.client.get('/cart/pay/balance/'), '/cart/')  # GET не платить
        self.client.post('/cart/pay/balance/', {'agree': 'on'})
        self.client.post('/cart/pay/balance/', {'agree': 'on'})  # повторний клік нічого не списує

        user.refresh_from_db()
        self.assertEqual(user.balance, 100)
        self.assertIn(material, user.purchased_materials.all())
        order = Order.objects.get(user=user, status='paid')
        self.assertIsNotNone(order.instant_access_agreed_at)

    def test_payment_needs_cart_checkbox(self):
        # Без галочки в Кошику (оферта, п. 14.1) сервер не приймає оплату — навіть якщо обійти перевірку в браузері
        user = self.make_user('buyer2@example.com', balance=300)
        material = StudyMaterial.objects.create(title='4. Тема', price=200)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, material=material)
        self.client.force_login(user)
        with mock.patch('materials.views.requests.post') as mono_post:
            for url in ('/cart/pay/balance/', '/cart/pay/mono/'):
                for data in ({}, {'agree': ''}):
                    self.assertRedirects(self.client.post(url, data), '/cart/', fetch_redirect_response=False)
        mono_post.assert_not_called()
        user.refresh_from_db()
        self.assertEqual(user.balance, 300)
        self.assertFalse(Order.objects.filter(user=user).exists())
        self.assertContains(self.client.get('/cart/'), 'поставте галочку')

    def test_card_payment_records_cart_checkbox(self):
        user = self.make_user('buyer3@example.com')
        material = StudyMaterial.objects.create(title='5. Тема', price=200)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, material=material)
        self.client.force_login(user)
        with mock.patch('materials.views.requests.post') as mono_post:
            mono_post.return_value.json.return_value = {'invoiceId': 'inv-1', 'pageUrl': 'https://pay.mbnk.biz/inv-1'}
            response = self.client.post('/cart/pay/mono/', {'agree': 'on'})
        self.assertRedirects(response, 'https://pay.mbnk.biz/inv-1', fetch_redirect_response=False)
        self.assertIsNotNone(Order.objects.get(user=user).instant_access_agreed_at)


class SiteIconTests(BaseTestCase):
    ICON = 'images/favicon.svg'

    def test_manifest_lists_big_icons(self):
        response = self.client.get('/site.webmanifest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/manifest+json')
        data = json.loads(response.content)
        self.assertEqual(data['short_name'], 'ДО КВАДРАТУ')
        sizes = {(icon['sizes'], icon.get('purpose', 'any')) for icon in data['icons']}
        self.assertEqual(sizes, {('192x192', 'any'), ('512x512', 'any'),
                                 ('192x192', 'maskable'), ('512x512', 'maskable')})
        self.assertTrue(all(icon['src'].startswith('/static/images/icon-') for icon in data['icons']))

    def test_phones_find_big_icon_at_standard_address(self):
        for url in ('/apple-touch-icon.png', '/apple-touch-icon-precomposed.png'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, url)
            self.assertIn('images/apple-touch-icon', response['Location'])

    def test_icon_files_exist(self):
        from django.contrib.staticfiles import finders
        for name in ('favicon.svg', 'favicon-32.png', 'favicon.ico', 'apple-touch-icon.png', 'icon-192.png',
                     'icon-512.png', 'icon-maskable-192.png', 'icon-maskable-512.png'):
            self.assertIsNotNone(finders.find(f'images/{name}'), name)

    def test_standalone_pages_and_admin_have_icon(self):
        kid = self.make_user('kid@example.com')
        student = TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')
        material = StudyMaterial.objects.create(title='1. Тема', is_free=True, is_published=True,
                                                html_content='<p>x</p>')
        kid.purchased_materials.add(material)
        question = Question.objects.create(question_type='CHOICE', text='2+2?')
        question.materials.add(material)
        AnswerOption.objects.create(question=question, text='4', is_correct=True)
        pages = {'parent': f'/parents/{student.parent_token}/', 'admin': '/do-kvadratu-secret-control/login/'}
        for name, url in pages.items():
            self.assertContains(self.client.get(url), self.ICON, msg_prefix=name)
        self.client.force_login(kid)
        for name, url in {'reader': f'/download/{material.id}/', 'practice': f'/practice/{material.id}/',
                          'cabinet': '/cabinet/'}.items():
            self.assertContains(self.client.get(url), self.ICON, msg_prefix=name)

    def test_icons_are_not_behind_consent_page(self):
        user = User.objects.create_user(username='new', email='new@example.com', password='x')  # без згоди
        self.client.force_login(user)
        self.assertEqual(self.client.get('/site.webmanifest').status_code, 200)
        self.assertEqual(self.client.get('/apple-touch-icon.png').status_code, 302)
        self.assertIn('images/apple-touch-icon', self.client.get('/apple-touch-icon.png')['Location'])


class CabinetSectionsTests(BaseTestCase):
    def test_teacher_sections_collapsed_library_open(self):
        boss = self.make_user('boss@example.com', is_staff=True)
        kid = self.make_user('kid@example.com')
        TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')
        PracticeAttempt.objects.create(user=kid, material=StudyMaterial.objects.create(title='1. Тема'),
                                       score=5, max_score=10)
        self.client.force_login(boss)
        html = self.client.get('/cabinet/').content.decode()
        for key in ('journal', 'students', 'library', 'topup', 'review', 'settings'):
            # Розділ — <details> з заголовком <summary> (згортається натисканням); відкрита за замовчуванням
            # лише бібліотека — основний вміст кабінету
            tag = re.search(rf'<details\b[^>]*\bdata-section="{key}"[^>]*>', html)
            self.assertIsNotNone(tag, key)
            if key == 'library':
                self.assertRegex(tag.group(0), r'\sopen(?=[\s>=])', key)
            else:
                self.assertNotRegex(tag.group(0), r'\sopen(?=[\s>=])', key)
            self.assertRegex(html, rf'data-section="{key}"[^>]*>\s*<summary>', key)

    def test_student_does_not_see_teacher_sections(self):
        from materials.models import StudentPresentation
        kid = self.make_user('kid@example.com')
        PracticeAttempt.objects.create(user=kid, material=StudyMaterial.objects.create(title='1. Тема'),
                                       score=5, max_score=10)
        StudentPresentation.objects.create(student=kid, title='Урок 1', html_content='<p>x</p>')
        self.client.force_login(kid)
        response = self.client.get('/cabinet/')
        self.assertNotContains(response, 'data-section="journal"')
        self.assertNotContains(response, 'data-section="students"')
        for key in ('attempts', 'lessons', 'library'):
            self.assertContains(response, f'data-section="{key}"', msg_prefix=key)

    def test_settings_open_when_form_has_errors(self):
        self.client.force_login(self.make_user('kid@example.com'))
        response = self.client.post('/cabinet/', {'role': 'no-such-role', 'first_name': '', 'last_name': '',
                                                  'phone_number': '', 'target_grade': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-section="settings" open>')


    @staticmethod
    def panel_of(html, key):
        """Вкладка, у якій лежить розділ: найближча відкрита перед ним панель data-tab-panel"""
        pos = html.index(f'data-section="{key}"')
        return re.findall(r'data-tab-panel="(\w+)"', html[:pos])[-1]

    def test_teacher_cabinet_split_into_tabs(self):
        boss = self.make_user('boss@example.com', is_staff=True)
        kid = self.make_user('kid@example.com')
        TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')
        PracticeAttempt.objects.create(user=kid, material=StudyMaterial.objects.create(title='1. Тема'),
                                       score=5, max_score=10)
        self.client.force_login(boss)
        html = self.client.get('/cabinet/').content.decode()
        self.assertIn('data-default="teach"', html)
        for tab in ('learn', 'teach', 'account'):
            self.assertIn(f'role="tab" data-tab="{tab}"', html)
        expected = {'journal': 'teach', 'students': 'teach', 'library': 'learn',
                    'topup': 'account', 'review': 'account', 'settings': 'account'}
        for key, tab in expected.items():
            self.assertEqual(self.panel_of(html, key), tab, key)

    def test_student_tabs_without_teaching(self):
        kid = self.make_user('kid@example.com')
        PracticeAttempt.objects.create(user=kid, material=StudyMaterial.objects.create(title='1. Тема'),
                                       score=5, max_score=10)
        self.client.force_login(kid)
        html = self.client.get('/cabinet/').content.decode()
        self.assertIn('data-default="learn"', html)
        self.assertNotIn('data-tab="teach"', html)
        self.assertEqual(self.panel_of(html, 'attempts'), 'learn')
        response = self.client.post('/cabinet/', {'role': 'no-such-role', 'first_name': '', 'last_name': '',
                                                  'phone_number': '', 'target_grade': ''})
        self.assertContains(response, 'data-default="account"')



class CabinetNextStepTests(BaseTestCase):
    def setUp(self):
        self.kid = self.make_user('kid@example.com')
        self.lessons = [StudyMaterial.objects.create(title=f'{n}. Тема', price=50, is_published=True,
                                                     html_content='<p>урок</p>') for n in (1, 2, 3)]
        self.client.force_login(self.kid)

    def next_step(self):
        return self.client.get('/cabinet/').context['next_step']

    def test_new_user_is_sent_to_diagnostic(self):
        step = self.next_step()
        self.assertEqual(step['url'], '/diagnostic/')
        self.assertContains(self.client.get('/cabinet/'), 'Що далі')

    def test_next_lesson_after_last_practised(self):
        self.kid.purchased_materials.add(*self.lessons)
        self.assertEqual(self.next_step()['url'], f'/download/{self.lessons[0].id}/')
        PracticeAttempt.objects.create(user=self.kid, material=self.lessons[0], score=5, max_score=10)
        step = self.next_step()
        self.assertEqual((step['title'], step['url']), ('Наступний урок', f'/download/{self.lessons[1].id}/'))
        for lesson in self.lessons[1:]:
            PracticeAttempt.objects.create(user=self.kid, material=lesson, score=5, max_score=10)
        self.assertIsNone(self.next_step())

    def test_homework_comes_first(self):
        self.kid.purchased_materials.add(*self.lessons)
        request = TutorStudentRequest.objects.create(user=self.kid, real_name='Учень', course='grade_5', status='approved')
        Homework.objects.create(student=request, material=self.lessons[2],
                                due_date=timezone.localdate() + datetime.timedelta(days=3))
        step = self.next_step()
        self.assertEqual((step['title'], step['url']), ('Домашнє завдання', f'/practice/{self.lessons[2].id}/'))

    def test_teacher_has_no_next_step(self):
        self.client.force_login(self.make_user('boss@example.com', is_staff=True))
        self.assertNotIn('next_step', self.client.get('/cabinet/').context)


class GuestCartTests(BaseTestCase):
    def setUp(self):
        self.lesson = StudyMaterial.objects.create(title='1. Числа', price=100, is_published=True)
        self.free = StudyMaterial.objects.create(title='Формули', is_free=True, is_published=True)
        self.user = self.make_user('guest@example.com')
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        app = SocialApp.objects.create(provider='google', name='Google', client_id='id', secret='secret')
        app.sites.add(Site.objects.get_current())

    def test_guest_choice_waits_in_cart_after_login(self):
        self.assertContains(self.client.get(f'/material/{self.lesson.id}/', follow=True), 'можна через Google')
        response = self.client.post(f'/cart/add/{self.lesson.id}/')
        self.assertRedirects(response, '/login/?next=/cart/', fetch_redirect_response=False)
        self.client.post(f'/cart/add/{self.free.id}/')
        login = self.client.post('/login/?next=/cart/', {'login': 'guest@example.com', 'password': 'Pass12345!'})
        self.assertRedirects(login, '/cart/', fetch_redirect_response=False)
        self.assertTrue(CartItem.objects.filter(cart__user=self.user, material=self.lesson).exists())
        self.assertTrue(self.user.purchased_materials.filter(id=self.free.id).exists())
        self.assertNotIn('pending_cart', self.client.session)

    def test_owned_material_is_not_added_again(self):
        self.user.purchased_materials.add(self.lesson)
        self.client.post(f'/cart/add/{self.lesson.id}/')
        self.client.post('/login/', {'login': 'guest@example.com', 'password': 'Pass12345!'})
        self.assertFalse(CartItem.objects.filter(material=self.lesson).exists())

    def test_cart_shows_consent_and_support_contact(self):
        CartItem.objects.create(cart=Cart.objects.create(user=self.user), material=self.lesson)
        self.client.force_login(self.user)
        page = self.client.get('/cart/')
        self.assertContains(page, 'id="agree-checkbox"')
        self.assertContains(page, 'прошу відкрити матеріали одразу після оплати')
        self.assertContains(page, '(пункт 14.2)')
        self.assertContains(page, 'https://t.me/do_kvadratu_bot')

    def test_login_page_keeps_next_for_signup(self):
        self.assertContains(self.client.get('/login/?next=/cart/'), '/register/?next=/cart/')


class PricesPageTests(BaseTestCase):
    def test_prices_page_lists_all_options(self):
        StudyMaterial.objects.create(title='Тема', price=35, is_published=True)   # без теми в дереві — НМТ
        StudyMaterial.objects.create(title='Дешевша, але прихована', price=5)
        lesson = StudyMaterial.objects.create(title='Урок', price=60, is_published=True)
        bundle = StudyMaterial.objects.create(title='Пакет', price=80, is_bundle=True, is_published=True)
        bundle.included_materials.add(lesson, StudyMaterial.objects.get(title='Тема'))
        page = self.client.get('/prices/')
        self.assertContains(page, 'Підготовка до НМТ')
        self.assertContains(page, 'від 35 ₴')
        self.assertContains(page, 'Пакети тем — від 80 ₴, економія до 15 ₴')
        self.assertContains(page, 'Міні-групи — 240 ₴')
        self.assertContains(page, '/booking/')
        self.assertContains(page, '/for-tutors/')
        self.assertContains(self.client.get('/'), 'href="/prices/"')
        self.assertContains(self.client.get('/booking/'), '490 грн')
        self.assertIn('/prices/', self.client.get('/sitemap.xml').content.decode())


class NavigationTests(BaseTestCase):
    def test_short_menu_and_single_main_button(self):
        page = self.client.get('/').content.decode()
        menu = page[page.index('id="navLinks"'):page.index('</nav>')]
        footer = page[page.index('<footer'):page.index('</footer>')]
        for url in ('/materials/', '/diagnostic/', '/prices/', '/booking/'):
            self.assertIn(f'href="{url}', menu)
        for url in ('/about/', '/game/'):
            self.assertNotIn(f'href="{url}', menu)
            self.assertIn(f'href="{url}', footer)
        self.assertNotIn('ВІТРИНА', menu)   # без капслоку
        self.assertEqual(page.count('class="hero-btn"'), 1)

class ParentMaterialTests(BaseTestCase):
    def setUp(self):
        self.kid = self.make_user('kid@example.com')
        self.student = TutorStudentRequest.objects.create(user=self.kid, real_name='Учень', course='nmt',
                                                          status='approved')
        self.passed = StudyMaterial.objects.create(title='7. Квадратні рівняння', html_content='<p>note-seven</p>',
                                                   is_published=True)
        self.not_passed = StudyMaterial.objects.create(title='8. Дробові рівняння', html_content='<p>Конспект 8</p>',
                                                       is_published=True)
        self.no_html = StudyMaterial.objects.create(title='9. Корені', is_published=True)
        self.empty_html = StudyMaterial.objects.create(title='10. Ірраціональні рівняння', html_content='',
                                                       is_published=True)
        self.diag = StudyMaterial.objects.create(title='Вхідне діагностичне тестування НМТ',
                                                 html_content='<p>x</p>')
        for material in (self.passed, self.passed, self.no_html, self.empty_html, self.diag):
            PracticeAttempt.objects.create(user=self.kid, material=material, score=5, max_score=10)

    def url(self, material, token=None):
        return f'/parents/{token or self.student.parent_token}/topic/{material.id}/'

    def test_dashboard_lists_notes_of_passed_topics_once(self):
        response = self.client.get(f'/parents/{self.student.parent_token}/')
        self.assertContains(response, 'Пройдені презентації')
        self.assertContains(response, self.url(self.passed), count=1)
        for material in (self.not_passed, self.no_html, self.empty_html, self.diag):
            self.assertNotContains(response, self.url(material))

    def test_parent_opens_passed_topic_without_student_buttons(self):
        response = self.client.get(self.url(self.passed))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'note-seven')  # презентація (у json_script)
        self.assertContains(response, f'href="/parents/{self.student.parent_token}/"')  # кнопка «Назад»
        self.assertNotContains(response, '/practice/')
        self.assertEqual(response['Referrer-Policy'], 'no-referrer')

    def test_only_passed_topics_of_approved_nmt_students(self):
        for material in (self.not_passed, self.no_html, self.empty_html, self.diag):
            self.assertEqual(self.client.get(self.url(material)).status_code, 404, material.title)
        # Конспект іншого учня за своїм посиланням не відкрити
        other = TutorStudentRequest.objects.create(user=self.make_user('other@example.com'), real_name='Інший',
                                                   course='nmt', status='approved')
        self.assertEqual(self.client.get(self.url(self.passed, other.parent_token)).status_code, 404)
        TutorStudentRequest.objects.filter(pk=self.student.pk).update(status='pending')
        self.assertEqual(self.client.get(self.url(self.passed)).status_code, 404)
        # Батьки школяра теж бачать пройдені презентації
        TutorStudentRequest.objects.filter(pk=self.student.pk).update(status='approved', course='grade_7')
        self.assertEqual(self.client.get(self.url(self.passed)).status_code, 200)

    def test_parent_sees_how_the_test_went(self):
        question = Question.objects.create(text='Скільки буде 2 + 2?', question_type='SHORT', correct_short_answer='4')
        attempt = PracticeAttempt.objects.create(
            user=self.kid, material=self.passed, score=0, max_score=2,
            answers_json={'question_ids': str(question.id), 'q_short': {str(question.id): '5'}})
        dashboard = self.client.get(f'/parents/{self.student.parent_token}/')
        detail_url = f'/parents/{self.student.parent_token}/attempt/{attempt.id}/'
        self.assertContains(dashboard, detail_url)
        response = self.client.get(detail_url)
        self.assertContains(response, 'Скільки буде 2 + 2?')
        self.assertContains(response, '← До звіту')
        self.assertEqual(response['Referrer-Policy'], 'no-referrer')
        # Чужу спробу за своїм посиланням не відкрити
        other = TutorStudentRequest.objects.create(user=self.make_user('other2@example.com'), real_name='Інший',
                                                   course='nmt', status='approved')
        self.assertEqual(self.client.get(f'/parents/{other.parent_token}/attempt/{attempt.id}/').status_code, 404)

    def test_parent_reader_hides_pdf_link(self):
        StudyMaterial.objects.filter(pk=self.passed.pk).update(file='documents/7.pdf')
        with mock.patch.object(StudyMaterial._meta.get_field('file').storage, 'url',
                               return_value='https://cdn.example/7.pdf'):
            response = self.client.get(self.url(self.passed))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="action-btn btn-download"')
        self.assertNotContains(response, 'cdn.example/7.pdf')

    def test_unpublished_draft_stays_hidden(self):
        draft = StudyMaterial.objects.create(title='11. Чернетка', html_content='<p>secret-draft</p>',
                                             is_free=True, is_published=False)
        self.client.force_login(self.kid)
        # Практика з чернетки закрита навіть для безкоштовної — і батьки її не побачать
        self.assertEqual(self.client.post(f'/practice/{draft.id}/', {'question_ids': ''}).status_code, 404)
        PracticeAttempt.objects.create(user=self.kid, material=draft, score=0, max_score=0)  # стара спроба
        self.client.logout()
        self.assertEqual(self.client.get(self.url(draft)).status_code, 404)
        self.assertNotContains(self.client.get(f'/parents/{self.student.parent_token}/'), self.url(draft))
        # Учень має чернетку в бібліотеці (видав викладач) — тоді батьки бачать
        self.kid.purchased_materials.add(draft)
        self.assertEqual(self.client.get(self.url(draft)).status_code, 200)

    def test_parent_lesson_page_hides_referrer(self):
        from materials.models import StudentPresentation
        lesson = StudentPresentation.objects.create(student=self.kid, title='Урок 9', html_content='<p>x</p>')
        response = self.client.get(f'/parents/{self.student.parent_token}/lesson/{lesson.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Referrer-Policy'], 'no-referrer')

    def test_score_from_lesson_also_opens_topic(self):
        boss = self.make_user('boss@example.com', is_staff=True)
        self.client.force_login(boss)
        self.client.post('/cabinet/add-nmt-score/', {'student_id': self.student.id,
                                                     'material_id': self.not_passed.id, 'score': 7,
                                                     'max_score': 10})
        self.client.logout()
        self.assertEqual(self.client.get(self.url(self.not_passed)).status_code, 200)


class ParentDashboardTests(BaseTestCase):
    def test_each_student_has_own_working_parent_link(self):
        requests_ = [
            TutorStudentRequest.objects.create(user=self.make_user(f's{i}@example.com'), real_name=f'Учень {i}',
                                               course='nmt', status='approved')
            for i in range(2)
        ]
        self.assertNotEqual(requests_[0].parent_token, requests_[1].parent_token)
        for student_request in requests_:
            response = self.client.get(f'/parents/{student_request.parent_token}/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, student_request.real_name)
            # Секретне посилання не має потрапляти до інших сайтів (наприклад, Google Analytics)
            self.assertContains(response, '<meta name="referrer" content="no-referrer">')

    def test_parent_link_works_only_for_approved_students(self):
        for status in ('pending', 'rejected'):
            student = TutorStudentRequest.objects.create(user=self.make_user(f'{status}@example.com'),
                                                         real_name='Учень', course='nmt', status=status)
            self.assertEqual(self.client.get(f'/parents/{student.parent_token}/').status_code, 404)
            self.client.post(f'/parents/{student.parent_token}/review/',
                             {'reviewer_name': 'Мама', 'rating': '5', 'text': 'Дякуємо'})
        self.assertFalse(Review.objects.exists())

    def test_revoke_access_keeps_materials_student_paid_for(self):
        from django.contrib import admin
        from django.test import RequestFactory
        nmt = make_nmt_topic('1. Числа')
        bought = StudyMaterial.objects.create(title='Куплена тема', price=25, curriculum_topic=nmt, is_published=True)
        in_bundle = StudyMaterial.objects.create(title='Тема з пакета', price=25, curriculum_topic=nmt, is_published=True)
        bundle = StudyMaterial.objects.create(title='Пакет', price=100, curriculum_topic=nmt, is_bundle=True, is_published=True)
        bundle.included_materials.add(in_bundle)
        given = StudyMaterial.objects.create(title='Видана тема', price=25, curriculum_topic=nmt, is_published=True)
        kid = self.make_user('kid@example.com')
        kid.purchased_materials.add(bought, in_bundle, given)
        order = Order.objects.create(user=kid, total_amount=125, status='paid')
        OrderItem.objects.create(order=order, material=bought, price=25)
        OrderItem.objects.create(order=order, material=bundle, price=100)
        student = TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')

        request = RequestFactory().post('/')
        request.user = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[TutorStudentRequest]
        action = model_admin.get_actions(request)['revoke_student_access'][0]
        with mock.patch('materials.admin.messages.success'):
            action(model_admin, request, TutorStudentRequest.objects.filter(pk=student.pk))
        self.assertEqual(set(kid.purchased_materials.all()), {bought, in_bundle})

    def test_revoke_access_keeps_everything_if_a_paid_bundle_was_deleted(self):
        from django.contrib import admin
        from django.test import RequestFactory
        nmt = make_nmt_topic('1. Числа')
        bundle = StudyMaterial.objects.create(title='Пакет', price=100, curriculum_topic=nmt, is_bundle=True)
        topic = StudyMaterial.objects.create(title='Тема з пакета', price=25, curriculum_topic=nmt, is_published=True)
        bundle.included_materials.add(topic)
        kid = self.make_user('kid2@example.com')
        kid.purchased_materials.add(topic)
        order = Order.objects.create(user=kid, total_amount=100, status='paid')
        OrderItem.objects.create(order=order, material=bundle, price=100)
        bundle.delete()  # OrderItem.material стає NULL — уже не видно, що було в пакеті
        student = TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')

        request = RequestFactory().post('/')
        request.user = self.make_user('boss2@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[TutorStudentRequest]
        action = model_admin.get_actions(request)['revoke_student_access'][0]
        with mock.patch('materials.admin.messages.success'), mock.patch('materials.admin.messages.warning') as warn:
            action(model_admin, request, TutorStudentRequest.objects.filter(pk=student.pk))
        self.assertEqual(set(kid.purchased_materials.all()), {topic})
        warn.assert_called_once()

    def test_revoke_access_keeps_everything_if_an_old_purchase_was_deleted(self):
        from django.contrib import admin
        from django.test import RequestFactory
        from users.models import PurchaseHistory
        topic = StudyMaterial.objects.create(title='Тема', price=25, is_published=True)
        old_bundle = StudyMaterial.objects.create(title='Старий пакет', price=100, is_bundle=True)
        kid = self.make_user('kid3@example.com')
        kid.purchased_materials.add(topic)
        PurchaseHistory.objects.create(student=kid, material=old_bundle, price_paid=100)
        old_bundle.delete()  # покупка старим способом: матеріал став NULL
        student = TutorStudentRequest.objects.create(user=kid, real_name='Учень', course='nmt', status='approved')

        request = RequestFactory().post('/')
        request.user = self.make_user('boss3@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[TutorStudentRequest]
        action = model_admin.get_actions(request)['revoke_student_access'][0]
        with mock.patch('materials.admin.messages.success'), mock.patch('materials.admin.messages.warning') as warn:
            action(model_admin, request, TutorStudentRequest.objects.filter(pk=student.pk))
        self.assertEqual(set(kid.purchased_materials.all()), {topic})
        warn.assert_called_once()

    def test_admin_can_regenerate_parent_link(self):
        from django.contrib import admin
        from django.test import RequestFactory
        student = TutorStudentRequest.objects.create(user=self.make_user('kid@example.com'), real_name='Учень',
                                                     course='nmt', status='approved')
        old_token = student.parent_token
        request = RequestFactory().post('/')
        request.user = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[TutorStudentRequest]
        action = model_admin.get_actions(request)['regenerate_parent_links'][0]
        with mock.patch('materials.admin.messages.success'):
            action(model_admin, request, TutorStudentRequest.objects.filter(pk=student.pk))
        student.refresh_from_db()
        self.assertNotEqual(student.parent_token, old_token)
        self.assertEqual(self.client.get(f'/parents/{old_token}/').status_code, 404)
        self.assertEqual(self.client.get(f'/parents/{student.parent_token}/').status_code, 200)


class BotApiTests(BaseTestCase):
    def setUp(self):
        self.make_user('kid@example.com', telegram_id='12345')

    def test_library_api_closed_without_token(self):
        response = self.client.get('/api/bot/library/12345/')
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(b'kid@example.com', response.content)

    @override_settings(BOT_API_TOKEN='bot-secret')
    def test_library_api_requires_correct_token(self):
        self.assertEqual(self.client.get('/api/bot/library/12345/', HTTP_X_BOT_TOKEN='wrong').status_code, 403)
        response = self.client.get('/api/bot/library/12345/', HTTP_X_BOT_TOKEN='bot-secret')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['student_email'], 'kid@example.com')



class ReviewTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('reader@example.com', first_name='Профіль')
        self.material = StudyMaterial.objects.create(title='7. Квадратні рівняння', price=100, is_published=True)
        self.client.force_login(self.user)

    @mock.patch('materials.views.send_telegram_notification')
    def test_material_page_review_form_submits(self, notify):
        page = self.client.get(f'/material/{self.material.id}/', follow=True)
        self.assertContains(page, 'name="reviewer_name"')

        self.client.post('/submit-review/', {'rating': 5, 'text': 'Корисно', 'reviewer_name': 'Оля',
                                             'material_id': self.material.id})
        review = Review.objects.get(material=self.material)
        self.assertEqual(review.reviewer_name, 'Оля')

        review.is_approved = True
        review.save()
        page = self.client.get(f'/material/{self.material.id}/', follow=True)
        self.assertContains(page, 'Оля')
        self.assertNotContains(page, 'Профіль')

    @mock.patch('materials.views.send_telegram_notification')
    def test_home_shows_reviewer_name_not_profile_name(self, notify):
        Review.objects.create(user=self.user, reviewer_name='Мама Тараса', text='Дякуємо', is_approved=True)
        old = Review.objects.create(user=self.user, text='Старий відгук', is_approved=True)  # reviewer_name = «Анонім»
        Review.objects.filter(id=old.id).update(created_at=datetime.datetime(2026, 9, 1, tzinfo=datetime.timezone.utc))
        page = self.client.get('/')
        self.assertContains(page, 'Мама Тараса')
        self.assertContains(page, 'Профіль')  # старий відгук показує ім'я з профілю, як і раніше

    @mock.patch('materials.views.send_telegram_notification')
    def test_invalid_rating_rejected(self, notify):
        for rating in (999, 0, 'abc'):
            self.client.post('/submit-review/', {'rating': rating, 'text': 't', 'reviewer_name': 'n'})
        self.assertFalse(Review.objects.exists())
        notify.assert_not_called()

    @mock.patch('materials.views.send_telegram_notification')
    def test_telegram_message_is_html_escaped(self, notify):
        self.client.post('/submit-review/', {'rating': 4, 'text': 'x < y & <b>', 'reviewer_name': '<Оля>'})
        message = notify.call_args[0][0]
        self.assertIn('x &lt; y &amp; &lt;b&gt;', message)
        self.assertIn('&lt;Оля&gt;', message)

    @mock.patch('materials.views.send_telegram_notification')
    def test_redirect_back_stays_on_site(self, notify):
        response = self.client.post('/submit-review/', {'rating': 5, 'text': 't', 'reviewer_name': 'n'},
                                    HTTP_REFERER='https://evil.example.com/')
        self.assertEqual(response.url, '/cabinet/')


class PurchaseAccessTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('buyer2@example.com', balance=1000)
        self.lesson1 = StudyMaterial.objects.create(title='1. Числа', price=100, is_published=True)
        self.lesson2 = StudyMaterial.objects.create(title='2. Дроби', price=100, is_published=True)
        self.bundle = StudyMaterial.objects.create(title='Пакет', price=150, is_bundle=True, is_published=True)
        self.bundle.included_materials.add(self.lesson1, self.lesson2)
        self.client.force_login(self.user)

    def test_owned_bundle_cannot_be_added_again(self):
        self.user.purchased_materials.add(self.lesson1, self.lesson2)
        page = self.client.get(f'/material/{self.bundle.id}/', follow=True)
        self.assertContains(page, 'ВИ ВЖЕ ПРИДБАЛИ')
        self.client.post(f'/cart/add/{self.bundle.id}/')
        self.assertFalse(CartItem.objects.filter(material=self.bundle).exists())

    def test_partially_owned_bundle_can_be_bought(self):
        self.user.purchased_materials.add(self.lesson1)
        self.client.post(f'/cart/add/{self.bundle.id}/')
        self.assertTrue(CartItem.objects.filter(material=self.bundle).exists())

    def test_legacy_buy_endpoint_removed(self):
        self.assertEqual(self.client.post(f'/buy/{self.bundle.id}/').status_code, 404)

    def test_state_changing_endpoints_ignore_get(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, material=self.lesson1)
        expected = {f'/cart/add/{self.lesson2.id}/': self.lesson2.get_absolute_url(),
                    f'/cart/remove/{item.id}/': '/cart/', '/cart/pay/balance/': '/cart/', '/cart/pay/mono/': '/cart/'}
        for url, target in expected.items():
            self.assertRedirects(self.client.get(url), target, fetch_redirect_response=False, msg_prefix=url)
        self.assertFalse(CartItem.objects.filter(material=self.lesson2).exists())
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 1000)
        self.assertTrue(CartItem.objects.filter(id=item.id).exists())

    def test_foreign_site_post_without_csrf_token_is_rejected(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(f'/cart/add/{self.lesson1.id}/').status_code, 403)

    def test_unpublished_material_hidden_from_strangers(self):
        hidden = StudyMaterial.objects.create(title='Чернетка', price=100, is_published=False)
        self.assertEqual(Client().get(f'/material/{hidden.id}/', follow=True).status_code, 404)
        self.assertEqual(self.client.get(f'/material/{hidden.id}/', follow=True).status_code, 404)
        self.client.post(f'/cart/add/{hidden.id}/')
        self.assertFalse(CartItem.objects.filter(material=hidden).exists())

        self.user.purchased_materials.add(hidden)
        self.assertEqual(self.client.get(f'/material/{hidden.id}/', follow=True).status_code, 200)

    def test_owner_of_unpublished_bundle_sees_it(self):
        self.user.purchased_materials.add(self.lesson1, self.lesson2)
        StudyMaterial.objects.filter(id=self.bundle.id).update(is_published=False)
        self.assertContains(self.client.get(f'/material/{self.bundle.id}/', follow=True), 'ВИ ВЖЕ ПРИДБАЛИ')

    def test_staff_preview_of_unpublished_has_no_buy_button(self):
        hidden = StudyMaterial.objects.create(title='Чернетка', price=100, is_published=False)
        self.user.is_staff = True
        self.user.save()
        page = self.client.get(f'/material/{hidden.id}/', follow=True)
        self.assertContains(page, 'не опубліковано')
        self.assertNotContains(page, 'ДОДАТИ В КОШИК')

    def test_bundle_granted_directly_counts_as_owned(self):
        self.user.purchased_materials.add(self.bundle)
        self.assertContains(self.client.get(f'/material/{self.bundle.id}/', follow=True), 'ВИ ВЖЕ ПРИДБАЛИ')
        self.client.post(f'/cart/add/{self.bundle.id}/')
        self.assertFalse(CartItem.objects.filter(material=self.bundle).exists())

    def test_practice_of_unpublished_material_is_404_without_title_leak(self):
        hidden = StudyMaterial.objects.create(title='Секретна тема', price=100, is_published=False)
        response = self.client.get(f'/practice/{hidden.id}/', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, 'Секретна тема', status_code=404)

    def test_practice_post_ignores_questions_from_other_lessons(self):
        own = Question.objects.create(text='own', question_type='SHORT', correct_short_answer='1')
        own.materials.add(self.lesson1)
        foreign = Question.objects.create(text='foreign', question_type='SHORT', correct_short_answer='SECRET-42')
        foreign.materials.add(self.lesson2)
        self.user.purchased_materials.add(self.lesson1)

        response = self.client.post(f'/practice/{self.lesson1.id}/', {'question_ids': f'{own.id},{foreign.id}'})
        self.assertNotContains(response, 'SECRET-42')
        self.assertEqual(response.context['max_score'], 2)

    def test_practice_requires_purchase(self):
        question = Question.objects.create(text='2+2', question_type='SHORT', correct_short_answer='4')
        question.materials.add(self.lesson1)

        response = self.client.get(f'/practice/{self.lesson1.id}/')
        self.assertRedirects(response, self.lesson1.get_absolute_url(), fetch_redirect_response=False)
        self.client.post(f'/practice/{self.lesson1.id}/', {'question_ids': str(question.id), f'q_{question.id}': '4'})
        self.assertFalse(PracticeAttempt.objects.exists())

        self.user.purchased_materials.add(self.lesson1)
        self.assertEqual(self.client.get(f'/practice/{self.lesson1.id}/').status_code, 200)

    @mock.patch.object(StudyMaterial._meta.get_field('file').storage, 'url',
                       return_value='https://res.cloudinary.com/demo/raw/upload/documents/lesson.pdf')
    @mock.patch('materials.views.requests.get')
    def test_reader_does_not_download_pdf(self, requests_get, storage_url):
        StudyMaterial.objects.filter(id=self.lesson1.id).update(file='documents/lesson.pdf')
        self.user.purchased_materials.add(self.lesson1)
        response = self.client.get(f'/download/{self.lesson1.id}/')
        self.assertEqual(response.status_code, 200)
        requests_get.assert_not_called()
        self.assertEqual(self.client.get(f'/download/{self.lesson2.id}/').status_code, 404)


class AnswerCheckingTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('pupil@example.com')
        self.client.force_login(self.user)
        self.q1 = Question.objects.create(text='q1', question_type='CHOICE')
        self.q1_wrong = AnswerOption.objects.create(question=self.q1, text='A')
        AnswerOption.objects.create(question=self.q1, text='B', is_correct=True)
        self.q2 = Question.objects.create(text='q2', question_type='CHOICE')
        self.q2_right = AnswerOption.objects.create(question=self.q2, text='C', is_correct=True)
        self.match = Question.objects.create(text='m', question_type='MATCH')
        opt = AnswerOption.objects.create(question=self.match, text='А')
        self.match_item = MatchItem.objects.create(question=self.match, text='1', correct_option=opt)

    def test_option_from_other_question_does_not_score(self):
        response = self.client.post('/diagnostic/', {'question_ids': f'{self.q1.id}',
                                                     f'question_{self.q1.id}': self.q2_right.id})
        self.assertEqual(response.context['total_score'], 0)

    def test_garbage_input_does_not_crash(self):
        response = self.client.post('/diagnostic/', {
            'question_ids': f'abc,{self.q1.id},,{self.match.id},99999999999999999999999',
            f'question_{self.q1.id}': 'xyz',
            f'match_{self.match_item.id}': 'not-a-number',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['max_score'], 4)

    def test_correct_answers_still_score(self):
        right = self.q1.options.get(is_correct=True)
        response = self.client.post('/diagnostic/', {
            'question_ids': f'{self.q1.id},{self.match.id}',
            f'question_{self.q1.id}': right.id,
            f'match_{self.match_item.id}': self.match_item.correct_option_id,
        })
        self.assertEqual(response.context['total_score'], 2)


class DiagnosticResultsTests(BaseTestCase):
    def setUp(self):
        self.topic = make_nmt_topic('12. Відсотки')
        self.question = Question.objects.create(text='q', question_type='CHOICE', curriculum_topic=self.topic)
        AnswerOption.objects.create(question=self.question, text='A', is_correct=True)
        self.wrong = AnswerOption.objects.create(question=self.question, text='B', is_correct=False)
        self.linked = StudyMaterial.objects.create(title='12. Відсотки', is_published=True,
                                                   curriculum_topic=self.topic)
        self.hidden = StudyMaterial.objects.create(title='Чернетка', is_published=False, curriculum_topic=self.topic)

    def test_weak_topic_recommends_published_materials_of_that_topic(self):
        response = self.client.post('/diagnostic/', {'question_ids': str(self.question.id),
                                                     f'question_{self.question.id}': str(self.wrong.id)})
        self.assertIn(self.linked, response.context['recommendations'])
        self.assertNotIn(self.hidden, response.context['recommendations'])
        self.assertContains(response, 'Записатися на заняття')
        self.assertContains(response, "diagnostic_complete")
        # Гість бачить, що результат не збережено, і пропозицію зареєструватися
        self.assertContains(response, 'не збережено')


class LessonPreviewTests(BaseTestCase):
    @staticmethod
    def slides_html(count):
        slides = ''.join(f'<section class="slide-card" data-slide="{n}"><p>Слайд-{n}</p>'
                         f'<section class="inner">вкладена</section></section>' for n in range(1, count + 1))
        return f'<html><head><title>Урок</title></head><body>{slides}<script>go()</script></body></html>'

    def setUp(self):
        self.lesson = StudyMaterial.objects.create(title='1.1 Числа', price=100, is_published=True,
                                                   html_content=self.slides_html(8))

    def test_preview_shows_only_first_slides(self):
        page = self.client.get(f'/material/{self.lesson.id}/preview/')
        self.assertEqual(page.status_code, 200)
        html = page.context['preview_html']
        for n in (1, 2, 3):
            self.assertIn(f'Слайд-{n}<', html)
        for n in (4, 8):
            self.assertNotIn(f'Слайд-{n}<', html)
        self.assertIn('ще 5 слайдів', html)
        self.assertIn('<script>go()</script>', html)
        self.assertNotIn('Слайд-8', page.content.decode())
        self.assertContains(page, 'Придбати повний урок')

    def test_detail_page_links_to_preview(self):
        self.assertContains(self.client.get(f'/material/{self.lesson.id}/', follow=True), f'/material/{self.lesson.id}/preview/')

    def test_no_preview_for_owner_free_or_short_lessons(self):
        user = self.make_user('owner@example.com')
        user.purchased_materials.add(self.lesson)
        self.client.force_login(user)
        self.assertNotContains(self.client.get(f'/material/{self.lesson.id}/', follow=True), '/preview/')
        self.assertRedirects(self.client.get(f'/material/{self.lesson.id}/preview/'),
                             f'/download/{self.lesson.id}/', fetch_redirect_response=False)
        self.client.logout()
        short = StudyMaterial.objects.create(title='Короткий', price=100, is_published=True,
                                             html_content=self.slides_html(2))
        hidden = StudyMaterial.objects.create(title='Чернетка', price=100, html_content=self.slides_html(8))
        for material in (short, hidden):
            self.assertEqual(self.client.get(f'/material/{material.id}/preview/').status_code, 404)
        free = StudyMaterial.objects.create(title='Безкоштовний', is_free=True, is_published=True,
                                            html_content=self.slides_html(8))
        self.assertNotContains(self.client.get(f'/material/{free.id}/', follow=True), '/preview/')


class SeoTests(BaseTestCase):
    def test_sitemap_lists_published_materials_on_main_domain(self):
        published = StudyMaterial.objects.create(title='Тема', is_published=True)
        hidden = StudyMaterial.objects.create(title='Прихована', is_published=False)
        body = self.client.get('/sitemap.xml').content.decode()
        self.assertIn(f'https://dokvadratu.com.ua{published.get_absolute_url()}', body)
        self.assertNotIn(f'/material/{hidden.id}-', body)
        self.assertIn('https://dokvadratu.com.ua/booking/', body)
        self.assertIn('Sitemap: https://dokvadratu.com.ua/sitemap.xml', self.client.get('/robots.txt').content.decode())

    def test_material_page_has_canonical_and_own_description(self):
        material = StudyMaterial.objects.create(title='Квадратні рівняння', description='Усе про дискримінант',
                                                is_published=True)
        page = self.client.get(f'{material.get_absolute_url()}?utm_source=telegram')
        self.assertContains(page, f'<link rel="canonical" href="https://dokvadratu.com.ua{material.get_absolute_url()}">',
                            html=False)
        self.assertContains(page, '<meta name="description" content="Усе про дискримінант">', html=False)
        self.assertContains(page, 'content="Квадратні рівняння | ДО КВАДРАТУ"')
        self.assertContains(page, 'social_banner.jpg')

    def test_favicon_redirects_to_static_icon(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('images/favicon.ico'))


class TeacherFormsTests(BaseTestCase):
    def setUp(self):
        self.teacher = self.make_user('teacher@example.com', is_staff=True)
        self.student = TutorStudentRequest.objects.create(user=self.make_user('kid2@example.com'),
                                                          real_name='Учень', course='grade_7', status='approved')
        self.material = StudyMaterial.objects.create(title='1. Тема')
        self.topic = make_nmt_topic('Дроби')
        self.client.force_login(self.teacher)

    def report_data(self, **overrides):
        data = {'student_id': self.student.id, 'curriculum_topic': self.topic.id, 'nush_modeling': 10, 'nush_solving': 9,
                'nush_analysis': 8, 'homework_status': 'completed', 'teacher_comment': ''}
        data.update(overrides)
        return data

    def test_valid_report_saved(self):
        self.client.post('/cabinet/add-report/', self.report_data())
        self.assertEqual(StudentReport.objects.get().nush_solving, 9)

    def test_parent_sees_short_summary_of_lesson(self):
        # Батьки просили «у два слова»: підготовка, відповіді, старанність — угорі сторінки
        self.client.post('/cabinet/add-report/', self.report_data(readiness='ready', answers='hints', effort='trying',
                                                                 teacher_comment='Молодець'))
        report = StudentReport.objects.get()
        self.assertEqual(report.summary_items, ['✅ Підготовка: добра', '💬 Відповіді: з підказками', '💪 Старається',
                                                'ДЗ: 🟢 Виконано повністю'])
        page = Client().get(f'/parents/{self.student.parent_token}/')
        self.assertContains(page, 'Останнє заняття')
        self.assertContains(page, '💬 Відповіді: з підказками', count=1)
        self.assertNotContains(page, 'Попередні заняття')
        self.assertContains(page, '<details class="nush-details', html=False)

    def test_summary_is_optional(self):
        self.client.post('/cabinet/add-report/', self.report_data(homework_status='not_assigned'))
        self.assertEqual(StudentReport.objects.get().summary_items, [])
        self.client.post('/cabinet/add-report/', self.report_data(effort='hack'))
        self.assertEqual(StudentReport.objects.count(), 1)

    def test_bad_report_shows_error_instead_of_500(self):
        for bad in ({'nush_modeling': ''}, {'nush_modeling': 13}, {'curriculum_topic': ''}, {'homework_status': 'hack'}):
            response = self.client.post('/cabinet/add-report/', self.report_data(**bad))
            self.assertEqual(response.status_code, 302)
        self.assertFalse(StudentReport.objects.exists())

    def test_nmt_score_validated(self):
        base = {'student_id': self.student.id, 'material_id': self.material.id}
        for score, max_score in ((-1, 18), (20, 18), ('x', 18), (5, 0)):
            response = self.client.post('/cabinet/add-nmt-score/', dict(base, score=score, max_score=max_score))
            self.assertEqual(response.status_code, 302)
        self.assertFalse(PracticeAttempt.objects.exists())
        self.client.post('/cabinet/add-nmt-score/', dict(base, score=15, max_score=18))
        self.assertEqual(PracticeAttempt.objects.get().score, 15)


class TopupTests(BaseTestCase):
    @mock.patch('materials.views.requests.post')
    def test_bad_amounts_do_not_crash_or_create_orders(self, mono_post):
        self.client.force_login(self.make_user('t@example.com'))
        for amount in ('nan', 'inf', '-5', '0', '10.5', ''):
            response = self.client.post('/cabinet/topup/', {'amount': amount})
            self.assertEqual(response.status_code, 302, amount)
        self.assertFalse(Order.objects.exists())
        mono_post.assert_not_called()

    @mock.patch('materials.views.requests.post')
    def test_valid_amount_creates_invoice(self, mono_post):
        mono_post.return_value.json.return_value = {'pageUrl': 'https://pay.mbnk.biz/x', 'invoiceId': 'inv1'}
        self.client.force_login(self.make_user('t2@example.com'))
        response = self.client.post('/cabinet/topup/', {'amount': '250'})
        self.assertEqual(response.url, 'https://pay.mbnk.biz/x')
        self.assertEqual(mono_post.call_args.kwargs['json']['amount'], 25000)
        self.assertIn('timeout', mono_post.call_args.kwargs)


class ReviewDisplayNameTests(BaseTestCase):
    def test_anonymous_choice_is_respected_for_new_reviews(self):
        user = self.make_user('anon@example.com', first_name='Тарас')
        review = Review.objects.create(user=user, reviewer_name='Анонім', text='t', is_approved=True)
        self.assertEqual(review.display_name, 'Анонім')

        Review.objects.filter(id=review.id).update(created_at=datetime.datetime(2026, 9, 1, tzinfo=datetime.timezone.utc))
        review.refresh_from_db()
        self.assertEqual(review.display_name, 'Тарас')  # старий відгук до появи поля


class HalloweenDecorTests(BaseTestCase):
    def home(self, day):
        with mock.patch('materials.context_processors.timezone.localdate', return_value=day):
            return self.client.get('/').content.decode()

    def test_decor_only_from_17_october_to_1_november(self):
        for day in (datetime.date(2026, 10, 17), datetime.date(2026, 10, 31), datetime.date(2026, 11, 1)):
            page = self.home(day)
            self.assertIn('Математичні страшилки', page, day)
            self.assertIn('hero-section halloween', page, day)
        for day in (datetime.date(2026, 10, 16), datetime.date(2026, 11, 2), datetime.date(2027, 3, 1)):
            self.assertNotIn('Математичні страшилки', self.home(day), day)

    def test_site_wide_decor_on_other_pages(self):
        with mock.patch('materials.context_processors.timezone.localdate', return_value=datetime.date(2026, 10, 31)):
            for url in ('/materials/', '/booking/', '/diagnostic/'):
                page = self.client.get(url).content.decode()
                self.assertIn('hw-site-bat', page, url)
                self.assertIn('щасливого Хелловіну', page, url)
        with mock.patch('materials.context_processors.timezone.localdate', return_value=datetime.date(2026, 11, 2)):
            self.assertNotIn('hw-site-bat', self.client.get('/materials/').content.decode())


class DangerousAdminActionsTests(BaseTestCase):
    def test_data_wiping_actions_removed(self):
        from django.contrib import admin
        from django.test import RequestFactory
        request = RequestFactory().get('/')
        request.user = self.make_user('boss2@example.com', is_staff=True, is_superuser=True)
        for model in (Question, StudyMaterial):
            names = set(admin.site._registry[model].get_actions(request))
            self.assertFalse(names & {'populate_nmt_test', 'import_materials_from_excel'}, model.__name__)


class PromoBannerTests(BaseTestCase):
    def render(self, url, day):
        with mock.patch('materials.models.timezone.localdate', return_value=day):
            return self.client.get(url).content.decode()

    def test_teacher_day_banners_removed(self):
        # Акція до Дня вчителя скінчилась: банерів і знижки на заняття немає навіть у її дати
        day = datetime.date(2026, 10, 11)
        self.assertNotIn('Акція до Дня Вчителя', self.render('/', day))
        booking = self.render('/booking/', day)
        self.assertNotIn('Акція до Дня Вчителя', booking)
        self.assertNotIn('192 грн', booking)
        self.assertIn('240 грн', booking)

    def test_booking_explains_first_lesson(self):
        booking = self.client.get('/booking/').content.decode()
        for text in ('Онлайн у Zoom', '60 хвилин', 'Перше заняття безкоштовне', 'визначимо рівень знань',
                     'href="#calendar"', 'id="calendar"', '490 грн'):
            self.assertIn(text, booking)



class PromoCodeTests(BaseTestCase):
    """Промокоди з адмінки: строк дії, стеля −30%, один раз на покупця, не сумуються зі знижкою за діагностикою."""

    def setUp(self):
        from .models import PromoCode
        self.PromoCode = PromoCode
        self.user = self.make_user('promo@example.com', balance=1000)
        self.lesson = StudyMaterial.objects.create(title='1. Тема', price=100, is_published=True)
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, material=self.lesson)
        self.client.force_login(self.user)

    def apply(self, code):
        return self.client.post('/cart/', {'action': 'apply_promo', 'promo_code': code}, follow=True)

    def total(self):
        return Cart.objects.get(pk=self.cart.pk).get_total_price()

    def test_code_from_admin_applies_case_insensitive_within_dates(self):
        today = timezone.localdate()
        self.PromoCode.objects.create(code='осінь', discount_percent=20, starts_on=today,
                                      ends_on=today + datetime.timedelta(days=3))
        self.assertContains(self.apply(' Осінь '), 'Промокод ОСІНЬ застосовано: −20%')
        self.assertEqual(self.total(), 80)
        self.assertContains(self.client.get('/cart/'), 'АКТИВОВАНО: ОСІНЬ (−20%)')

    def test_wrong_expired_future_and_disabled_codes(self):
        today = timezone.localdate()
        self.assertContains(self.apply('НЕМАЄ'), 'Такого промокоду немає')
        self.PromoCode.objects.create(code='МИНУВ', discount_percent=10, starts_on=today - datetime.timedelta(days=9),
                                      ends_on=today - datetime.timedelta(days=1))
        self.assertContains(self.apply('минув'), 'Термін дії цього промокоду минув')
        self.PromoCode.objects.create(code='СКОРО', discount_percent=10, starts_on=today + datetime.timedelta(days=2))
        self.assertContains(self.apply('скоро'), 'почне діяти з')
        promo = self.PromoCode.objects.create(code='ДІЄ', discount_percent=10)
        self.apply('діє')
        self.assertEqual(self.total(), 90)
        promo.is_active = False   # вимкнено в адмінці — знижка зникає й з кошика
        promo.save()
        self.assertEqual(self.total(), 100)

    def test_discount_is_capped_at_30_percent(self):
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.PromoCode(code='БАГАТО', discount_percent=40).full_clean()
        self.PromoCode.objects.create(code='БАГАТО', discount_percent=40)   # в обхід форми — однаково не більше 30%
        self.apply('багато')
        self.assertEqual(self.total(), 70)

    def test_once_per_user_and_recorded_in_order(self):
        self.PromoCode.objects.create(code='РАЗ', discount_percent=10)
        self.apply('раз')
        with mock.patch('materials.views.send_telegram_notification'):
            self.client.post('/cart/pay/balance/', {'agree': 'on'})
        order = Order.objects.get(user=self.user)
        self.assertEqual((order.promo_code, int(order.total_amount)), ('РАЗ', 90))
        CartItem.objects.create(cart=self.cart, material=StudyMaterial.objects.create(title='2. Тема', price=100))
        self.assertEqual(self.total(), 100)
        self.assertContains(self.apply('раз'), 'Ви вже скористалися цим промокодом')

    def test_promo_and_diagnostic_discounts_do_not_add_up(self):
        self.PromoCode.objects.create(code='МАЛО', discount_percent=5)
        offer = DiagnosticOffer.objects.create(user=self.user, discount_percent=15,
                                               expires_at=timezone.now() + datetime.timedelta(hours=1))
        offer.materials.add(self.lesson)
        self.assertContains(self.apply('мало'), 'знижка за діагностикою вигідніша')
        self.assertEqual(self.total(), 85)
        page = self.client.get('/cart/')
        self.assertContains(page, 'Знижка за діагностикою')
        self.assertContains(page, 'Знижки не сумуються')
        self.PromoCode.objects.filter(code='МАЛО').update(discount_percent=25)
        self.assertEqual(self.total(), 75)


class CabinetStudentNameTests(BaseTestCase):
    def test_apostrophe_and_script_in_name_are_safe(self):
        teacher = self.make_user('t@example.com', is_staff=True)
        for course, name in (('grade_7', "Мар'яна"), ('nmt', "x');alert(1);//")):
            TutorStudentRequest.objects.create(user=self.make_user(f'{course}@example.com'), real_name=name,
                                               course=course, status='approved')
        self.client.force_login(teacher)
        html = self.client.get('/cabinet/').content.decode()
        self.assertNotIn("openReportForm('", html)
        self.assertNotIn("openNmtForm('", html)
        self.assertIn('data-student-name="Мар&#x27;яна"', html)
        self.assertNotIn("alert(1);//')", html)


class CourseChoicesTests(BaseTestCase):
    def test_form_offers_every_grade_with_its_own_value(self):
        self.client.force_login(self.make_user('kid5@example.com'))
        html = self.client.get('/cabinet/').content.decode()
        for value, label in TutorStudentRequest.COURSE_CHOICES:
            self.assertIn(f'<option value="{value}">{label}</option>', html)

    @mock.patch('materials.views.send_telegram_notification')
    def test_grade_5_saved_as_grade_5(self, notify):
        user = self.make_user('kid6@example.com')
        self.client.force_login(user)
        self.client.post('/request-student/', {'real_name': 'Учень', 'course': 'grade_5'})
        self.assertEqual(TutorStudentRequest.objects.get(user=user).course, 'grade_5')


class OwnClassAccessTests(BaseTestCase):
    """Учень власника сайту (чи репетитора з підпискою), підтверджений у класі, бачить усі теми свого класу
    (і лише їх) без купівлі."""

    def setUp(self):
        from django.core.management import call_command
        call_command('import_curriculum', stdout=open('/dev/null', 'w'))
        topic = lambda grade, subject, start: CurriculumTopic.objects.get(
            chapter__grade__name=grade, chapter__grade__subject__name=subject, name__startswith=start)
        lesson = lambda t: StudyMaterial.objects.create(title=t.name, curriculum_topic=t, html_content='<p>урок</p>')
        self.algebra9 = lesson(topic('9 клас', 'Алгебра (7-9 класи)', '1.3. '))
        self.geometry9 = lesson(topic('9 клас', 'Геометрія (7-9 класи)', '2.4. '))
        self.algebra8 = lesson(topic('8 клас', 'Алгебра (7-9 класи)', '1.1. '))
        self.pupil = self.make_user('pupil9@example.com')
        self.request = TutorStudentRequest.objects.create(user=self.pupil, real_name='Соломія', course='grade_9',
                                                          status='approved')
        self.client.force_login(self.pupil)

    def test_cabinet_library_has_filter_by_course_and_title(self):
        html = self.client.get('/cabinet/').content.decode()
        self.assertIn('id="lib-search"', html)
        self.assertRegex(html, r'<option value="[^"]*9 клас[^"]*">')
        self.assertIn(f'data-title="{self.algebra9.title.lower()}"', html)

    def test_approved_pupil_opens_every_course_of_own_grade_only(self):
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/download/{self.geometry9.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/download/{self.algebra8.id}/').status_code, 404)
        html = self.client.get('/cabinet/').content.decode()
        self.assertIn(self.algebra9.title, html)
        self.assertIn(self.geometry9.title, html)
        self.assertNotIn(self.algebra8.title, html)

    def test_pending_request_or_other_teachers_pupil_gets_nothing(self):
        self.request.status = 'pending'
        self.request.save()
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 404)
        self.request.status = 'approved'
        self.request.teacher = self.make_user('tutor@example.com')
        self.request.save()
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 404)

    def test_tutors_pupil_opens_own_grade_while_subscription_is_active(self):
        tutor = self.make_user('tutor@example.com')
        self.request.teacher = tutor
        self.request.save()
        license_ = TeacherLicense.objects.create(teacher=tutor, scope='school',
                                                 valid_until=timezone.localdate() + datetime.timedelta(days=30))
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/download/{self.geometry9.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/download/{self.algebra8.id}/').status_code, 404)
        self.assertIn(self.geometry9.title, self.client.get('/cabinet/').content.decode())
        # Підписка лише на НМТ чи прострочена — повного доступу до класу немає
        license_.scope = 'nmt'
        license_.save()
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 404)
        license_.scope = 'school'
        license_.valid_until = timezone.localdate() - datetime.timedelta(days=1)
        license_.save()
        self.assertEqual(self.client.get(f'/download/{self.algebra9.id}/').status_code, 404)


class AdminLoginRateLimitTests(BaseTestCase):
    def setUp(self):
        cache.clear()
        self.admin_user = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        self.url = '/do-kvadratu-secret-control/login/'

    def login(self, password):
        return self.client.post(self.url, {'username': 'boss@example.com', 'password': password})

    def test_lockout_after_repeated_failures(self):
        for _ in range(10):
            self.assertEqual(self.login('wrong').status_code, 200)
        self.assertEqual(self.login('wrong').status_code, 429)
        self.assertEqual(self.login('Pass12345!').status_code, 429)  # навіть правильний пароль чекає

    def test_success_resets_counter(self):
        for _ in range(5):
            self.login('wrong')
        self.assertEqual(self.login('Pass12345!').status_code, 302)
        self.client.logout()
        for _ in range(9):
            self.assertEqual(self.login('wrong').status_code, 200)

    def test_unicode_lookalike_email_shares_the_counter(self):
        for _ in range(10):
            self.login('wrong')
        lookalike = 'ｂoss@example.com'  # повноширинна «b»
        response = self.client.post(self.url, {'username': lookalike, 'password': 'Pass12345!'})
        self.assertEqual(response.status_code, 429)
        response = self.client.post(self.url, {'username': ' BOSS@example.com ', 'password': 'wrong'})
        self.assertEqual(response.status_code, 429)

    def test_unknown_emails_do_not_fill_the_cache(self):
        from django.core.cache import cache as default_cache
        for i in range(50):
            self.client.post(self.url, {'username': f'junk{i}@example.com', 'password': 'x'})
        self.assertFalse(any('admin-login-failures' in str(k) for k in default_cache._cache))

    def test_robots_does_not_reveal_admin_url(self):
        self.assertNotIn('secret-control', self.client.get('/robots.txt').content.decode())


class DrfAuthTests(BaseTestCase):
    def test_api_ignores_basic_auth(self):
        # Раніше DRF перевіряв логін/пароль із заголовка — підбір паролів в обхід лімітів allauth
        self.make_user('victim2@example.com')
        bad = base64.b64encode(b'victim2@example.com:wrong').decode()
        response = self.client.get('/api/materials/', HTTP_AUTHORIZATION=f'Basic {bad}')
        self.assertEqual(response.status_code, 200)


class PasswordResetTests(BaseTestCase):
    def test_old_url_redirects_to_allauth(self):
        self.assertRedirects(self.client.get('/reset_password/'), '/accounts/password/reset/',
                             fetch_redirect_response=False)
        self.assertContains(self.client.get('/accounts/password/reset/'), 'ЗАБУЛИ ПАРОЛЬ?')

    def test_google_only_user_gets_reset_link(self):
        from django.core import mail
        user = self.make_user('google@example.com')
        user.set_unusable_password()
        user.save()
        response = self.client.post('/accounts/password/reset/', {'email': 'google@example.com'})
        self.assertRedirects(response, '/accounts/password/reset/done/', fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/accounts/password/reset/key/', mail.outbox[0].body)


class ImportMaterialsCommandTests(BaseTestCase):
    """Команду запускає Render при кожному деплої (Build Command: ./build.sh && python manage.py import_materials)."""

    def setUp(self):
        import os
        import tempfile
        from openpyxl import Workbook
        from pypdf import PdfWriter

        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, 'import_files'))
        wb = Workbook()
        ws = wb.active
        ws.append(['Назва матеріалу', 'Ціна', 'Файл', 'Безкоштовно (1/0)', 'Пакет (1/0)'])
        ws.append(['1. Числові множини', 0, '1. Числові множини.pdf', 1, 0])
        ws.append(['2. Нова тема', 19, '2. Нова тема.pdf', 0, 0])
        ws.append(['Вся алгебра для НМТ', 399, 'Bundle_01.pdf', 0, 1])
        wb.save(os.path.join(self.tmp, 'matrix.xlsx'))
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with open(os.path.join(self.tmp, 'import_files', '2. Нова тема.pdf'), 'wb') as f:
            writer.write(f)

        self.old_cwd = os.getcwd()
        os.chdir(self.tmp)
        self.addCleanup(os.chdir, self.old_cwd)

        from django.core.files.storage import InMemoryStorage
        patcher = mock.patch.object(StudyMaterial._meta.get_field('file'), 'storage', InMemoryStorage())
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_command(self):
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('import_materials', stdout=out)
        return out.getvalue()

    def test_existing_materials_are_not_touched(self):
        existing = StudyMaterial.objects.create(title='1. Числові множини', price=99, is_published=False,
                                                is_free=False)
        self.run_command()
        existing.refresh_from_db()
        self.assertEqual((existing.price, existing.is_published, existing.is_free), (99, False, False))
        self.assertFalse(existing.file)

    def test_new_rows_are_created_once(self):
        self.run_command()
        self.run_command()
        self.assertEqual(StudyMaterial.objects.count(), 3)
        new = StudyMaterial.objects.get(title='2. Нова тема')
        self.assertEqual((new.price, new.is_published, new.is_free), (25, True, False))
        self.assertTrue(new.file)
        bundle = StudyMaterial.objects.get(title='Вся алгебра для НМТ')
        self.assertEqual((bundle.price, bundle.is_bundle), (399, True))
        self.assertFalse(bundle.file)  # PDF немає — матеріал створено без файлу



class ErrorAlertTests(BaseTestCase):
    def emit_error(self, path='/broken/'):
        import logging
        import sys
        from django.test import RequestFactory
        try:
            raise ValueError('щось зламалось <b>')
        except ValueError:
            logging.getLogger('django.request').error('Internal Server Error: %s', path, exc_info=sys.exc_info(),
                                                      extra={'status_code': 500, 'request': RequestFactory().get(path)})

    @override_settings(TELEGRAM_BOT_TOKEN='123:abc', TELEGRAM_ADMIN_ID='42')
    @mock.patch('do_kvadratu.logging_handlers.requests.post')
    def test_500_alert_sent_once_per_cooldown(self, post):
        self.emit_error()
        self.emit_error()
        self.assertEqual(post.call_count, 1)
        text = post.call_args.kwargs['json']['text']
        self.assertIn('/broken/', text)
        self.assertIn('ValueError', text)
        self.assertIn('&lt;b&gt;', text)
        self.emit_error('/other/')
        self.assertEqual(post.call_count, 2)

    @mock.patch('do_kvadratu.logging_handlers.requests.post', side_effect=ConnectionError('down'))
    @override_settings(TELEGRAM_BOT_TOKEN='123:abc', TELEGRAM_ADMIN_ID='42')
    def test_alert_failure_does_not_break_request(self, post):
        self.emit_error()  # не повинно кинути виняток


class MonoStatusTests(MonoWebhookBase):
    """Відмови, прострочення, повернення і сторінка результату оплати."""

    def test_failure_and_expired_cancel_pending_order(self):
        for status, invoice in (('failure', 'inv-f'), ('expired', 'inv-e')):
            order = Order.objects.create(user=self.user, total_amount=100, mono_invoice_id=invoice)
            self.post_webhook({'invoiceId': invoice, 'status': status})
            order.refresh_from_db()
            self.assertEqual(order.status, 'cancelled')
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 0)

    @mock.patch('materials.views.send_telegram_notification')
    def test_reversal_after_payment_marks_refunded_and_alerts(self, notify):
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'})
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'reversed'})
        self.topup.refresh_from_db()
        self.assertEqual(self.topup.status, 'refunded')
        self.assertIn('Повернення коштів', notify.call_args[0][0])

    def test_success_arriving_after_reversal_is_ignored(self):
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'reversed'})
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'success'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 0)

    def test_processing_status_changes_nothing(self):
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'processing'})
        self.topup.refresh_from_db()
        self.assertEqual(self.topup.status, 'pending')

    def test_result_page_checks_status_when_webhook_lost(self):
        status_response = mock.Mock()
        status_response.json.return_value = {'status': 'success'}
        self.client.force_login(self.user)
        with mock.patch('materials.views.requests.get', return_value=status_response) as get:
            response = self.client.get(f'/payment/result/{self.topup.id}/')
        self.assertContains(response, 'Оплата пройшла успішно')
        self.assertEqual(get.call_args.kwargs['params'], {'invoiceId': 'inv-topup'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 500)

    def test_result_page_pending_and_failed(self):
        self.client.force_login(self.user)
        with mock.patch('materials.views.requests.get', side_effect=ConnectionError('down')):
            self.assertContains(self.client.get(f'/payment/result/{self.topup.id}/'), 'Чекаємо підтвердження')
        Order.objects.filter(id=self.topup.id).update(status='cancelled')
        self.assertContains(self.client.get(f'/payment/result/{self.topup.id}/'), 'Оплата не пройшла')

    def test_result_page_hidden_from_other_users(self):
        self.client.force_login(self.make_user('stranger@example.com'))
        self.assertEqual(self.client.get(f'/payment/result/{self.topup.id}/').status_code, 404)

    @mock.patch('materials.views.requests.post')
    def test_invoice_redirects_back_to_result_page(self, mono_post):
        mono_post.return_value.json.return_value = {'pageUrl': 'https://pay.mbnk.biz/x', 'invoiceId': 'inv-new'}
        self.client.force_login(self.user)
        self.client.post('/cabinet/topup/', {'amount': '100'})
        order = Order.objects.get(mono_invoice_id='inv-new')
        self.assertEqual(mono_post.call_args.kwargs['json']['redirectUrl'],
                         f'https://dokvadratu.com.ua/payment/result/{order.id}/')

    def test_admin_action_checks_pending_orders(self):
        from django.contrib import admin
        from django.test import RequestFactory
        status_response = mock.Mock()
        status_response.json.return_value = {'status': 'expired'}
        request = RequestFactory().post('/')
        request.user = self.make_user('boss3@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[Order]
        with mock.patch('materials.views.requests.get', return_value=status_response), \
                mock.patch.object(model_admin, 'message_user'):
            model_admin.check_monobank_status(request, Order.objects.all())
        self.topup.refresh_from_db()
        self.assertEqual(self.topup.status, 'cancelled')


class SignupWithoutEmailTests(BaseTestCase):
    @override_settings(EMAIL_BACKEND='materials.tests.BrokenEmailBackend')
    def test_signup_survives_smtp_failure(self):
        response = self.client.post('/register/', {
            'email': 'newkid@example.com', 'password1': 'Strong-Pass-2026!', 'password2': 'Strong-Pass-2026!',
            'terms': 'on'})
        self.assertNotEqual(response.status_code, 500)
        self.assertTrue(User.objects.filter(email='newkid@example.com').exists())


class BrokenEmailBackend:
    def __init__(self, *args, **kwargs):
        pass

    def send_messages(self, messages):
        raise OSError('Gmail daily limit exceeded')


class SpamLimitTests(BaseTestCase):
    @mock.patch('materials.views.send_telegram_notification')
    def test_review_limit(self, notify):
        self.client.force_login(self.make_user('spammer@example.com'))
        for i in range(7):
            self.client.post('/submit-review/', {'rating': 5, 'text': f'т{i}', 'reviewer_name': 'n'})
        self.assertEqual(Review.objects.count(), 5)
        self.assertEqual(notify.call_count, 5)

    @mock.patch('materials.views.send_telegram_notification')
    def test_question_error_limit(self, notify):
        self.client.force_login(self.make_user('spammer2@example.com'))
        question = Question.objects.create(text='q', question_type='SHORT', correct_short_answer='1')
        codes = [self.client.post('/api/report-error/', json.dumps({'question_id': question.id, 'message': 'x'}),
                                  content_type='application/json').status_code for _ in range(21)]
        self.assertEqual(codes[:20], [200] * 20)
        self.assertEqual(codes[20], 429)

    @mock.patch('materials.views.send_telegram_notification')
    def test_parent_review_limit(self, notify):
        student = TutorStudentRequest.objects.create(user=self.make_user('kid9@example.com'), real_name='Учень',
                                                     course='nmt', status='approved')
        for _ in range(5):
            self.client.post(f'/parents/{student.parent_token}/review/',
                             {'rating': 5, 'text': 'Дякуємо', 'reviewer_name': 'Мама'})
        self.assertEqual(Review.objects.count(), 3)



class ReviewFollowUpTests(MonoWebhookBase):
    def test_cancelled_order_rechecked_on_result_page(self):
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'failure'})
        status_response = mock.Mock()
        status_response.json.return_value = {'status': 'success'}  # повторна спроба вдалась, вебхук загубився
        self.client.force_login(self.user)
        with mock.patch('materials.views.requests.get', return_value=status_response):
            self.assertContains(self.client.get(f'/payment/result/{self.topup.id}/'), 'Оплата пройшла успішно')
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 500)

    def test_failed_page_does_not_claim_money_was_not_taken(self):
        self.post_webhook({'invoiceId': 'inv-topup', 'status': 'expired'})
        status_response = mock.Mock()
        status_response.json.return_value = {'status': 'expired'}
        self.client.force_login(self.user)
        with mock.patch('materials.views.requests.get', return_value=status_response):
            response = self.client.get(f'/payment/result/{self.topup.id}/')
        self.assertContains(response, 'Оплата не пройшла')
        self.assertNotContains(response, 'Гроші не списано')
        self.assertContains(response, 'Якщо гроші все ж списано')

    def test_admin_action_rechecks_cancelled(self):
        from django.contrib import admin
        from django.test import RequestFactory
        Order.objects.filter(id=self.topup.id).update(status='cancelled')
        status_response = mock.Mock()
        status_response.json.return_value = {'status': 'success'}
        request = RequestFactory().post('/')
        request.user = self.make_user('boss4@example.com', is_staff=True, is_superuser=True)
        model_admin = admin.site._registry[Order]
        with mock.patch('materials.views.requests.get', return_value=status_response), \
                mock.patch.object(model_admin, 'message_user'):
            model_admin.check_monobank_status(request, Order.objects.all())
        self.topup.refresh_from_db()
        self.assertEqual(self.topup.status, 'paid')


class ReviewFollowUpMiscTests(BaseTestCase):
    @override_settings(TELEGRAM_BOT_TOKEN='123:abc', TELEGRAM_ADMIN_ID='42')
    @mock.patch('do_kvadratu.logging_handlers.requests.post')
    def test_same_bug_on_many_urls_alerts_once(self, post):
        StudyMaterial.objects.create(title='1. Тема', is_published=True)
        StudyMaterial.objects.create(title='2. Тема', is_published=True)
        client = Client(raise_request_exception=False)
        with mock.patch('materials.views.MaterialDetailView.get_context_data', side_effect=KeyError('boom')):
            for material in StudyMaterial.objects.all():
                self.assertEqual(client.get(f'/material/{material.id}/', follow=True).status_code, 500)
        self.assertEqual(post.call_count, 1)

    def test_malformed_error_report_is_400_without_alert(self):
        self.client.force_login(self.make_user('r@example.com'))
        with self.assertNoLogs('materials', level='ERROR'):
            for body in ('not json', '[1, 2]', '"str"'):
                response = self.client.post('/api/report-error/', body, content_type='application/json')
                self.assertEqual(response.status_code, 400, body)

    @override_settings(EMAIL_BACKEND='materials.tests.BrokenEmailBackend')
    def test_password_reset_warns_when_mail_fails(self):
        self.make_user('forgot@example.com')
        response = self.client.post('/accounts/password/reset/', {'email': 'forgot@example.com'}, follow=True)
        self.assertContains(response, 'Не вдалося надіслати лист')


class QueryCountTests(BaseTestCase):
    """Сторінки не повинні робити окремий запит на кожен рядок і тягнути HTML-презентації даремно."""

    def setUp(self):
        from django.db import connection
        from django.test.utils import CaptureQueriesContext
        self.connection, self.capture = connection, CaptureQueriesContext
        self.user = self.make_user('perf@example.com')
        self.materials = [StudyMaterial.objects.create(title=f'{i}. Тема', price=25, is_published=True,
                                                       html_content='<p>' + 'x' * 1000 + '</p>') for i in range(1, 11)]
        self.client.force_login(self.user)

    def queries(self, url, client=None):
        with self.capture(self.connection) as ctx:
            response = (client or self.client).get(url)
        self.assertEqual(response.status_code, 200, url)
        return ctx.captured_queries

    def test_cart_queries_do_not_grow_with_items(self):
        cart = Cart.objects.create(user=self.user, promo_code='ВЧИТЕЛЬ')
        for material in self.materials[:2]:
            CartItem.objects.create(cart=cart, material=material)
        few = len(self.queries('/cart/'))
        for material in self.materials[2:]:
            CartItem.objects.create(cart=cart, material=material)
        self.assertEqual(len(self.queries('/cart/')), few)

    def test_list_pages_do_not_load_presentations(self):
        self.user.purchased_materials.add(*self.materials)
        for url in ('/materials/', '/cabinet/', '/cart/'):
            for query in self.queries(url):
                self.assertNotIn('html_content', query['sql'], f"{url}: {query['sql'][:300]}")

    def test_reader_still_shows_presentation(self):
        self.user.purchased_materials.add(self.materials[0])
        self.assertContains(self.client.get(f'/download/{self.materials[0].id}/'), 'x' * 1000)

    def test_parent_dashboard_queries_do_not_grow_with_attempts(self):
        student = TutorStudentRequest.objects.create(user=self.user, real_name='Учень', course='nmt', status='approved')
        PracticeAttempt.objects.create(user=self.user, material=self.materials[0], score=5)
        few = len(self.queries(f'/parents/{student.parent_token}/', Client()))
        for material in self.materials[1:]:
            PracticeAttempt.objects.create(user=self.user, material=material, score=5)
        self.assertEqual(len(self.queries(f'/parents/{student.parent_token}/', Client())), few)

    def test_admin_match_question_lists_only_its_options(self):
        staff = self.make_user('admin@example.com', is_staff=True, is_superuser=True)
        other = Question.objects.create(text='other', question_type='CHOICE')
        AnswerOption.objects.create(question=other, text='ЧУЖИЙ-ВАРІАНТ')
        question = Question.objects.create(text='m', question_type='MATCH')
        own = AnswerOption.objects.create(question=question, text='СВІЙ-ВАРІАНТ')
        MatchItem.objects.create(question=question, text='1', correct_option=own)
        admin_client = Client()
        admin_client.force_login(staff)
        page = admin_client.get(f'/do-kvadratu-secret-control/materials/question/{question.id}/change/')
        self.assertContains(page, 'СВІЙ-ВАРІАНТ')
        self.assertNotContains(page, 'ЧУЖИЙ-ВАРІАНТ')

    def test_diagnostic_picks_22_without_loading_whole_bank(self):
        algebra, geometry = make_nmt_topic('1. Числа', chapter_order=10), make_nmt_topic('30. Трикутники', chapter_order=600)
        for i in range(20):
            for topic in (algebra, geometry):
                for q_type in ('CHOICE', 'MATCH', 'SHORT'):
                    q = Question.objects.create(text=f'{q_type}{i}', question_type=q_type, curriculum_topic=topic,
                                                correct_short_answer='1')
                    AnswerOption.objects.create(question=q, text='a', is_correct=True)
        response = Client().get('/diagnostic/?topics=all')
        self.assertEqual(len(response.context['questions']), 15 + 3 + 4)
        queries = self.queries('/diagnostic/?topics=all', Client())
        option_queries = [q for q in queries if 'FROM "materials_answeroption"' in q['sql']]
        self.assertLessEqual(len(option_queries), 2)  # варіанти + правильні відповіді відповідностей
        self.assertLessEqual(len(queries), 8)



class DeferredPresentationSafetyTests(BaseTestCase):
    """HTML-презентація не завантажується за замовчуванням — переконуємось, що збереження її не стирає."""

    def setUp(self):
        self.material = StudyMaterial.objects.create(title='1. Тема', price=25, html_content='<p>СЛАЙДИ</p>',
                                                     curriculum_topic=make_nmt_topic('1. Тема'))

    def test_saving_deferred_instance_keeps_presentation(self):
        material = StudyMaterial.objects.get(id=self.material.id)
        material.price = 30
        material.save()
        self.assertEqual(StudyMaterial.objects.get(id=self.material.id).html_content, '<p>СЛАЙДИ</p>')

    def test_admin_edit_keeps_presentation(self):
        staff = self.make_user('editor@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(staff)
        url = f'/do-kvadratu-secret-control/materials/studymaterial/{self.material.id}/change/'
        page = self.client.get(url)
        self.assertContains(page, 'СЛАЙДИ')
        form = page.context['adminform'].form
        data = {name: ('' if value is None else value) for name, value in form.initial.items()
                if name not in ('file', 'image', 'tags', 'included_materials')}
        data.update({'price': 35, 'description': data.get('description') or ''})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, getattr(response, 'context', None) and
                         response.context['adminform'].form.errors)
        material = StudyMaterial.objects.get(id=self.material.id)
        self.assertEqual((material.price, material.html_content), (35, '<p>СЛАЙДИ</p>'))


class OrderAfterAccountDeletionTests(BaseTestCase):
    def test_paid_order_survives_account_deletion_with_buyer_email(self):
        kid = self.make_user('gone@example.com')
        order = Order.objects.create(user=kid, total_amount=100, status='paid')
        self.assertEqual(order.customer_email, 'gone@example.com')
        kid.delete()
        order.refresh_from_db()
        self.assertIsNone(order.user)
        self.assertEqual(order.customer_email, 'gone@example.com')
        self.assertIn('gone@example.com', str(order))

    @mock.patch('materials.views.send_telegram_notification')
    def test_late_payment_for_deleted_account_is_recorded_not_granted(self, notify):
        from materials.views import apply_mono_status
        kid = self.make_user('late@example.com')
        order = Order.objects.create(user=kid, total_amount=50, status='pending', mono_invoice_id='inv-late')
        kid.delete()
        result = apply_mono_status('inv-late', 'success')
        self.assertEqual(result.status, 'paid')
        notify.assert_called_once()
        self.assertIn('late@example.com', notify.call_args[0][0])


class LegalPagesTests(BaseTestCase):
    def test_offer_and_privacy_show_approved_texts(self):
        offer = self.client.get('/offer/')
        self.assertContains(offer, 'Редакція від 22.10.2026')
        self.assertContains(offer, '10.16. <strong>Підписка з супроводом.</strong>')
        self.assertContains(offer, 'Перше (діагностичне) заняття — безкоштовне')
        self.assertContains(offer, 'квитанція, яку Monobank автоматично надає')
        self.assertContains(offer, 'href="/privacy/"')
        self.assertContains(offer, '16. Підписка для викладачів')
        self.assertContains(offer, '25. Реквізити Продавця')
        self.assertContains(offer, 'на умовах розділу 17;')
        self.assertNotContains(offer, '{%')
        privacy = self.client.get('/privacy/')
        self.assertContains(privacy, 'Редакція від 22.10.2026')
        self.assertContains(privacy, 'Google Analytics')
        self.assertContains(privacy, 'href="/offer/"')

    def test_terms_version_matches_published_edition(self):
        # Дата редакції на сторінках і TERMS_VERSION мають змінюватися разом
        from django.conf import settings as dj_settings
        y, m, d = dj_settings.TERMS_VERSION[:10].split('-')   # «2026-10-19b» — друга редакція того ж дня
        self.assertContains(self.client.get('/offer/'), f'Редакція від {d}.{m}.{y}')


class PracticePoolTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('practice@example.com')
        self.client.force_login(self.user)
        self.topic3 = make_nmt_topic('3. Степені')
        self.lesson3 = StudyMaterial.objects.create(title='3. Степені', price=0, is_free=True, is_published=True,
                                                    curriculum_topic=self.topic3)
        self.lesson5 = StudyMaterial.objects.create(title='5. Дроби', price=0, is_free=True, is_published=True)

    def make_short(self, text, *materials, topic=None):
        q = Question.objects.create(text=text, question_type='SHORT', correct_short_answer='1', curriculum_topic=topic)
        q.materials.add(*materials)
        return q

    def shown_ids(self):
        response = self.client.get(f'/practice/{self.lesson3.id}/')
        self.assertEqual(response.status_code, 200)
        return set(response.context['q_short'])

    def test_own_question_stays_even_with_later_tag(self):
        own = self.make_short('own', self.lesson3, self.lesson5, topic=self.topic3)
        self.make_short('mixed', self.lesson3, self.lesson5)  # чужа тема + пізніший тег — виключається
        pool_ids = {q.id for q in self.shown_ids()}
        self.assertEqual(pool_ids, {own.id})

    def test_later_tag_rule_still_applies_to_other_questions(self):
        self.make_short('mixed', self.lesson3, self.lesson5)
        response = self.client.get(f'/practice/{self.lesson3.id}/')
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)

    def test_unseen_questions_come_first(self):
        old = [self.make_short(f'old{i}', self.lesson3) for i in range(3)]
        new = self.make_short('new', self.lesson3)
        PracticeAttempt.objects.create(user=self.user, material=self.lesson3, score=0, max_score=2,
                                       answers_json={'question_ids': ','.join(str(q.id) for q in old)})
        other = self.make_user('other@example.com')
        PracticeAttempt.objects.create(user=other, material=self.lesson3, score=0, max_score=2,
                                       answers_json={'question_ids': str(new.id)})
        for _ in range(10):
            self.assertEqual({q.id for q in self.shown_ids()}, {new.id})

    def test_repeats_only_when_no_new_left(self):
        seen = self.make_short('seen', self.lesson3)
        PracticeAttempt.objects.create(user=self.user, material=self.lesson3, score=0, max_score=2,
                                       answers_json={'question_ids': str(seen.id)})
        self.assertEqual({q.id for q in self.shown_ids()}, {seen.id})

    def test_broken_attempt_json_is_ignored(self):
        q = self.make_short('q', self.lesson3)
        for bad in (None, [], {'question_ids': None}, {'question_ids': 'abc,,'}):
            PracticeAttempt.objects.create(user=self.user, material=self.lesson3, score=0, max_score=2,
                                           answers_json=bad)
        self.assertEqual({x.id for x in self.shown_ids()}, {q.id})


BANK_SAMPLE = '''TOPIC_NAME = "34. Теорема косинусів та теорема синусів"
TASKS = [
    {
        "type": "CHOICE", "difficulty": 1, "text": r"Нове завдання $a^2$", "svg_code": "",
        "options": [(r"А) 1", False), (r"Б) 2", True)],
        "topic_tags": ["34. Теореми косинусів та теорема синусів", "99. Нема такого"]
    },
    {
        "type": "SHORT", "difficulty": 2, "text": "Уже є в базі", "answer": "5",
        "topic_tags": ["34. Теорема косинусів та теорема синусів"]
    },
    {
        "type": "MATCH", "difficulty": 3, "text": "Відповідність",
        "options": ["А) x", "Б) y"],
        "matches": [("1. one", "А) x"), ("2. two", "Б) y")],
        "topic_tags": ["34. Теорема косинусів та теорема синусів"]
    },
    {"type": "SHORT", "difficulty": 2, "text": "Без відповіді", "topic_tags": []},
    {"type": "CHOICE", "difficulty": 1, "text": "Нове  завдання $a^2$", "svg_code": "",
     "options": [(r"А) 1", False), (r"Б) 2", True)]},
]
'''


class BankImportTests(BaseTestCase):
    url = '/do-kvadratu-secret-control/materials/question/import-bank/'

    def setUp(self):
        self.admin = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(self.admin)
        self.lesson34 = StudyMaterial.objects.create(title='34. Теорема косинусів та теорема синусів', price=10)
        self.topic34 = make_nmt_topic('34. Теорема косинусів та теорема синусів')
        Question.objects.create(text='Уже є в базі', question_type='SHORT', correct_short_answer='5')

    def upload(self, source, action='preview'):
        from django.core.files.uploadedfile import SimpleUploadedFile
        f = SimpleUploadedFile('bank_34.py', source.encode('utf-8'))
        return self.client.post(self.url, {'action': action, 'bank_file': f})

    def test_preview_reports_without_writing(self):
        response = self.upload(BANK_SAMPLE)
        self.assertEqual(response.status_code, 200)
        report = response.context['report']
        self.assertEqual(report.total, 5)
        self.assertEqual(report.to_add, [1, 3])
        self.assertEqual([i for i, _ in report.duplicates], [2, 5])  # 5-те — повтор 1-го з цього ж файлу
        self.assertEqual([i for i, _ in report.errors], [4])
        self.assertEqual(report.aliased_tags,
                         {'34. Теореми косинусів та теорема синусів': '34. Теорема косинусів та теорема синусів'})
        self.assertEqual(report.unknown_tags, {'99. Нема такого': 1})
        self.assertEqual(Question.objects.count(), 1)

    def test_same_text_with_other_options_is_not_a_duplicate(self):
        # Загальні умови («Узгодьте вираз (1–3) із …») повторюються в завданнях з різним змістом
        source = BANK_SAMPLE.replace('(r"А) 1", False), (r"Б) 2", True)]},\n]', '(r"А) 3", True), (r"Б) 4", False)]},\n]')
        report = self.upload(source).context['report']
        self.assertEqual(report.to_add, [1, 3, 5])
        self.assertEqual([i for i, _ in report.duplicates], [2])

    def test_duplicate_text_filter_lists_copies_side_by_side(self):
        old = Question.objects.create(text='Знайдіть  $x$.', question_type='SHORT', correct_short_answer='1')
        new = Question.objects.create(text='Знайдіть $x$.', question_type='SHORT', correct_short_answer='2')
        response = self.client.get('/do-kvadratu-secret-control/materials/question/?dup=yes')
        self.assertEqual([q.id for q in response.context['cl'].result_list], [old.id, new.id])

    def test_picture_filter(self):
        svg = Question.objects.create(text='SVG', question_type='SHORT', svg_code='<svg></svg>')
        Question.objects.create(text='Пробіли', question_type='SHORT', svg_code='  \n ')
        url = '/do-kvadratu-secret-control/materials/question/?picture='
        self.assertEqual([q.id for q in self.client.get(url + 'yes').context['cl'].result_list], [svg.id])
        self.assertNotIn(svg, self.client.get(url + 'no').context['cl'].result_list)

    def test_task_topic_overrides_file_topic(self):
        # Файл з усіма банками: тема кожного завдання — у полі "topic"
        topic21 = make_nmt_topic('21. Показникові рівняння')
        source = ('TOPIC_NAME = "Усі банки завдань"\nTASKS = [\n'
                  '{"type": "SHORT", "difficulty": 1, "text": "a", "answer": "1", "topic": "21. Показникові рівняння"},\n'
                  '{"type": "SHORT", "difficulty": 1, "text": "b", "answer": "2", "topic": "34. Теорема косинусів та теорема синусів"},\n]')
        self.upload(source)
        self.client.post(self.url, {'action': 'import'})
        self.assertEqual(Question.objects.get(text='a').curriculum_topic, topic21)
        self.assertEqual(Question.objects.get(text='b').curriculum_topic, self.topic34)

    def test_import_adds_tasks_and_binds_typo_tag_to_lesson_34(self):
        self.upload(BANK_SAMPLE)
        response = self.client.post(self.url, {'action': 'import'})
        self.assertRedirects(response, '/do-kvadratu-secret-control/materials/question/',
                             fetch_redirect_response=False)
        self.assertEqual(Question.objects.count(), 3)
        choice = Question.objects.get(text__startswith='Нове завдання')
        self.assertEqual(list(choice.materials.all()), [self.lesson34])
        self.assertEqual(choice.curriculum_topic, self.topic34)
        self.assertEqual(choice.options.filter(is_correct=True).get().text, 'Б) 2')
        match = Question.objects.get(text='Відповідність')
        self.assertEqual({(m.text, m.correct_option.text) for m in match.match_items.all()},
                         {('1. one', 'А) x'), ('2. two', 'Б) y')})
        # повторне завантаження того ж файлу нічого не додає
        self.upload(BANK_SAMPLE)
        self.client.post(self.url, {'action': 'import'})
        self.assertEqual(Question.objects.count(), 3)

    def test_file_is_never_executed(self):
        import os
        marker = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'bank-executed-marker')
        if os.path.exists(marker):
            os.remove(marker)
        evil = f'TOPIC_NAME = "x"\nTASKS = [open({marker!r}, "w").write("1")]\n'
        response = self.upload(evil)
        self.assertContains(response, 'лише літерали')
        self.assertFalse(os.path.exists(marker))
        for source in ('import os\nTOPIC_NAME = "x"\nTASKS = []', 'TOPIC_NAME = "x"\nTASKS = []\nTASKS[0]["a"] = 1',
                       'TOPIC_NAME = "x"\nTASKS = [{"a": 1} + {}]', 'TOPIC_NAME = "x"'):
            self.assertIn('error', self.upload(source).context)
        self.assertEqual(Question.objects.count(), 1)

    def test_import_without_preview_does_nothing(self):
        response = self.client.post(self.url, {'action': 'import'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

    def test_requires_add_permission(self):
        staff = self.make_user('staff@example.com', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_changelist_has_upload_button(self):
        page = self.client.get('/do-kvadratu-secret-control/materials/question/')
        self.assertContains(page, 'Завантажити завдання')

    def test_all_repo_bank_files_parse(self):
        import glob
        from .bank_import import parse_bank_source, validate_task
        paths = sorted(glob.glob('import_files/bank_*.py'))
        self.assertTrue(paths)
        for path in paths:
            with open(path, encoding='utf-8') as f:
                _, tasks = parse_bank_source(f.read())
            for i, task in enumerate(tasks, start=1):
                self.assertEqual(validate_task(task), [], f'{path} №{i}')


class LibraryAndStorefrontTests(BaseTestCase):
    def setUp(self):
        self.nmt_topic = make_nmt_topic('1. Числа')
        subject = CurriculumSubject.objects.create(name='Алгебра (7-9 класи)', order=2)
        grade = CurriculumGrade.objects.create(subject=subject, name='8 клас', number=8)
        chapter = CurriculumChapter.objects.create(grade=grade, name='Розділ 1')
        self.school_topic = CurriculumTopic.objects.create(chapter=chapter, name='Квадратні рівняння')
        self.nmt = StudyMaterial.objects.create(title='1. Числа', price=25, is_published=True,
                                                curriculum_topic=self.nmt_topic)
        self.school = StudyMaterial.objects.create(title='Квадратні рівняння', price=30, is_published=True,
                                                   curriculum_topic=self.school_topic)
        self.not_owned = StudyMaterial.objects.create(title='2. Не куплена', price=25, is_published=True)
        self.bundle = StudyMaterial.objects.create(title='Вся алгебра', price=399, is_bundle=True, is_published=True)
        self.bundle.included_materials.add(self.nmt, self.not_owned)

    def test_storefront_shows_course_and_grade_badge(self):
        page = self.client.get('/materials/')
        self.assertContains(page, 'Алгебра · 8 клас')
        self.assertContains(page, 'Підготовка до НМТ')

    def test_library_groups_by_grade_and_lists_bundle_topics(self):
        kid = self.make_user('lib@example.com')
        kid.purchased_materials.add(self.nmt, self.school, self.bundle)
        self.client.force_login(kid)
        response = self.client.get('/cabinet/')
        groups = [(g['label'], [m.title for m in g['materials']]) for g in response.context['library_groups']]
        self.assertEqual(groups, [('Алгебра · 8 клас', ['Квадратні рівняння']), ('Підготовка до НМТ', ['1. Числа'])])
        [entry] = response.context['library_bundles']
        self.assertEqual([(t['material'].title, t['owned']) for t in entry['topics']],
                         [('1. Числа', True), ('2. Не куплена', False)])
        # Пакет не веде в порожню читалку, а не куплена тема — не посилання
        self.assertNotContains(response, f'/download/{self.bundle.id}/')
        self.assertNotContains(response, f'/download/{self.not_owned.id}/')
        self.assertContains(response, f'/download/{self.nmt.id}/')


class NmtCurriculumTests(BaseTestCase):
    def test_nmt_topics_mirror_material_files(self):
        # Конспекти й завдання банку прив'язуються до теми НМТ за номером — назви мають збігатися з конспектами
        import os
        from django.conf import settings as dj_settings
        from materials.management.commands.import_curriculum import NMT_CURRICULUM
        topics = [t['topic_name'] for g in NMT_CURRICULUM['grades'] for c in g['chapters'] for t in c['topics']]
        files = [f[:-4] for f in os.listdir(os.path.join(dj_settings.BASE_DIR, 'import_files')) if f.endswith('.pdf')]
        self.assertEqual(sorted(topics), sorted(files))
        self.assertEqual([int(t.split('.')[0]) for t in topics], list(range(1, 47)))


class AdminConvenienceTests(BaseTestCase):
    def setUp(self):
        self.boss = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(self.boss)

    def test_index_lists_what_needs_attention(self):
        StudyMaterial.objects.create(title='Без презентації', is_published=True)
        TutorStudentRequest.objects.create(user=self.make_user('kid@example.com'), real_name='Учень', course='nmt')
        items = {i['label']: i for i in self.client.get('/do-kvadratu-secret-control/').context['attention_items']}
        self.assertEqual(items['Нові заявки на статус учня']['count'], 1)
        self.assertEqual(items['Опубліковані матеріали без презентації']['count'], 1)
        self.assertEqual(items['Нові скарги на завдання']['count'], 0)
        for item in items.values():
            self.assertEqual(self.client.get(item['url']).status_code, 200, item['label'])

    def test_html_file_upload_replaces_presentation(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        material = StudyMaterial.objects.create(title='1. Тема', price=25, html_content='<p>старе</p>')
        url = f'/do-kvadratu-secret-control/materials/studymaterial/{material.id}/change/'
        data = {'title': '1. Тема', 'price': 25, 'description': '', 'html_content': '<p>старе</p>'}
        response = self.client.post(url, dict(data, html_file=SimpleUploadedFile('1.txt', b'x')))
        self.assertContains(response, 'Потрібен файл .html')
        upload = SimpleUploadedFile('1.html', '﻿<p>нове</p>'.encode('utf-8'))
        self.assertEqual(self.client.post(url, dict(data, html_file=upload)).status_code, 302)
        self.assertEqual(StudyMaterial.objects.get(id=material.id).html_content, '<p>нове</p>')


class QuestionAdminTests(BaseTestCase):
    url = '/do-kvadratu-secret-control/materials/question/'

    def setUp(self):
        self.client.force_login(self.make_user('boss@example.com', is_staff=True, is_superuser=True))
        self.t21, self.t22 = make_nmt_topic('21. Показникові рівняння'), make_nmt_topic('22. Логарифмічні рівняння')
        self.good = Question.objects.create(text='Добре', question_type='CHOICE', curriculum_topic=self.t21)
        for i in range(5):
            AnswerOption.objects.create(question=self.good, text=str(i), is_correct=(i == 0))
        self.broken = Question.objects.create(text='Без відповіді', question_type='SHORT', curriculum_topic=self.t22)

    def test_topic_filter_appears_after_grade_and_health_column(self):
        grade = self.t21.chapter.grade_id
        self.assertNotContains(self.client.get(self.url), 'тема (спершу оберіть клас)')
        response = self.client.get(self.url, {'curriculum_topic__chapter__grade__id__exact': grade, 'topic': self.t22.id})
        self.assertContains(response, 'тема (спершу оберіть клас)')
        self.assertEqual(list(response.context['cl'].result_list), [self.broken])
        self.assertContains(response, '⚠ немає правильної відповіді')

    def test_bulk_edit_changes_topic_difficulty_and_lessons(self):
        lesson = StudyMaterial.objects.create(title='21. Показникові рівняння')
        ids = [self.good.id, self.broken.id]
        intermediate = self.client.post(self.url, {'action': 'bulk_edit_questions', '_selected_action': ids})
        self.assertContains(intermediate, 'Обрано завдань: 2')
        self.client.post(self.url, {'action': 'bulk_edit_questions', '_selected_action': ids, 'apply': '1',
                                    'curriculum_topic': self.t21.id, 'difficulty': '3', 'add_material': lesson.id})
        self.assertEqual(set(Question.objects.values_list('curriculum_topic', 'difficulty')), {(self.t21.id, 3)})
        self.assertEqual(lesson.practice_questions.count(), 2)


class ShuffledOptionsTests(BaseTestCase):
    def test_choice_options_are_relabelled_after_shuffle_and_results_show_them_without_letters(self):
        from materials.templatetags.question_tags import shuffled_options
        q = Question.objects.create(text='q', question_type='CHOICE')
        for i, letter in enumerate('АБВГД'):
            AnswerOption.objects.create(question=q, text=f'{letter}) варіант {i}', is_correct=(i == 1))
        with mock.patch('materials.templatetags.question_tags.random.shuffle', side_effect=lambda items: items.reverse()):
            options = shuffled_options(q)
        self.assertEqual([o.display_text for o in options],
                         ['А) варіант 4', 'Б) варіант 3', 'В) варіант 2', 'Г) варіант 1', 'Д) варіант 0'])
        self.assertEqual(AnswerOption.objects.get(is_correct=True).body, 'варіант 1')


class MathSprintTests(BaseTestCase):
    def make_questions(self, material, count, **extra):
        for i in range(count):
            q = Question.objects.create(text=f'{material.title} {i} {extra}', question_type='CHOICE',
                                        difficulty=extra.get('difficulty', 1), svg_code=extra.get('svg_code', ''))
            AnswerOption.objects.create(question=q, text='А) 1', is_correct=True)
            AnswerOption.objects.create(question=q, text='Б) 2', is_correct=False)
            q.materials.add(material)

    def test_guest_without_free_topics_gets_no_bank_questions(self):
        self.make_questions(StudyMaterial.objects.create(title='Платна', price=10), 5)
        response = self.client.get('/game/sprint/')
        self.assertEqual(response.context['questions_list'], [])
        self.assertEqual(response.context['available_materials'], [])

    def test_only_easy_questions_without_picture_and_topics_with_enough_of_them(self):
        free = StudyMaterial.objects.create(title='Безкоштовна', price=0, is_free=True, is_published=True)
        thin = StudyMaterial.objects.create(title='Мало завдань', price=0, is_free=True, is_published=True)
        self.make_questions(StudyMaterial.objects.create(title='Чернетка', price=0, is_free=True), 5)
        self.make_questions(free, 4)
        self.make_questions(free, 3, difficulty=3)
        self.make_questions(free, 3, svg_code='<svg></svg>')
        self.make_questions(thin, 3)
        response = self.client.get('/game/sprint/')
        self.assertEqual(response.context['available_materials'], [free])
        self.assertEqual(len(response.context['questions_list']), 4)
        self.assertEqual(response.context['questions_list'][0]['lesson_url'], free.get_absolute_url())
        # Тему, де завдань замало, не можна обрати навіть через URL
        response = self.client.get(f'/game/sprint/?material_id={thin.id}')
        self.assertIsNone(response.context['selected_material'])

    def test_sprint_gives_no_balance_bonus(self):
        user = self.make_user('kid@example.com')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/game/sprint/').status_code, 200)
        response = self.client.post('/game/sprint/', '{"correct_count": 50}', content_type='application/json')
        self.assertEqual(response.status_code, 405)
        user.refresh_from_db()
        self.assertEqual(user.balance, 0)


class GamesTests(BaseTestCase):
    def setUp(self):
        self.free = StudyMaterial.objects.create(title='1. Безкоштовна', price=0, is_free=True, is_published=True)
        self.paid = StudyMaterial.objects.create(title='2. Платна', price=10)
        self.kid = self.make_user('kid@example.com')

    def choice(self, material, text='2+2?'):
        q = Question.objects.create(text=text, question_type='CHOICE', difficulty=1)
        right = AnswerOption.objects.create(question=q, text='А) 4', is_correct=True)
        wrong = AnswerOption.objects.create(question=q, text='Б) 5', is_correct=False)
        q.materials.add(material)
        return q, right, wrong

    def answer(self, **data):
        return self.client.post('/game/answer/', json.dumps(data), content_type='application/json')

    def test_short_answer_matching(self):
        from .games import short_answer_matches
        self.assertTrue(short_answer_matches('0,5', '1/2'))
        self.assertTrue(short_answer_matches(' 0.50 ', '0.5'))
        self.assertTrue(short_answer_matches('−3', '-3'))
        self.assertFalse(short_answer_matches('0.51', '0.5'))
        self.assertFalse(short_answer_matches('', '0'))
        self.assertTrue(short_answer_matches('Так', 'так'))
        # Мішане число: «2 3/5» = 13/5, а не 23/5
        self.assertTrue(short_answer_matches('2 3/5', '13/5'))
        self.assertTrue(short_answer_matches('13/5', '2 3/5'))
        self.assertFalse(short_answer_matches('2 3/5', '23/5'))
        self.assertTrue(short_answer_matches('−1 1/2', '-3/2'))
        self.assertTrue(short_answer_matches('2 3/4 кг', '11/4'))
        self.assertTrue(short_answer_matches('1 000', '1000'))

    def test_answer_is_checked_on_server_and_mistakes_are_tracked(self):
        q, right, wrong = self.choice(self.free)
        self.client.force_login(self.kid)
        response = self.answer(question_id=q.id, option_id=wrong.id).json()
        self.assertEqual(response, {'correct': False, 'option_id': right.id})
        mistake = GameMistake.objects.get(user=self.kid, question=q)
        self.assertTrue(self.answer(question_id=q.id, option_id=right.id).json()['correct'])
        mistake.refresh_from_db()
        self.assertEqual(mistake.correct_streak, 1)
        self.answer(question_id=q.id, option_id=wrong.id)  # помилка обнуляє серію
        mistake.refresh_from_db()
        self.assertEqual(mistake.correct_streak, 0)
        self.answer(question_id=q.id, option_id=right.id)
        self.answer(question_id=q.id, option_id=right.id)  # двічі поспіль — засвоєно
        self.assertFalse(GameMistake.objects.filter(user=self.kid).exists())

    def test_match_and_short_answers(self):
        q = Question.objects.create(text='Пари', question_type='MATCH')
        a = AnswerOption.objects.create(question=q, text='А) 1')
        b = AnswerOption.objects.create(question=q, text='Б) 2')
        one = MatchItem.objects.create(question=q, text='1. x', correct_option=a)
        two = MatchItem.objects.create(question=q, text='2. y', correct_option=b)
        q.materials.add(self.free)
        self.assertTrue(self.answer(question_id=q.id, pairs={one.id: a.id, two.id: b.id}).json()['correct'])
        self.assertFalse(self.answer(question_id=q.id, pairs={one.id: b.id, two.id: a.id}).json()['correct'])
        short = Question.objects.create(text='Половина', question_type='SHORT', correct_short_answer='0.5')
        short.materials.add(self.free)
        self.assertTrue(self.answer(question_id=short.id, answer='1/2').json()['correct'])

    def test_no_answers_for_paid_topics_and_none_in_page(self):
        q, right, _ = self.choice(self.paid)
        self.assertEqual(self.answer(question_id=q.id, option_id=right.id).status_code, 404)
        for i in range(2):
            pair = Question.objects.create(text=f'Пари {i}', question_type='MATCH')
            option = AnswerOption.objects.create(question=pair, text='А) 1')
            MatchItem.objects.create(question=pair, text='1. x', correct_option=option)
            pair.materials.add(self.free)
        response = self.client.get('/game/pairs/')
        self.assertEqual(len(response.context['questions']), 2)
        self.assertNotIn('is_correct', response.content.decode())
        self.assertNotIn('correct_option', response.content.decode())

    def test_mistakes_game_and_practice_records_mistakes(self):
        self.assertEqual(self.client.get('/game/mistakes/').status_code, 302)
        q, right, wrong = self.choice(self.free)
        self.client.force_login(self.kid)
        self.client.post(f'/practice/{self.free.id}/', {'question_ids': str(q.id), f'q_{q.id}': str(wrong.id)})
        self.assertTrue(GameMistake.objects.filter(user=self.kid, question=q).exists())
        response = self.client.get('/game/mistakes/')
        self.assertEqual([item['id'] for item in response.context['questions']], [q.id])
        self.assertContains(self.client.get('/game/'), 'Завдань у списку: 1')


class PlatformHardeningTests(BaseTestCase):
    def test_practice_accepts_equivalent_short_answers(self):
        material = StudyMaterial.objects.create(title='1. Тема', price=0, is_free=True, is_published=True)
        q = Question.objects.create(text='Половина', question_type='SHORT', correct_short_answer='0.5')
        q.materials.add(material)
        self.client.force_login(self.make_user('kid@example.com'))
        response = self.client.post(f'/practice/{material.id}/', {'question_ids': str(q.id), f'q_{q.id}': '0,50'})
        self.assertEqual(response.context['total_score'], 2)

    def test_hsts_header_on_https(self):
        response = self.client.get('/', secure=True)
        self.assertEqual(response['Strict-Transport-Security'], 'max-age=31536000')

    def test_stored_lessons_get_pinned_mathjax(self):
        import importlib
        from django.apps import apps
        material = StudyMaterial.objects.create(
            title='Урок', html_content='<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>')
        importlib.import_module('materials.migrations.0039_pin_mathjax_in_lessons').forwards(apps, None)
        material.refresh_from_db()
        self.assertIn('npm/mathjax@3.2.2/es5', material.html_content)


class DiagnosticHistoryTests(BaseTestCase):
    def setUp(self):
        self.topic = make_nmt_topic('21. Показникові рівняння')
        self.lesson = StudyMaterial.objects.create(title='21. Показникові рівняння', price=10, is_published=True,
                                                   curriculum_topic=self.topic)
        self.q = Question.objects.create(text='2^x = 8', question_type='CHOICE', curriculum_topic=self.topic)
        self.right = AnswerOption.objects.create(question=self.q, text='А) 3', is_correct=True)
        self.wrong = AnswerOption.objects.create(question=self.q, text='Б) 4', is_correct=False)
        self.kid = self.make_user('kid@example.com')
        self.client.force_login(self.kid)

    def take(self, option):
        return self.client.post('/diagnostic/', {'question_ids': str(self.q.id), f'question_{self.q.id}': str(option.id)})

    def test_progress_and_weak_topics_are_shown(self):
        first = self.take(self.wrong)
        self.assertIsNone(first.context['previous_percent'])
        self.assertEqual(first.context['recommendations'], [self.lesson])

        html = self.client.get('/cabinet/').content.decode()
        self.assertIn('data-section="diagnostics"', html)
        self.assertIn('Що повторити за останньою діагностикою', html)
        self.assertIn(self.lesson.get_absolute_url(), html)

        second = self.take(self.right)
        self.assertEqual((second.context['previous_percent'], second.context['percent_change']), (0, 100))
        self.assertContains(second, 'Минулого разу за цими темами: 0%')
        cabinet = self.client.get('/cabinet/')
        self.assertEqual([a.change for a in cabinet.context['diagnostics']], [100, None])
        self.assertContains(cabinet, 'слабких тем немає')
        # Діагностики не дублюються в результатах практики
        self.assertEqual(list(cabinet.context['my_attempts']), [])

    def test_empty_diagnostic_is_not_saved(self):
        response = self.client.post('/diagnostic/', {'question_ids': str(self.q.id)})
        self.assertContains(response, 'Ви не відповіли на жодне завдання')
        self.assertFalse(PracticeAttempt.objects.filter(user=self.kid).exists())

    def test_cabinet_focuses_on_five_weakest_topics(self):
        ids = []
        for i in range(7):
            topic = make_nmt_topic(f'{i + 1}. Тема {i}')
            q = Question.objects.create(text=f'Завдання {i}', question_type='CHOICE', curriculum_topic=topic)
            AnswerOption.objects.create(question=q, text='А) так', is_correct=True)
            ids.append(q.id)
        # Неіснуючий варіант — відповідь є (спроба зберігається), але неправильна, тож усі 7 тем слабкі
        self.client.post('/diagnostic/', {'question_ids': ','.join(map(str, ids)), f'question_{ids[0]}': '0'})
        cabinet = self.client.get('/cabinet/')
        self.assertEqual(len(cabinet.context['diagnostic_weak_topics']), 5)
        self.assertEqual(cabinet.context['diagnostic_more_weak'], 2)
        self.assertContains(cabinet, 'І ще 2 теми нижче 50%')


class DiagnosticTopicChoiceTests(BaseTestCase):
    def setUp(self):
        self.topics = [make_nmt_topic(f'{i}. Тема {i}', chapter_order=i) for i in (1, 2, 3)]
        for topic in self.topics:
            for i in range(6):
                for q_type in ('CHOICE', 'MATCH', 'SHORT'):
                    q = Question.objects.create(text=f'{topic.name} {q_type} {i}', question_type=q_type,
                                                curriculum_topic=topic, correct_short_answer='1')
                    AnswerOption.objects.create(question=q, text='А) 1', is_correct=True)
        self.empty = make_nmt_topic('9. Без завдань', chapter_order=9)
        school_subject = CurriculumSubject.objects.create(name='Алгебра', order=1)
        school_grade = CurriculumGrade.objects.create(subject=school_subject, name='7 клас')
        chapter = CurriculumChapter.objects.create(grade=school_grade, name='Вирази', order=1)
        self.school_topic = CurriculumTopic.objects.create(chapter=chapter, name='Шкільна тема')
        q = Question.objects.create(text='Шкільне', question_type='CHOICE', curriculum_topic=self.school_topic)
        AnswerOption.objects.create(question=q, text='А) 1', is_correct=True)

    def test_picker_groups_each_chapter_once_in_course_order(self):
        # Теми створено впереміш: розділи не повинні дублюватися, а теми — йти за номером
        mixed = [make_nmt_topic(name, chapter_order=order) for name, order in
                 (('42. Циліндр', 9), ('32. Рівнобедрений трикутник', 8), ('39. Вступ до стереометрії', 9),
                  ('37. Многокутники', 8), ('43. Конус', 9))]
        for topic in mixed:
            q = Question.objects.create(text=topic.name, question_type='CHOICE', curriculum_topic=topic)
            AnswerOption.objects.create(question=q, text='А) 1', is_correct=True)
        groups = self.client.get('/diagnostic/').context['chapters']
        names = [g['chapter'].name for g in groups]
        self.assertEqual(names, ['Розділ 1', 'Розділ 2', 'Розділ 3', 'Розділ 8', 'Розділ 9'])
        self.assertEqual([t.name for t in groups[-1]['topics']], ['39. Вступ до стереометрії', '42. Циліндр', '43. Конус'])
        self.assertEqual([t.name for t in groups[-2]['topics']], ['32. Рівнобедрений трикутник', '37. Многокутники'])

    def test_picker_lists_only_nmt_topics_with_questions(self):
        response = self.client.get('/diagnostic/')
        self.assertTemplateUsed(response, 'materials/diagnostic_choose.html')
        listed = [t for group in response.context['chapters'] for t in group['topics']]
        self.assertEqual(listed, self.topics)
        self.assertContains(response, '?topics=all')

    def test_selected_topics_only_and_balanced(self):
        chosen = self.topics[:2]
        response = self.client.get('/diagnostic/', {'topic': [t.id for t in chosen] + [self.school_topic.id]})
        questions = response.context['questions']
        self.assertEqual(len(questions), 12 + 3 + 4)  # з вибором відповіді в двох темах лише 2×6
        self.assertEqual({q.curriculum_topic_id for q in questions}, {t.id for t in chosen})
        choice_topics = [q.curriculum_topic_id for q in questions if q.question_type == 'CHOICE']
        self.assertEqual(sorted(choice_topics.count(t.id) for t in chosen), [6, 6])  # по колу: банк має по 6
        self.assertEqual(response.context['scope'], f'{chosen[0].id},{chosen[1].id}')
        self.assertContains(response, 'name="scope"')
        self.assertContains(response, '19 завдань ·')
        from .views import tasks_word
        self.assertEqual([tasks_word(n) for n in (1, 4, 5, 11, 14, 19, 21, 22)],
                         ['завдання', 'завдання', 'завдань', 'завдань', 'завдань', 'завдань', 'завдання', 'завдання'])

    def test_comparison_and_cabinet_use_same_topic_set(self):
        self.client.force_login(self.make_user('kid@example.com'))
        q = Question.objects.filter(curriculum_topic=self.topics[0], question_type='CHOICE').first()
        option = q.options.first()

        def take(scope):
            return self.client.post('/diagnostic/', {'question_ids': str(q.id), f'question_{q.id}': str(option.id),
                                                     'scope': scope})

        take(str(self.topics[0].id))
        self.assertIsNone(take('all').context['previous_percent'])  # інший набір тем — не порівнюємо
        self.assertEqual(take(str(self.topics[0].id)).context['previous_percent'], 100)
        cabinet = self.client.get('/cabinet/')
        labels = [(a.scope_label, a.change) for a in cabinet.context['diagnostics']]
        self.assertEqual(labels, [('1. Тема 1', 0), ('Усі теми НМТ', None), ('1. Тема 1', None)])


class DiagnosticOfferTests(BaseTestCase):
    def setUp(self):
        self.topic = make_nmt_topic('21. Показникові рівняння')
        self.paid = StudyMaterial.objects.create(title='21. Показникові рівняння', price=200, is_published=True,
                                                 curriculum_topic=self.topic)
        self.free = StudyMaterial.objects.create(title='21. Безкоштовний конспект', price=0, is_free=True,
                                                 is_published=True, curriculum_topic=self.topic)
        self.other = StudyMaterial.objects.create(title='30. Інша тема', price=100, is_published=True)
        self.q = Question.objects.create(text='2^x = 8', question_type='CHOICE', curriculum_topic=self.topic)
        AnswerOption.objects.create(question=self.q, text='А) 3', is_correct=True)
        self.wrong = AnswerOption.objects.create(question=self.q, text='Б) 4', is_correct=False)
        self.kid = self.make_user('kid@example.com', balance=1000)

    def take(self):
        return self.client.post('/diagnostic/', {'question_ids': str(self.q.id), f'question_{self.q.id}': str(self.wrong.id)})

    def test_offer_bundle_of_paid_weak_lessons_with_discount_and_timer(self):
        self.client.force_login(self.kid)
        response = self.take()
        offer = DiagnosticOffer.objects.get(user=self.kid)
        self.assertEqual(list(offer.materials.all()), [self.paid])  # без безкоштовного
        self.assertEqual((response.context['offer_full'], response.context['offer_price']), (200, 170))
        self.assertContains(response, 'Купити пакет зі знижкою')
        self.assertContains(response, 'id="offer-timer"')
        self.assertContains(response, 'До НМТ')

    def test_buying_bundle_applies_discount_only_to_offer_lessons_and_charges_it(self):
        self.client.force_login(self.kid)
        self.take()
        self.client.post('/diagnostic/offer/')
        cart = Cart.objects.get(user=self.kid)
        CartItem.objects.create(cart=cart, material=self.other)
        self.assertEqual(cart.get_total_price(), 170 + 100)
        self.assertContains(self.client.get('/cart/'), 'Знижка за діагностикою −15%')
        self.client.post('/cart/pay/balance/', {'agree': 'on'})
        self.kid.refresh_from_db()
        self.assertEqual(self.kid.balance, 1000 - 270)
        self.assertTrue(self.kid.purchased_materials.filter(id=self.paid.id).exists())

    def test_one_offer_per_30_days_and_no_discount_after_expiry(self):
        self.client.force_login(self.kid)
        self.take()
        self.take()
        self.assertEqual(DiagnosticOffer.objects.filter(user=self.kid).count(), 1)
        DiagnosticOffer.objects.update(expires_at=timezone.now() - datetime.timedelta(minutes=1))
        response = self.take()
        self.assertEqual(DiagnosticOffer.objects.filter(user=self.kid).count(), 1)
        self.assertIsNone(response.context['offer'])
        self.assertContains(response, 'раз на 30 днів')
        cart, _ = Cart.objects.get_or_create(user=self.kid)
        CartItem.objects.create(cart=cart, material=self.paid)
        self.assertEqual(cart.get_total_price(), 200)

    def test_repeat_diagnostic_on_other_topics_gets_discount_for_its_own_lessons(self):
        # Перша діагностика — одна тема, друга (поки знижка діє) — інша: пакет показує уроки саме другої
        topic2 = make_nmt_topic('42. Циліндр')
        paid2 = StudyMaterial.objects.create(title='42. Циліндр', price=100, is_published=True, curriculum_topic=topic2)
        q2 = Question.objects.create(text='V циліндра', question_type='CHOICE', curriculum_topic=topic2)
        AnswerOption.objects.create(question=q2, text='А) 1', is_correct=True)
        wrong2 = AnswerOption.objects.create(question=q2, text='Б) 2', is_correct=False)
        self.client.force_login(self.kid)
        self.take()
        response = self.client.post('/diagnostic/', {'question_ids': str(q2.id), f'question_{q2.id}': str(wrong2.id)})
        self.assertEqual(response.context['offer_materials'], [paid2])
        self.assertEqual((response.context['offer_full'], response.context['offer_price']), (100, 85))
        self.assertContains(response, 'Купити пакет зі знижкою')
        offer = DiagnosticOffer.objects.get(user=self.kid)
        self.assertEqual(set(offer.materials.all()), {self.paid, paid2})
        self.client.post('/diagnostic/offer/', {'material': [str(paid2.id)]})
        cart = Cart.objects.get(user=self.kid)
        self.assertEqual([i.material for i in cart.items.all()], [paid2])
        self.assertEqual(cart.get_total_price(), 85)

    def test_after_expiry_page_says_when_next_discount_is_possible(self):
        self.client.force_login(self.kid)
        self.take()
        DiagnosticOffer.objects.update(expires_at=timezone.now() - datetime.timedelta(minutes=1))
        self.assertContains(self.take(), 'наступна буде можлива з')

    def test_guest_sees_offer_and_gets_it_after_login(self):
        response = self.take()
        self.assertContains(response, 'Зареєструватися й отримати знижку')
        self.assertFalse(DiagnosticOffer.objects.exists())
        self.client.force_login(self.kid)  # сесія гостя зберігається після входу
        page = self.client.get('/diagnostic/offer/')
        self.assertContains(page, 'Купити пакет зі знижкою')
        self.assertEqual(list(DiagnosticOffer.objects.get(user=self.kid).materials.all()), [self.paid])

    def test_owned_lessons_are_not_offered(self):
        self.kid.purchased_materials.add(self.paid)
        self.client.force_login(self.kid)
        self.assertNotIn('offer_materials', self.take().context)
        self.assertFalse(DiagnosticOffer.objects.exists())

    def test_home_shows_audiences_and_grades_with_published_lessons(self):
        topic = make_school_topic('1.1. Натуральні числа', 5, 101)
        StudyMaterial.objects.create(title='1.1. Натуральні числа', price=0, is_free=True, is_published=True,
                                     curriculum_topic=topic)
        StudyMaterial.objects.create(title='1.2. Чернетка', price=0, is_free=True, curriculum_topic=topic)
        empty = make_school_topic('1.1. Подільність', 6, 201)
        page = self.client.get('/')
        self.assertContains(page, 'Репетиторам і вчителям')
        self.assertContains(page, 'Практика, що підлаштовується під учня')
        self.assertContains(page, f'?grade={topic.chapter.grade_id}')
        self.assertContains(page, '5 клас · Математика (5-6 класи)<')
        self.assertNotContains(page, f'?grade={empty.chapter.grade_id}')
        self.assertNotContains(page, 'stats-strip')
        self.assertContains(page, 'Тренуйтеся граючи')

    def test_countdown_words_and_storefront_banner(self):
        from .views import uk_plural
        self.assertEqual([uk_plural(n, 'день', 'дні', 'днів') for n in (1, 2, 5, 11, 21, 22, 112, 213)],
                         ['день', 'дні', 'днів', 'днів', 'день', 'дні', 'днів', 'днів'])
        self.assertContains(self.client.get('/materials/'), 'Пройдіть безкоштовну діагностику')


def make_school_topic(name, grade_number, order, chapter_order=10, subject='Математика (5-6 класи)'):
    subject_obj, _ = CurriculumSubject.objects.get_or_create(name=subject)
    grade, _ = CurriculumGrade.objects.get_or_create(subject=subject_obj, name=f'{grade_number} клас',
                                                     defaults={'number': grade_number})
    chapter, _ = CurriculumChapter.objects.get_or_create(grade=grade, name=f'Розділ {chapter_order}',
                                                         order=chapter_order)
    return CurriculumTopic.objects.create(chapter=chapter, name=name, order=order)


class ChapterBundleTests(BaseTestCase):
    """Пакет розділу: 70% суми платних тем, не дорожче за 1,5 місячної підписки; нові уроки — покупцям пакета."""

    def setUp(self):
        from .models import ClassPlan
        ClassPlan.objects.filter(number=5).update(price_month=99)
        self.lessons = [self.lesson(i) for i in range(1, 6)]   # 1.1 безкоштовна, 4 платні по 29 ₴

    def lesson(self, n, price=29):
        return StudyMaterial.objects.create(
            title=f'1.{n}. Тема', price=0 if n == 1 else price, is_free=n == 1, is_published=True,
            curriculum_topic=make_school_topic(f'1.{n}. Тема', 5, 100 + n))

    def sync(self):
        from .pricing import sync_chapter_bundles
        return sync_chapter_bundles()

    def bundle(self):
        return StudyMaterial.objects.get(bundle_chapter__isnull=False)

    def test_bundle_created_with_all_lessons_and_shown_in_grade(self):
        self.assertEqual(self.sync(), (1, 0))
        bundle = self.bundle()
        self.assertEqual(bundle.price, 81)   # 0,7 × 116
        self.assertTrue(bundle.is_bundle and bundle.is_published)
        self.assertEqual(set(bundle.included_materials.all()), set(self.lessons))
        self.assertEqual(bundle.title, 'Пакет: Розділ 10 · Математика · 5 клас')
        self.assertFalse(bundle.is_nmt)
        grade = bundle.bundle_chapter.grade
        self.assertContains(self.client.get(f'/materials/?grade={grade.id}'), bundle.title)
        self.assertContains(self.client.get('/prices/'), 'Пакет розділу')
        self.assertEqual(self.sync(), (0, 0))   # повторний запуск нічого не змінює

    def test_price_is_capped_by_one_and_a_half_month_subscriptions(self):
        for n in range(6, 12):
            self.lesson(n)
        self.sync()
        self.assertEqual(self.bundle().price, 149)   # 0,7 × 290 = 203 > 1,5 × 99

    def test_too_few_paid_lessons_no_bundle(self):
        StudyMaterial.objects.filter(pk__in=[m.pk for m in self.lessons[2:]]).delete()
        self.assertEqual(self.sync(), (0, 0))

    def test_new_lesson_opens_for_buyers_only(self):
        self.sync()
        buyer, other = self.make_user('buyer@example.com', balance=500), self.make_user('other@example.com')
        CartItem.objects.create(cart=Cart.objects.create(user=buyer), material=self.bundle())
        self.client.force_login(buyer)
        with mock.patch('materials.views.send_telegram_notification'):
            self.client.post('/cart/pay/balance/', {'agree': 'on'})
        self.assertEqual(buyer.purchased_materials.count(), 5)
        new = self.lesson(6)
        self.assertEqual(self.sync(), (0, 1))   # ціна 0,7 × 145 = 102
        self.assertEqual(self.bundle().price, 102)
        self.assertTrue(buyer.purchased_materials.filter(pk=new.pk).exists())
        self.assertFalse(other.purchased_materials.exists())

    def test_manual_price_and_unpublishing_are_kept(self):
        self.sync()
        StudyMaterial.objects.filter(bundle_chapter__isnull=False).update(price=60, price_is_manual=True,
                                                                           is_published=False)
        self.lesson(6)
        self.sync()
        bundle = self.bundle()
        self.assertEqual((bundle.price, bundle.is_published), (60, False))
        self.assertEqual(bundle.included_materials.count(), 6)

class TelegramRemindersTests(BaseTestCase):
    """Нагадування в Telegram: прив'язка з кабінету, що нагадувати, кожне — один раз."""

    def setUp(self):
        from .models import ClassPlan, PracticeRun
        self.PracticeRun = PracticeRun
        self.pupil = self.make_user('remind@example.com')
        self.pupil.telegram_id = '555'
        self.pupil.save()
        self.lesson = StudyMaterial.objects.create(title='1.2. Цифри', price=29, is_published=True,
                                                   curriculum_topic=make_school_topic('1.2. Цифри', 5, 102))
        self.plan = ClassPlan.objects.get(number=5)

    def keys(self):
        from .reminders import due_reminders
        return sorted(key for _, key, _, _ in due_reminders())

    def test_link_payload_is_signed(self):
        from .reminders import link_chat, link_payload, user_from_payload
        payload = link_payload(self.pupil)
        self.assertRegex(payload, r'^[A-Za-z0-9_-]{1,64}$')
        self.assertEqual(user_from_payload(payload), self.pupil)
        self.assertIsNone(user_from_payload(payload[:-1] + ('0' if payload[-1] != '0' else '1')))
        self.assertIsNone(user_from_payload(f'link{self.pupil.id}'))
        other = self.make_user('other@example.com')
        link_chat(other, 555)   # той самий чат — тепер інший акаунт
        self.pupil.refresh_from_db()
        self.assertIsNone(self.pupil.telegram_id)

    def test_cabinet_card_connects_and_disconnects(self):
        self.client.force_login(self.pupil)
        self.assertContains(self.client.get('/cabinet/'), 'Вимкнути нагадування')
        self.client.post('/telegram/unlink/')
        self.pupil.refresh_from_db()
        self.assertIsNone(self.pupil.telegram_id)
        self.assertContains(self.client.get('/cabinet/'), 'https://t.me/do_kvadratu_bot?start=link')

    def test_homework_due_tomorrow_until_done(self):
        from .models import Homework
        student = TutorStudentRequest.objects.create(user=self.pupil, real_name='Учень', course='grade_5',
                                                     status='approved')
        today = timezone.localdate()
        hw = Homework.objects.create(student=student, material=self.lesson, due_date=today + datetime.timedelta(days=1))
        Homework.objects.create(student=student, material=self.lesson, due_date=today + datetime.timedelta(days=5))
        self.assertEqual(self.keys(), [f'hw:{hw.id}'])
        hw.attempt = PracticeAttempt.objects.create(user=self.pupil, material=self.lesson, score=5)
        hw.save()
        self.assertEqual(self.keys(), [])

    def test_subscription_ending_unless_renewed(self):
        today = timezone.localdate()
        sub = ClassSubscription.objects.create(user=self.pupil, number=5, plan=self.plan,
                                               valid_until=today + datetime.timedelta(days=2))
        ClassSubscription.objects.create(user=self.pupil, number=6, valid_until=today + datetime.timedelta(days=20))
        self.assertEqual(self.keys(), [f'sub:{sub.id}'])
        ClassSubscription.objects.create(user=self.pupil, number=5, valid_until=today + datetime.timedelta(days=40))
        self.assertEqual(self.keys(), [])

    def test_abandoned_practice_only_own_and_recent(self):
        run = self.PracticeRun.objects.create(user=self.pupil, material=self.lesson, profile='A')
        self.assertEqual(self.keys(), [])   # щойно почата — ще не кинута
        two_days, ten_days = (timezone.now() - datetime.timedelta(days=d) for d in (2, 10))
        self.PracticeRun.objects.filter(pk=run.pk).update(updated_at=two_days)
        old = self.PracticeRun.objects.create(user=self.pupil, material=self.lesson, profile='B')
        self.PracticeRun.objects.filter(pk=old.pk).update(updated_at=ten_days)
        self.assertEqual(self.keys(), [f'run:{run.id}'])
        self.PracticeRun.objects.filter(pk=run.pk).update(finished_at=timezone.now())
        self.assertEqual(self.keys(), [])

    def test_each_reminder_sent_once_retry_on_failure_unlink_when_blocked(self):
        from .models import ReminderLog
        from .reminders import send_due_reminders
        today = timezone.localdate()
        ClassSubscription.objects.create(user=self.pupil, number=5, valid_until=today + datetime.timedelta(days=1))
        with mock.patch('materials.reminders.send_message', return_value=False):
            self.assertEqual(send_due_reminders(), 0)
        self.assertFalse(ReminderLog.objects.exists())   # не дійшло — спробуємо ще
        with mock.patch('materials.reminders.send_message', return_value=True) as send:
            self.assertEqual(send_due_reminders(), 1)
            self.assertEqual(send_due_reminders(), 0)
        chat, text, button = send.call_args[0]
        self.assertEqual(chat, '555')
        self.assertIn('Підписка на 5 клас закінчується', text)
        self.assertIn('/subscribe/?class=5', button[1])
        PracticeRun = self.PracticeRun
        run = PracticeRun.objects.create(user=self.pupil, material=self.lesson, profile='A')
        PracticeRun.objects.filter(pk=run.pk).update(updated_at=timezone.now() - datetime.timedelta(days=2))
        with mock.patch('materials.reminders.send_message', return_value=None):   # бота заблоковано
            send_due_reminders()
        self.pupil.refresh_from_db()
        self.assertIsNone(self.pupil.telegram_id)

    @override_settings(TELEGRAM_BOT_TOKEN='42:TEST', REMINDERS_DAILY=True)
    def test_daily_run_starts_once_in_evening_hours(self):
        from django.core.cache import cache
        from .reminders import maybe_send_daily
        cache.clear()
        evening = timezone.make_aware(datetime.datetime(2026, 10, 22, 17, 0))
        morning = timezone.make_aware(datetime.datetime(2026, 10, 23, 9, 0))
        with mock.patch('materials.reminders.threading.Thread') as thread:
            with mock.patch('materials.reminders.timezone.localtime', return_value=morning):
                maybe_send_daily()
            self.assertFalse(thread.called)
            with mock.patch('materials.reminders.timezone.localtime', return_value=evening):
                maybe_send_daily()
                maybe_send_daily()
            self.assertEqual(thread.call_count, 1)
            cache.clear()
            with self.settings(REMINDERS_DAILY=False), \
                    mock.patch('materials.reminders.timezone.localtime', return_value=evening):
                maybe_send_daily()
            self.assertEqual(thread.call_count, 1)

class CabinetProgressAndRenewalTests(BaseTestCase):
    """Прогрес за курсом, плашка «Підписка закінчується», ціни: FAQ, кнопка балансу в кошику."""

    def setUp(self):
        from .models import ClassPlan
        self.pupil = self.make_user('progress@example.com')
        self.client.force_login(self.pupil)
        self.lessons = [StudyMaterial.objects.create(
            title=f'1.{n}. Тема', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic(f'1.{n}. Тема', 5, 100 + n)) for n in range(1, 5)]
        self.plan = ClassPlan.objects.get(number=5)

    def subscribe(self, days):
        return ClassSubscription.objects.create(user=self.pupil, number=5, plan=self.plan,
                                                valid_until=timezone.localdate() + datetime.timedelta(days=days))

    def test_course_progress_counts_practiced_topics(self):
        self.subscribe(30)
        for material in (self.lessons[0], self.lessons[0], self.lessons[2]):
            PracticeAttempt.objects.create(user=self.pupil, material=material, score=5)
        self.assertContains(self.client.get('/cabinet/'), 'Пройдено <b>2 з 4</b> тем')

    def test_subscription_ending_banner_only_last_week(self):
        self.subscribe(20)
        self.assertNotContains(self.client.get('/cabinet/'), 'class="sub-ending"')
        ClassSubscription.objects.all().delete()
        self.subscribe(3)
        page = self.client.get('/cabinet/')
        self.assertContains(page, 'закінчується <b>через 3 дні</b>')
        self.assertContains(page, '/subscribe/?class=5#class-5')
        self.subscribe(40)   # продовжено — плашки немає
        self.assertNotContains(self.client.get('/cabinet/'), 'class="sub-ending"')

    def test_prices_faq(self):
        page = self.client.get('/prices/')
        self.assertContains(page, 'Часті запитання')
        self.assertContains(page, 'доступ не обмежений у часі')
        self.assertContains(page, 'tel:+380974022042')

    def test_balance_button_only_when_enough(self):
        CartItem.objects.create(cart=Cart.objects.create(user=self.pupil), material=self.lessons[1])
        User.objects.filter(pk=self.pupil.pk).update(balance=10)
        page = self.client.get('/cart/')
        self.assertNotContains(page, 'Списати з балансу')
        self.assertContains(page, 'для оплати з балансу не вистачає')
        User.objects.filter(pk=self.pupil.pk).update(balance=100)
        page = self.client.get('/cart/')
        self.assertContains(page, 'Списати з балансу')
        self.assertNotContains(page, 'не вистачає')

class SchoolDescriptionsAndReviewFormTests(BaseTestCase):
    """Шкільні уроки — не «конспект для НМТ»; форма відгуку; заява учня згорнута для всіх, кому вона не потрібна."""

    def setUp(self):
        from .models import DEFAULT_MATERIAL_DESCRIPTION
        self.lesson = StudyMaterial.objects.create(
            title='1.2. Цифри', price=29, is_published=True, description=DEFAULT_MATERIAL_DESCRIPTION,
            curriculum_topic=make_school_topic('1.2. Цифри', 5, 102))
        self.nmt = StudyMaterial.objects.create(title='5. Відсотки', price=25, is_published=True)
        self.user = self.make_user('desc@example.com')

    def test_school_lesson_described_as_interactive_lesson(self):
        page = self.client.get(f'/material/{self.lesson.id}/', follow=True).content.decode()
        head = page[:page.index('</head>')]
        self.assertIn('Інтерактивний урок за шкільною програмою (Математика · 5 клас)', page)
        self.assertNotIn('Авторський конспект', page)
        self.assertNotIn('НМТ', head.split('og:description')[1][:300])
        self.assertIn('інтерактивний урок з математики (Математика · 5 клас)', head)
        self.assertContains(self.client.get('/materials/'), 'Інтерактивний урок за шкільною')
        nmt = self.client.get(f'/material/{self.nmt.id}/', follow=True).content.decode()
        self.assertIn('Авторський конспект', nmt)
        self.assertIn('конспект для підготовки до НМТ', nmt)

    def test_own_description_is_kept(self):
        StudyMaterial.objects.filter(pk=self.lesson.pk).update(description='Мій опис уроку.')
        self.assertContains(self.client.get(f'/material/{self.lesson.id}/', follow=True), 'Мій опис уроку.')

    def test_review_form_has_text_field_and_moderation_note(self):
        self.client.force_login(self.user)
        page = self.client.get(f'/material/{self.lesson.id}/', follow=True)
        self.assertContains(page, '<label for="review-text"')
        self.assertContains(page, "Відгук з'явиться на сайті після перевірки.")
        self.assertContains(self.client.get('/cabinet/'), "Відгук з'явиться на сайті після перевірки.")

    def test_student_status_request_is_collapsed_until_used(self):
        self.client.force_login(self.user)
        page = self.client.get('/cabinet/').content.decode()
        self.assertIn('<details class="student-status-card student-status-ask"', page)
        self.assertIn('Підтвердити статус учня', page)
        TutorStudentRequest.objects.create(user=self.user, real_name='Учень', course='grade_5', status='pending')
        page = self.client.get('/cabinet/').content.decode()
        self.assertIn('<div class="student-status-card"', page)
        self.assertIn('Заявка на розгляді', page)

class SelfLearnerParentPageTests(BaseTestCase):
    """Сторінка для батьків учня, що вчиться сам: посилання з кабінету, без звітів викладача, можна змінити й вимкнути."""

    def setUp(self):
        self.pupil = self.make_user('self@example.com')
        self.lesson = StudyMaterial.objects.create(
            title='1.2. Цифри', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic('1.2. Цифри', 5, 102))
        self.pupil.purchased_materials.add(self.lesson)
        PracticeAttempt.objects.create(user=self.pupil, material=self.lesson, score=5, answers_json={'answers': []})
        self.client.force_login(self.pupil)

    def link(self):
        self.pupil.refresh_from_db()
        return f'/parents/{self.pupil.parent_token}/' if self.pupil.parent_token else None

    def test_create_open_reset_and_disable_link(self):
        cabinet = self.client.get('/cabinet/')
        self.assertContains(cabinet, 'Створити посилання')
        self.client.post('/parents/link/', {'action': 'create', 'name': 'Тарас'})
        first = self.link()
        self.assertContains(self.client.get('/cabinet/'), f'https://dokvadratu.com.ua{first}')
        page = Client().get(first)
        self.assertContains(page, 'Тарас')
        self.assertContains(page, 'Самостійне навчання · шкільна програма')
        self.assertContains(page, '1.2. Цифри')
        self.assertNotContains(page, 'Звітів про заняття ще немає')
        self.assertNotContains(page, 'ставить вчитель')
        self.assertEqual(Client().get(f'{first}topic/{self.lesson.id}/').status_code, 200)
        self.client.post('/parents/link/', {'action': 'reset'})
        second = self.link()
        self.assertNotEqual(first, second)
        self.assertEqual(Client().get(first).status_code, 404)
        self.assertEqual(Client().get(second).status_code, 200)
        self.client.post('/parents/link/', {'action': 'off'})
        self.assertIsNone(self.link())
        self.assertEqual(Client().get(second).status_code, 404)

    def test_teachers_student_gets_link_from_teacher(self):
        TutorStudentRequest.objects.create(user=self.pupil, real_name='Учень', course='grade_5', status='approved')
        self.assertNotContains(self.client.get('/cabinet/'), 'Створити посилання')

class StorefrontSortAndOwnedTests(BaseTestCase):
    def setUp(self):
        self.cheap = StudyMaterial.objects.create(title='1.1. Дешева', price=10, is_published=True,
                                                  curriculum_topic=make_school_topic('1.1. Дешева', 5, 101))
        self.dear = StudyMaterial.objects.create(title='1.2. Дорога', price=90, is_published=True,
                                                 curriculum_topic=make_school_topic('1.2. Дорога', 5, 102))
        self.mid = StudyMaterial.objects.create(title='1.3. Середня', price=50, is_published=True,
                                                curriculum_topic=make_school_topic('1.3. Середня', 5, 103))
        self.bundle = StudyMaterial.objects.create(title='Пакет', price=100, is_published=True, is_bundle=True)
        self.bundle.included_materials.add(self.cheap, self.dear)
        self.user = self.make_user('shop@example.com')

    def titles(self, query=''):
        return [m.title for m in self.client.get('/materials/' + query).context['materials'] if not m.is_bundle]

    def test_sorting(self):
        self.assertEqual(self.titles(), ['1.1. Дешева', '1.2. Дорога', '1.3. Середня'])
        self.assertEqual(self.titles('?sort=price'), ['1.1. Дешева', '1.3. Середня', '1.2. Дорога'])
        self.assertEqual(self.titles('?sort=-price'), ['1.2. Дорога', '1.3. Середня', '1.1. Дешева'])
        self.assertEqual(self.titles('?sort=new'), ['1.3. Середня', '1.2. Дорога', '1.1. Дешева'])
        self.assertContains(self.client.get('/materials/?sort=price'), '<option value="price" selected>')

    def test_hide_owned(self):
        self.assertNotContains(self.client.get('/materials/'), 'Сховати те, що вже маю')
        self.client.force_login(self.user)
        self.user.purchased_materials.add(self.cheap, self.dear)
        page = self.client.get('/materials/?hide_owned=1')
        shown = {m.title for m in page.context['materials']}
        self.assertEqual(shown, {'1.3. Середня'})   # куплені теми й пакет з ними сховано
        ClassSubscription.objects.create(user=self.user, number=5, valid_until=timezone.localdate())
        self.assertEqual(list(self.client.get('/materials/?hide_owned=1').context['materials']), [])
        self.assertEqual(len(self.client.get('/materials/').context['materials']), 4)

class FriendlyUrlTests(BaseTestCase):
    def test_translit_slug(self):
        from .slugs import slugify_title
        self.assertEqual(slugify_title('1.2. Цифри. Десятковий запис натуральних чисел'),
                         '1-2-tsyfry-desiatkovyi-zapys-naturalnykh-chysel')
        self.assertEqual(slugify_title("1.13. Розв'язування задач"), '1-13-rozviazuvannia-zadach')
        self.assertEqual(slugify_title('Юля Їжак Згода'), 'yulia-yizhak-zghoda')
        self.assertLessEqual(len(slugify_title('дуже ' * 40)), 60)
        self.assertEqual(slugify_title('!!!'), 'material')

    def test_old_and_wrong_urls_redirect_permanently(self):
        lesson = StudyMaterial.objects.create(title='1.2. Цифри', price=29, is_published=True)
        url = lesson.get_absolute_url()
        self.assertEqual(url, f'/material/{lesson.id}-1-2-tsyfry/')
        self.assertContains(self.client.get(url), '1.2. Цифри')
        self.assertRedirects(self.client.get(f'/material/{lesson.id}/'), url, status_code=301)
        self.assertRedirects(self.client.get(f'/material/{lesson.id}-stara-nazva/'), url, status_code=301)
        self.assertContains(self.client.get('/materials/'), f'href="{url}"')

    def test_unpublished_title_is_not_revealed(self):
        hidden = StudyMaterial.objects.create(title='Секретна тема', price=29)
        response = self.client.get(f'/material/{hidden.id}/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.client.get(hidden.get_absolute_url()).status_code, 404)

class SchoolPracticeTests(BaseTestCase):
    def setUp(self):
        self.user = self.make_user('pupil@example.com')
        self.client.force_login(self.user)
        self.topic1 = make_school_topic('1.1. Натуральні числа', 5, 101)
        self.topic2 = make_school_topic('1.2. Цифри', 5, 102)
        self.topic3 = make_school_topic('1.3. Порівняння', 5, 103)
        self.lesson = self.make_lesson(self.topic2)

    def make_lesson(self, topic, **extra):
        extra.setdefault('is_free', True)
        return StudyMaterial.objects.create(title=topic.name, price=0, is_published=True, curriculum_topic=topic, **extra)

    def make_choice(self, text, topic, difficulty=1, skill='SOLVE', hint='', solution=''):
        q = Question.objects.create(text=text, question_type='CHOICE', curriculum_topic=topic, difficulty=difficulty,
                                    nush_skill=skill, hint=hint, solution=solution)
        AnswerOption.objects.create(question=q, text='А) 1', is_correct=False)
        AnswerOption.objects.create(question=q, text='Б) 2', is_correct=True)
        return q

    def fill_bank(self, topic):
        for level in (1, 2, 3):
            for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
                for i in range(3):
                    self.make_choice(f'{skill}{level}-{i}', topic, difficulty=level, skill=skill)

    def current(self, lesson=None):
        response = self.client.get(f'/practice/{(lesson or self.lesson).id}/')
        self.assertEqual(response.status_code, 200)
        return response.context['question']

    def check(self, question, answer, lesson=None):
        return self.client.post(f'/practice/{(lesson or self.lesson).id}/check/', json.dumps(
            {'question_id': question.id, 'answer': answer}), content_type='application/json')

    def answer(self, lesson=None, correct=True):
        q = self.current(lesson)
        option = q.options.get(is_correct=correct)
        return q, self.check(q, str(option.id), lesson).json()

    def run_state(self, lesson=None):
        return PracticeRun.objects.get(user=self.user, material=lesson or self.lesson, finished_at=None).state

    def algebra8(self):
        topic = make_school_topic('3.2. Формула коренів', 8, 302, subject='Алгебра (7-9 класи)')
        return topic, self.make_lesson(topic)

    def test_profiles_and_button_labels(self):
        from .practice import practice_button_label, practice_profile
        self.assertEqual(practice_profile(self.lesson), 'A')
        algebra = make_school_topic('2.1. Функція', 8, 201, subject='Алгебра (7-9 класи)')
        analysis = make_school_topic('4.2. Похідна', 10, 402, subject='Алгебра і початки аналізу (10-11 класи)')
        nmt = make_nmt_topic('26. Похідна')
        self.assertEqual(practice_profile(StudyMaterial(title='x', curriculum_topic=algebra)), 'B')
        self.assertEqual(practice_profile(StudyMaterial(title='x', curriculum_topic=analysis)), 'C')
        self.assertIsNone(practice_profile(StudyMaterial(title='x', curriculum_topic=nmt)))
        self.assertIsNone(practice_profile(StudyMaterial(title='26. Похідна')))
        self.assertEqual(practice_button_label(self.lesson), '✏️ Тренажер')
        self.assertEqual(practice_button_label(StudyMaterial(title='x', curriculum_topic=nmt)), '🎯 Практика НМТ')

    def test_ladder_climbs_after_two_right_and_steps_down_after_two_wrong(self):
        topic, lesson = self.algebra8()
        self.fill_bank(topic)
        self.assertEqual(self.current(lesson).difficulty, 1)
        self.answer(lesson)
        _, data = self.answer(lesson)
        self.assertEqual((data['level'], data['level_change']), (2, 1))
        self.assertEqual(self.current(lesson).difficulty, 2)
        self.answer(lesson, correct=False)
        _, data = self.answer(lesson, correct=False)
        self.assertEqual((data['level'], data['level_change']), (1, -1))

    def test_fast_pupil_masters_in_seven_tasks_with_all_criteria_on_top(self):
        topic, lesson = self.algebra8()
        self.fill_bank(topic)
        statuses = [self.answer(lesson)[1]['status'] for _ in range(7)]
        self.assertEqual(statuses, ['active'] * 6 + ['mastered'])
        top = [e['skill'] for e in self.run_state(lesson)['history'] if e['level'] == 3]
        self.assertEqual(sorted(top), ['ANALYZE', 'MODEL', 'SOLVE'])
        self.assertIsNone(self.client.get(f'/practice/{lesson.id}/').context['question'])  # лише «Побачити оцінку»

        response = self.client.post(f'/practice/{lesson.id}/')
        attempt = PracticeAttempt.objects.get(user=self.user)
        self.assertRedirects(response, f'/attempt/{attempt.id}/', fetch_redirect_response=False)
        self.assertEqual((attempt.nush_modeling, attempt.nush_solving, attempt.nush_analysis), (12, 12, 12))
        self.assertEqual((attempt.score, attempt.max_score), (14, 14))
        details = self.client.get(f'/attempt/{attempt.id}/')
        self.assertContains(details, 'Тему опановано')
        # Наступний вхід (другий урок, ДЗ) — нова практика одразу з третьої сходинки: тему вже опановано
        self.assertEqual(self.current(lesson).difficulty, 3)
        self.assertContains(self.client.get(f'/practice/{lesson.id}/'), 'Продовжуємо зі сходинки 3')

    def test_next_practice_resumes_from_the_level_reached(self):
        topic, lesson = self.algebra8()
        self.fill_bank(topic)
        self.answer(lesson)
        self.answer(lesson)                      # піднявся на сходинку 2
        self.client.post(f'/practice/{lesson.id}/')   # завершив, не дійшовши до кінця
        self.assertEqual(self.current(lesson).difficulty, 2)
        state = self.run_state(lesson)
        self.assertEqual((state['level'], state['start_level']), (2, 2))
        self.answer(lesson, correct=False)
        _, data = self.answer(lesson, correct=False)
        self.assertEqual(data['level'], 1)       # сходинки працюють як звичайно

    def test_summary_and_first_practice_start_from_the_first_level(self):
        from .practice import resume_level
        self.assertEqual(resume_level(None), 1)
        self.assertEqual(resume_level({'kind': 'summary', 'level': 3, 'history': [{}]}), 1)
        self.assertEqual(resume_level({'kind': 'lesson', 'level': 2, 'history': []}), 1)
        self.assertEqual(resume_level({'kind': 'lesson', 'level': 2, 'history': [{}]}), 2)
        self.assertEqual(resume_level({'kind': 'lesson', 'level': 3, 'status': 'mastered', 'history': [{}]}), 3)

    def master_with_bosses(self):
        topic, lesson = self.algebra8()
        self.fill_bank(topic)
        self.boss = self.make_choice('Бос', topic, difficulty=4)
        self.ultra = self.make_choice('Ультра', topic, difficulty=5)
        statuses = [self.answer(lesson)[1]['status'] for _ in range(7)]
        self.assertEqual(statuses[-1], 'mastered')
        return lesson

    def test_boss_and_ultra_boss_give_trophies_without_touching_grades(self):
        lesson = self.master_with_bosses()
        page = self.client.get(f'/practice/{lesson.id}/')
        self.assertContains(page, '⚔️ Бос — прийняти виклик')
        self.assertRedirects(self.client.get(f'/practice/{lesson.id}/?boss=1'), f'/practice/{lesson.id}/',
                             fetch_redirect_response=False)
        page = self.client.get(f'/practice/{lesson.id}/')
        self.assertEqual(page.context['question'], self.boss)
        self.assertContains(page, 'Спроб: 2, підказок немає')
        q, data = self.answer(lesson, correct=False)          # перша спроба — без підказки, друга лишається
        from .practice import BOSS_HINT
        self.assertEqual((data['finished'], data['hint']), (False, BOSS_HINT))
        data = self.check(q, str(q.options.get(is_correct=True).id), lesson).json()
        self.assertTrue(data['boss_won'])
        self.assertEqual((data['status'], data['boss_next']), ('mastered', '👑 Ультра-бос'))

        self.client.get(f'/practice/{lesson.id}/?boss=1')
        page = self.client.get(f'/practice/{lesson.id}/')
        self.assertEqual(page.context['question'], self.ultra)
        self.assertContains(page, 'Спроб: 1')
        _, data = self.answer(lesson)
        self.assertTrue(data['boss_won'])
        self.assertIsNone(data['boss_next'])
        self.assertNotContains(self.client.get(f'/practice/{lesson.id}/'), 'прийняти виклик</a>')

        self.client.post(f'/practice/{lesson.id}/')
        attempt = PracticeAttempt.objects.get(user=self.user)
        self.assertEqual((attempt.nush_modeling, attempt.nush_solving, attempt.nush_analysis), (12, 12, 12))
        self.assertEqual((attempt.score, attempt.max_score), (14, 14))     # боси — не в балах
        self.assertNotIn(str(self.boss.id), attempt.answers_json['question_ids'].split(','))
        self.assertEqual(attempt.boss_trophy, '👑 Ультра-бос')
        self.assertContains(self.client.get(f'/attempt/{attempt.id}/'), '👑 Ультра-бос переможений')
        self.assertFalse(GameMistake.objects.filter(user=self.user, question=self.boss).exists())

    def test_lost_boss_changes_nothing_and_closes_ultra(self):
        lesson = self.master_with_bosses()
        self.client.get(f'/practice/{lesson.id}/?boss=1')
        self.answer(lesson, correct=False)
        _, data = self.answer(lesson, correct=False)
        self.assertFalse(data['boss_won'])
        self.assertIsNone(data['boss_next'])
        page = self.client.get(f'/practice/{lesson.id}/')
        self.assertContains(page, 'бос виявився сильнішим')
        self.client.get(f'/practice/{lesson.id}/?boss=1')   # повторний виклик у цій практиці не дає боса
        self.assertIsNone(self.client.get(f'/practice/{lesson.id}/').context['question'])
        self.client.post(f'/practice/{lesson.id}/')
        attempt = PracticeAttempt.objects.get(user=self.user)
        self.assertEqual((attempt.nush_modeling, attempt.nush_solving, attempt.nush_analysis), (12, 12, 12))
        self.assertEqual(attempt.boss_trophy, '')

    def test_bosses_never_appear_on_the_ladder_and_need_mastery(self):
        topic, lesson = self.algebra8()
        self.make_choice('Легке', topic, difficulty=1)
        self.make_choice('Бос', topic, difficulty=4)
        self.assertEqual(self.current(lesson).difficulty, 1)
        self.client.get(f'/practice/{lesson.id}/?boss=1')    # тему ще не опановано — бос не відкривається
        self.answer(lesson)
        page = self.client.get(f'/practice/{lesson.id}/')
        self.assertIsNone(page.context['question'])          # завдання скінчились, боса не підсунуто
        self.assertEqual(self.run_state(lesson)['status'], 'empty')

    def test_slow_pupil_gets_grade_of_the_level_reached(self):
        topic, lesson = self.algebra8()
        self.fill_bank(topic)
        for correct in (True, True, False, True, False, True):   # піднявся на сходинку 2 і там то так, то ні
            self.answer(lesson, correct=correct)
        self.client.post(f'/practice/{lesson.id}/')
        grades = [g for _, g in PracticeAttempt.objects.get().nush_grades if g is not None]
        self.assertTrue(7 <= max(grades) <= 9 and all(g <= 9 for g in grades), grades)

    def test_trainer_gives_hint_then_second_try_for_half_points(self):
        q = self.make_choice('q', self.topic2, skill='MODEL', hint='Порахуй ще раз', solution='Це 2')
        self.assertEqual(self.current(), q)
        first = self.check(q, str(q.options.get(is_correct=False).id)).json()
        self.assertEqual(first, {'correct': False, 'finished': False, 'hint': 'Порахуй ще раз'})
        second = self.check(q, str(q.options.get(is_correct=True).id)).json()
        self.assertTrue(second['correct'] and second['finished'])
        self.assertEqual(second['solution'], 'Це 2')
        self.assertEqual(self.check(q, '1').status_code, 409)   # спроби закінчились
        self.client.post(f'/practice/{self.lesson.id}/')
        attempt = PracticeAttempt.objects.get(user=self.user)
        self.assertEqual((attempt.score, attempt.max_score), (1, 2))
        self.assertEqual(attempt.nush_modeling, 4)   # розв'язав на сходинці 1 (середній рівень), але не з першої спроби
        self.assertIsNone(attempt.nush_solving)
        self.assertTrue(GameMistake.objects.filter(user=self.user, question=q).exists())

    def test_progress_is_kept_when_pupil_leaves(self):
        for i in range(3):
            self.make_choice(f'q{i}', self.topic2)
        first = self.current()
        self.assertEqual(self.current(), first)   # повернувся — те саме завдання
        self.check(first, str(first.options.get(is_correct=True).id))
        self.assertNotEqual(self.current(), first)
        self.assertEqual(PracticeRun.objects.filter(user=self.user).count(), 1)

    def test_every_fifth_task_reviews_earlier_topics_and_later_topics_never_appear(self):
        for i in range(10):
            self.make_choice(f'own{i}', self.topic2)
        old = self.make_choice('old', self.topic1)
        later = self.make_choice('later', self.topic3)
        Question.objects.create(text='match', question_type='MATCH', curriculum_topic=self.topic2)
        shown = []
        for _ in range(6):
            q, _ = self.answer()
            shown.append(q)
        self.assertEqual(shown[4], old)
        self.assertNotIn(later, shown)
        self.assertTrue(all(q.question_type == 'CHOICE' for q in shown))

    def test_finish_early_saves_what_was_solved(self):
        self.fill_bank(self.topic2)
        q, _ = self.answer()
        self.client.post(f'/practice/{self.lesson.id}/')
        attempt = PracticeAttempt.objects.get()
        self.assertEqual(attempt.answers_json['question_ids'], str(q.id))
        self.assertEqual(sum(1 for _, g in attempt.nush_grades if g is not None), 1)

    def test_limit_stops_practice(self):
        self.fill_bank(self.topic2)
        with mock.patch('materials.practice.MAX_TASKS', 3):
            statuses = [self.answer(correct=False)[1].get('status') for _ in range(6)]
        # Тренажер: дві хибні спроби — завдання завершене
        self.assertIn('limit', statuses)

    def test_check_rejects_other_question(self):
        q = self.make_choice('q', self.topic2)
        other = self.make_choice('other', self.topic3)
        self.current()
        self.assertEqual(self.check(other, '1').status_code, 409)
        self.assertEqual(self.check(q, '').status_code, 400)   # порожня відповідь не з'їдає спробу

    def test_paid_school_lesson_needs_purchase(self):
        self.lesson.is_free = False
        self.lesson.save()
        q = self.make_choice('q', self.topic2)
        response = self.client.get(f'/practice/{self.lesson.id}/')
        self.assertRedirects(response, self.lesson.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(self.check(q, '1').status_code, 404)

    def make_typed(self, q_type, spec, topic=None):
        return Question.objects.create(text=f'{q_type}?', question_type=q_type, spec=spec,
                                       curriculum_topic=topic or self.topic2)

    def test_new_types_are_checked_on_the_server_without_leaking_answers(self):
        topic, lesson = self.algebra8()
        cases = [
            ('MULTI', {'options': [['1', True], ['0', False], ['5', True]]}, [2, 0], [0]),
            ('TF', {'statements': [['a', True], ['b', False]]}, [True, False], [True, True]),
            ('FIELDS', {'fields': [['x₁ =', '2'], ['x₂ =', '-3']], 'unordered': True}, ['-3', '2,0'], ['2', '3']),
            ('ERROR', {'steps': ['s1', 's2', 's3'], 'wrong': 1}, 1, 2),
            ('GROUP', {'groups': ['N', 'не N'], 'items': [['7', 0], ['0', 1]]}, [0, 1], [1, 1]),
            ('EXPR', {'answer': '2(a+b)', 'vars': ['a', 'b']}, '2a + 2b', 'a+2b'),
            ('POINT', {'min': 0, 'max': 2, 'step': 0.25, 'answer': 0.75}, 0.75, 1),
            ('COORD', {'xmin': -5, 'xmax': 5, 'ymin': -5, 'ymax': 5, 'step': 1, 'answer': [2, -1]}, [2, -1], [-1, 2]),
        ]
        for q_type, spec, right, wrong in cases:
            with self.subTest(q_type):
                Question.objects.all().delete()
                PracticeRun.objects.all().delete()
                q = self.make_typed(q_type, spec, topic)
                page = self.client.get(f'/practice/{lesson.id}/')
                public = page.context['spec']
                self.assertNotIn('answer', public)
                self.assertNotIn('correct', public)
                self.assertNotIn('wrong', public)
                self.assertFalse(self.check(q, wrong, lesson).json()['correct'])
                PracticeRun.objects.all().delete()
                self.client.get(f'/practice/{lesson.id}/')
                self.assertTrue(self.check(q, right, lesson).json()['correct'])

    def test_order_answer_uses_screen_positions(self):
        q = self.make_typed('ORDER', {'items': ['1', '10', '100', '1000']})
        page = self.client.get(f'/practice/{self.lesson.id}/')
        perm = self.run_state()['history'][-1]['perm']
        self.assertEqual(page.context['spec']['items'], [['1', '10', '100', '1000'][i] for i in perm])
        positions = [perm.index(i) for i in range(4)]
        data = self.check(q, positions[::-1]).json()
        self.assertFalse(data['correct'])
        self.assertTrue(self.check(q, positions).json()['correct'])

    def test_pupil_text_is_escaped_on_results(self):
        topic, lesson = self.algebra8()
        q = self.make_typed('EXPR', {'answer': 'a', 'vars': ['a']}, topic)
        self.client.get(f'/practice/{lesson.id}/')
        self.check(q, '<b>x</b>', lesson)
        response = self.client.post(f'/practice/{lesson.id}/', follow=True)
        self.assertContains(response, '&lt;b&gt;x&lt;/b&gt;')

    def test_skill_grade_scale(self):
        from .practice import skill_grade
        self.assertIsNone(skill_grade([]))
        self.assertEqual(skill_grade([(1, False, False, False)]), 1)
        self.assertEqual(skill_grade([(1, True, True, True), (1, True, True, True)]), 6)
        self.assertEqual(skill_grade([(1, True, True, True), (2, True, True, True)]), 9)
        self.assertEqual(skill_grade([(3, True, True, True), (3, False, False, False)]), 11)
        self.assertEqual(skill_grade([(3, True, True, True)]), 12)


SCHOOL_BANK = '''TOPIC_NAME = "1.2. Цифри"
COURSE = "Математика (5-6 класи)"
GRADE = "5 клас"
TASKS = [
    {"type": "CHOICE", "difficulty": 1, "skill": "MODEL", "text": "Скільки цифр?", "hint": "Порахуй",
     "solution": "Десять", "options": [("10", True), ("9", False)]},
    {"type": "SHORT", "difficulty": 2, "skill": "WRONG", "text": "Погане", "answer": "1"},
    {"type": "SHORT", "difficulty": 2, "topic": "9.9. Нема такої", "text": "Чужа тема", "answer": "1"},
    {"type": "GROUP", "difficulty": 1, "skill": "SOLVE", "text": "Розклади", "groups": ["N", "не N"],
     "items": [("7", 0), ("0", 1)], "solution": "0 не натуральне"},
    {"type": "EXPR", "difficulty": 2, "text": "Вираз", "answer": "2(a+", "vars": ["a"]},
    {"type": "POINT", "difficulty": 2, "text": "Точка", "min": 0, "max": 2, "step": 0.5, "answer": 3},
]
'''


class SchoolBankImportTests(BaseTestCase):
    url = '/do-kvadratu-secret-control/materials/question/import-bank/'

    def setUp(self):
        self.client.force_login(self.make_user('boss2@example.com', is_staff=True, is_superuser=True))
        self.topic = make_school_topic('1.2. Цифри', 5, 102)
        make_school_topic('1.2. Цифри', 6, 102, subject='Інший курс')  # така сама назва в іншому курсі
        self.lesson = StudyMaterial.objects.create(title='Цифри', price=0, curriculum_topic=self.topic)

    def upload(self, action):
        from django.core.files.uploadedfile import SimpleUploadedFile
        return self.client.post(self.url, {'action': action, 'bank_file': SimpleUploadedFile('b.py', SCHOOL_BANK.encode())})

    def test_school_bank_resolves_topic_by_course_and_grade(self):
        report = self.upload('preview').context['report']
        self.assertEqual(report.to_add, [1, 4])
        self.assertEqual([i for i, _ in report.errors], [2, 3, 5, 6])
        self.assertIn('Нема такої', report.errors[1][1])
        self.client.post(self.url, {'action': 'import'})
        q = Question.objects.get(text='Скільки цифр?')
        self.assertEqual((q.curriculum_topic, q.nush_skill, q.hint, q.solution), (self.topic, 'MODEL', 'Порахуй', 'Десять'))
        self.assertEqual(list(q.materials.all()), [self.lesson])
        group = Question.objects.get(text='Розклади')
        self.assertEqual(group.spec, {'groups': ['N', 'не N'], 'items': [['7', 0], ['0', 1]]})
        # Повторний імпорт — дублікати, нічого не додається
        report = self.upload('preview').context['report']
        self.assertEqual(len(report.duplicates), 2)

    def test_course_without_grade_is_rejected(self):
        from .bank_import import BankFormatError, parse_bank_source
        with self.assertRaises(BankFormatError):
            parse_bank_source('TOPIC_NAME = "x"\nCOURSE = "y"\nTASKS = []\n')


class LessonPracticeTests(BaseTestCase):
    """Вчитель на уроці показує екран і сам натискає; практика зараховується обраному учню."""

    def setUp(self):
        self.teacher = self.make_user('teacher@example.com', is_staff=True)
        self.pupil = self.make_user('kid@example.com')
        self.request = TutorStudentRequest.objects.create(user=self.pupil, real_name='Петренко Оля', course='grade_5',
                                                          status='approved')
        other = self.make_user('pending@example.com')
        TutorStudentRequest.objects.create(user=other, real_name='Ще не підтверджений', status='pending')
        topic = make_school_topic('1.1. Натуральні числа', 5, 101)
        self.lesson = StudyMaterial.objects.create(title='1.1', price=100, is_published=True, curriculum_topic=topic)
        for i in range(4):
            q = Question.objects.create(text=f'q{i}', question_type='CHOICE', curriculum_topic=topic, difficulty=1)
            AnswerOption.objects.create(question=q, text='А) 1', is_correct=False)
            AnswerOption.objects.create(question=q, text='Б) 2', is_correct=True)
        self.client.force_login(self.teacher)

    def url(self, query=''):
        return f'/practice/{self.lesson.id}/{query}'

    def answer(self, query, correct=False):
        q = self.client.get(self.url(query)).context['question']
        option = q.options.get(is_correct=correct)
        return self.client.post(f'/practice/{self.lesson.id}/check/{query}', json.dumps(
            {'question_id': q.id, 'answer': str(option.id)}), content_type='application/json')

    def test_teacher_first_chooses_the_pupil(self):
        response = self.client.get(self.url())
        self.assertTemplateUsed(response, 'materials/practice_choose_student.html')
        self.assertContains(response, 'Петренко Оля')
        self.assertNotContains(response, 'Ще не підтверджений')
        self.assertContains(response, '?demo=1')

    def test_lesson_practice_is_credited_to_the_pupil(self):
        query = f'?student={self.request.id}'
        page = self.client.get(self.url(query))
        self.assertContains(page, 'class="lesson"')
        self.assertContains(page, 'Петренко Оля')
        self.assertContains(page, escapejs(f'/practice/{self.lesson.id}/check/{query}'))   # адреса в JS-рядку
        self.answer(query, correct=False)
        self.answer(query, correct=False)   # тренажер: друга спроба
        response = self.client.post(self.url(query))
        attempt = PracticeAttempt.objects.get()
        self.assertEqual((attempt.user, attempt.conducted_by), (self.pupil, self.teacher))
        self.assertRedirects(response, f'/attempt/{attempt.id}/', fetch_redirect_response=False)
        self.assertTrue(GameMistake.objects.filter(user=self.pupil).exists())
        self.assertFalse(GameMistake.objects.filter(user=self.teacher).exists())

        details = self.client.get(f'/attempt/{attempt.id}/')
        self.assertEqual(details.context['report_student'], self.request)
        self.assertContains(details, 'Додати в звіт заняття')
        self.assertContains(details, f'?student={self.request.id}')   # «Ще раз» — з тим самим учнем

        # Учень бачить свою спробу, позначену «на уроці»
        self.client.force_login(self.pupil)
        self.assertContains(self.client.get('/cabinet/'), 'на уроці')

    def test_report_from_results_reaches_the_dashboard(self):
        response = self.client.post('/cabinet/add-report/', {
            'student_id': self.request.id, 'curriculum_topic': self.lesson.curriculum_topic_id,
            'nush_modeling': 7, 'nush_solving': 8, 'nush_analysis': 6, 'homework_status': 'not_assigned',
            'teacher_comment': ''})
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)
        self.assertEqual(StudentReport.objects.get().nush_solving, 8)

    def test_demo_saves_nothing(self):
        self.answer('?demo=1', correct=True)
        response = self.client.post(self.url('?demo=1'))
        self.assertTemplateUsed(response, 'materials/practice_school_results.html')
        self.assertContains(response, 'Демонстрація')
        self.assertFalse(PracticeAttempt.objects.exists())
        self.assertFalse(PracticeRun.objects.exists())
        self.assertFalse(GameMistake.objects.exists())

    def test_check_without_choice_is_refused(self):
        q = Question.objects.first()
        response = self.client.post(f'/practice/{self.lesson.id}/check/', json.dumps(
            {'question_id': q.id, 'answer': '1'}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_lesson_and_homework_runs_do_not_mix(self):
        query = f'?student={self.request.id}'
        lesson_question = self.client.get(self.url(query)).context['question']
        self.lesson.is_free = True
        self.lesson.save()
        self.client.force_login(self.pupil)
        self.client.get(self.url('?student=999'))   # параметр учня для учня нічого не змінює
        runs = PracticeRun.objects.filter(user=self.pupil)
        self.assertEqual(sorted(r.teacher_id is None for r in runs), [False, True])
        self.assertEqual(runs.get(teacher=self.teacher).state['history'][0]['qid'], lesson_question.id)


class LearningSituationsTests(BaseTestCase):
    """Нестандартні ситуації: тренування для батьків, підказка вчителя, ДЗ, «застряг», прогалини, виправлення, групи."""

    def setUp(self):
        self.teacher = self.make_user('t2@example.com', is_staff=True)
        self.pupil = self.make_user('p2@example.com')
        self.request = TutorStudentRequest.objects.create(user=self.pupil, real_name='Оля', course='grade_5',
                                                          status='approved')
        self.topic_old = make_school_topic('1.1. Натуральні числа', 5, 101)
        self.topic = make_school_topic('1.2. Цифри', 5, 102)
        self.topic_next = make_school_topic('1.3. Порівняння', 5, 103)
        self.lesson = StudyMaterial.objects.create(title='1.2. Цифри', price=100, is_published=True,
                                                   curriculum_topic=self.topic)
        self.old_lesson = StudyMaterial.objects.create(title='1.1. Натуральні', price=0, is_published=True,
                                                       curriculum_topic=self.topic_old)
        self.next_lesson = StudyMaterial.objects.create(title='1.3. Порівняння', price=0, is_published=True,
                                                        curriculum_topic=self.topic_next)

    def bank(self, topic, levels=(1, 2, 3), per=3):
        for level in levels:
            for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
                for i in range(per):
                    q = Question.objects.create(text=f'{topic.id}-{skill}{level}-{i}', question_type='CHOICE',
                                                curriculum_topic=topic, difficulty=level, nush_skill=skill)
                    AnswerOption.objects.create(question=q, text='А) 1', is_correct=False)
                    AnswerOption.objects.create(question=q, text='Б) 2', is_correct=True)

    def answer(self, query='', correct=True, assisted=False, lesson=None):
        lesson = lesson or self.lesson
        q = self.client.get(f'/practice/{lesson.id}/{query}').context['question']
        payload = {'question_id': q.id, 'answer': str(q.options.get(is_correct=correct).id)}
        if assisted:
            payload['assisted'] = True
        data = self.client.post(f'/practice/{lesson.id}/check/{query}', json.dumps(payload),
                                content_type='application/json').json()
        return q, data

    def lesson_query(self):
        return f'?student={self.request.id}'

    def test_parents_see_level_and_trend_not_points(self):
        self.client.force_login(self.teacher)
        self.bank(self.topic)
        for correct in (False, False, False, False):
            self.answer(self.lesson_query(), correct=correct)
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        for _ in range(7):
            self.answer(self.lesson_query())
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        response = self.client.get(f'/parents/{self.request.parent_token}/')
        self.assertContains(response, 'Тренування на платформі')
        self.assertContains(response, 'початковий → <strong>високий</strong>')
        self.assertContains(response, 'тему опановано')
        self.assertNotContains(response, 'балів')
        # Батьки розбирають кожну спробу: завдання й відповіді, без кнопок учня і без балів
        self.assertContains(response, 'Як проходив тренування й тести')
        attempt = PracticeAttempt.objects.filter(user=self.request.user).latest('created_at')
        detail = self.client.get(f'/parents/{self.request.parent_token}/attempt/{attempt.id}/')
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, '← До звіту')
        self.assertNotContains(detail, '🔁 Ще раз')
        self.assertNotContains(detail, 'балів')
        self.assertNotContains(detail, 'add-report')

    def test_assisted_task_does_not_move_the_ladder_or_count(self):
        self.client.force_login(self.teacher)
        self.bank(self.topic)
        self.answer(self.lesson_query(), assisted=True)
        self.answer(self.lesson_query(), assisted=True)
        run = PracticeRun.objects.get()
        self.assertEqual((run.state['level'], run.state['ok']), (1, 0))
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        attempt = PracticeAttempt.objects.get()
        self.assertEqual(attempt.max_score, 0)
        self.assertEqual(attempt.nush_grades, [])
        # Для учня, що практикується сам, позначка ігнорується
        self.lesson.is_free = True
        self.lesson.save()
        self.client.force_login(self.pupil)
        self.answer(assisted=True)
        self.assertNotIn('assisted', PracticeRun.objects.get(teacher=None).state['history'][0])

    def test_homework_flow(self):
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        due = timezone.localdate() + datetime.timedelta(days=3)
        self.client.post('/homework/assign/', {'student_id': self.request.id, 'material_id': self.lesson.id,
                                               'due_date': due.isoformat()})
        hw = Homework.objects.get()
        self.assertEqual(self.client.get('/cabinet/').context['homeworks'][0].state, 'waiting')

        # Урок платний і не куплений, але ДЗ відкриває практику
        self.client.force_login(self.pupil)
        cabinet = self.client.get('/cabinet/')
        self.assertContains(cabinet, 'Мої домашні завдання')
        self.answer()
        self.client.force_login(self.teacher)
        row = self.client.get('/cabinet/').context['homeworks'][0]
        self.assertEqual((row.state, row.answered), ('started', 1))
        self.assertEqual(self.client.get('/cabinet/').context['homeworks'][0].label, '🟠 Почав, не завершив')

        # Вчитель зараховує зроблене
        self.client.post(f'/homework/{hw.id}/credit/')
        hw.refresh_from_db()
        self.assertEqual(hw.attempt.user, self.pupil)
        self.assertIsNone(hw.attempt.conducted_by)
        self.assertEqual(self.client.get('/cabinet/').context['homeworks'][0].state, 'done')

    def test_homework_result_is_the_first_attempt_and_home_lesson_gap_warns(self):
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        for _ in range(4):
            self.answer(self.lesson_query(), correct=False)
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')   # на уроці — початковий рівень
        Homework.objects.create(teacher=self.teacher, student=self.request, material=self.lesson,
                                due_date=timezone.localdate())
        self.client.force_login(self.pupil)
        for _ in range(7):
            self.answer()
        self.client.post(f'/practice/{self.lesson.id}/')
        first = PracticeAttempt.objects.filter(user=self.pupil, conducted_by=None).get()
        self.answer()
        self.client.post(f'/practice/{self.lesson.id}/')   # друга домашня спроба результату ДЗ не змінює
        self.assertEqual(Homework.objects.get().attempt, first)
        self.client.force_login(self.teacher)
        row = self.client.get('/cabinet/').context['homeworks'][0]
        self.assertIn('Вдома 12', row.warning)

    def test_report_status_comes_from_homework(self):
        from .homework import report_status
        self.assertEqual(report_status(self.request), 'not_assigned')
        Homework.objects.create(student=self.request, material=self.lesson,
                                due_date=timezone.localdate() - datetime.timedelta(days=1))
        self.assertEqual(report_status(self.request), 'not_submitted')

    def test_stuck_pupil_and_gaps_are_flagged(self):
        self.bank(self.topic)
        self.bank(self.topic_old, levels=(1,))
        self.client.force_login(self.teacher)
        for _ in range(16):   # тренажер: 2 спроби на завдання — 8 завдань без правильних
            self.answer(self.lesson_query(), correct=False)
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        attempt = PracticeAttempt.objects.get()
        self.assertTrue(attempt.answers_json['stuck'])
        self.assertEqual(attempt.answers_json['gaps'], [self.topic_old.id])
        details = self.client.get(f'/attempt/{attempt.id}/')
        self.assertContains(details, 'Що далі')
        self.assertContains(details, self.topic_old.name)
        attention = self.client.get('/cabinet/').context['attention']
        self.assertEqual(attention[0]['gap_names'], [self.topic_old.name])

    def test_mastered_pupil_gets_next_topic(self):
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        for _ in range(7):
            self.answer(self.lesson_query())
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        details = self.client.get(f'/attempt/{PracticeAttempt.objects.get().id}/')
        self.assertEqual(details.context['next_material'], self.next_lesson)
        self.assertContains(details, f'/practice/{self.next_lesson.id}/?student={self.request.id}')

    def test_teacher_moves_or_deletes_attempt(self):
        other_user = self.make_user('p3@example.com')
        other = TutorStudentRequest.objects.create(user=other_user, real_name='Марко', status='approved')
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        self.answer(self.lesson_query())
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        attempt = PracticeAttempt.objects.get()
        self.client.post(f'/attempt/{attempt.id}/manage/', {'action': 'move', 'student_id': other.id})
        attempt.refresh_from_db()
        self.assertEqual(attempt.user, other_user)
        self.client.post(f'/attempt/{attempt.id}/manage/', {'action': 'delete'})
        self.assertFalse(PracticeAttempt.objects.exists())
        self.client.force_login(self.pupil)
        self.client.post(f'/attempt/1/manage/', {'action': 'delete'})   # учень не може

    def test_fixing_a_question_recalculates_grades(self):
        from .practice import recalculate_attempts
        self.bank(self.topic, levels=(1,), per=1)
        self.client.force_login(self.teacher)
        q, data = self.answer(self.lesson_query(), correct=False)
        self.answer(self.lesson_query(), correct=False)
        self.client.post(f'/practice/{self.lesson.id}/{self.lesson_query()}')
        attempt = PracticeAttempt.objects.get()
        self.assertEqual(attempt.score, 0)
        # У банку була помилка: «правильним» мав бути варіант, який обрав учень
        q.options.update(is_correct=models.Case(models.When(text='А) 1', then=True), default=False))
        self.assertEqual(recalculate_attempts(q), 1)
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, 2)

    def test_units_after_number_are_accepted(self):
        from .games import short_answer_matches
        self.assertTrue(short_answer_matches('5 см', '5'))
        self.assertTrue(short_answer_matches('12,5 кг', '12.5'))
        self.assertFalse(short_answer_matches('5 x', '5'))

    def test_group_lesson_rotates_pupils_and_keeps_separate_ladders(self):
        other_user = self.make_user('p4@example.com')
        other = TutorStudentRequest.objects.create(user=other_user, real_name='Марко', course='grade_5',
                                                   status='approved')
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        group = f'?g={self.request.id}&g={other.id}'
        page = self.client.get(f'/practice/{self.lesson.id}/{group}')
        self.assertEqual(page.context['actor'].student, self.request)
        self.assertEqual(page.context['next_query'], f'{group}&student={other.id}')
        self.answer(f'{group}&student={self.request.id}')
        self.answer(f'{group}&student={self.request.id}')   # Оля піднялась на 2-гу сходинку
        self.answer(f'{group}&student={other.id}', correct=False)
        response = self.client.post(f'/practice/{self.lesson.id}/{group}', {'scope': 'group'})
        self.assertTemplateUsed(response, 'materials/practice_group_results.html')
        self.assertEqual({a.user for a in PracticeAttempt.objects.all()}, {self.pupil, other_user})
        self.assertEqual(PracticeRun.objects.filter(finished_at=None).count(), 0)

    def test_group_page_checks_answer_for_the_current_pupil(self):
        """Адреса перевірки в JS — без «&amp;»: інакше сервер не бачить учня групи (409) і сторінка лише перезавантажується."""
        other = TutorStudentRequest.objects.create(user=self.make_user('p6@example.com'), real_name='Марко',
                                                   course='grade_5', status='approved')
        self.bank(self.topic)
        self.client.force_login(self.teacher)
        query = f'?g={self.request.id}&g={other.id}&student={other.id}'
        page = self.client.get(f'/practice/{self.lesson.id}/{query}')
        url = json.loads('"%s"' % re.search(r"fetch\('([^']*)'", page.content.decode()).group(1))
        self.assertEqual(url, f'/practice/{self.lesson.id}/check/{query}')
        q = page.context['question']
        response = self.client.post(url, json.dumps({'question_id': q.id, 'answer': str(q.options.get(is_correct=True).id)}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['correct'])

    def test_review_task_on_top_step_does_not_hide_a_criterion(self):
        """Повторення на третій сходинці — легке завдання: критерій з нього не вважається «пройденим» на вершині."""
        self.bank(self.topic)
        self.bank(self.topic_old, levels=(1,))
        self.client.force_login(self.teacher)
        statuses = [self.answer(self.lesson_query())[1]['status'] for _ in range(8)]
        self.assertEqual(statuses[-1], 'mastered')
        history = PracticeRun.objects.get().state['history']
        top = sorted(e['skill'] for e in history if e['difficulty'] == 3)
        self.assertEqual(top, ['ANALYZE', 'MODEL', 'SOLVE'])



class SummaryAndDiagnosticTests(BaseTestCase):
    """Узагальнення розділу — сходинки за всіма темами розділу; діагностика за клас — карта прогалин без оцінки."""

    def setUp(self):
        from .curriculum import ensure_special_topics
        self.teacher = self.make_user('t5@example.com', is_staff=True)
        self.pupil = self.make_user('p5@example.com')
        self.request = TutorStudentRequest.objects.create(user=self.pupil, real_name='Оля', course='grade_6',
                                                          status='approved')
        self.topics = [make_school_topic(f'1.{i}. Тема {i}', 5, 100 + i) for i in range(1, 4)]
        self.other_chapter = make_school_topic('2.1. Відрізок', 5, 201, chapter_order=20)
        for topic in self.topics + [self.other_chapter]:
            for level in (1, 2, 3):
                for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
                    q = Question.objects.create(text=f'{topic.name}-{skill}{level}', question_type='CHOICE',
                                                curriculum_topic=topic, difficulty=level, nush_skill=skill)
                    AnswerOption.objects.create(question=q, text='А) 1', is_correct=False)
                    AnswerOption.objects.create(question=q, text='Б) 2', is_correct=True)
        self.assertEqual(ensure_special_topics(CurriculumGrade, CurriculumChapter, CurriculumTopic, StudyMaterial), 3)
        self.assertEqual(ensure_special_topics(CurriculumGrade, CurriculumChapter, CurriculumTopic, StudyMaterial), 0)
        self.summary = StudyMaterial.objects.get(curriculum_topic__kind='summary',
                                                 curriculum_topic__chapter=self.topics[0].chapter)
        self.diagnostic = StudyMaterial.objects.get(curriculum_topic__kind='diagnostic')
        self.client.force_login(self.teacher)
        self.query = f'?student={self.request.id}'

    def answer(self, material, correct=True):
        q = self.client.get(f'/practice/{material.id}/{self.query}').context['question']
        data = self.client.post(f'/practice/{material.id}/check/{self.query}', json.dumps(
            {'question_id': q.id, 'answer': str(q.options.get(is_correct=correct).id)}),
            content_type='application/json').json()
        return q, data

    def test_special_materials_are_hidden_but_ready(self):
        self.assertFalse(self.summary.is_published)
        self.assertTrue(self.summary.is_free)
        self.assertEqual(self.summary.title, 'Узагальнення: Розділ 10')
        self.assertIn(self.summary, self.client.get('/cabinet/').context['special_materials'])
        response = self.client.get(f'/practice/start/?material_id={self.summary.id}')
        self.assertRedirects(response, f'/practice/{self.summary.id}/', fetch_redirect_response=False)

    def test_summary_rotates_topics_of_the_chapter_only(self):
        shown = [self.answer(self.summary)[0] for _ in range(3)]
        self.assertEqual({q.curriculum_topic for q in shown}, set(self.topics))
        self.client.post(f'/practice/{self.summary.id}/{self.query}')
        attempt = PracticeAttempt.objects.get()
        self.assertEqual(attempt.answers_json['kind'], 'summary')
        self.assertEqual(len(attempt.answers_json['topic_map']), 3)
        self.assertIsNotNone(attempt.nush_solving or attempt.nush_modeling or attempt.nush_analysis)
        self.assertContains(self.client.get(f'/attempt/{attempt.id}/'), 'По темах розділу')

    def test_diagnostic_is_one_try_per_task_across_the_grade_without_grades(self):
        q, data = self.answer(self.diagnostic, correct=False)
        self.assertTrue(data['finished'])   # навіть у тренажері 5 кл. — одна спроба
        plan = PracticeRun.objects.get().state['plan']
        self.assertEqual(len(plan), 8)   # 4 теми × 2 базові завдання
        self.assertTrue(all(Question.objects.get(id=i).difficulty <= 2 for i in plan))
        for _ in range(7):
            data = self.answer(self.diagnostic)[1]
        self.assertEqual(data['status'], 'done')
        self.client.post(f'/practice/{self.diagnostic.id}/{self.query}')
        attempt = PracticeAttempt.objects.get()
        self.assertEqual(attempt.nush_grades, [])
        self.assertFalse(attempt.answers_json['stuck'])
        details = self.client.get(f'/attempt/{attempt.id}/')
        self.assertContains(details, 'Карта тем')
        self.assertNotContains(details, 'Додати в звіт заняття')
        parents = self.client.get(f'/parents/{self.request.parent_token}/')
        self.assertContains(parents, 'Діагностика: з чого починаємо')
        self.assertContains(parents, self.topics[0].name)

    def test_diagnostic_can_be_homework_although_unpublished(self):
        Homework.objects.create(teacher=self.teacher, student=self.request, material=self.diagnostic,
                                due_date=timezone.localdate())
        self.client.force_login(self.pupil)
        self.assertEqual(self.client.get(f'/practice/{self.diagnostic.id}/').status_code, 200)


class TutorAccountTests(BaseTestCase):
    """Репетитор з підпискою на клас: свої учні, свої класи — і нічого чужого."""

    def setUp(self):
        self.owner = self.make_user('owner@example.com', is_staff=True)
        self.tutor = self.make_user('tutor@example.com', role='teacher')
        self.other_tutor = self.make_user('tutor2@example.com', role='teacher')
        self.topic5 = make_school_topic('1.1. Натуральні', 5, 101)
        self.topic8 = make_school_topic('1.1. Дроби', 8, 101, subject='Алгебра (7-9 класи)')
        self.lesson5 = StudyMaterial.objects.create(title='5 кл', price=100, is_published=True, curriculum_topic=self.topic5)
        self.lesson8 = StudyMaterial.objects.create(title='8 кл', price=100, is_published=True, curriculum_topic=self.topic8)
        for topic in (self.topic5, self.topic8):
            q = Question.objects.create(text=f'q{topic.id}', question_type='CHOICE', curriculum_topic=topic, difficulty=1)
            AnswerOption.objects.create(question=q, text='А) 1', is_correct=True)
            AnswerOption.objects.create(question=q, text='Б) 2', is_correct=False)
        today = timezone.localdate()
        TeacherLicense.objects.create(teacher=self.tutor, grade=self.topic5.chapter.grade,
                                      valid_until=today + datetime.timedelta(days=30))
        TeacherLicense.objects.create(teacher=self.other_tutor, grade=self.topic5.chapter.grade,
                                      valid_until=today + datetime.timedelta(days=30))
        self.kid = self.make_user('kid5@example.com')
        self.kid_request = TutorStudentRequest.objects.create(user=self.kid, real_name='Мій учень', course='grade_5',
                                                              status='approved', teacher=self.tutor)
        self.owners_kid = self.make_user('owners@example.com')
        self.owners_request = TutorStudentRequest.objects.create(user=self.owners_kid, real_name='Учень власника',
                                                                 status='approved')
        self.others_kid = self.make_user('others@example.com')
        self.others_request = TutorStudentRequest.objects.create(user=self.others_kid, real_name='Чужий учень',
                                                                 status='approved', teacher=self.other_tutor)

    def test_tutor_cabinet_shows_only_own_pupils_and_licensed_lessons(self):
        self.client.force_login(self.tutor)
        context = self.client.get('/cabinet/').context
        self.assertEqual(list(context['my_students']), [self.kid_request])
        self.assertIn('/join/', context['invite_url'])
        self.assertEqual([m for g in context['tutor_lessons'] for m in g['materials']], [self.lesson5])
        self.assertNotIn('nmt_materials', context)
        self.assertEqual({m.id for m in context['school_materials']}, {self.lesson5.id})

    def test_owner_keeps_own_pupils_only(self):
        self.client.force_login(self.owner)
        context = self.client.get('/cabinet/').context
        self.assertEqual(list(context['my_students']), [self.owners_request])
        # Власник теж запрошує посиланням — учні стають його учнями без заявки
        code = context['invite_url'].rstrip('/').rsplit('/', 1)[-1]
        newbie = self.make_user('owners-new@example.com')
        self.client.force_login(newbie)
        self.client.post(f'/join/{code}/', {'real_name': 'Новий', 'course': 'grade_6'})
        self.client.force_login(self.owner)
        self.assertEqual(len(self.client.get('/cabinet/').context['my_students']), 2)

    def test_lesson_practice_cannot_target_someone_elses_pupil(self):
        self.client.force_login(self.tutor)
        page = self.client.get(f'/practice/{self.lesson5.id}/')
        self.assertEqual(page.context['students'], [self.kid_request])
        page = self.client.get(f'/practice/{self.lesson5.id}/?student={self.others_request.id}')
        self.assertTemplateUsed(page, 'materials/practice_choose_student.html')   # не зараховується чужому
        self.assertEqual(self.client.get(f'/practice/{self.lesson5.id}/?student={self.kid_request.id}').status_code, 200)

    def test_tutor_shows_licensed_grade_only(self):
        self.client.force_login(self.tutor)
        self.assertEqual(self.client.get(f'/download/{self.lesson5.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/download/{self.lesson8.id}/').status_code, 404)
        response = self.client.get(f'/practice/{self.lesson8.id}/')
        self.assertRedirects(response, self.lesson8.get_absolute_url(), fetch_redirect_response=False)

    def test_tutor_sees_attempts_of_own_pupils_only(self):
        mine = PracticeAttempt.objects.create(user=self.kid, material=self.lesson5, score=1, max_score=2,
                                              answers_json={'mode': 'A', 'history': [], 'question_ids': ''})
        theirs = PracticeAttempt.objects.create(user=self.others_kid, material=self.lesson5, score=1, max_score=2,
                                                answers_json={'mode': 'A', 'history': [], 'question_ids': ''})
        self.client.force_login(self.tutor)
        self.assertEqual(self.client.get(f'/attempt/{mine.id}/').status_code, 200)
        self.assertEqual(self.client.get(f'/attempt/{theirs.id}/').status_code, 404)
        self.assertEqual(list(self.client.get('/cabinet/').context['students_attempts']), [mine])
        self.client.post(f'/attempt/{theirs.id}/manage/', {'action': 'delete'})
        self.assertTrue(PracticeAttempt.objects.filter(id=theirs.id).exists())

    def test_tutor_cannot_report_or_assign_to_others(self):
        self.client.force_login(self.tutor)
        response = self.client.post('/homework/assign/', {'student_id': self.others_request.id,
                                                          'material_id': self.lesson5.id, 'due_date': '2030-01-01'})
        self.assertEqual(response.status_code, 404)
        response = self.client.post('/cabinet/add-report/', {'student_id': self.owners_request.id})
        self.assertEqual(response.status_code, 404)
        self.client.post('/homework/assign/', {'student_id': self.kid_request.id, 'material_id': self.lesson8.id,
                                               'due_date': '2030-01-01'})
        self.assertFalse(Homework.objects.exists())   # 8 клас — не в підписці

    def test_pupil_of_tutor_practises_licensed_grade_for_free(self):
        self.client.force_login(self.kid)
        self.assertEqual(self.client.get(f'/practice/{self.lesson5.id}/').status_code, 200)
        response = self.client.get(f'/practice/{self.lesson8.id}/')
        self.assertRedirects(response, self.lesson8.get_absolute_url(), fetch_redirect_response=False)
        # Учень у 5 класі, підписка викладача покриває 5 клас — презентація теж відкрита
        self.assertEqual(self.client.get(f'/download/{self.lesson5.id}/').status_code, 200)

    def test_expired_license_turns_tutor_features_off(self):
        TeacherLicense.objects.filter(teacher=self.tutor).update(valid_until=timezone.localdate() - datetime.timedelta(days=1))
        self.client.force_login(self.tutor)
        context = self.client.get('/cabinet/').context
        self.assertTrue(context['tutor_offer'])
        self.assertNotIn('my_students', context)
        self.client.force_login(self.kid)
        response = self.client.get(f'/practice/{self.lesson5.id}/')
        self.assertRedirects(response, self.lesson5.get_absolute_url(), fetch_redirect_response=False)

    def test_teacher_role_alone_gives_no_full_game_access(self):
        from .games import game_materials
        nobody = self.make_user('wannabe@example.com', role='teacher')
        materials, label = game_materials(nobody)
        self.assertNotEqual(label, 'Повний доступ викладача')
        self.assertFalse(materials.filter(id=self.lesson5.id).exists())
        self.assertTrue(game_materials(self.tutor)[0].filter(id=self.lesson5.id).exists())

    def test_invite_link_makes_a_pupil(self):
        from .teachers import invite_for
        code = invite_for(self.tutor).code
        newbie = self.make_user('newbie@example.com')
        self.client.force_login(newbie)
        self.assertContains(self.client.get(f'/join/{code}/'), 'Запрошення від викладача')
        self.client.post(f'/join/{code}/', {'real_name': 'Нова Учениця', 'course': 'grade_5'})
        request = TutorStudentRequest.objects.get(user=newbie)
        self.assertEqual((request.teacher, request.status), (self.tutor, 'approved'))
        # Учень іншого викладача не перехоплюється
        other_code = invite_for(self.other_tutor).code
        self.client.post(f'/join/{other_code}/', {'real_name': 'X', 'course': 'grade_5'})
        self.assertEqual(TutorStudentRequest.objects.get(user=newbie).teacher, self.tutor)
        self.client.logout()
        self.assertRedirects(self.client.get(f'/join/{code}/'), f'/login/?next=/join/{code}/', fetch_redirect_response=False)


class TutorJourneyTests(BaseTestCase):
    """Наскрізний сценарій репетитора: запрошення → групове заняття → ДЗ → звіт → сторінка батьків."""

    def test_full_journey(self):
        from .teachers import invite_for
        tutor = self.make_user('journey-tutor@example.com', role='teacher')
        topic = make_school_topic('1.1. Натуральні', 5, 101)
        TeacherLicense.objects.create(teacher=tutor, grade=topic.chapter.grade,
                                      valid_until=timezone.localdate() + datetime.timedelta(days=60))
        lesson = StudyMaterial.objects.create(title='1.1', price=200, is_published=True, curriculum_topic=topic,
                                              html_content='<html><body>slides</body></html>')
        for level in (1, 2, 3):
            for skill in ('MODEL', 'SOLVE', 'ANALYZE'):
                for i in range(3):
                    q = Question.objects.create(text=f'{skill}{level}{i}', question_type='CHOICE',
                                                curriculum_topic=topic, difficulty=level, nush_skill=skill)
                    AnswerOption.objects.create(question=q, text='А) так', is_correct=True)
                    AnswerOption.objects.create(question=q, text='Б) ні', is_correct=False)
        code = invite_for(tutor).code

        pupils = []
        for name in ('Оля', 'Марко'):
            user = self.make_user(f'{name}@example.com')
            self.client.force_login(user)
            self.client.post(f'/join/{code}/', {'real_name': name, 'course': 'grade_5'})
            pupils.append(TutorStudentRequest.objects.get(user=user))

        # Заняття: показ презентації й групова практика
        self.client.force_login(tutor)
        self.assertEqual(self.client.get(f'/download/{lesson.id}/').status_code, 200)
        group = f'?g={pupils[0].id}&g={pupils[1].id}'

        def answer(query, correct=True):
            q = self.client.get(f'/practice/{lesson.id}/{query}').context['question']
            return self.client.post(f'/practice/{lesson.id}/check/{query}', json.dumps(
                {'question_id': q.id, 'answer': str(q.options.get(is_correct=correct).id)}),
                content_type='application/json').json()

        for _ in range(2):
            answer(f'{group}&student={pupils[0].id}')
            answer(f'{group}&student={pupils[1].id}', correct=False)
            answer(f'{group}&student={pupils[1].id}', correct=False)
        self.client.post(f'/practice/{lesson.id}/{group}', {'scope': 'group'})
        lesson_attempts = PracticeAttempt.objects.filter(conducted_by=tutor)
        self.assertEqual(lesson_attempts.count(), 2)

        # Звіт і ДЗ Марку
        marko_attempt = lesson_attempts.get(user=pupils[1].user)
        details = self.client.get(f'/attempt/{marko_attempt.id}/')
        self.assertContains(details, 'Додати в звіт заняття')
        self.client.post('/cabinet/add-report/', {
            'student_id': pupils[1].id, 'curriculum_topic': topic.id, 'nush_modeling': 4, 'nush_solving': 4,
            'nush_analysis': 4, 'homework_status': 'not_assigned', 'teacher_comment': 'Тренуємо вдома'})
        self.client.post('/homework/assign/', {'student_id': pupils[1].id, 'material_id': lesson.id,
                                               'due_date': (timezone.localdate() + datetime.timedelta(days=3)).isoformat()})

        # Марко вдома: урок не куплений, але практика доступна (ДЗ + підписка викладача)
        self.client.force_login(pupils[1].user)
        self.assertContains(self.client.get('/cabinet/'), 'Мої домашні завдання')
        for _ in range(7):
            answer('')
        self.client.post(f'/practice/{lesson.id}/')
        homework_attempt = Homework.objects.get().attempt
        self.assertEqual(homework_attempt.answers_json['status'], 'mastered')

        # Викладач бачить виконане ДЗ; батьки — звіт і зростання рівня
        self.client.force_login(tutor)
        self.assertEqual(self.client.get('/cabinet/').context['homeworks'][0].state, 'done')
        parents = self.client.get(f'/parents/{pupils[1].parent_token}/')
        self.assertContains(parents, 'Тренуємо вдома')
        self.assertContains(parents, '<strong>високий</strong>')
        self.assertContains(parents, '📈')


class SchoolContentTests(BaseTestCase):
    """Контент у content/school/* (презентації й банки) має проходити перевірку та імпортуватися."""

    def test_repository_content_passes_checks_and_imports(self):
        from pathlib import Path
        from django.core.management import call_command
        call_command('import_curriculum', stdout=open('/dev/null', 'w'))
        folders = sorted(p for p in (Path(settings.BASE_DIR) / 'content' / 'school').iterdir() if p.is_dir())
        self.assertTrue(folders)
        for folder in folders:
            with self.subTest(folder=folder.name):
                call_command('import_school_content', str(folder), stdout=open('/dev/null', 'w'))
        lesson = StudyMaterial.objects.get(curriculum_topic__name__startswith='1.1. ',
                                           curriculum_topic__chapter__grade__name='5 клас')
        self.assertTrue(lesson.is_published)   # новий урок з репозиторію одразу на вітрині
        self.assertGreaterEqual(Question.objects.filter(materials=lesson).count(), 45)

    def test_deploy_import_is_repeatable_and_does_not_stop_on_errors(self):
        """Деплой запускає імпорт усіх класів щоразу: повторний запуск нічого не дублює, правка уроку в адмінці
        лишається, змінений файл оновлює урок, а папка з помилкою не зупиняє решту."""
        import json
        import tempfile
        from pathlib import Path
        from django.core.management import call_command
        from django.core.management.base import CommandError
        call_command('import_curriculum', stdout=open('/dev/null', 'w'))
        quiet = {'stdout': open('/dev/null', 'w')}
        call_command('import_school_content', all_folders=True, keep_going=True, **quiet)
        questions = Question.objects.count()
        lesson = StudyMaterial.objects.get(curriculum_topic__name__startswith='1.1. ',
                                           curriculum_topic__chapter__grade__name='5 клас')
        self.assertEqual(len(lesson.html_source_hash), 64)
        StudyMaterial.objects.filter(pk=lesson.pk).update(html_content='правка в адмінці')

        with tempfile.TemporaryDirectory() as broken:
            (Path(broken) / 'meta.json').write_text(json.dumps({'course': 'Немає', 'grade': '5 клас'}))
            with self.assertRaises(CommandError):
                call_command('import_school_content', broken, **quiet)
            call_command('import_school_content', broken, all_folders=True, keep_going=True, **quiet)

        self.assertEqual(Question.objects.count(), questions)
        lesson.refresh_from_db()
        self.assertEqual(lesson.html_content, 'правка в адмінці')

        # Файл у репозиторії змінився (інший відбиток) — деплой записує нову версію
        # Знятий з публікації в адмінці урок деплой знову не публікує, навіть коли файл змінився
        StudyMaterial.objects.filter(pk=lesson.pk).update(html_source_hash='старий файл', is_published=False)
        call_command('import_school_content', all_folders=True, keep_going=True, **quiet)
        lesson.refresh_from_db()
        self.assertTrue(lesson.html_content.startswith('<!DOCTYPE html>'))
        self.assertFalse(lesson.is_published)

        # --draft: нові уроки — чернетками
        StudyMaterial.objects.filter(curriculum_topic__chapter__grade__name='7 клас').delete()
        call_command('import_school_content', 'content/school/geometry-7', draft=True, **quiet)
        self.assertFalse(StudyMaterial.objects.filter(curriculum_topic__chapter__grade__name='7 клас',
                                                      is_published=True).exists())

    def test_checker_rejects_broken_files(self):
        from .content_check import check_bank, check_presentation
        problems, _ = check_presentation('<!DOCTYPE html><html><head></head><body><img src="x.png"></body></html>')
        self.assertTrue(any('img' in p for p in problems))
        self.assertTrue(any('keydown' in p for p in problems))
        bad = [{'type': 'POINT', 'difficulty': 1, 'skill': 'MODEL', 'text': 'x', 'min': 0, 'max': 10, 'step': 1,
                'answer': 3, 'solution': 's'}]
        problems, warnings = check_bank(bad)
        self.assertTrue(any('hint' in p for p in problems))
        self.assertTrue(any('рекомендовано 45' in w for w in warnings))


class AdminContentPasteTests(BaseTestCase):
    """Вставляння контенту в адмінку: банк кодом у поле, перевірка презентації після збереження."""

    def setUp(self):
        self.admin = self.make_user('paste-admin@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(self.admin)
        self.topic = make_school_topic('1.2. Цифри', 5, 102)

    def test_bank_can_be_pasted_and_gets_quality_report(self):
        source = '''TOPIC_NAME = "1.2. Цифри"
COURSE = "Математика (5-6 класи)"
GRADE = "5 клас"
TASKS = [{"type": "SHORT", "difficulty": 1, "skill": "SOLVE", "text": "Скільки цифр?", "answer": "10",
          "solution": "Десять: від 0 до 9."}]
'''
        url = '/do-kvadratu-secret-control/materials/question/import-bank/'
        response = self.client.post(url, {'action': 'preview', 'bank_text': source})
        self.assertEqual(response.context['report'].to_add, [1])
        self.assertTrue(any('hint' in p for p in response.context['quality_problems']))
        self.client.post(url, {'action': 'import'})
        self.assertEqual(Question.objects.get().curriculum_topic, self.topic)

    def test_presentation_is_checked_after_save(self):
        material = StudyMaterial.objects.create(title='1.2', price=0, curriculum_topic=self.topic)
        url = f'/do-kvadratu-secret-control/materials/studymaterial/{material.id}/change/'
        form = self.client.get(url).context['adminform'].form
        data = {k: v for k, v in form.initial.items()
                if v is not None and not isinstance(v, (list, tuple)) and k not in ('image', 'file')}
        data.update({'title': '1.2', 'price': 0, 'curriculum_topic': self.topic.id,
                     'html_content': '<!DOCTYPE html><html><head></head><body><img src="a.png"></body></html>',
                     'description': 'x'})
        response = self.client.post(url, data, follow=True)
        text = ' '.join(str(m) for m in response.context['messages'])
        self.assertIn('Презентація: зображення <img> заборонені', text)


class TutorPlansTests(BaseTestCase):
    """Тарифи репетиторів: «Школа» на всі класи з лімітом учнів, НМТ-додаток, пробний період, оплата."""

    def setUp(self):
        from .models import TeacherPlan
        self.tutor = self.make_user('plans-tutor@example.com')
        self.topic5 = make_school_topic('1.1. Натуральні', 5, 101)
        self.topic8 = make_school_topic('1.1. Дроби', 8, 101, subject='Алгебра (7-9 класи)')
        self.nmt = make_nmt_topic('7. Квадратні рівняння')
        self.lesson5 = StudyMaterial.objects.create(title='5', price=50, is_published=True, curriculum_topic=self.topic5)
        self.lesson8 = StudyMaterial.objects.create(title='8', price=50, is_published=True, curriculum_topic=self.topic8)
        self.lesson_nmt = StudyMaterial.objects.create(title='7. КР', price=50, is_published=True, curriculum_topic=self.nmt)
        TeacherPlan.objects.all().delete()   # стартові тарифи з міграції
        self.start = TeacherPlan.objects.create(name='Старт', kind='school', max_students=1, price_month=300,
                                                price_year=2400, is_active=True)
        self.pro = TeacherPlan.objects.create(name='Профі', kind='school', max_students=15, price_month=600,
                                              is_active=True)
        self.nmt_plan = TeacherPlan.objects.create(name='НМТ', kind='nmt', price_month=200, is_active=True)
        TeacherPlan.objects.create(name='Прихований', kind='school', price_month=1, is_active=False)

    def pay(self, plan, period='month'):
        with mock.patch('materials.views.create_mono_invoice', return_value='https://pay.example/1'):
            response = self.client.post(f'/for-tutors/buy/{plan.id}/{period}/', {'agree': 'on'})
        order = Order.objects.filter(teacher_plan=plan).latest('id')
        from .views import apply_mono_status
        order.mono_invoice_id = f'inv-{order.id}'
        order.save()
        with mock.patch('materials.views.send_telegram_notification'):
            apply_mono_status(order.mono_invoice_id, 'success')
        return response, order

    def test_pay_plan_from_balance(self):
        self.tutor.balance = 500
        self.tutor.save()
        self.client.force_login(self.tutor)
        page = self.client.get('/for-tutors/')
        self.assertContains(page, 'На місяць — з балансу')
        self.assertNotContains(page, 'На навчальний рік — з балансу')   # 2400 ₴ > 500 ₴
        response = self.client.post(f'/for-tutors/buy/{self.start.id}/month/', {'agree': 'on', 'method': 'balance'})
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.balance, 200)
        license_ = TeacherLicense.objects.get(teacher=self.tutor, plan=self.start)
        self.assertFalse(license_.is_trial)
        self.assertTrue(Order.objects.filter(user=self.tutor, teacher_plan=self.start, status='paid').exists())

    def test_balance_too_small_charges_nothing(self):
        self.tutor.balance = 100
        self.tutor.save()
        self.client.force_login(self.tutor)
        self.client.post(f'/for-tutors/buy/{self.start.id}/month/', {'agree': 'on', 'method': 'balance'})
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.balance, 100)
        self.assertFalse(TeacherLicense.objects.filter(teacher=self.tutor).exists())
        self.assertFalse(Order.objects.filter(user=self.tutor).exists())

    def test_trial_is_offered_before_paid_plans_and_explained_when_used(self):
        self.client.force_login(self.tutor)
        html = self.client.get('/for-tutors/').content.decode()
        self.assertLess(html.index('Почати пробний період'), html.index('Тарифи «Школа 5–11»'))
        self.client.post('/for-tutors/trial/')
        self.assertContains(self.client.get('/for-tutors/'), 'пробний період на цьому акаунті вже використано')

    def test_owner_sees_why_there_is_nothing_to_buy(self):
        owner = self.make_user('owner-plans@example.com')
        owner.is_staff = True
        owner.save()
        self.client.force_login(owner)
        page = self.client.get('/for-tutors/')
        self.assertContains(page, 'Ви власник сайту')
        self.assertContains(page, 'налаштувати тарифи')
        self.assertNotContains(page, 'Почати пробний період')

    def test_school_plan_opens_every_school_grade_but_not_nmt(self):
        from .teachers import can_teach
        self.client.force_login(self.tutor)
        self.pay(self.start)
        self.assertTrue(can_teach(self.tutor, self.lesson5))
        self.assertTrue(can_teach(self.tutor, self.lesson8))
        self.assertFalse(can_teach(self.tutor, self.lesson_nmt))
        self.pay(self.nmt_plan)
        self.assertTrue(can_teach(self.tutor, self.lesson_nmt))

    def test_nmt_addon_needs_a_school_plan(self):
        self.client.force_login(self.tutor)
        with mock.patch('materials.views.create_mono_invoice', return_value='https://pay.example/1'):
            self.client.post(f'/for-tutors/buy/{self.nmt_plan.id}/month/', {'agree': 'on'})
        self.assertFalse(Order.objects.exists())

    def test_payment_grants_and_renewal_extends(self):
        from .teachers import add_months
        self.client.force_login(self.tutor)
        response, order = self.pay(self.start)
        self.assertRedirects(response, 'https://pay.example/1', fetch_redirect_response=False)
        self.assertEqual(order.total_amount, 300)
        license_ = TeacherLicense.objects.get(teacher=self.tutor)
        today = timezone.localdate()
        self.assertEqual((license_.scope, license_.max_students, license_.valid_until),
                         ('school', 1, add_months(today, 1)))
        self.pay(self.start)   # продовження — після кінця чинної
        latest = TeacherLicense.objects.filter(teacher=self.tutor).latest('valid_until')
        self.assertEqual(latest.valid_until, add_months(license_.valid_until + datetime.timedelta(days=1), 1))
        self.pay(self.pro)     # інший тариф — діє одразу
        from .teachers import student_limit
        self.assertEqual(student_limit(self.tutor), 15)
        self.assertContains(self.client.get(f'/payment/result/{order.id}/'), 'Підписку репетитора «Старт» оформлено')

    def test_school_year_period(self):
        from .teachers import period_end
        self.assertEqual(period_end(datetime.date(2026, 10, 18), 'year'), datetime.date(2027, 6, 30))
        self.assertEqual(period_end(datetime.date(2027, 5, 1), 'year'), datetime.date(2028, 6, 30))
        self.assertEqual(period_end(datetime.date(2027, 1, 31), 'month'), datetime.date(2027, 2, 28))

    def test_student_limit_blocks_new_pupils_and_nmt_addon_adds_none(self):
        from .teachers import invite_for, student_limit
        self.client.force_login(self.tutor)
        self.pay(self.start)
        self.pay(self.nmt_plan)
        self.assertEqual(student_limit(self.tutor), 1)
        code = invite_for(self.tutor).code
        for email in ('first@example.com', 'second@example.com'):
            self.client.force_login(self.make_user(email))
            self.client.post(f'/join/{code}/', {'real_name': email, 'course': 'grade_5'})
        self.assertEqual(TutorStudentRequest.objects.filter(teacher=self.tutor).count(), 1)
        self.client.force_login(self.tutor)
        self.assertContains(self.client.get('/cabinet/'), 'ліміт вичерпано')

    def test_trial_once_with_two_pupils_and_everything(self):
        from .teachers import can_teach, student_limit
        self.client.force_login(self.tutor)
        self.assertContains(self.client.get('/for-tutors/'), 'Пробний період')
        self.client.post('/for-tutors/trial/')
        self.assertTrue(can_teach(self.tutor, self.lesson8) and can_teach(self.tutor, self.lesson_nmt))
        self.assertEqual(student_limit(self.tutor), 2)
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.role, 'teacher')
        self.client.post('/for-tutors/trial/')
        self.assertEqual(TeacherLicense.objects.filter(teacher=self.tutor).count(), 2)
        self.assertNotContains(self.client.get('/for-tutors/'), 'Почати пробний період')

    def test_page_shows_only_active_plans(self):
        response = self.client.get('/for-tutors/')
        self.assertContains(response, 'Старт')
        self.assertNotContains(response, 'Прихований')
        self.assertContains(response, 'Увійти, щоб оформити')


class CurriculumTreeUpdateTests(BaseTestCase):
    """Доповнення дерева тем: нові теми й перенумерування наявних без втрати прив'язаних уроків."""

    def old_chapter(self, subject, grade_name, number, chapter_name, topics):
        subject_obj, _ = CurriculumSubject.objects.get_or_create(name=subject)
        grade, _ = CurriculumGrade.objects.get_or_create(subject=subject_obj, name=grade_name, defaults={'number': number})
        chapter = CurriculumChapter.objects.create(grade=grade, name=chapter_name, order=10)
        for order, name in enumerate(topics, start=1):
            CurriculumTopic.objects.create(chapter=chapter, name=name, order=order)
        return chapter

    def test_renumbers_existing_topics_keeps_lessons_and_adds_new_ones(self):
        from .curriculum import apply_tree_update, ensure_special_topics
        geo = self.old_chapter('Геометрія (7-9 класи)', '8 клас', 8, 'Розділ 1. Чотирикутники', [
            '1.1. Чотирикутник та його елементи. Сума кутів', '1.2. Паралелограм. Означення, властивості та ознаки',
            '1.3. Прямокутник, ромб, квадрат', '1.4. Трапеція. Середня лінія трапеції',
            '1.5. Вписані та описані чотирикутники'])
        alg = self.old_chapter('Алгебра (7-9 класи)', '9 клас', 9,
                               'Розділ 4. Основи комбінаторики, теорії ймовірностей та статистики', [
                                   '4.1. Комбінаторні правила суми та добутку', '4.2. Ймовірність випадкової події',
                                   '4.3. Початкові відомості про статистику'])
        ensure_special_topics(CurriculumGrade, CurriculumChapter, CurriculumTopic, StudyMaterial)
        trapezoid = CurriculumTopic.objects.get(chapter=geo, name='1.4. Трапеція. Середня лінія трапеції')
        lesson = StudyMaterial.objects.create(title=trapezoid.name, price=0, is_free=True, curriculum_topic=trapezoid)

        args = (CurriculumGrade, CurriculumChapter, CurriculumTopic, StudyMaterial)
        self.assertGreater(apply_tree_update(*args), 0)
        self.assertEqual(apply_tree_update(*args), 0)   # повторний запуск нічого не змінює

        names = list(CurriculumTopic.objects.filter(chapter=geo, kind='lesson').order_by('order').values_list('name', flat=True))
        self.assertEqual(names, ['1.1. Чотирикутник та його елементи. Сума кутів',
                                 '1.2. Паралелограм. Означення, властивості та ознаки', '1.3. Прямокутник, ромб, квадрат',
                                 '1.4. Середня лінія трикутника', '1.5. Трапеція. Середня лінія трапеції',
                                 '1.6. Центральні та вписані кути', '1.7. Вписані та описані чотирикутники'])
        lesson.refresh_from_db()
        self.assertEqual(lesson.curriculum_topic_id, trapezoid.id)   # той самий запис теми — урок не загубився
        self.assertEqual(lesson.title, '1.5. Трапеція. Середня лінія трапеції')

        alg.refresh_from_db()
        self.assertEqual(alg.name, 'Розділ 4. Елементи прикладної математики')
        summary = CurriculumTopic.objects.get(chapter=alg, kind='summary')
        self.assertEqual(summary.name, 'Узагальнення: Розділ 4. Елементи прикладної математики')
        self.assertEqual(StudyMaterial.objects.get(curriculum_topic=summary).title, summary.name)
        self.assertEqual(CurriculumTopic.objects.filter(chapter=alg, kind='lesson').count(), 6)

    def test_prompt_tree_matches_site_classifier(self):
        """Дерево тем у промпті — дослівно те, що створює import_curriculum (інакше банк не знайде тему)."""
        import re
        from pathlib import Path
        from materials.management.commands.import_curriculum import ALL_CURRICULUMS
        expected = [t['topic_name'] for course in ALL_CURRICULUMS for grade in course['grades']
                    for chapter in grade['chapters'] for t in chapter['topics']]
        tree = (Path(settings.BASE_DIR) / 'docs' / 'html_prompt.md').read_text().split('## 7. ДЕРЕВО')[1]
        self.assertEqual(re.findall(r'^  - (.+)$', tree, flags=re.M), expected)
        chapters = [c['chapter_name'] for course in ALL_CURRICULUMS for g in course['grades'] for c in g['chapters']]
        self.assertEqual(re.findall(r'^- \*\*(.+)\*\*$', tree, flags=re.M), chapters)

    def test_lesson_prompt_is_built_from_sources(self):
        import importlib.util
        from pathlib import Path
        path = Path(settings.BASE_DIR) / 'docs' / 'build_lesson_prompt.py'
        spec = importlib.util.spec_from_file_location('build_lesson_prompt', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual((path.parent / 'lesson_prompt.md').read_text(), module.OUT,
                         'запустіть python docs/build_lesson_prompt.py')


class SchoolPriceRuleTests(BaseTestCase):
    """Ціни шкільних уроків за правилами: перша тема розділу безкоштовна, решта — за ціною теми, ручна ціна лишається."""

    def setUp(self):
        from .models import SchoolPriceRule
        self.default_rule = SchoolPriceRule.objects.get(grade=None)   # створює міграція: 29 грн, перша тема безкоштовна
        self.first = make_school_topic('1.1. Перша', 5, 1)
        self.second = make_school_topic('1.2. Друга', 5, 2)
        summary = CurriculumTopic.objects.create(chapter=self.first.chapter, name='Узагальнення', order=99,
                                                 kind='summary')
        diagnostic = CurriculumTopic.objects.create(chapter=self.first.chapter, name='Діагностика', order=100,
                                                    kind='diagnostic')
        self.lessons = {name: StudyMaterial.objects.create(title=name, curriculum_topic=topic, is_free=True)
                        for name, topic in (('first', self.first), ('second', self.second), ('summary', summary),
                                            ('diagnostic', diagnostic))}
        self.nmt = StudyMaterial.objects.create(title='1. НМТ', price=19)

    def prices(self):
        return {name: StudyMaterial.objects.values_list('price', 'is_free').get(pk=m.pk)
                for name, m in self.lessons.items()}

    def test_default_rule(self):
        from .pricing import apply_price_rules
        self.assertEqual(apply_price_rules(), 2)
        self.assertEqual(self.prices(), {'first': (0, True), 'second': (29, False), 'summary': (29, False),
                                         'diagnostic': (0, True)})
        self.nmt.refresh_from_db()
        self.assertEqual((self.nmt.price, self.nmt.is_free), (19, False))
        self.assertEqual(apply_price_rules(), 0)

    def test_grade_rule_and_manual_price(self):
        from .models import SchoolPriceRule
        from .pricing import apply_price_rules
        SchoolPriceRule.objects.create(grade=self.first.chapter.grade, topic_price=39, first_topic_free=False)
        StudyMaterial.objects.filter(pk=self.lessons['second'].pk).update(price=5, is_free=False, price_is_manual=True)
        apply_price_rules()
        self.assertEqual(self.prices(), {'first': (39, False), 'second': (5, False), 'summary': (39, False),
                                         'diagnostic': (0, True)})

    def test_admin_rule_reprices_and_admin_edit_makes_price_manual(self):
        boss = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(boss)
        admin_url = '/do-kvadratu-secret-control/materials/'
        response = self.client.post(f'{admin_url}schoolpricerule/{self.default_rule.pk}/change/',
                                    {'grade': '', 'topic_price': '35', 'first_topic_free': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.prices()['second'], (35, False))

        second = self.lessons['second']
        changelist = f'{admin_url}studymaterial/'
        StudyMaterial.objects.filter(pk=second.pk).update(html_content='<html>')
        self.assertContains(self.client.get(changelist, {'ready': 'no_bank'}), 'second')
        # Зміна ціни прямо в списку робить її ручною: правила її більше не чіпають
        response = self.client.post(changelist, {
            'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1', 'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(second.pk), 'form-0-price': '50', 'form-0-is_published': 'on',
            '_save': 'Зберегти'})
        self.assertEqual(response.status_code, 302)
        second.refresh_from_db()
        self.assertEqual((second.price, second.price_is_manual, second.is_published), (50, True, True))
        self.client.post(changelist, {'action': 'price_by_rules', '_selected_action': [second.pk]})
        self.assertEqual(self.prices()['second'], (35, False))
        self.client.post(changelist, {'action': 'unpublish', '_selected_action': [second.pk]})
        second.refresh_from_db()
        self.assertFalse(second.is_published)


class ClassSubscriptionTests(BaseTestCase):
    """Підписка учня на клас: вітрина, оплата з балансу й карткою, доступ до всіх уроків класу на строк."""

    def setUp(self):
        from .models import ClassPlan
        self.algebra7 = StudyMaterial.objects.create(
            title='1.1. Алгебра', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic('1.1. Алгебра', 7, 1, subject='Алгебра (7-9 класи)'))
        self.geometry7 = StudyMaterial.objects.create(
            title='1.2. Геометрія', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic('1.2. Геометрія', 7, 2, subject='Геометрія (7-9 класи)'))
        self.algebra8 = StudyMaterial.objects.create(
            title='1.1. Вісім', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic('1.1. Вісім', 8, 1, subject='Алгебра (7-9 класи)'))
        ClassPlan.objects.update(is_active=False)   # міграція вмикає 5 клас — тут перевіряємо з нуля
        self.plan7 = ClassPlan.objects.get(number=7)   # ціни з міграцій: 119 / 790
        self.pupil = self.make_user('pupil7@example.com', balance=400)
        self.client.force_login(self.pupil)

    def download(self, material):
        return self.client.get(f'/download/{material.id}/').status_code

    def test_storefront_shows_only_classes_on_sale(self):
        self.assertNotContains(self.client.get('/subscribe/'), '7 клас</h3>')
        self.assertNotContains(self.client.get('/prices/'), 'Підписка на клас')
        self.assertEqual(self.client.post(f'/subscribe/buy/{self.plan7.id}/month/',
                                          {'agree': 'on', 'method': 'balance'}).status_code, 404)
        self.plan7.is_active = True
        self.plan7.save()
        page = self.client.get('/subscribe/')
        self.assertContains(page, '7 клас</h3>')
        self.assertContains(page, 'Алгебра і геометрія')
        self.assertContains(page, 'Уже готово уроків: 2 з 2')
        self.assertContains(page, 'На місяць — з балансу')        # 119 ₴ ≤ 400 ₴
        self.assertNotContains(page, 'На навчальний рік — з балансу')   # 790 ₴ > 400 ₴
        self.assertContains(self.client.get('/prices/'), '7 клас — від 119 ₴/міс')
        grade = self.algebra7.curriculum_topic.chapter.grade
        self.assertContains(self.client.get(f'/materials/?grade={grade.id}'), 'Увесь 7 клас')
        self.assertContains(self.client.get(f'/material/{self.algebra7.id}/', follow=True), 'Або весь 7 клас за підпискою')

    def test_pay_from_balance_opens_whole_class_until_end_of_period(self):
        from .teachers import period_end
        self.plan7.is_active = True
        self.plan7.save()
        self.assertEqual(self.download(self.algebra7), 404)
        with mock.patch('materials.views.send_telegram_notification'):
            response = self.client.post(f'/subscribe/buy/{self.plan7.id}/month/', {'agree': 'on', 'method': 'balance'})
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)
        self.pupil.refresh_from_db()
        self.assertEqual(self.pupil.balance, 281)
        order = Order.objects.get(class_plan=self.plan7)
        self.assertEqual((order.status, order.plan_period, int(order.total_amount)), ('paid', 'month', 119))
        subscription = self.pupil.class_subscriptions.get()
        self.assertEqual(subscription.valid_until, period_end(timezone.localdate(), 'month'))
        self.assertEqual(self.download(self.algebra7), 200)
        self.assertEqual(self.download(self.geometry7), 200)
        self.assertEqual(self.download(self.algebra8), 404)
        cabinet = self.client.get('/cabinet/').content.decode()
        self.assertIn('Підписка: 7 клас', cabinet)
        self.assertIn(self.geometry7.title, cabinet)
        # Продовження до кінця чинної — новий період після неї; закінчилась — доступ зник
        with mock.patch('materials.views.send_telegram_notification'):
            self.client.post(f'/subscribe/buy/{self.plan7.id}/month/', {'agree': 'on', 'method': 'balance'})
        latest = self.pupil.class_subscriptions.order_by('-valid_until').first()
        self.assertEqual(latest.valid_until,
                         period_end(subscription.valid_until + datetime.timedelta(days=1), 'month'))
        # Знятий з публікації урок підписка не відкриває (свій клас учня власника — відкривав би)
        StudyMaterial.objects.filter(pk=self.geometry7.pk).update(is_published=False)
        self.assertEqual(self.download(self.geometry7), 404)
        self.assertNotIn(self.geometry7.title, self.client.get('/cabinet/').content.decode())
        self.pupil.class_subscriptions.update(valid_until=timezone.localdate() - datetime.timedelta(days=1))
        self.assertEqual(self.download(self.algebra7), 404)

    def test_month_paid_is_credited_to_year_once(self):
        self.plan7.is_active = True
        self.plan7.save()
        User.objects.filter(pk=self.pupil.pk).update(balance=1000)
        buy = lambda period: self.client.post(f'/subscribe/buy/{self.plan7.id}/{period}/',
                                              {'agree': 'on', 'method': 'balance'})
        with mock.patch('materials.views.send_telegram_notification'):
            buy('month')
            self.assertContains(self.client.get('/subscribe/'), 'рік для вас — <strong>671 ₴</strong>')
            buy('year')
        self.pupil.refresh_from_db()
        self.assertEqual(self.pupil.balance, 1000 - 119 - 671)
        self.assertEqual(int(Order.objects.get(class_plan=self.plan7, plan_period='year').total_amount), 671)
        # Ту саму місячну оплату вдруге не зараховуємо
        self.assertNotContains(self.client.get('/subscribe/'), 'рік для вас')

    def test_card_payment_grants_after_monobank_confirms(self):
        from .views import apply_mono_status
        self.plan7.is_active = True
        self.plan7.save()
        self.assertRedirects(self.client.post(f'/subscribe/buy/{self.plan7.id}/year/', {'method': 'card'}),
                             '/subscribe/', fetch_redirect_response=False)   # без галочки згоди
        with mock.patch('materials.views.create_mono_invoice', return_value='https://pay.example/1'):
            response = self.client.post(f'/subscribe/buy/{self.plan7.id}/year/', {'agree': 'on', 'method': 'card'})
        self.assertRedirects(response, 'https://pay.example/1', fetch_redirect_response=False)
        order = Order.objects.get(class_plan=self.plan7)
        self.assertEqual((order.status, int(order.total_amount)), ('pending', 790))
        self.assertEqual(self.download(self.algebra7), 404)
        order.mono_invoice_id = 'inv-class'
        order.save()
        with mock.patch('materials.views.send_telegram_notification') as notify:
            apply_mono_status('inv-class', 'success')
        self.assertIn('Нова підписка на клас', notify.call_args[0][0])
        self.assertEqual(self.download(self.algebra7), 200)
        self.assertContains(self.client.get(f'/payment/result/{order.id}/'), 'Підписку на 7 клас оформлено')


    def test_cart_suggests_class_subscription_for_several_lessons(self):
        from .subscriptions import grant_class
        cart = Cart.objects.create(user=self.pupil)
        CartItem.objects.create(cart=cart, material=self.algebra7)
        CartItem.objects.create(cart=cart, material=self.algebra8)
        hint = 'а весь 7 клас'
        self.assertNotContains(self.client.get('/cart/'), hint)   # клас не продається
        self.plan7.is_active = True
        self.plan7.save()
        self.assertNotContains(self.client.get('/cart/'), hint)   # один урок 7 класу — підказка ще зайва
        CartItem.objects.create(cart=cart, material=self.geometry7)
        page = self.client.get('/cart/')
        self.assertContains(page, '2 уроки 7 класу = <strong>58 ₴</strong>')
        self.assertContains(page, 'а весь 7 клас — <strong>119 ₴/міс</strong>')
        self.assertContains(page, 'усі 2 уроки класу й практика')
        self.assertContains(page, '/subscribe/?class=7#class-7')
        grant_class(self.pupil, self.plan7, 'month')
        self.assertNotContains(self.client.get('/cart/'), hint)   # уже передплачено

class ClassSupportTests(BaseTestCase):
    """Підписка з супроводом: місяць підписки на клас, і на цей час учень — учень власника сайту."""

    def setUp(self):
        from .models import ClassPlan
        self.lesson = StudyMaterial.objects.create(
            title='1.1. Алгебра', price=29, is_published=True, html_content='<p>урок</p>',
            curriculum_topic=make_school_topic('1.1. Алгебра', 7, 1, subject='Алгебра (7-9 класи)'))
        self.plan = ClassPlan.objects.get(number=7)
        self.plan.is_active, self.plan.support_price_month = True, 449
        self.plan.save()
        self.pupil = self.make_user('support@example.com', balance=1000)
        self.client.force_login(self.pupil)

    def buy(self, **extra):
        data = {'agree': 'on', 'method': 'balance', 'real_name': 'Коваль Оля', **extra}
        return self.client.post(f'/subscribe/buy/{self.plan.id}/support/', data)

    def test_balance_purchase_makes_pupil_owners_student_for_a_month(self):
        page = self.client.get('/subscribe/')
        self.assertContains(page, 'З супроводом — 449 ₴')
        self.assertContains(page, 'Вільних місць: 15')
        with mock.patch('materials.views.send_telegram_notification') as notify:
            self.assertRedirects(self.buy(), '/cabinet/', fetch_redirect_response=False)
        self.assertIn('Новий учень на супроводі', notify.call_args[0][0])
        request = TutorStudentRequest.objects.get(user=self.pupil)
        self.assertEqual((request.status, request.teacher, request.course, request.real_name),
                         ('approved', None, 'grade_7', 'Коваль Оля'))
        subscription = self.pupil.class_subscriptions.get()
        self.assertTrue(subscription.with_support)
        self.assertEqual(request.support_until, subscription.valid_until)
        self.assertLess((subscription.valid_until - timezone.localdate()).days, 32)
        self.pupil.refresh_from_db()
        self.assertEqual(self.pupil.balance, 551)
        self.assertEqual(self.client.get(f'/download/{self.lesson.id}/').status_code, 200)
        self.assertContains(self.client.get('/cabinet/'), 'Супровід діє до')
        boss = self.make_user('boss@example.com', is_staff=True)
        self.client.force_login(boss)
        self.assertContains(self.client.get('/cabinet/'), '🤝 Супровід до')
        self.assertContains(self.client.get('/prices/'), 'З супроводом — 449 ₴/міс')

    def test_renewal_extends_support_not_after_year_subscription(self):
        from .subscriptions import grant_class
        year = grant_class(self.pupil, self.plan, 'year')
        self.buy()
        self.buy()
        request = TutorStudentRequest.objects.get(user=self.pupil)
        self.assertLess(request.support_until, year.valid_until)
        self.assertGreater((request.support_until - timezone.localdate()).days, 50)

    def test_support_ends_after_paid_month(self):
        from .subscriptions import end_expired_support
        self.buy()
        request = TutorStudentRequest.objects.get(user=self.pupil)
        request.support_until = timezone.localdate() - datetime.timedelta(days=1)
        request.save()
        self.pupil.class_subscriptions.update(valid_until=request.support_until)
        self.assertEqual(self.client.get(f'/download/{self.lesson.id}/').status_code, 404)
        end_expired_support()
        request.refresh_from_db()
        self.assertEqual(request.status, 'ended')
        self.assertContains(self.client.get('/cabinet/'), 'Супровід завершився')

    def test_permanent_student_keeps_status(self):
        TutorStudentRequest.objects.create(user=self.pupil, real_name='Учень', course='grade_7', status='approved')
        self.buy()
        self.assertIsNone(TutorStudentRequest.objects.get(user=self.pupil).support_until)

    def test_tutors_student_and_full_seats_are_refused(self):
        tutor = self.make_user('tutor@example.com')
        request = TutorStudentRequest.objects.create(user=self.pupil, real_name='Учень', course='grade_7',
                                                     status='approved', teacher=tutor)
        self.buy()
        self.assertFalse(self.pupil.class_subscriptions.exists())
        request.delete()
        type(self.plan).objects.filter(pk=self.plan.pk).update(support_seats=0)   # місця — в адмінці
        self.buy()
        self.assertContains(self.client.get('/subscribe/'), 'Вільних місць зараз немає')
        self.assertFalse(self.pupil.class_subscriptions.exists())
        self.buy(real_name='')
        self.assertFalse(self.pupil.class_subscriptions.exists())

    def test_card_payment_uses_name_from_order(self):
        from .views import apply_mono_status
        with mock.patch('materials.views.create_mono_invoice', return_value='https://pay.example/2'):
            self.buy(method='card')
        order = Order.objects.get(class_plan=self.plan)
        self.assertEqual((order.plan_period, order.student_name, int(order.total_amount)), ('support', 'Коваль Оля', 449))
        order.mono_invoice_id = 'inv-support'
        order.save()
        with mock.patch('materials.views.send_telegram_notification') as notify:
            apply_mono_status('inv-support', 'success')
        self.assertIn('Новий учень на супроводі', notify.call_args[0][0])
        self.assertEqual(TutorStudentRequest.objects.get(user=self.pupil).real_name, 'Коваль Оля')

    def test_migration_prices(self):
        from .models import ClassPlan
        prices = dict(ClassPlan.objects.values_list('number', 'price_year'))
        self.assertEqual((prices[5], prices[6], prices[8], prices[11]), (690, 690, 790, 890))
        self.assertEqual(ClassPlan.objects.get(number=5).support_price_month, 449)


class LaunchPricesMigrationTests(BaseTestCase):
    """Міграція 0051 (рішення власника 19.10.2026): 5 клас продається, тарифи викладача мають ціни."""

    def test_launch_state(self):
        from .models import ClassPlan, TeacherPlan
        plan5 = ClassPlan.objects.get(number=5)
        self.assertTrue(plan5.is_active)
        self.assertEqual(plan5.note, 'Ранній доступ: нові уроки щотижня')
        self.assertFalse(ClassPlan.objects.filter(is_active=True).exclude(number=5).exists())
        start = TeacherPlan.objects.get(name='Старт')
        self.assertEqual((start.price_month, start.price_year, start.is_active), (249, 1790, True))
        self.assertContains(self.client.get('/subscribe/'), '5 клас</h3>')
        self.assertContains(self.client.get('/for-tutors/'), '249')

    def test_publishes_repository_lessons_only(self):
        import importlib
        from django.apps import apps
        launch = importlib.import_module('materials.migrations.0051_launch_prices').launch
        topic = make_school_topic('1.1. Тема', 5, 1)
        imported = StudyMaterial.objects.create(title='з репозиторію', curriculum_topic=topic, html_source_hash='x' * 64)
        manual = StudyMaterial.objects.create(title='вручну', curriculum_topic=topic)
        launch(apps, None)
        imported.refresh_from_db()
        manual.refresh_from_db()
        self.assertTrue(imported.is_published)
        self.assertFalse(manual.is_published)


class SalesReportTests(BaseTestCase):
    def test_report_splits_sales_by_kind(self):
        from decimal import Decimal
        from .models import ClassPlan, OrderItem
        boss = self.make_user('boss@example.com', is_staff=True, is_superuser=True)
        buyer = self.make_user('buyer@example.com')
        now = timezone.now()
        school = StudyMaterial.objects.create(title='1.2. Урок', price=29, curriculum_topic=make_school_topic('1.2. Урок', 5, 2))
        nmt = StudyMaterial.objects.create(title='7. НМТ', price=19)
        mixed = Order.objects.create(user=buyer, total_amount=48, status='paid', paid_at=now, mono_invoice_id='inv1')
        OrderItem.objects.create(order=mixed, material=school, price=29)
        OrderItem.objects.create(order=mixed, material=nmt, price=19)
        plan5 = ClassPlan.objects.get(number=5)
        Order.objects.create(user=buyer, total_amount=99, status='paid', paid_at=now, class_plan=plan5,
                             plan_period='month', mono_invoice_id='balance_payment')
        Order.objects.create(user=buyer, total_amount=200, status='paid', paid_at=now, mono_invoice_id='inv2')
        from .reports import sales_report
        row = sales_report(1)['rows'][0]
        self.assertEqual((row['school'], row['nmt']), (Decimal(29), Decimal(19)))
        self.assertEqual((row['class_sum'], row['class_new'], row['class_renew']), (Decimal(99), 1, 0))
        self.assertEqual((row['topup'], row['card'], row['sold']), (Decimal(200), Decimal(248), Decimal(147)))
        self.client.force_login(boss)
        page = self.client.get('/do-kvadratu-secret-control/materials/order/report/')
        self.assertContains(page, 'Продажі за місяцями')
        self.assertContains(self.client.get('/do-kvadratu-secret-control/'), 'Звіт продажів')


class ScheduleTests(BaseTestCase):
    """Розклад занять: тиждень викладача, постійні заняття, перенесення й скасування, звіт після заняття,
    найближчі заняття учня й батьків, підписка в календарі, нагадування."""

    def setUp(self):
        from .models import Lesson, LessonSeries
        self.Lesson, self.LessonSeries = Lesson, LessonSeries
        self.teacher = self.make_user('owner@example.com', is_staff=True)
        self.pupil = self.make_user('pupil@example.com', telegram_id='777')
        self.student = TutorStudentRequest.objects.create(user=self.pupil, real_name='Олена Учениця',
                                                          course='grade_5', status='approved')
        self.topic = make_school_topic('1.2. Цифри', 5, 102)
        self.client.force_login(self.teacher)
        self.today = timezone.localdate()

    def at(self, day, hour=16, minute=0):
        return timezone.make_aware(datetime.datetime.combine(day, datetime.time(hour, minute)))

    def add(self, day, time='16:00', **extra):
        data = {'student_id': self.student.id, 'date': day.isoformat(), 'time': time, 'duration': '60', **extra}
        with mock.patch('materials.reminders.send_message', return_value=True) as send:
            response = self.client.post('/cabinet/schedule/add/', data)
        self.assertEqual(response.status_code, 302)
        return send

    def test_week_page_only_for_teachers(self):
        self.assertEqual(self.client.get('/cabinet/schedule/').status_code, 200)
        self.client.force_login(self.pupil)
        self.assertRedirects(self.client.get('/cabinet/schedule/'), '/cabinet/', fetch_redirect_response=False)
        self.assertEqual(self.client.post('/cabinet/schedule/add/', {'student_id': self.student.id}).status_code, 302)
        self.assertFalse(self.Lesson.objects.exists())

    def test_one_off_lesson_shows_in_week_and_notifies_pupil(self):
        day = self.today + datetime.timedelta(days=2)
        send = self.add(day, note='Zoom')
        lesson = self.Lesson.objects.get()
        self.assertEqual(lesson.start, self.at(day))
        self.assertEqual(lesson.teacher, self.teacher)
        self.assertIn('Нове заняття', send.call_args[0][1])
        page = self.client.get(f'/cabinet/schedule/?week={day:%Y-%m-%d}')
        self.assertContains(page, 'Олена Учениця')
        self.assertContains(page, 'Zoom')

    def test_cannot_schedule_other_teachers_student(self):
        tutor = self.make_user('tutor@example.com')
        from .models import TeacherLicense
        TeacherLicense.objects.create(teacher=tutor, scope='school', valid_until=self.today + datetime.timedelta(days=30))
        self.student.teacher = self.teacher
        self.student.save()
        self.client.force_login(tutor)
        response = self.client.post('/cabinet/schedule/add/', {'student_id': self.student.id,
                                                               'date': self.today.isoformat(), 'time': '10:00'})
        self.assertEqual(response.status_code, 404)
        self.client.force_login(self.teacher)
        self.add(self.today + datetime.timedelta(days=1))
        lesson = self.Lesson.objects.get()
        self.client.force_login(tutor)
        self.assertEqual(self.client.post(f'/cabinet/schedule/{lesson.id}/cancel/').status_code, 404)

    def test_weekly_series_fills_ahead_and_single_date_can_move(self):
        from .schedule import FILL_WEEKS
        start = self.today + datetime.timedelta(days=1)
        self.add(start, repeat='weekly')
        series = self.LessonSeries.objects.get()
        self.assertEqual(series.weekday, start.weekday())
        self.assertGreaterEqual(self.Lesson.objects.count(), FILL_WEEKS)
        first, second = self.Lesson.objects.order_by('start')[:2]
        # Тиждень за київським часом (навіть через перехід на зимовий час — та сама година)
        self.assertEqual(second.series_date - first.series_date, datetime.timedelta(weeks=1))
        self.assertEqual(timezone.localtime(second.start).time(), datetime.time(16, 0))

        new_day = second.series_date + datetime.timedelta(days=1)
        with mock.patch('materials.reminders.send_message', return_value=True):
            self.client.post(f'/cabinet/schedule/{second.id}/move/', {'date': new_day.isoformat(), 'time': '18:30',
                                                                     'duration': '90', 'scope': 'one'})
        second.refresh_from_db()
        self.assertEqual(second.start, self.at(new_day, 18, 30))
        self.assertEqual(second.duration, 90)
        self.assertIsNotNone(second.moved_from)
        # Повторне заповнення не відтворює перенесену дату
        count = self.Lesson.objects.count()
        from .schedule import fill_series
        fill_series()
        self.assertEqual(self.Lesson.objects.count(), count)
        self.assertFalse(self.Lesson.objects.filter(start=self.at(second.series_date)).exists())

    def test_move_following_splits_series(self):
        start = self.today + datetime.timedelta(days=1)
        self.add(start, repeat='weekly')
        lessons = list(self.Lesson.objects.order_by('start'))
        third = lessons[2]
        new_day = third.series_date + datetime.timedelta(days=2)
        with mock.patch('materials.reminders.send_message', return_value=True):
            self.client.post(f'/cabinet/schedule/{third.id}/move/', {'date': new_day.isoformat(), 'time': '10:00',
                                                                    'duration': '60', 'scope': 'following'})
        old, new = self.LessonSeries.objects.order_by('id')
        self.assertEqual(old.ends_on, third.series_date - datetime.timedelta(days=1))
        self.assertEqual(new.weekday, new_day.weekday())
        self.assertEqual(new.starts_on, new_day)
        self.assertEqual(self.Lesson.objects.filter(series=old).count(), 2)
        self.assertEqual(self.Lesson.objects.filter(series=new).order_by('start').first().start, self.at(new_day, 10))

    def test_cancel_one_and_end_series(self):
        start = self.today + datetime.timedelta(days=1)
        self.add(start, repeat='weekly')
        first, second, third = self.Lesson.objects.order_by('start')[:3]
        with mock.patch('materials.reminders.send_message', return_value=True) as send:
            self.client.post(f'/cabinet/schedule/{first.id}/cancel/', {'scope': 'one'})
        first.refresh_from_db()
        self.assertEqual(first.status, 'cancelled')
        self.assertIn('скасовано', send.call_args[0][1])
        self.client.post(f'/cabinet/schedule/{first.id}/restore/')
        first.refresh_from_db()
        self.assertEqual(first.status, 'planned')
        with mock.patch('materials.reminders.send_message', return_value=True):
            self.client.post(f'/cabinet/schedule/{third.id}/cancel/', {'scope': 'following'})
        self.assertEqual(list(self.Lesson.objects.order_by('start')), [first, second])
        from .schedule import fill_series
        fill_series()
        self.assertEqual(self.Lesson.objects.count(), 2)

    def test_report_after_lesson_goes_to_parents(self):
        lesson = self.Lesson.objects.create(teacher=self.teacher, student=self.student,
                                            start=timezone.now() - datetime.timedelta(hours=2))
        cabinet = self.client.get('/cabinet/')
        self.assertContains(cabinet, 'Чекають звіту')
        page = self.client.get(f'/cabinet/schedule/{lesson.id}/report/')
        self.assertContains(page, 'Олена Учениця')
        self.client.post(f'/cabinet/schedule/{lesson.id}/report/', {
            'curriculum_topic': self.topic.id, 'nush_modeling': 9, 'nush_solving': 10, 'nush_analysis': 8,
            'homework_status': 'completed', 'readiness': 'ready', 'teacher_comment': 'Молодець'})
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'done')
        self.assertEqual(lesson.report.student, self.student)
        self.assertEqual(lesson.report.date, timezone.localtime(lesson.start).date())
        self.assertEqual(lesson.curriculum_topic, self.topic)
        self.assertNotContains(self.client.get('/cabinet/'), 'Чекають звіту')
        self.assertContains(self.client.get(f'/parents/{self.student.parent_token}/'), 'Молодець')
        # Звіт не дублюється
        self.client.post(f'/cabinet/schedule/{lesson.id}/report/', {'curriculum_topic': self.topic.id})
        self.assertEqual(StudentReport.objects.count(), 1)

    def test_pupil_and_parents_see_upcoming_lessons(self):
        self.Lesson.objects.create(teacher=self.teacher, student=self.student,
                                   start=self.at(self.today + datetime.timedelta(days=1), 15))
        self.Lesson.objects.create(teacher=self.teacher, student=self.student, status='cancelled',
                                   start=self.at(self.today + datetime.timedelta(days=2), 15))
        self.client.force_login(self.pupil)
        cabinet = self.client.get('/cabinet/')
        self.assertContains(cabinet, 'Мої заняття')
        self.assertContains(cabinet, 'Завтра о 15:00')
        self.assertContains(cabinet, 'calendar.google.com')
        parents = self.client.get(f'/parents/{self.student.parent_token}/')
        self.assertContains(parents, 'Найближчі заняття')
        self.assertContains(parents, f'/parents/{self.student.parent_token}/calendar.ics')

    def test_calendar_feeds_are_signed(self):
        from .schedule import feed_token
        lesson = self.Lesson.objects.create(teacher=self.teacher, student=self.student, note='Zoom, дроби',
                                            start=self.at(self.today + datetime.timedelta(days=1), 15))
        feed = self.client.get(f'/calendar/{feed_token("t", self.teacher.id)}.ics')
        self.assertEqual(feed['Content-Type'], 'text/calendar; charset=utf-8')
        body = feed.content.decode()
        self.assertIn(f'UID:lesson-{lesson.id}@', body)
        self.assertIn('SUMMARY:Заняття: Олена Учениця', body)
        self.assertIn('DESCRIPTION:Zoom\\, дроби', body)
        self.assertTrue(all(len(line.encode()) <= 75 for line in body.split('\r\n')))
        pupil_feed = self.client.get(f'/calendar/{feed_token("s", self.pupil.id)}.ics').content.decode()
        self.assertIn(f'UID:lesson-{lesson.id}@', pupil_feed)
        parent_feed = self.client.get(f'/parents/{self.student.parent_token}/calendar.ics').content.decode()
        self.assertIn(f'UID:lesson-{lesson.id}@', parent_feed)
        forged = feed_token('t', self.teacher.id).replace(f't{self.teacher.id}-', f't{self.pupil.id}-')
        self.assertEqual(self.client.get(f'/calendar/{forged}.ics').status_code, 404)
        self.assertEqual(self.client.get('/calendar/x1-abc.ics').status_code, 404)

    def test_ics_fold_keeps_utf8(self):
        from .schedule import ics_fold
        line = 'SUMMARY:' + 'Заняття з математики ' * 10
        folded = ics_fold(line)
        self.assertEqual(folded.replace('\r\n ', ''), line)
        self.assertTrue(all(len(part.encode()) <= 75 for part in folded.split('\r\n')))

    def test_reminders_for_tomorrow_and_soon(self):
        from .reminders import due_reminders, lessons_soon, send_due_reminders
        self.teacher.telegram_id = '888'
        self.teacher.save()
        tomorrow = self.at(self.today + datetime.timedelta(days=1), 15)
        lesson = self.Lesson.objects.create(teacher=self.teacher, student=self.student, start=tomorrow)
        self.Lesson.objects.create(teacher=self.teacher, student=self.student, status='cancelled',
                                   start=tomorrow + datetime.timedelta(hours=2))
        keys = sorted(key for _, key, _, _ in due_reminders())
        self.assertEqual(keys, [f'day:{self.teacher.id}:{tomorrow:%y%m%d}',
                                f'lesson:{lesson.id}:{timezone.localtime(tomorrow):%y%m%d%H%M}'])
        texts = {key: text for _, key, text, _ in due_reminders()}
        self.assertIn('Олена Учениця', texts[keys[0]])
        self.assertIn('Завтра о 15:00', texts[keys[1]])
        soon = lessons_soon(now=tomorrow - datetime.timedelta(hours=1))
        self.assertEqual([key for _, key, _, _ in soon], [f'soon:{lesson.id}:{timezone.localtime(tomorrow):%y%m%d%H%M}'])
        self.assertEqual(lessons_soon(now=tomorrow - datetime.timedelta(hours=3)), [])
        with mock.patch('materials.reminders.send_message', return_value=True):
            self.assertEqual(send_due_reminders(soon), 1)
            self.assertEqual(send_due_reminders(soon), 0)

    def test_overlap_warning(self):
        day = self.today + datetime.timedelta(days=3)
        self.add(day, time='16:00')
        with mock.patch('materials.reminders.send_message', return_value=True):
            response = self.client.post('/cabinet/schedule/add/', {
                'student_id': self.student.id, 'date': day.isoformat(), 'time': '16:30', 'duration': '60'}, follow=True)
        self.assertContains(response, 'У цей час уже є заняття')
        self.assertEqual(self.Lesson.objects.count(), 2)

    def test_fifty_minute_lesson(self):
        self.assertContains(self.client.get('/cabinet/schedule/'), '<option value="50">50 хв</option>')
        self.add(self.today + datetime.timedelta(days=1), duration='50')
        self.assertEqual(self.Lesson.objects.get().duration, 50)

    def test_bad_input_does_not_create(self):
        response = self.client.post('/cabinet/schedule/add/', {'student_id': self.student.id, 'date': 'вчора',
                                                               'time': '16:00'}, follow=True)
        self.assertContains(response, 'Вкажіть дату й час')
        response = self.client.post('/cabinet/schedule/add/', {'student_id': self.student.id,
                                                               'date': self.today.isoformat(), 'time': '16:00',
                                                               'duration': '999'}, follow=True)
        self.assertContains(response, 'Тривалість')
        self.assertFalse(self.Lesson.objects.exists())


class ScheduleReportConsistencyTests(BaseTestCase):
    """Звіт з практики на уроці (чи з кабінету) і звіт із розкладу — один звіт на заняття, без дублів."""

    def setUp(self):
        from .models import Lesson
        self.Lesson = Lesson
        self.teacher = self.make_user('owner2@example.com', is_staff=True)
        self.pupil = self.make_user('pupil2@example.com')
        self.student = TutorStudentRequest.objects.create(user=self.pupil, real_name='Петро Учень',
                                                          course='grade_5', status='approved')
        self.topic = make_school_topic('1.3. Числа', 5, 103)
        self.material = StudyMaterial.objects.create(title='1.3. Числа', price=29, curriculum_topic=self.topic)
        self.client.force_login(self.teacher)
        self.lesson = Lesson.objects.create(teacher=self.teacher, student=self.student,
                                            start=timezone.now() - datetime.timedelta(minutes=50))

    def report_data(self, **extra):
        return {'student_id': self.student.id, 'curriculum_topic': self.topic.id, 'nush_modeling': 7,
                'nush_solving': 8, 'nush_analysis': 9, 'homework_status': 'partial', **extra}

    def test_report_from_practice_closes_todays_lesson(self):
        self.client.post('/cabinet/add-report/', self.report_data())
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.status, 'done')
        self.assertEqual(self.lesson.report, StudentReport.objects.get())
        self.assertEqual(self.lesson.curriculum_topic, self.topic)
        self.assertNotContains(self.client.get('/cabinet/'), 'Чекають звіту')
        # Повторний звіт з розкладу не створюється
        self.assertEqual(self.client.get(f'/cabinet/schedule/{self.lesson.id}/report/').status_code, 302)
        self.assertEqual(StudentReport.objects.count(), 1)

    def test_existing_report_of_the_day_is_linked_not_duplicated(self):
        report = StudentReport.objects.create(student=self.student, curriculum_topic=self.topic,
                                              date=timezone.localtime(self.lesson.start).date())
        response = self.client.get(f'/cabinet/schedule/{self.lesson.id}/report/', follow=True)
        self.assertContains(response, 'уже є')
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.report, report)
        self.assertEqual(StudentReport.objects.count(), 1)

    def test_schedule_report_prefilled_from_lesson_practice(self):
        PracticeAttempt.objects.create(user=self.pupil, material=self.material, score=5, conducted_by=self.teacher,
                                       nush_modeling=6, nush_solving=11, nush_analysis=4)
        page = self.client.get(f'/cabinet/schedule/{self.lesson.id}/report/')
        self.assertContains(page, 'підставлено з практики')
        self.assertContains(page, 'name="nush_solving" min="1" max="12" value="11"')
        self.assertContains(page, f'<option value="{self.topic.id}" selected>')

    def test_nmt_score_marks_lesson_held(self):
        self.student.course = 'nmt'
        self.student.save()
        self.client.post('/cabinet/add-nmt-score/', {'student_id': self.student.id, 'material_id': self.material.id,
                                                     'score': 10, 'max_score': 18})
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.status, 'done')
        self.assertNotContains(self.client.get('/cabinet/'), 'Чекають звіту')

    def test_report_after_midnight_closes_late_evening_lesson(self):
        late = timezone.make_aware(datetime.datetime(2026, 10, 21, 23, 14))
        self.lesson.start = late
        self.lesson.save()
        PracticeAttempt.objects.create(user=self.pupil, material=self.material, score=5, conducted_by=self.teacher,
                                       nush_modeling=6, nush_solving=11, nush_analysis=4)
        PracticeAttempt.objects.filter(user=self.pupil).update(created_at=late + datetime.timedelta(minutes=55))
        after_midnight = timezone.make_aware(datetime.datetime(2026, 10, 22, 0, 20))
        date_field = StudentReport._meta.get_field('date')
        with mock.patch('django.utils.timezone.now', return_value=after_midnight), \
                mock.patch.object(date_field, 'default', lambda: after_midnight):
            page = self.client.get(f'/cabinet/schedule/{self.lesson.id}/report/')
            self.assertContains(page, 'name="nush_solving" min="1" max="12" value="11"')
            self.client.post('/cabinet/add-report/', self.report_data())
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.status, 'done')
        self.assertEqual(self.lesson.report.date, datetime.date(2026, 10, 22))

    def test_report_without_lesson_still_works(self):
        self.lesson.delete()
        self.client.post('/cabinet/add-report/', self.report_data())
        self.assertEqual(StudentReport.objects.count(), 1)


class StudyPlanTests(BaseTestCase):
    """Навчальний план учня: склад з дерева, зміни під учня, прогрес зі звітів, розклад, учень і батьки."""

    def setUp(self):
        from .models import Lesson, StudyPlanItem
        self.Lesson, self.Item = Lesson, StudyPlanItem
        self.teacher = self.make_user('plan-owner@example.com', is_staff=True)
        self.pupil = self.make_user('plan-pupil@example.com')
        self.student = TutorStudentRequest.objects.create(user=self.pupil, real_name='Ірина План',
                                                          course='grade_5', status='approved')
        self.t1 = make_school_topic('1.1. Натуральні числа', 5, 101)
        self.t2 = make_school_topic('1.2. Цифри', 5, 102)
        self.t3 = make_school_topic('1.3. Порівняння', 5, 103)
        self.other = make_school_topic('1.1. Дроби шостого класу', 6, 101, subject='Математика (5-6 класи)')
        self.grade5 = self.t1.chapter.grade
        self.client.force_login(self.teacher)

    def build(self):
        self.client.post(f'/cabinet/students/{self.student.id}/plan/build/', {'grade': [self.grade5.id]})
        return list(self.Item.objects.filter(student=self.student).order_by('position'))

    def names(self):
        return [item.name for item in self.Item.objects.filter(student=self.student).order_by('position')]

    def test_build_from_tree_marks_reported_topics_done(self):
        StudentReport.objects.create(student=self.student, curriculum_topic=self.t1)
        page = self.client.get(f'/cabinet/students/{self.student.id}/plan/')
        self.assertContains(page, 'Скласти план з дерева')
        self.assertContains(page, f'value="{self.grade5.id}" checked')   # клас учня — одразу обраний
        items = self.build()
        self.assertEqual([item.topic for item in items], [self.t1, self.t2, self.t3])
        self.assertEqual([item.status for item in items], ['done', 'todo', 'todo'])
        # Повторне додавання того самого класу не дублює теми
        self.build()
        self.assertEqual(self.Item.objects.count(), 3)

    def test_customize_order_skip_add_other_grade_and_own_topic(self):
        items = self.build()
        url = lambda item: f'/cabinet/plan-item/{item.id}/'
        self.client.post(url(items[2]), {'action': 'up'})
        self.assertEqual(self.names(), ['1.1. Натуральні числа', '1.3. Порівняння', '1.2. Цифри'])
        self.client.post(url(items[0]), {'action': 'move', 'position': '3'})
        self.assertEqual(self.names(), ['1.3. Порівняння', '1.2. Цифри', '1.1. Натуральні числа'])
        self.client.post(url(items[1]), {'action': 'status', 'status': 'skipped'})
        self.client.post(f'/cabinet/students/{self.student.id}/plan/add/', {'topic_id': self.other.id, 'where': 'next'})
        self.assertEqual(self.names()[0], '1.1. Дроби шостого класу')
        self.client.post(f'/cabinet/students/{self.student.id}/plan/add/', {'title': 'Підготовка до контрольної',
                                                                           'where': 'end'})
        self.assertEqual(self.names()[-1], 'Підготовка до контрольної')
        self.client.post(url(items[0]), {'action': 'note', 'note': 'плутає розряди'})
        self.client.post(url(items[2]), {'action': 'delete'})
        self.assertNotIn('1.3. Порівняння', self.names())
        self.assertEqual(sorted(self.Item.objects.values_list('position', flat=True)), [1, 2, 3, 4])

    def test_report_marks_topic_done_and_next_topic_in_schedule_and_report(self):
        self.build()
        self.client.post('/cabinet/add-report/', {'student_id': self.student.id, 'curriculum_topic': self.t1.id,
                                                  'nush_modeling': 8, 'nush_solving': 8, 'nush_analysis': 8,
                                                  'homework_status': 'completed'})
        self.assertEqual(self.Item.objects.get(topic=self.t1).status, 'done')
        tomorrow = timezone.localdate() + datetime.timedelta(days=1)
        start = timezone.make_aware(datetime.datetime.combine(tomorrow, datetime.time(15)))
        self.Lesson.objects.create(teacher=self.teacher, student=self.student, start=start)
        self.Lesson.objects.create(teacher=self.teacher, student=self.student, start=start + datetime.timedelta(hours=3))
        week = self.client.get(f'/cabinet/schedule/?week={tomorrow:%Y-%m-%d}')
        self.assertContains(week, '🧭 1.2. Цифри')
        self.assertContains(week, '🧭 1.3. Порівняння')
        past = self.Lesson.objects.create(teacher=self.teacher, student=self.student,   # учора — звіту за той день немає
                                          start=timezone.now() - datetime.timedelta(days=1))
        report = self.client.get(f'/cabinet/schedule/{past.id}/report/')
        self.assertContains(report, f'<option value="{self.t2.id}" selected>')

    def test_pupil_and_parents_see_plan_without_teacher_notes(self):
        items = self.build()
        self.client.post(f'/cabinet/plan-item/{items[1].id}/', {'action': 'note', 'note': 'СЕКРЕТНА ПРИМІТКА'})
        self.client.post(f'/cabinet/plan-item/{items[0].id}/', {'action': 'status', 'status': 'done'})
        self.assertContains(self.client.get(f'/cabinet/students/{self.student.id}/plan/'), 'СЕКРЕТНА ПРИМІТКА')
        parents = self.client.get(f'/parents/{self.student.parent_token}/')
        self.assertContains(parents, 'Навчальний план · пройдено 1 з 3 тем')
        self.assertNotContains(parents, 'СЕКРЕТНА ПРИМІТКА')
        self.client.force_login(self.pupil)
        cabinet = self.client.get('/cabinet/')
        self.assertContains(cabinet, 'Мій навчальний план')
        self.assertContains(cabinet, '1.2. Цифри')
        self.assertNotContains(cabinet, 'СЕКРЕТНА ПРИМІТКА')

    def test_only_own_students_and_licensed_topics(self):
        from .models import TeacherLicense
        items = self.build()
        tutor = self.make_user('plan-tutor@example.com')
        TeacherLicense.objects.create(teacher=tutor, scope='grade', grade=self.grade5,
                                      valid_until=timezone.localdate() + datetime.timedelta(days=30))
        self.client.force_login(tutor)
        self.assertEqual(self.client.get(f'/cabinet/students/{self.student.id}/plan/').status_code, 404)
        self.assertEqual(self.client.post(f'/cabinet/plan-item/{items[0].id}/', {'action': 'delete'}).status_code, 404)
        self.assertEqual(self.Item.objects.count(), 3)
        own = TutorStudentRequest.objects.create(user=self.make_user('own@example.com'), real_name='Свій',
                                                 course='grade_5', status='approved', teacher=tutor)
        self.client.post(f'/cabinet/students/{own.id}/plan/add/', {'topic_id': self.other.id})   # 6 клас — не в підписці
        self.assertFalse(self.Item.objects.filter(student=own).exists())
        self.client.post(f'/cabinet/students/{own.id}/plan/add/', {'topic_id': self.t2.id})
        self.assertEqual([i.topic for i in self.Item.objects.filter(student=own)], [self.t2])

    def test_nmt_student_plan_from_nmt_tree(self):
        nmt = make_nmt_topic('Числові множини')
        self.student.course = 'nmt'
        self.student.save()
        page = self.client.get(f'/cabinet/students/{self.student.id}/plan/')
        self.assertContains(page, f'value="{nmt.chapter.grade_id}" checked')

    def report(self, topic):
        self.client.post('/cabinet/add-report/', {'student_id': self.student.id, 'curriculum_topic': topic.id,
                                                  'nush_modeling': 8, 'nush_solving': 8, 'nush_analysis': 8,
                                                  'homework_status': 'completed'})

    def slots(self):
        from .plans import next_slots
        return [name for name, _ in next_slots([self.student.id]).get(self.student.id, [])]

    def test_topic_for_several_lessons(self):
        items = self.build()
        self.client.post(f'/cabinet/plan-item/{items[0].id}/', {'action': 'lessons', 'lessons': '2'})
        self.assertEqual(self.slots(), ['1.1. Натуральні числа', '1.1. Натуральні числа', '1.2. Цифри', '1.3. Порівняння'])
        self.report(self.t1)
        item = self.Item.objects.get(id=items[0].id)
        self.assertEqual((item.status, item.held), ('todo', 1))
        self.assertContains(self.client.get(f'/cabinet/students/{self.student.id}/plan/'), '2 уроки · проведено 1')
        self.report(self.t1)
        self.assertEqual(self.Item.objects.get(id=items[0].id).status, 'done')
        self.assertEqual(self.slots(), ['1.2. Цифри', '1.3. Порівняння'])

    def test_two_topics_in_one_lesson(self):
        items = self.build()
        self.client.post(f'/cabinet/plan-item/{items[2].id}/', {'action': 'join', 'joined': '1'})
        self.assertEqual(self.slots(), ['1.1. Натуральні числа', '1.2. Цифри + 1.3. Порівняння'])
        self.report(self.t3)   # звіт з будь-якою з об'єднаних тем закриває обидві
        self.assertEqual(list(self.Item.objects.filter(id__in=[items[1].id, items[2].id])
                              .values_list('status', flat=True)), ['done', 'done'])
        self.assertEqual(self.Item.objects.get(id=items[0].id).status, 'todo')
        # Переміщення розриває об'єднання
        self.client.post(f'/cabinet/plan-item/{items[2].id}/', {'action': 'join', 'joined': '1'})
        self.client.post(f'/cabinet/plan-item/{items[1].id}/', {'action': 'up'})
        self.assertFalse(self.Item.objects.get(id=items[2].id).joined)
        # Першу тему плану нема з чим об'єднати
        first = self.Item.objects.filter(student=self.student).order_by('position').first()
        self.client.post(f'/cabinet/plan-item/{first.id}/', {'action': 'join', 'joined': '1'})
        self.assertFalse(self.Item.objects.get(id=first.id).joined)

    def test_repeat_and_skip(self):
        items = self.build()
        self.report(self.t1)
        self.client.post(f'/cabinet/plan-item/{items[0].id}/', {'action': 'repeat'})
        self.assertEqual(self.names()[-1], '1.1. Натуральні числа')
        self.client.post(f'/cabinet/plan-item/{items[1].id}/', {'action': 'status', 'status': 'skipped'})
        self.assertEqual(self.slots(), ['1.3. Порівняння', '1.1. Натуральні числа'])
        self.report(self.t1)   # повторення закривається наступним звітом з темою
        self.assertEqual(self.slots(), ['1.3. Порівняння'])
        # Додати тему з дерева, що вже є в плані, — теж повторення
        self.client.post(f'/cabinet/students/{self.student.id}/plan/add/', {'topic_id': self.t3.id, 'where': 'end'})
        self.assertEqual(self.names().count('1.3. Порівняння'), 2)


class SheetSyncTests(BaseTestCase):
    """Google-таблиця розкладу: вивантаження для скрипта таблиці, імпорт майбутніх уроків з CSV."""

    HEADER = ('Lesson type,Student,Start date,Weekday,Subject,Start time,End Date,End time,Price (Mindful of taxes),'
              'Зняття з ФОП,Price (Mindful of summer costs & taxes),Taxes,,summer costs,Price,Month,Year,Status1,Тема,'
              'Причина скасування уроку,Інформація про перенесення уроку,Lesson index\n')

    def setUp(self):
        from .models import Lesson, LessonSeries
        self.Lesson, self.LessonSeries = Lesson, LessonSeries
        self.teacher = self.make_user('sheet-owner@example.com', is_staff=True)
        self.vlad = TutorStudentRequest.objects.create(user=self.make_user('vlad@example.com'),
                                                       real_name='Влад Пастушок', course='grade_5', status='approved')
        self.oleksii = TutorStudentRequest.objects.create(user=self.make_user('oleksii@example.com'),
                                                          real_name='Олексій Шевцов', course='grade_8', status='approved')
        self.client.force_login(self.teacher)
        self.today = timezone.localdate()
        # Наступний понеділок і ще 4 понеділки; на третій — «канікули» (рядка немає)
        monday = self.today + datetime.timedelta(days=7 - self.today.weekday())
        self.mondays = [monday + datetime.timedelta(weeks=n) for n in range(5)]

    def csv(self):
        lines = [self.HEADER]
        for n, day in enumerate(self.mondays):
            if n != 2:
                lines.append(f'Індивідуальний,Влад Пастушок,{day:%d.%m.%Y},1,Влад (5 клас),16:00:00,{day:%d.%m.%Y},'
                             f'16:50:00,376,+,320,24,+,56,400,{day.month},{day.year},Ще рано,,,,1\n')
        once = self.mondays[1] + datetime.timedelta(days=3)
        lines.append(f'Група (8 клас),Олексій,{once:%d.%m.%Y},4,Олексій,17:10:00,{once:%d.%m.%Y},18:00:00,'
                     f'235,+,200,15,+,35,250,{once.month},{once.year},Ще рано,,,,1\n')
        past = self.today - datetime.timedelta(days=3)
        lines.append(f'Індивідуальний,Влад Пастушок,{past:%d.%m.%Y},1,Влад,16:00:00,{past:%d.%m.%Y},16:50:00,'
                     f'376,+,320,24,+,56,400,{past.month},{past.year},Оплачено,Цифри,,,1\n')
        lines.append(f'Індивідуальний,Хтось Невідомий,{self.mondays[0]:%d.%m.%Y},1,Х,12:00:00,'
                     f'{self.mondays[0]:%d.%m.%Y},13:00:00,1,,,,,,1,1,2026,Ще рано,,,,1\n')
        return ''.join(lines)

    def upload(self, **extra):
        from django.core.files.uploadedfile import SimpleUploadedFile
        return self.client.post('/cabinet/schedule/import/', {
            'file': SimpleUploadedFile('rozklad.csv', self.csv().encode(), content_type='text/csv'), **extra})

    def test_preview_matches_names_and_shows_plan(self):
        page = self.upload()
        self.assertContains(page, 'Майбутніх уроків у таблиці: <b>6</b>')
        self.assertContains(page, '🔁 щопонеділка о 16:00, 50 хв — уроків: 4')
        self.assertContains(page, f'value="{self.oleksii.id}" selected')   # «Олексій» → Олексій Шевцов
        self.assertContains(page, 'class="missing"')                        # «Хтось Невідомий» — без пари
        self.assertFalse(self.Lesson.objects.exists())

    def test_import_creates_series_with_gaps_and_single_lessons_once(self):
        page = self.upload()
        csv_text = page.context['csv']
        data = {'csv': csv_text, 'confirm': '1'}
        for item in page.context['names']:
            data[f"map_{item['index']}"] = item['student'].id if item['student'] else ''
        self.client.post('/cabinet/schedule/import/', data)
        series = self.LessonSeries.objects.get(student=self.vlad)
        self.assertEqual((series.weekday, series.time, series.duration), (0, datetime.time(16), 50))
        self.assertEqual((series.starts_on, series.ends_on), (self.mondays[0], self.mondays[-1]))
        lessons = list(self.Lesson.objects.filter(series=series).order_by('start'))
        self.assertEqual([l.status for l in lessons], ['planned', 'planned', 'cancelled', 'planned', 'planned'])
        self.assertEqual(lessons[2].cancel_reason, 'Немає в таблиці (канікули?)')
        single = self.Lesson.objects.get(student=self.oleksii)
        self.assertEqual(timezone.localtime(single.start).time(), datetime.time(17, 10))
        self.assertEqual(single.duration, 50)
        self.vlad.refresh_from_db(); self.oleksii.refresh_from_db()
        self.assertEqual((self.vlad.sheet_name, self.oleksii.sheet_name), ('Влад Пастушок', 'Олексій'))
        # Повторний імпорт нічого не дублює
        self.client.post('/cabinet/schedule/import/', data)
        self.assertEqual(self.LessonSeries.objects.count(), 1)
        self.assertEqual(self.Lesson.objects.count(), 6)

    def test_export_for_sheet_is_signed_and_uses_sheet_name(self):
        from .schedule import feed_token
        self.oleksii.sheet_name = 'Олексій'
        self.oleksii.save()
        start = timezone.make_aware(datetime.datetime.combine(self.mondays[0], datetime.time(17, 10)))
        lesson = self.Lesson.objects.create(teacher=self.teacher, student=self.oleksii, start=start, duration=50)
        with mock.patch('materials.reminders.send_message', return_value=True):
            self.client.post(f'/cabinet/schedule/{lesson.id}/cancel/', {'scope': 'one', 'reason': 'хворіє'})
        data = self.client.get(f'/calendar/{feed_token("t", self.teacher.id)}.json').json()
        row = next(item for item in data['lessons'] if item['id'] == lesson.id)
        self.assertEqual(row['name'], 'Олексій')
        self.assertEqual((row['date'], row['start'], row['end']),
                         (f'{self.mondays[0]:%d.%m.%Y}', '17:10:00', '18:00:00'))
        self.assertEqual((row['status'], row['reason'], row['weekday']), ('cancelled', 'хворіє', 1))
        self.assertEqual(self.client.get(f'/calendar/{feed_token("s", self.teacher.id)}.json').status_code, 404)
        forged = feed_token('t', self.teacher.id).replace(f't{self.teacher.id}-', f't{self.vlad.user_id}-')
        self.assertEqual(self.client.get(f'/calendar/{forged}.json').status_code, 404)

    def test_auto_mapping_names_from_owner_sheet(self):
        from .sheet_sync import auto_mapping
        make = lambda name: TutorStudentRequest.objects.create(
            user=self.make_user(f'{len(name)}{name[:3]}@example.com'), real_name=name, course='grade_9',
            status='approved')
        daniil, yatsenko, polina = make('Даніїл Желтіков'), make('Яценко Олексій'), make('Покора Поліна')
        self.oleksii.real_name = 'Шевцов Олексій'
        self.oleksii.save()
        students = list(TutorStudentRequest.objects.all())
        names = ['Данило Пастушок', 'Олексій', 'Поліна', 'Олексій Шевцов', 'Влад Пастушок']
        mapping = auto_mapping(names, students)
        self.assertEqual(mapping, {'Данило Пастушок': None, 'Олексій': yatsenko, 'Поліна': polina,
                                   'Олексій Шевцов': self.oleksii, 'Влад Пастушок': self.vlad})
        daniil.sheet_name = 'Данило Пастушок'   # обрали вручну один раз — далі сайт пам'ятає
        daniil.save()
        self.assertEqual(auto_mapping(names, list(TutorStudentRequest.objects.all()))['Данило Пастушок'], daniil)

    def test_sheet_script_download(self):
        response = self.client.get('/cabinet/schedule/sheet-script/')
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
        self.assertIn('function syncSchedule()', response.content.decode())
        self.client.force_login(self.vlad.user)
        self.assertEqual(self.client.get('/cabinet/schedule/sheet-script/').status_code, 404)

    def test_import_page_only_for_teachers(self):
        self.client.force_login(self.vlad.user)
        self.assertRedirects(self.client.get('/cabinet/schedule/import/'), '/cabinet/', fetch_redirect_response=False)

    def test_sheet_script_logic(self):
        """Логіка скрипта таблиці (tools/schedule_sheet_sync.gs) — якщо в оточенні є node."""
        import shutil
        import subprocess
        if not shutil.which('node'):
            self.skipTest('немає node')
        result = subprocess.run(['node', str(settings.BASE_DIR / 'tools' / 'schedule_sheet_sync.test.js')],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
