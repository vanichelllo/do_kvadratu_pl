import base64
import datetime
import hashlib
import json
from unittest import mock

import ecdsa
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from .models import (AnswerOption, Cart, CartItem, MatchItem, Order, OrderItem, PracticeAttempt, Question, Review,
                     StudentReport, StudyMaterial, TutorStudentRequest)

User = get_user_model()

# У тестах не ходимо в Cloudinary і не потребуємо collectstatic
TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


@override_settings(STORAGES=TEST_STORAGES, TELEGRAM_BOT_TOKEN='', TELEGRAM_ADMIN_ID='')
class BaseTestCase(TestCase):
    def make_user(self, email, **extra):
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


class MonoWebhookTests(BaseTestCase):
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
        self.client.post('/cart/pay/balance/')
        self.client.post('/cart/pay/balance/')  # повторний клік нічого не списує

        user.refresh_from_db()
        self.assertEqual(user.balance, 100)
        self.assertIn(material, user.purchased_materials.all())
        self.assertEqual(Order.objects.filter(user=user, status='paid').count(), 1)


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

    def test_legacy_buy_endpoint_does_not_charge_bundle_twice(self):
        self.client.post(f'/buy/{self.bundle.id}/')
        self.client.post(f'/buy/{self.bundle.id}/')
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 850)

    def test_state_changing_endpoints_ignore_get(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, material=self.lesson1)
        expected = {f'/cart/add/{self.lesson2.id}/': f'/material/{self.lesson2.id}/',
                    f'/cart/remove/{item.id}/': '/cart/', '/cart/pay/balance/': '/cart/', '/cart/pay/mono/': '/cart/',
                    f'/buy/{self.lesson2.id}/': f'/material/{self.lesson2.id}/'}
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


class TeacherFormsTests(BaseTestCase):
    def setUp(self):
        self.teacher = self.make_user('teacher@example.com', is_staff=True)
        self.student = TutorStudentRequest.objects.create(user=self.make_user('kid2@example.com'),
                                                          real_name='Учень', course='grade_7', status='approved')
        self.material = StudyMaterial.objects.create(title='1. Тема')
        self.client.force_login(self.teacher)

    def report_data(self, **overrides):
        data = {'student_id': self.student.id, 'topic': 'Дроби', 'nush_modeling': 10, 'nush_solving': 9,
                'nush_analysis': 8, 'homework_status': 'completed', 'teacher_comment': ''}
        data.update(overrides)
        return data

    def test_valid_report_saved(self):
        self.client.post('/cabinet/add-report/', self.report_data())
        self.assertEqual(StudentReport.objects.get().nush_solving, 9)

    def test_bad_report_shows_error_instead_of_500(self):
        for bad in ({'nush_modeling': ''}, {'nush_modeling': 13}, {'topic': ''}, {'homework_status': 'hack'}):
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
        from .models import DiagnosticTopic
        request = RequestFactory().get('/')
        request.user = self.make_user('boss2@example.com', is_staff=True, is_superuser=True)
        for model in (DiagnosticTopic, StudyMaterial):
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
