from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True