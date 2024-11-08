import logging
import json
from datetime import datetime
from database.models import LogEntry
from database.config import SessionLocal

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        with SessionLocal() as session:
            log_entry = LogEntry(
                timestamp=datetime.fromtimestamp(record.created),
                service=record.name,
                level=record.levelname,
                message=record.getMessage(),
                metadata=self._get_metadata(record)
            )
            session.add(log_entry)
            session.commit()

    def _get_metadata(self, record):
        metadata = {
            'filename': record.filename,
            'funcName': record.funcName,
            'lineno': record.lineno
        }
        if hasattr(record, 'request_id'):
            metadata['request_id'] = record.request_id
        return metadata

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Добавляем вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(console_handler)
    
    # Добавляем запись в БД
    db_handler = DatabaseHandler()
    logger.addHandler(db_handler)
    
    return logger 