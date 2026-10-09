# ДО КВАДРАТУ — освітня платформа (dokvadratu.com.ua)

Сайт для підготовки до НМТ з математики: вітрина конспектів (PDF + HTML-презентації), практика НМТ,
діагностичний тест, кабінет учня й викладача, дашборд для батьків, оплата через Monobank і Telegram-бот.

Стек: Python 3.14, Django 6.0, django-allauth (вхід через email і Google), PostgreSQL на Render,
Cloudinary для файлів, aiogram 3 (бот працює через вебхук усередині сайту).

## Локальний запуск

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

У файлі `.env` для локальної роботи потрібно `DEBUG=True` (або власний `SECRET_KEY`).

## Тести

```bash
python manage.py test
```

На GitHub тести запускаються автоматично для кожного запиту на об'єднання (`.github/workflows/tests.yml`).

## Деплой (Render)

- Build Command: `./build.sh && python manage.py import_materials`
  - `build.sh` встановлює залежності, збирає статику й застосовує міграції;
  - `import_materials` додає **нові** конспекти з `matrix.xlsx` і `import_files/` (наявні не змінює).
- Gunicorn бере налаштування з `gunicorn.conf.py` (потоки, тайм-аут).
- Версія Python — у `.python-version`.

### Змінні оточення на Render

| Змінна | Для чого |
|---|---|
| `SECRET_KEY` | обов'язкова; без неї сайт не стартує |
| `USE_POSTGRES=True`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | база даних |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | файли конспектів |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | листи (Gmail) |
| `MONOBANK_TOKEN` | оплата |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_ID` | бот і сповіщення власнику (зокрема про помилки сайту) |
| `TELEGRAM_WEBHOOK_SECRET` | необов'язкова; секрет вебхука бота (`setWebhook` з `secret_token`) |
| `WEB_CONCURRENCY` | необов'язкова; кількість процесів gunicorn (за замовчуванням 1) |

## Корисне

- Адмінка: `/do-kvadratu-secret-control/`
- Помилки сайту пишуться в логи Render і надходять сповіщенням у Telegram.
- Завислі оплати можна перевірити в адмінці: «Orders» → дія «Перевірити статус у Monobank».
- Заявки з анкети бота: адмінка → «Заявки з бота».
