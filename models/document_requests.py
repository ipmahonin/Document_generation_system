import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import enum

class RequesrStatus(str, enum.Enum):
    pending = 'pending'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'

class DocumentRequest(Base):
    __tablename__ = 'DocumentRequest'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey('Template.id'), nullable=False)
    input_data = Column(JSON, nullable=False)
    status = Column(Enum(RequesrStatus), default=RequesrStatus.pending, nullable=False)
    file_path = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)