import base64
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

        self.assertEqual(self.client.get('/cart/pay/balance/').status_code, 405)  # GET не платить
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
        Review.objects.create(user=self.user, text='Старий відгук', is_approved=True)  # reviewer_name = «Анонім»
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

    def test_state_changing_endpoints_reject_get(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, material=self.lesson1)
        for url in (f'/cart/add/{self.lesson2.id}/', f'/cart/remove/{item.id}/', '/cart/pay/balance/',
                    '/cart/pay/mono/', f'/buy/{self.lesson2.id}/'):
            self.assertEqual(self.client.get(url).status_code, 405, url)
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
            'question_ids': f'abc,{self.q1.id},,{self.match.id}',
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
