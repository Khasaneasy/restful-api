from sqlalchemy import (
    Boolean, Column, DateTime,
    ForeignKey, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(Integer, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class ReferralCode(Base):
    __tablename__ = "referral_codes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)
