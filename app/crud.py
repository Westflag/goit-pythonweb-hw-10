from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from datetime import date, timedelta

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    try:
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except IntegrityError:
        db.rollback()
        return None

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, first_name: str = None, last_name: str = None, email: str = None):
    query = db.query(models.Contact)
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    return query.all()

def get_upcoming_birthdays(db: Session):
    today = date.today()
    upcoming_date = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birthday >= today,
        models.Contact.birthday <= upcoming_date
    ).all()