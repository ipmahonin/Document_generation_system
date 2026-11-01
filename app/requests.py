from fastapi import APIRouter, Depends, HTTPException, Query
from db import get_db
from sqlalchemy.orm import Session
from app.security import get_current_user
from shemas.requests import RequestsCreat
from models.auth import Users
from uuid import UUID
from servise.requests import get_id, get_all, creat, delete, get_download
from  servise.exceptions import NotFoundError, BadRequestError
from fastapi.responses import FileResponse

requests = APIRouter()

@requests.post('',status_code=201)
def creat_requests(data: RequestsCreat, db: Session = Depends(get_db), user: Users = Depends(get_current_user) ):
    try:
        return creat(db=db, user_id=user.id,data=data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server fail")

@requests.get('',status_code=200)
def get_requests(
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(10, ge=1, le=100, description="Количество записей на странице")
    ):
    try:
        return get_all(db=db, user_id=user.id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server fail")

@requests.get('/{id}', status_code=200)
def get_requests_id(id: UUID, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    try:
        return get_id(db=db,id=id,user_id=user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server fail")

@requests.get('/{id}/download', status_code=200)
def download_requests(id: UUID, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    try:
        result = get_download(db=db, id=id, user_id=user.id)
        return FileResponse(
            path=result.file_path,
            media_type="application/pdf",
            filename=f'{result.id}.pdf'
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server fail")

@requests.delete('/{id}', status_code=204)
def delete_requests(id: UUID, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    try:
        return delete(db=db,id=id,user_id=user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server fail")
