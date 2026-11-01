from config import REDIS_URL
import redis
from uuid import UUID

CACHED_KEY = 'teplates:all'
CASHE_TTL=300

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def invalidate_templates_cache():
    redis_client.delete(CACHED_KEY)
    print("[Cache] Кэш шаблонов сброшен")

def get_user_cashed_key(user_id:UUID):
    return f'user_requests:{user_id}'