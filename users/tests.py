from django.contrib.auth import get_user_model
from django.test import TestCase

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
