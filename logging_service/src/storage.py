from .database import MongoDBClient
from .schemas import LogEntry, LogLevel
from typing import List, Optional
from datetime import datetime
import asyncio


class LogStorage:
    def __init__(self):
        self.db_client = None

    async def connect(self):
        self.db_client = await MongoDBClient().connect()
        return self

    async def save_log(self, log_entry: dict):
        if not self.db_client:
            await self.connect()
        
        collection = self.db_client.get_logs_collection()
        await collection.insert_one(log_entry)
        
    async def advanced_query(
        self, 
        service_name: str, 
        levels: Optional[List[LogLevel]] = None,  # Используем LogLevel из schemas
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None, 
        limit: int = 10
    ) -> List[LogEntry]:  # Возвращаем список LogEntry
        if not self.db_client:
            await self.connect()
        
        collection = self.db_client.get_logs_collection()
        
        # Построение фильтра
        query = {"service_name": service_name}
        
        # Добавляем фильтр по уровням, если они указаны
        if levels:
            query["level"] = {"$in": [level.value for level in levels]}  # Преобразуем enum в строковые значения
        
        # Фильтр по времени
        if start_time and end_time:
            query["timestamp"] = {
                "$gte": start_time, 
                "$lte": end_time
            }
        elif start_time:
            query["timestamp"] = {"$gte": start_time}
        elif end_time:
            query["timestamp"] = {"$lte": end_time}

        # Выполняем запрос с сортировкой по убыванию времени
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        
        # Преобразуем cursor в список
        logs = await cursor.to_list(length=limit)
        
        return logs



async def get_unique_services(self) -> List[str]:
        if not self.db_client:
            await self.connect()
        
        collection = self.db_client.get_logs_collection()
        return await collection.distinct('service_name')