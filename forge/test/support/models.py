from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['User']

class User(declarative_base()):
    __tablename__ = 'users'
    id   = Column(Integer, primary_key=True)
    name = Column(String)