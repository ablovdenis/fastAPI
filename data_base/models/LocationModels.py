from .BaseModels import *

class LocationModel(Base, IDAndCreated_atModel, Is_publishedModel):
    __tablename__ = "locations"
    name = Column(String, nullable=False)
    posts = relationship("PostModel", back_populates="location")