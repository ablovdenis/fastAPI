from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime as dati
from ..database import Base


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=dati.utcnow)
    text = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    pub_date = Column(DateTime(timezone=True), default=dati.utcnow)
    images = relationship("PostImageModel", back_populates="post", passive_deletes=True)

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    author = relationship("UserModel", back_populates="posts")
    location = relationship("LocationModel", back_populates="posts")
    category = relationship("CategoryModel", back_populates="posts")
    comments = relationship(
        "CommentModel", back_populates="post", passive_deletes=True
    )
