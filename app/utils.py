import jwt
from config import SECRET_KEY, ALGORITHM

def decode_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY,ALGORITHM)
        return payload
    except jwt.PyJWKError:
        return None