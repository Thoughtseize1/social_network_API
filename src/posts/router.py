from datetime import datetime, date
from typing import List

from fastapi import APIRouter, status, Form, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_async_session
from src.database.models import User, Post
from src.posts.repository import PostQuery
from src.posts.schemas import PostSchemaResponse
from src.posts.utils import get_post_or_raise_404, get_analytics_by_days
from src.users.users import current_active_user

posts_router = APIRouter(prefix="/post", tags=["posts"])


@posts_router.get("/", response_model=List[PostSchemaResponse])
async def get_all_user_posts(
        current_user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    return current_user.posts


@posts_router.get("/all", response_model=List[PostSchemaResponse])
async def get_all_posts(
        session: AsyncSession = Depends(get_async_session),
):
    # Получите все посты для всех пользователей из базы данных
    # Это просто пример, вам нужно адаптировать его к вашей логике
    all_posts = await session.execute(select(Post).order_by(Post.created_at.desc()))
    return all_posts.scalars().all()


@posts_router.post(
    "/create", response_model=PostSchemaResponse, status_code=status.HTTP_201_CREATED
)
async def create_post(
        text: str = Form(...),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    post = await PostQuery.create(text=text, user=user, session=session)
    return post


@posts_router.get("/{post_id}", response_model=PostSchemaResponse)
async def get_post(
        post_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)):
    post = await PostQuery.read(post_id, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!"
        )
    return post


@posts_router.post("/{post_id}/like", response_model=None, status_code=status.HTTP_200_OK)
async def like_post(
        post_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    try:
        post = await get_post_or_raise_404(post_id=post_id, session=session)
        if user in post.likers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already liked this post",
            )

        await PostQuery.like_post(post=post, user=user, session=session)
        return {"message": "Post liked successfully", "total_likes": len(post.likers)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@posts_router.post("/{post_id}/unlike", response_model=None, status_code=status.HTTP_200_OK)
async def unlike_post(
        post_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    try:
        post = await get_post_or_raise_404(post_id=post_id, session=session)
        if user not in post.likers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have not liked this post",
            )

        await PostQuery.unlike_post(post=post, user=user, session=session)

        return {"message": "Post unliked successfully", "total_likes": len(post.likers)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@posts_router.get("/analytics/")
async def get_analytics(
        date_from: str,
        date_to: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)

):
    if not date_from and not date_to:
        return {"error": "Both date_from and date_to are required."}

    try:
        _date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date_from format. Please use YYYY-MM-DD."}

    try:
        if date_from and not date_to:
            print('TUTA')
            return await get_analytics_by_days(_date_from, date.today(), session)
        _date_to = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date_from format. Please use YYYY-MM-DD."}
    return await get_analytics_by_days(_date_from, _date_to, session)
