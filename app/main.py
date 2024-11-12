from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config import settings


app = FastAPI()
database = Database(settings.DATABASE_URL)
metada = MetaData()
engine = create_engine(settings.DATABASE_URL)


@app.on_event('startup')
async def startup():
    await database.connect


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect
