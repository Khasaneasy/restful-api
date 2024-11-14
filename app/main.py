from fastapi import Depends, FastAPI, HTTPException, status
from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config import settings
from app import auth, crud, schemas


app = FastAPI()
database = Database(settings.DATABASE_URL)
metadata = MetaData()
engine = create_engine(settings.DATABASE_URL)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post('/register', response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "hashed_password": hashed_password,
        "is_active": True
    }
    created_user = await crud.create_user(database, user_data)

    return created_user
