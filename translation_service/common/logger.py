# common/logger.py
import uuid
import requests
from enum import Enum
from typing import Dict, Any
import socket
import os

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ServiceLogger:
    def __init__(
        self, 
        service_name: str, 
        logging_url: str = None
    ):
        self.service_name = service_name
        self.logging_url = logging_url or os.getenv(
            'LOGGING_SERVICE_URL', 
            'http://localhost:8008/logging/log'
        )
        self.trace_id = str(uuid.uuid4())

    def _send_log(
        self, 
        level: LogLevel, 
        message: Dict[str, Any]
    ):
        try:
            payload = {
                "service_name": self.service_name,
                "level": level.value,
                "message": message,
                "trace_id": self.trace_id
            }
            # requests.post(self.logging_url, json=payload, timeout=2)
            print(f"Sending log: {payload}")  # Отладочное сообщение
            response = requests.post(self.logging_url, json=payload, timeout=2)
            print(f"Log response: {response.status_code}, {response.text}")  # Отладочное сообщение
        except Exception as e:
            # Fallback - локальное логирование
            print(f"Logging failed: {e}")

    def info(self, message: Dict[str, Any]):
        self._send_log(LogLevel.INFO, message)

    def error(self, message: Dict[str, Any]):
        self._send_log(LogLevel.ERROR, message)

    # Другие методы логирования...