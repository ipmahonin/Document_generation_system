#!/bin/bash

set -e

case "$1" in
    web)
        echo "1. Применяем миграции базы данных..."
        alembic upgrade head

        echo "2. Запускаем сидер шаблонов..."
        python -c 'from servise.template_seeder import seed_templates; seed_templates()'

        echo "3. Запускаем FastAPI приложение..."
        exec uvicorn main:app --host 0.0.0.0 --port 8000
        ;;
    worker)
        echo "Запуск Celery"
        exec celery -A core.celery_app.celery_app worker --loglevel=info
        ;;
esac