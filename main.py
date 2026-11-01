from fastapi import FastAPI
from app.auth import auth
from app.templates import templates
from app.requests import requests
app = FastAPI()

app.include_router(auth,prefix='/auth')
app.include_router(templates, prefix='/templates')
app.include_router(requests, prefix='/requests')