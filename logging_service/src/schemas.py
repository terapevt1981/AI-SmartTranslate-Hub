# logging_service/src/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogEntry(BaseModel):
    service_name: str
    level: LogLevel
    message: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: Optional[str] = None  # Для распределенной трассировки

# class LogQuery(BaseModel):
#     service_name: Optional[str] = None
#     level: Optional[str] = None  # Строка, которую можно разделить на список
#     start_time: Optional[datetime] = None
#     end_time: Optional[datetime] = None
#     limit: int = 100
    
class LogQuery(BaseModel):
    service_name: Optional[str] = None
    levels: Optional[List[LogLevel]] = None  # Список уровней логирования
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100