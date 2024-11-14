from sqlalchemy import insert
from app.models import User
from app.schemas import UserResponse


async def create_user(database, user_data: dict) -> UserResponse:
    query = insert(User).values(**user_data).returning(User)

    result = await database.fetch_one(query)

    return UserResponse(
        id=result["id"],
        email=result["email"],
        is_active=result["is_active"]
    )
