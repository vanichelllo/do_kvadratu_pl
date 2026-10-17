import base64
import datetime
import hashlib
import json
import re
from unittest import mock

import ecdsa
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from .models import (AnswerOption, Cart, CartItem, CurriculumChapter, CurriculumGrade, CurriculumSubject,
                     CurriculumTopic, MatchItem, Order, OrderItem, PracticeAttempt, Question, Review, StudentReport,
                     StudyMaterial, TutorStudentRequest)

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


@override_settings(STORAGES=TEST_STORAGES, TELEGRAM_BOT_TOKEN='', TELEGRAM_ADMIN_ID='')
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
        self.assertContains(response, 'Конспекти пройдених тем')
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
        for field, value in (('status', 'pending'), ('course', 'grade_7')):
            TutorStudentRequest.objects.filter(pk=self.student.pk).update(**{field: value})
            self.assertEqual(self.client.get(self.url(self.passed)).status_code, 404, value)
            TutorStudentRequest.objects.filter(pk=self.student.pk).update(status='approved', course='nmt')

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
        page = self.client.get(f'/material/{self.material.id}/')
        self.assertContains(page, 'name="reviewer_name"')

        self.client.post('/submit-review/', {'rating': 5, 'text': 'Корисно', 'reviewer_name': 'Оля',
                                             'material_id': self.material.id})
        review = Review.objects.get(material=self.material)
        self.assertEqual(review.reviewer_name, 'Оля')

        review.is_approved = True
        review.save()
        page = self.client.get(f'/material/{self.material.id}/')
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
        page = self.client.get(f'/material/{self.bundle.id}/')
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
        expected = {f'/cart/add/{self.lesson2.id}/': f'/material/{self.lesson2.id}/',
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
        self.assertEqual(Client().get(f'/material/{hidden.id}/').status_code, 404)
        self.assertEqual(self.client.get(f'/material/{hidden.id}/').status_code, 404)
        self.client.post(f'/cart/add/{hidden.id}/')
        self.assertFalse(CartItem.objects.filter(material=hidden).exists())

        self.user.purchased_materials.add(hidden)
        self.assertEqual(self.client.get(f'/material/{hidden.id}/').status_code, 200)

    def test_owner_of_unpublished_bundle_sees_it(self):
        self.user.purchased_materials.add(self.lesson1, self.lesson2)
        StudyMaterial.objects.filter(id=self.bundle.id).update(is_published=False)
        self.assertContains(self.client.get(f'/material/{self.bundle.id}/'), 'ВИ ВЖЕ ПРИДБАЛИ')

    def test_staff_preview_of_unpublished_has_no_buy_button(self):
        hidden = StudyMaterial.objects.create(title='Чернетка', price=100, is_published=False)
        self.user.is_staff = True
        self.user.save()
        page = self.client.get(f'/material/{hidden.id}/')
        self.assertContains(page, 'не опубліковано')
        self.assertNotContains(page, 'ДОДАТИ В КОШИК')

    def test_bundle_granted_directly_counts_as_owned(self):
        self.user.purchased_materials.add(self.bundle)
        self.assertContains(self.client.get(f'/material/{self.bundle.id}/'), 'ВИ ВЖЕ ПРИДБАЛИ')
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
        self.assertRedirects(response, f'/material/{self.lesson1.id}/', fetch_redirect_response=False)
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
        self.linked = StudyMaterial.objects.create(title='12. Відсотки', is_published=True,
                                                   curriculum_topic=self.topic)
        self.hidden = StudyMaterial.objects.create(title='Чернетка', is_published=False, curriculum_topic=self.topic)

    def test_weak_topic_recommends_published_materials_of_that_topic(self):
        response = self.client.post('/diagnostic/', {'question_ids': str(self.question.id)})
        self.assertIn(self.linked, response.context['recommendations'])
        self.assertNotIn(self.hidden, response.context['recommendations'])
        self.assertContains(response, 'Записатися на заняття')
        self.assertContains(response, "diagnostic_complete")
        # Гість бачить, що результат не збережено, і пропозицію зареєструватися
        self.assertContains(response, 'не збережено')


class SeoTests(BaseTestCase):
    def test_sitemap_lists_published_materials_on_main_domain(self):
        published = StudyMaterial.objects.create(title='Тема', is_published=True)
        hidden = StudyMaterial.objects.create(title='Прихована', is_published=False)
        body = self.client.get('/sitemap.xml').content.decode()
        self.assertIn(f'https://dokvadratu.com.ua/material/{published.id}/', body)
        self.assertNotIn(f'/material/{hidden.id}/', body)
        self.assertIn('https://dokvadratu.com.ua/booking/', body)
        self.assertIn('Sitemap: https://dokvadratu.com.ua/sitemap.xml', self.client.get('/robots.txt').content.decode())

    def test_material_page_has_canonical_and_own_description(self):
        material = StudyMaterial.objects.create(title='Квадратні рівняння', description='Усе про дискримінант',
                                                is_published=True)
        page = self.client.get(f'/material/{material.id}/?utm_source=telegram')
        self.assertContains(page, f'<link rel="canonical" href="https://dokvadratu.com.ua/material/{material.id}/">',
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

    def test_banners_shown_during_promo(self):
        day = datetime.date(2026, 10, 11)
        self.assertIn('Акція до Дня Вчителя', self.render('/', day))
        booking = self.render('/booking/', day)
        self.assertIn('Акція до Дня Вчителя', booking)
        self.assertIn('192 грн', booking)

    def test_banners_hidden_after_promo(self):
        day = datetime.date(2026, 10, 12)
        self.assertNotIn('Акція до Дня Вчителя', self.render('/', day))
        booking = self.render('/booking/', day)
        self.assertNotIn('Акція до Дня Вчителя', booking)
        self.assertNotIn('192 грн', booking)
        self.assertNotIn('-20%', booking)
        self.assertIn('240 грн', booking)

    def test_cart_discount_follows_same_dates(self):
        user = self.make_user('promo@example.com')
        cart = Cart.objects.create(user=user, promo_code='ВЧИТЕЛЬ')
        CartItem.objects.create(cart=cart, material=StudyMaterial.objects.create(title='1. Тема', price=100))
        with mock.patch('materials.models.timezone.localdate', return_value=datetime.date(2026, 10, 11)):
            self.assertEqual(cart.get_total_price(), 60)
        with mock.patch('materials.models.timezone.localdate', return_value=datetime.date(2026, 10, 12)):
            self.assertEqual(cart.get_total_price(), 100)


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
                self.assertEqual(client.get(f'/material/{material.id}/').status_code, 500)
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
        response = Client().get('/diagnostic/')
        self.assertEqual(len(response.context['questions']), 15 + 3 + 4)
        queries = self.queries('/diagnostic/', Client())
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
        self.assertContains(offer, 'Редакція від 10.10.2026')
        self.assertContains(offer, 'Перше (діагностичне) заняття — безкоштовне')
        self.assertContains(offer, 'квитанція, яку Monobank автоматично надає')
        self.assertContains(offer, 'href="/privacy/"')
        self.assertNotContains(offer, '{%')
        privacy = self.client.get('/privacy/')
        self.assertContains(privacy, 'Редакція від 10.10.2026')
        self.assertContains(privacy, 'Google Analytics')
        self.assertContains(privacy, 'href="/offer/"')

    def test_terms_version_matches_published_edition(self):
        # Дата редакції на сторінках і TERMS_VERSION мають змінюватися разом
        from django.conf import settings as dj_settings
        y, m, d = dj_settings.TERMS_VERSION.split('-')
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
    def test_sprint_gives_no_balance_bonus(self):
        user = self.make_user('kid@example.com')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/game/sprint/').status_code, 200)
        response = self.client.post('/game/sprint/', '{"correct_count": 50}', content_type='application/json')
        self.assertEqual(response.status_code, 405)
        user.refresh_from_db()
        self.assertEqual(user.balance, 0)
