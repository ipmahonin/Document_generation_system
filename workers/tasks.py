from core.celery_app import celery_app
from db import SessionLocal
from celery.exceptions import MaxRetriesExceededError
from uuid import UUID
from repositories.requests import requests_get_id, requests_update
from datetime import datetime, timezone
from servise.pdf_generator import get_output_pdf_path, render_pdf_from_html
from repositories.templates import get_teplates_by_id
from models.auth import Users
from repositories.notifications import notification_creat, notification_update
from servise.dto import NotificationCreat
from models.document_requests import RequesrStatus
from models.notifications import NotificationStatus
from redis_cashed.redis_cashed import redis_client, get_user_cashed_key



@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def generate_document_task(self, request_id: str,  delivery_type: str):
    db = SessionLocal()
    try:
        request = requests_get_id(db=db, id=UUID(request_id))
        request.started_at = datetime.now(timezone.utc)
        request.status = RequesrStatus.pending
        request = requests_update(db=db, data=request)

        cashed_key =get_user_cashed_key(user_id=request.user_id)
        redis_client.delete(cashed_key)

        print(f'Выполнение генерации по запросу {request_id}')
        output_path = get_output_pdf_path(request_id=request_id)
        template = get_teplates_by_id(db=db, id= request.template_id)
        result = render_pdf_from_html(
            template_text=template.html,
            data= request.input_data,
            output_pdf_path= output_path
        )
        request.status = RequesrStatus.completed
        request.completed_at = datetime.now(timezone.utc)
        request.file_path = output_path
        requests_update(db=db, data=request)

        cashed_key =get_user_cashed_key(user_id=request.user_id)
        redis_client.delete(cashed_key)
                            
        print(f'Генерация готова по запросу {request_id}')
        send_notification_task.delay(request_id=request_id, delivery_type=delivery_type)
    except Exception as e:
        print(f"Ошибка при генерации документа: {e}")
        db.rollback()
        try:
            print(f"Ошибка в задаче {request_id}: {e}. Пробуем повторить...")
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: Запрос {request_id} провалил все попытки выполнения.")
            request.status = RequesrStatus.failed
            request.completed_at = datetime.now(timezone.utc)
            request.error_message = (f"Ошибка при генерации документа: {e}")
            request = requests_update(db=db,data=request)
            raise
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def send_notification_task(self, request_id: str, delivery_type: str):
    db = SessionLocal()
    try:
        request = requests_get_id(db=db, id=request_id)

        data = NotificationCreat(
             user_id=request.user_id,
             request_id=request.id,
             status= NotificationStatus.pending,
             type=delivery_type
        )

        notification = notification_creat(db=db, data=data)
    
        print(f'Отправка сообщения о готовности запроса {request.id} по {delivery_type}')

        notification.sent_at = datetime.now(timezone.utc)
        notification.status = NotificationStatus.sent

        notification = notification_update(db=db, notification=notification)

    except Exception as e:
        print(f"Ошибка при отправки сообщения {e}")
        try:
            print(f"Ошибка при отправки сообщения о готовности {request_id}: {e}. Пробуем повторить...")
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
                    print(f"КРИТИЧЕСКАЯ ОШИБКА: Запрос на отправку {request_id} провалил все попытки выполнения.")
                    notification.status = NotificationStatus.failed
                    notification = notification_update(db=db, notification=notification)
                    raise
    finally:
            db.close()
