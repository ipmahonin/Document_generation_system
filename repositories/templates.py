from models.templates import Template
from sqlalchemy.orm import Session
from servise.dto import TemplateCreatDTO
from uuid import UUID

def template_creat(db: Session, data: TemplateCreatDTO):
    template = Template(name=data.name, slug=data.slug, descript = data.descript, schema = data.schema, html = data.htm)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

def template_get_slug(db:Session, slug: str):
    return db.query(Template).filter(Template.slug == slug).first()

def template_get_all(db:Session):
    return db.query(Template).all()

def get_teplates_by_id(db: Session, id: UUID):
    return db.query(Template).filter(Template.id == id).first()