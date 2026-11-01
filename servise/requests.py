from sqlalchemy.orm import Session
from repositories.requests import requests_creat, requests_delete, requests_get, requests_get_id
from servise.dto import RequestsCreatDTO
from shemas.requests import RequestsCreat
from repositories.templates import template_get_slug
from uuid import UUID
import jsonschema
from jsonschema.exceptions import ValidationError as JSONschemaValidationError
from  servise.exceptions import NotFoundError, BadRequestError
from redis_cashed.redis_cashed import redis_client, CASHE_TTL, get_user_cashed_key
import json
from workers.tasks import generate_document_task
import os




def creat(db: Session, user_id: UUID, data: RequestsCreat):
    template = template_get_slug(db=db, slug=data.template_slug)
    
    if template is None:
        raise NotFoundError('Template not found')

    try:
        jsonschema.validate(instance=data.input_data, schema=template.schema)
    except JSONschemaValidationError as e:
        raise BadRequestError("Bad request")


    request_dto = RequestsCreatDTO(
        user_id=user_id,
        template_id=template.id,
        input_data=data.input_data
    )

    

    result_db = requests_creat(db=db, data= request_dto)

    result = {
        'id': str(result_db.id),
        'status': result_db.status,
        'created_at': result_db.created_at
    }

    cashed_key =get_user_cashed_key(user_id=user_id)
    redis_client.delete(cashed_key)
    print(f'Cбросили кеш пользователя {user_id}')

    generate_document_task.delay(
            request_id=str(result_db.id),
            delivery_type=data.type
        )
    print(f'Отправили запрос {result_db.id} в очередь')

    return(result)

def get_all(db:Session, user_id: UUID):
    cashed_key =get_user_cashed_key(user_id=user_id)
    cached_data = redis_client.get(cashed_key)
    if cached_data:
        print("Данные о запросах из Redisa")
        return json.loads(cached_data)
    print("Данные о запросах в Redis отсутствуют")
    
    requests = requests_get(db=db, user_id=user_id)
    result = [
        {
            'id': str(request.id),
            'status': request.status
        } for request in requests
    ]

    redis_client.setex(cashed_key, CASHE_TTL, json.dumps(result))
    print('Положили запросы usera в Redis')

    return result

def get_id(db: Session, id: UUID, user_id: UUID):
    request = requests_get_id(db=db, id=id)
    if request is None:
        raise NotFoundError('Request not found')
    if not(request.user_id == user_id):
            raise BadRequestError("Bad request")
    return{
        'id':request.id,
        'status':request.status,
        'error_message': request.error_message,
        'created_at': request.created_at,
        'started_at': request.started_at,
        'completed_at': request.completed_at
    }

def delete(db:Session, user_id:UUID, id:UUID):
    request = requests_get_id(db=db, id=id)
    if request is None:
        raise NotFoundError('Request not found')
    if not(request.status == 'pending'):
        raise BadRequestError("Status is not pending")
    if not(request.user_id == user_id):
        raise BadRequestError("Bad request")
    result = requests_delete(db=db, request=request)
    return{
        'id': result.id,
        'status':'delete'
    }

def get_download(db: Session, id: UUID, user_id: UUID):
    db_request = requests_get_id(db=db, id=id)

    if db_request is None:
        raise NotFoundError('Request not found')
    if not(db_request.user_id == user_id):
            raise BadRequestError("Bad request")
    if not(db_request.status == 'comleted'):
        raise BadRequestError("Not comleted")
    if not os.path.exists(db_request.file_path):
        raise NotFoundError('File not found')

    return db_request
    


            