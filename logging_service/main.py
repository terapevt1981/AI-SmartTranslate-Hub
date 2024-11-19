from fastapi import FastAPI, BackgroundTasks, HTTPException, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import LogEntry, LogQuery
from src.storage import LogStorage
import uvicorn
import datetime
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Logging Service")

# CORS middleware для возможности межсервисного взаимодействия
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_storage = None

@app.on_event("startup")
async def startup_event():
    global log_storage
    log_storage = await LogStorage().connect()

@app.post("/logging/log")
async def receive_log(
    log_entry: LogEntry, 
    background_tasks: BackgroundTasks
):
    """Эндпоинт для получения логов от сервисов"""
    try:
        # Преобразуем Pydantic модель в словарь для MongoDB
        log_dict = log_entry.dict()
        background_tasks.add_task(log_storage.save_log, log_dict)
        return {"status": "logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
##
@app.post("/logging/query")
async def query_logs(query: LogQuery):
    if not query.service_name:
        raise HTTPException(status_code=400, detail="service_name is required")

    try:
        # # Преобразуем строки уровней в enum, если они указаны
        # levels = [LogLevel(level.strip()) for level in query.level.split(',')] if query.level else None

        logs = await log_storage.advanced_query(
            service_name=query.service_name,
            levels=query.levels,  # Передаем список уровней
            start_time=query.start_time,
            end_time=query.end_time,
            limit=query.limit
        )
        
        # Преобразование ObjectId и datetime в строку
        processed_logs = []
        for log in logs:
            # Преобразуем _id в строку, если это ObjectId
            if '_id' in log:
                log['_id'] = str(log['_id'])
            
            # Преобразуем datetime в строку для всех полей
            for key, value in log.items():
                if isinstance(value, datetime.datetime):
                    log[key] = value.isoformat()
            
            processed_logs.append(log)
        
        return JSONResponse(content=processed_logs)
    
    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid log level")
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )

@app.get("/logging/services")
async def list_services():
    """Получение списка сервисов, которые логировались"""
    return await log_storage.get_unique_services()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/logs.html") as f:
        return f.read()

@app.websocket("/ws/logs")
async def log_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Здесь вы можете реализовать логику для отправки логов в реальном времени
        # Например, отправка новых логов по мере их поступления
        await websocket.send_text("New log entry")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)