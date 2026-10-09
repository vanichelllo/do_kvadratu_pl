from unittest import mock

from django.test import TestCase, override_settings


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
