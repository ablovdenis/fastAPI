from .BaseModels import *

class CommentModel(Base, IDAndCreated_atModel, TextModel):
    __tablename__ = "comments"
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post = relationship("PostModel", back_populates="comments")
    author = relationship("UserModel", back_populates="comments")