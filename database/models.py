from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    settings = Column(JSON)

class Translation(Base):
    __tablename__ = 'translations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    source_text = Column(String)
    translated_text = Column(String)
    source_language = Column(String)
    target_language = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    model_used = Column(String)

class LogEntry(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, server_default=func.now())
    service = Column(String)
    level = Column(String)
    message = Column(String)
    metadata = Column(JSON) 