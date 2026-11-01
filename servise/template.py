from sqlalchemy.orm import Session
from repositories.templates import template_get_all, template_get_slug
from redis_cashed.redis_cashed import redis_client, CACHED_KEY, CASHE_TTL
import json
from  servise.exceptions import NotFoundError
def get_all(db: Session):
    cashed_data = redis_client.get(CACHED_KEY)

    if cashed_data:
        print('Данные из Redis')
        return json.loads(cashed_data)
    print('Не нашли данные в Redis')

    templates = template_get_all(db=db)
    if not templates:
        raise NotFoundError('Templates not found')
    
    result = [{
                'name':template.name,
                'descript':template.descript
            } for template in templates]

    redis_client.setex(CACHED_KEY, CASHE_TTL, json.dumps(result))
    print('Положили данные в Redis')
    return result

def get_slug(db:Session, slug: str):
    template = template_get_slug(db=db, slug=slug)
    if template is None:
        raise NotFoundError('Template not found')
    return {
                'name':template.name,
                'slug':template.slug,
                'descript':template.descript,
                'schema': template.schema['required']
            }
        