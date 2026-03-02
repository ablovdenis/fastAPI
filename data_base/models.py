from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime as dati

class Base(DeclarativeBase):
    pass

class IDModel:
    id = Column(Integer, primary_key=True, index=True)

class IDAndCreated_atModel(IDModel):
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)

class TextModel:
    text = Column(Text, nullable=False)

class TitleModel:
    title = Column(String, nullable=False)

class Is_publishedModel:
    is_published = Column(Boolean, default=True, nullable=False)

class UserModel(Base, IDModel):
    __tablename__ = "users"
    nickname = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    bio_info = Column(Text, default="")
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), default=dati.utcnow)
    posts = relationship("PostModel", back_populates="author", foreign_keys="PostModel.author_id")
    comments = relationship("CommentModel", back_populates="author")

class CategoryModel(Base, IDAndCreated_atModel, TitleModel, Is_publishedModel):
    __tablename__ = "categories"
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    posts = relationship("PostModel", back_populates="category")


class LocationModel(Base, IDAndCreated_atModel, Is_publishedModel):
    __tablename__ = "locations"
    name = Column(String, nullable=False)
    posts = relationship("PostModel", back_populates="location")


class PostModel(Base, IDAndCreated_atModel, TextModel, TitleModel, Is_publishedModel):
    __tablename__ = "posts"
    pub_date = Column(DateTime, nullable=False)
    image = Column(String, default="", nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    author = relationship("UserModel", back_populates="posts",
                          foreign_keys=[author_id])
    location = relationship("LocationModel", back_populates="posts")
    category = relationship("CategoryModel", back_populates="posts")
    comments = relationship(
        "CommentModel", back_populates="post", cascade="all, delete-orphan"
    )


class CommentModel(Base, IDAndCreated_atModel, TextModel):
    __tablename__ = "comments"
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post = relationship("PostModel", back_populates="comments")
    author = relationship("UserModel", back_populates="comments")