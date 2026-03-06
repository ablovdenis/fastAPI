from .BaseModels import *

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