import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import enum

class NotificationType(str, enum.Enum):
    email = 'email'
    webhook = 'webhook'

class NotificationStatus(str, enum.Enum):
    pending = 'pending'
    sent = 'sent'
    failed = 'failed'

class Notification(Base):
    __tablename__ = 'Notification'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    document_request_id = Column(UUID(as_uuid=True), ForeignKey('DocumentRequest.id'))
    type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.pending, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)