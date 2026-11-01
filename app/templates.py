from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from app.security import get_current_user
from servise.template import get_all, get_slug
from  servise.exceptions import NotFoundError

templates = APIRouter()

@templates.get('', status_code=200)
def templates_get(db: Session = Depends(get_db) ,user = Depends(get_current_user)):
    try:
        return get_all(db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Server fail')

@templates.get('/{slug}', status_code=200)
def templates_get_slug(slug: str, db: Session = Depends(get_db) ,user = Depends(get_current_user)):
    try:
        return get_slug(db=db, slug=slug)
    except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Server fail')