from fastapi import Depends, FastAPI, HTTPException, status
from databases import Database
from datetime import datetime
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


@app.post('/referral-code', response_model=schemas.ReferralCodeResponse)
async def create_code(owner_id: int, code: str, expires_at: datetime,
                      database=Depends(database)):
    await crud.delete_referral_code(
        database,
        owner_id
    )
    return await crud.create_referral_code(database,
                                           owner_id, code,
                                           expires_at)


@app.get('/referral-code', response_model=schemas.ReferralCodeResponse)
async def get_code(email: str, database=Depends(database)):
    referral_code = await crud.get_referral_code_by_email(database, email)
    if not referral_code:
        raise HTTPException(status_code=404, detail="Referral code not found")
    return referral_code


@app.delete('/referral-code', status_code=204)
async def delete_code(owner_id: int, database=Depends(database)):
    await crud.delete_referral_code(database, owner_id)
