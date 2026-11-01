import uuid
from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Template(Base):
    __tablename__ = 'Template'

    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4)
    name = Column (String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    descript = Column(Text, nullable=True)
    schema = Column(JSON, nullable= False)
    html = Column(Text, nullable=False)
