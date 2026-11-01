from config import REDIS_URL
import redis
from uuid import UUID

CACHED_KEY = 'teplates:all'
CASHE_TTL=300

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def invalidate_templates_cache():
    redis_client.delete(CACHED_KEY)
    print("[Cache] Кэш шаблонов сброшен")

def get_user_cashed_key(user_id:UUID, skip: int, limit: int):
    version_key = f"user:{user_id}:cache_version"
    version = redis_client.get(version_key) or 0
    return f'user_requests:{user_id}:v:{version}:skip:{skip}:limit:{limit}'

def delete_user_cashed(user_id: UUID):
    version_key = f"user:{user_id}:cache_version"
    redis_client.incr(version_key)