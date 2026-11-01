from sqlalchemy import Column, String, Boolean, DateTime
from db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

class Users(Base):
    __tablename__ = 'Users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_activ = Column (Boolean, default=True, nullable=False)