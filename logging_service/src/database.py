# logging_service/src/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

host_mongodb = os.getenv('HOST_MONGODB')
password_mongodb = os.getenv('PASSWORD_MONGODB')

class MongoDBClient:
    def __init__(
        self,
        host=host_mongodb, 
        port=27017, 
        username='admin', 
        password=password_mongodb,
        database='logging_db'
    ):
        self.connection_string = f'mongodb://{username}:{password}@{host}:{port}'
        self.client = None
        self.db = None
        self.database_name = database

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Проверка подключения
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            return self
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        if self.client:
            self.client.close()

    def get_logs_collection(self):
        return self.db['service_logs']