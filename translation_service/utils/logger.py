import logging
from datetime import datetime
from database.models import LogEntry
from database.config import SessionLocal
import json

class DatabaseLogger(logging.Handler):
    def emit(self, record):
        with SessionLocal() as session:
            log_entry = LogEntry(
                timestamp=datetime.utcnow(),
                service=record.name,
                level=record.levelname,
                message=record.getMessage(),
                metadata=json.loads(record.metadata) if hasattr(record, 'metadata') else {}
            )
            session.add(log_entry)
            session.commit()

def setup_logger(service_name):
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(DatabaseLogger())
    return logger 