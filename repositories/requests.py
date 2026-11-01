from models.document_requests import DocumentRequest
from sqlalchemy.orm import Session
from servise.dto import RequestsCreatDTO, RequestsGetDTO
from uuid import UUID

def requests_creat(db:Session, data: RequestsCreatDTO):
    requests=DocumentRequest(user_id=data.user_id, template_id=data.template_id, input_data=data.input_data)
    db.add(requests)
    db.commit()
    db.refresh(requests)
    return requests

def requests_get(db: Session, data: RequestsGetDTO):
    return db.query(DocumentRequest).filter(DocumentRequest.user_id == data.user_id).offset(data.skip).limit(data.limit).all()

def requests_get_id(db: Session, id: UUID):
    return db.query(DocumentRequest).filter(DocumentRequest.id == id).first()

def requests_delete(db: Session ,request: DocumentRequest):
    db.delete(request)
    db.commit()
    return request

def requests_update(db:Session, data:DocumentRequest):
    db.commit()
    db.refresh(data)
    return data
