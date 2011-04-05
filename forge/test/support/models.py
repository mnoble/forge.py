from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['User']

class User(declarative_base()):
    __tablename__ = 'users'
    id   = Column(Integer, primary_key=True)
    name = Column(String)
    age  = Column(Integer)


class Car(declarative_base()):
    __tablename__ = 'cars'
    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    owner   = relationship(User)