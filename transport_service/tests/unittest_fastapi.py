from fastapi import FastAPI
from fastapi.routing import APIRouter
import pytest

# Создаем тестовый роутер
transport_router = APIRouter(prefix="/api/v1/transport")

@transport_router.get("/")
def root():
    return {"message": "Transport service"}

@transport_router.get("/status")
def status():
    return {"status": "ok"}

# Pytest-версия
def test_router_paths():
    # Проверка префикса роутера
    assert transport_router.prefix == "/api/v1/transport"
    
    # Проверка количества маршрутов
    assert len(transport_router.routes) == 2
    
    # Проверка путей
    route_paths = [route.path for route in transport_router.routes]
    assert "/" in route_paths
    assert "/status" in route_paths

# Дополнительные проверки
def test_route_consistency():
    # Проверка отсутствия дублей
    route_paths = [route.path for route in transport_router.routes]
    assert len(route_paths) == len(set(route_paths))

# Функция для ручной проверки
def validate_router(router):
    """
    Ручная функция валидации роутера
    """
    errors = []
    
    # Проверка префикса
    if not router.prefix.startswith("/"):
        errors.append("Префикс должен начинаться с '/'")
    
    # Проверка уникальности путей
    paths = [route.path for route in router.routes]
    if len(paths) != len(set(paths)):
        errors.append("Обнаружены дублирующиеся пути")
    
    return errors

# Пример использования функции валидации
def test_router_manual_validation():
    errors = validate_router(transport_router)
    assert len(errors) == 0, f"Обнаружены ошибки: {errors}"