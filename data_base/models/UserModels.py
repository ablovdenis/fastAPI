from .BaseModels import *

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