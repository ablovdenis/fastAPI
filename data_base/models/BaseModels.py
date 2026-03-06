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