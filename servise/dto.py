from  dataclasses import dataclass
from typing import Any
from uuid import UUID
from models.notifications import NotificationType, NotificationStatus

@dataclass
class UserRegisterDTO:
    email: str
    hash_password: str
    full_name: str

@dataclass
class TemplateCreatDTO:
    name: str
    slug: str
    schema: dict[str: Any]
    htm: str
    descript : str | None=None

@dataclass
class RequestsCreatDTO:
    user_id: UUID
    template_id: UUID
    input_data: dict

@dataclass
class NotificationCreat:
    user_id: UUID
    request_id: UUID
    type: NotificationType
    status: NotificationStatus

@dataclass
class RequestsGetDTO:
    user_id: UUID
    skip: int = 0
    limit: int = 10