from pydantic import BaseModel
from typing import Dict, Any

class ServiceRequest(BaseModel):
    service: str
    endpoint: str
    method: str
    payload: Dict[str, Any]

class ServiceResponse(BaseModel):
    status: int
    data: Dict[str, Any] 