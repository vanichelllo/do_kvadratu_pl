#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
# Уроки й банки завдань з content/school: усе, що злито в main, з'являється на сайті (файли з помилками пропускаються)
python manage.py import_school_content --all --keep-going
