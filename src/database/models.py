from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, Integer, DateTime, func, String, Column, UUID, Table

from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


association_table = Table(
    "user_likes",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id")),
    Column("post_id", Integer, ForeignKey("posts.id")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table_args__ = {"extend_existing": True}
    username = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    posts = relationship("Post", back_populates="owner", lazy="joined")
    liked_posts = relationship("Post", secondary=association_table, back_populates="likers")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    text = Column(String(555), nullable=True, default=None)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None, onupdate=func.now(), nullable=True)
    owner = relationship("User", back_populates="posts", lazy="noload")
    likers = relationship("User", secondary=association_table, back_populates="liked_posts")
