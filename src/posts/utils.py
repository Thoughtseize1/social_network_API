from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Post, association_table
from src.posts.repository import PostQuery


async def get_post_or_raise_404(post_id: int, session: AsyncSession) -> Post:
    """
    The get_post_or_raise_404 function is a helper function that will return the post with the
    given id, or raise an HTTP 404 error if no such post exists.

    :param post_id: int: Specify the type of the parameter
    :param session: AsyncSession: Pass a database session to the function
    :return: A Post object
    """
    post = await PostQuery.read(post_id=post_id, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


async def get_analytics_by_days(date_from: datetime.date, date_to: datetime.date, session: AsyncSession):
    """
    Retrieves analytics data within a specified date range.

    This function takes in a start date (`date_from`) and an end date (`date_to`),
    and returns a dictionary with dates as keys and the corresponding count of associations for each date as values.

    :param date_from: datetime.date: The start date for the analytics data.
    :param date_to: datetime.date: The end date for the analytics data.
    :param session: AsyncSession: The asynchronous database session object.

    :return: dict: A dictionary with dates as keys and association counts for each date as values.

    """
    print("Getting analytics")
    datetime_from = datetime.combine(date_from, datetime.min.time())
    datetime_to = datetime.combine(date_to, datetime.max.time())
    query = (
        select(
            func.date(association_table.c.created_at).label("date"),
            func.count().label("count")
        )
        .where(association_table.c.created_at.between(datetime_from, datetime_to))
        .group_by(func.date(association_table.c.created_at))
    )

    result = await session.execute(query)
    analytics_data = result.fetchall()
    analytics_dict = {str(date): count for date, count in analytics_data}
    return analytics_dict
