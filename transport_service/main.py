from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
import logging
from prometheus_client import Counter, Histogram
import os

app = FastAPI(title="Transport Service")
PORT = int(os.getenv('PORT', '8080'))

# Метрики
request_counter = Counter('transport_requests_total', 'Total requests processed')
latency_histogram = Histogram('request_latency_seconds', 'Request latency')

class ServiceRequest(BaseModel):
    service: str
    endpoint: str
    method: str
    payload: Dict[Any, Any]

@app.post("/route")
async def route_request(request: ServiceRequest):
    request_counter.inc()
    
    service_endpoints = {
        "translation": "http://translation-service:8080",
        "telegram": "http://telegram-bot-service:8080"
    }
    
    if request.service not in service_endpoints:
        raise HTTPException(status_code=400, message="Unknown service")
        
    try:
        async with httpx.AsyncClient() as client:
            with latency_histogram.time():
                response = await client.request(
                    method=request.method,
                    url=f"{service_endpoints[request.service]}/{request.endpoint}",
                    json=request.payload
                )
        return response.json()
    except Exception as e:
        logging.error(f"Error routing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 