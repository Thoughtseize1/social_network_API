from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Post
from src.posts.schemas import PostSchemaUpdate


class PostQuery:
    @staticmethod
    async def create(
            text: str, user: User, session: AsyncSession
    ) -> Post:
        """
        Create a new post.

        :param text: str: The text content of the post.
        :param user: User: The user who is the owner of the post.
        :param session: AsyncSession: The database session.

        :return: Post: The newly created post object.

        """
        post = Post(text=text, owner_id=user.id)
        session.add(post)
        await session.commit()
        return post

    @staticmethod
    async def read(post_id: int, session: AsyncSession) -> Post | None:
        """
        Read a post from the database.

        :param post_id: int: The ID of the post to retrieve.
        :param session: AsyncSession: The database session.

        :return: Post | None: The post object if found, otherwise None.

        """
        stmt = select(Post).where(Post.id == post_id)
        post = await session.execute(stmt)
        return post.scalars().unique().one_or_none()

    @staticmethod
    async def update(
            post: Post,
            session: AsyncSession,
            post_data: PostSchemaUpdate = None,
    ) -> Post:
        """
        Update a post in the database.

        :param post: Post: The post object to update.
        :param session: AsyncSession: The database session.
        :param post_data: PostSchemaUpdate | None: The data to update the post with.

        :return: Post: The updated post object.

        """
        if post_data:
            post.text = post_data.text
        await session.commit()
        await session.refresh(post)
        return post

    @staticmethod
    async def delete(post: Post, session: AsyncSession) -> None:
        """
        Delete a post from the database.

        :param post: Post: The post object to delete.
        :param session: AsyncSession: The database session.
        :return: None.
        """
        await session.delete(post)
        await session.commit()

    @staticmethod
    async def like_post(post: Post, user: User, session: AsyncSession) -> None:
        """
        Like a post.

        :param post: Post: The post object to like.
        :param user: User: The user liking the post.
        :param session: AsyncSession: The database session.

        :return: None.

        """
        user.liked_posts.append(post)
        await session.commit()

    @staticmethod
    async def unlike_post(post: Post, user: User, session: AsyncSession) -> None:
        """
        Allow a user to unlike a post.

        :param post: Post: The post object to unlike.
        :param user: User: The user unliking the post.
        :param session: AsyncSession: The database session.
        :return: None.
        """
        post.likers.remove(user)
        await session.commit()
