from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User


async def update_last_login(user: User, session: AsyncSession):
    user.last_login = datetime.now()
    await session.commit()


async def update_last_request_time(user: User, session: AsyncSession):
    user.last_request_time = datetime.now()
    await session.commit()
