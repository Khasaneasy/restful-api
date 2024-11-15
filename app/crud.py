from sqlalchemy import insert, select, delete
from app.models import User, ReferralCode
from app.schemas import UserResponse, ReferralCodeResponse


async def create_user(database, user_data: dict) -> UserResponse:
    """Создание нового пользователя."""
    query = insert(User).values(**user_data).returning(User)

    result = await database.fetch_one(query)

    return UserResponse(
        id=result["id"],
        email=result["email"],
        is_active=result["is_active"]
    )


async def create_referral_code(
        database, ownner_id: int,
        code: str, expires_at) -> ReferralCodeResponse:
    """Создание нового реферального кода для пользователя."""
    query = insert(ReferralCodeResponse).values(
        ownner_id=ownner_id,
        code=code,
        expires_at=expires_at
    ).returning(ReferralCode)
    result = await database.fetch_one(query)
    return ReferralCodeResponse(
        code=result["code"],
        owner_id=result["owner_id"],
        expires_at=result["expires_at"]
    )


async def get_referral_code_by_email(database, email: str) -> ReferralCodeResponse:
    """Получение кода по email."""
    user_query = select(User.id).where(User.email == email)
    user = await database.fetch_one(user_query)
    if not user:
        return None

    code_query = select(ReferralCode).where(ReferralCode.owner_id == user["id"])
    referral_code = await database.fetch_one(code_query)
    if not referral_code:
        return None

    return ReferralCodeResponse(
        code=referral_code["code"],
        owner_id=referral_code["owner_id"],
        expires_at=referral_code["expires_at"]
    )


async def delete_referral_code(database, owner_id: int) -> None:
    """Удаление кода по ID."""
    query = delete(ReferralCode).where(ReferralCode.owner_id == owner_id)
    await database.execute(query)
