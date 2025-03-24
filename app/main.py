from fastapi import FastAPI

from app import models, database, contacts

# Ініціалізація бази даних за допомогою ORM SQLAlchemy
models.Base.metadata.create_all(bind=database.engine)

# Ініціалізація FastAPI з автоматичною генерацією Swagger документації
app = FastAPI(
    title="Contact Management API",
    description="API для управління контактами з підтримкою REST CRUD, пошуку та перегляду днів народжень",
    version="1.0.0"
)

app.include_router(contacts.router, prefix="/api/v1", tags=["Contacts"])