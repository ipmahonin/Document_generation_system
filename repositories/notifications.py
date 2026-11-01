from models.notifications import Notification
from sqlalchemy.orm import Session
from uuid import UUID
from servise.dto import NotificationCreat

def notification_creat(db: Session, data: NotificationCreat):
    notificatiom = Notification(user_id = data.user_id,  document_request_id = data.request_id, type = data.type, status = data.status)
    db.add(notificatiom)
    db.commit()
    db.refresh(notificatiom)
    return notificatiom

def notification_update(db: Session, notification: Notification):
    db.commit()
    db.refresh(notification)
    return notification
