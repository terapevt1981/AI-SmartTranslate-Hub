FROM python:3.9-slim

WORKDIR /app

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Копируем файлы проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]