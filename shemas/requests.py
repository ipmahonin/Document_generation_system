from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class DeliveryType(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"

class RequestsCreat(BaseModel):
    template_slug: str
    input_data:Dict[str, Any]
    type: DeliveryType = DeliveryType.EMAIL