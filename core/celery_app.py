from celery import Celery 
from config import RABBITMQ_URL, REDIS_URL

celery_app = Celery(
    'worker',
    broker=RABBITMQ_URL,
    backend=REDIS_URL,
    include=['workers.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utс=True
)