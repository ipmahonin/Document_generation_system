import os
import json 
from config import TEMPLATES_DIR
from repositories.templates import template_creat, template_get_slug, template_get_all
from servise.dto import TemplateCreatDTO
from db import SessionLocal
from redis_cashed.redis_cashed import invalidate_templates_cache

def seed_templates():
    db = SessionLocal()
    cache_needs_clearing = False
    try:
        if not os.path.exists(TEMPLATES_DIR):
            print('Шаблоны не найдены')
            return

        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith('.json'):
                slug = filename.replace('.json','')
                json_path = os.path.join(TEMPLATES_DIR, filename)
                html_path = os.path.join(TEMPLATES_DIR, f'{slug}.html')

                existing_template = template_get_slug(db=db, slug=slug)

                if not existing_template:

                    with open(json_path, 'r', encoding='utf-8') as f:
                        schema_data = json.load(f)
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_data = f.read()

                    human_name = schema_data.get("name")
                    description = schema_data.get("description")
                    
                    data_template=TemplateCreatDTO(
                        name=human_name,
                        slug=slug,
                        descript=description,
                        schema=schema_data,
                        htm=html_data
                    )
                    cache_needs_clearing = True
                    result = template_creat(db=db, data=data_template)
                    print(f"[Seeder] Шаблон '{slug}' добавлен.")
        if cache_needs_clearing:
            invalidate_templates_cache()
    except Exception as e:
        db.rollback()
        print(f"[Seeder Error] Ошибка при загрузке шаблонов: {e}")
    finally:
        db.close()

