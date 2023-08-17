from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
