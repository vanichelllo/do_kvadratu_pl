from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

User = get_user_model()


class UserAdminTests(TestCase):
    def setUp(self):
        self.boss = User.objects.create_superuser(username='boss', email='boss@example.com', password='Pass12345!')
        self.client.force_login(self.boss)

    def test_search_by_email(self):
        User.objects.create_user(username='kid', email='findme@example.com', password='x')
        response = self.client.get('/do-kvadratu-secret-control/users/customuser/', {'q': 'findme'})
        self.assertContains(response, 'findme@example.com')

    def test_change_form_hides_password_hash(self):
        kid = User.objects.create_user(username='kid', email='kid@example.com', password='x')
        response = self.client.get(f'/do-kvadratu-secret-control/users/customuser/{kid.id}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, kid.password)

    def test_user_created_in_admin_can_log_in(self):
        self.client.post('/do-kvadratu-secret-control/users/customuser/add/', {
            'email': 'new@example.com', 'username': 'new@example.com', 'usable_password': 'true',
            'password1': 'Strong-Pass-2026!', 'password2': 'Strong-Pass-2026!',
        })
        user = User.objects.get(email='new@example.com')
        self.assertTrue(user.check_password('Strong-Pass-2026!'))


class TermsConsentTests(TestCase):
    def setUp(self):
        # Сторінка реєстрації показує кнопку Google — потрібен запис Social application
        app = SocialApp.objects.create(provider='google', name='Google', client_id='id', secret='secret')
        app.sites.add(Site.objects.get_current())

    def signup(self, **extra):
        data = {'email': 'newkid@example.com', 'password1': 'Strong-Pass-2026!', 'password2': 'Strong-Pass-2026!'}
        data.update(extra)
        return self.client.post('/register/', data)

    def test_signup_requires_terms_on_server(self):
        response = self.signup()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'потрібно погодитися з умовами')
        self.assertFalse(User.objects.filter(email='newkid@example.com').exists())

    def test_signup_records_terms_acceptance(self):
        self.signup(terms='on')
        user = User.objects.get(email='newkid@example.com')
        self.assertIsNotNone(user.terms_accepted_at)
        self.assertEqual(user.terms_version, settings.TERMS_VERSION)

    def test_user_without_consent_is_asked_first(self):
        # Так виглядає користувач, який увійшов через Google або зареєструвався раніше
        user = User.objects.create_user(username='g', email='g@example.com', password='x')
        self.client.force_login(user)
        response = self.client.get('/cabinet/')
        self.assertRedirects(response, '/accept-terms/?next=%2Fcabinet%2F', fetch_redirect_response=False)

        page = self.client.get('/accept-terms/?next=/cabinet/')
        self.assertContains(page, 'Договору оферти')

        response = self.client.post('/accept-terms/', {'next': '/cabinet/'})
        self.assertContains(response, 'Поставте галочку')
        user.refresh_from_db()
        self.assertIsNone(user.terms_accepted_at)

        response = self.client.post('/accept-terms/', {'next': '/cabinet/', 'terms': 'on'})
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)
        user.refresh_from_db()
        self.assertEqual(user.terms_version, settings.TERMS_VERSION)
        self.assertEqual(self.client.get('/cabinet/').status_code, 200)

    def test_accept_terms_ignores_foreign_next(self):
        user = User.objects.create_user(username='g', email='g@example.com', password='x')
        self.client.force_login(user)
        response = self.client.post('/accept-terms/', {'next': 'https://evil.example/', 'terms': 'on'})
        self.assertRedirects(response, '/cabinet/', fetch_redirect_response=False)

    def test_documents_and_staff_are_not_blocked(self):
        user = User.objects.create_user(username='g', email='g@example.com', password='x')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/offer/').status_code, 200)
        self.assertEqual(self.client.get('/privacy/').status_code, 200)

        boss = User.objects.create_user(username='b', email='b@example.com', password='x', is_staff=True)
        self.client.force_login(boss)
        self.assertEqual(self.client.get('/cabinet/').status_code, 200)

    def test_new_terms_version_asks_again(self):
        user = User.objects.create_user(username='g', email='g@example.com', password='x')
        user.accept_terms()
        self.client.force_login(user)
        self.assertEqual(self.client.get('/cabinet/').status_code, 200)
        with override_settings(TERMS_VERSION='2099-01-01'):
            response = self.client.get('/cabinet/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith('/accept-terms/'))


class AnalyticsConsentTests(TestCase):
    def setUp(self):
        app = SocialApp.objects.create(provider='google', name='Google', client_id='id', secret='secret')
        app.sites.add(Site.objects.get_current())

    def test_google_analytics_not_loaded_without_consent(self):
        page = self.client.get('/offer/')
        # Скрипт Google не підключається в HTML напряму — лише з JS після «Дозволити»
        self.assertNotContains(page, '<script async src="https://www.googletagmanager.com')
        self.assertContains(page, 'id="declineCookiesBtn"')

    def test_sign_up_event_is_sent_once(self):
        response = self.client.post('/register/', {
            'email': 'newkid@example.com', 'password1': 'Strong-Pass-2026!', 'password2': 'Strong-Pass-2026!',
            'terms': 'on'})
        page = self.client.get(response['Location'])
        self.assertContains(page, 'dk-analytics-events')
        self.assertContains(page, '"sign_up"')
        self.assertNotContains(self.client.get('/offer/'), 'dk-analytics-events')
