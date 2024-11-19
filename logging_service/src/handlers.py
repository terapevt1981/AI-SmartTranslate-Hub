# logging_service/src/handlers.py
from fastapi import FastAPI, APIRouter, BackgroundTasks, HTTPException
from .schemas import LogEntry, LogQuery
from .storage import LogStorage

app = FastAPI()

app.include_router(log_router)

log_router = APIRouter(prefix="/logging")

@log_router.post("/log")
async def receive_log(
    log_entry: LogEntry, 
    background_tasks: BackgroundTasks
):
    """Эндпоинт для получения логов от сервисов"""
    try:
        background_tasks.add_task(LogStorage().save_log, log_entry)
        return {"status": "logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@log_router.post("/query")
async def query_logs(query: LogQuery):
    """Расширенный поиск логов с фильтрацией"""
    storage = LogStorage()
    return await storage.advanced_query(
        service_name=query.service_name,
        level=query.level,
        start_time=query.start_time,
        end_time=query.end_time,
        limit=query.limit
    )

@log_router.get("/services")
async def list_services():
    """Получение списка сервисов, которые логировались"""
    storage = LogStorage()
    return await storage.get_unique_services()