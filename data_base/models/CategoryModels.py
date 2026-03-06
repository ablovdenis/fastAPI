from .BaseModels import *

class CategoryModel(Base, IDAndCreated_atModel, TitleModel, Is_publishedModel):
    __tablename__ = "categories"
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    posts = relationship("PostModel", back_populates="category")