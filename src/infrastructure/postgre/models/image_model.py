from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PostImageModel(Base):
    __tablename__ = "post_images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    post = relationship("PostModel", back_populates="images")