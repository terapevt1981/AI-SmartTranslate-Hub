# Translation Service

## Обзор
Translation Service - это микросервис на базе FastAPI, обрабатывающий запросы на перевод текста с использованием OpenAI API. Является частью проекта AI SmartTranslate Hub.

## Возможности
- REST API для перевода текста
- Интеграция с OpenAI API
- Асинхронная обработка запросов
- Обработка ошибок и валидация
- Поддержка Docker
- Готовность к развертыванию в Kubernetes

## Предварительные требования
- Python 3.9+
- Ключ OpenAI API
- Docker
- FastAPI

## Локальная настройка разработки
1. Создание виртуального окружения:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Установка зависимостей:
```bash
pip install -r requirements.txt
```

3. Создание файла `.env`:
```env
OPENAI_API_KEY=ваш_api_ключ
```

4. Запуск сервиса:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Документация API
После запуска сервиса доступны:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Развертывание с Docker
1. Сборка образа:
```bash
docker build -t translation_service:latest .
```

2. Запуск контейнера:
```bash
docker run -d \
  --name translation_service \
  -p 8000:8000 \
  -e OPENAI_API_KEY=ваш_api_ключ \
  translation_service:latest
```

## Развертывание в GKE

### Предварительные требования
- Установленный Google Cloud SDK
- Доступ к проекту Google Cloud
- Настроенный kubectl

### Шаги

1. Пометить и отправить Docker-образ:
```bash
export PROJECT_ID=ваш-project-id
docker tag translation_service:latest gcr.io/${PROJECT_ID}/translation_service:latest
docker push gcr.io/${PROJECT_ID}/translation_service:latest
```

2. Создание секрета Kubernetes для ключа OpenAI API:
```bash
kubectl create secret generic openai-secret \
  --from-literal=api_key=ваш_openai_api_ключ
```

3. Применение манифестов Kubernetes:
```bash
# Создание развертывания
kubectl apply -f k8s/deployment.yaml

# Создание сервиса
kubectl apply -f k8s/service.yaml
```

### Пример манифестов Kubernetes

deployment.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: translation-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: translation-service
  template:
    metadata:
      labels:
        app: translation-service
    spec:
      containers:
      - name: translation-service
        image: gcr.io/PROJECT_ID/translation_service:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api_key
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
```

service.yaml:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: translation-service
spec:
  selector:
    app: translation-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

## Мониторинг и масштабирование

### Мониторинг
1. Включение Google Cloud Monitoring:
```bash
gcloud services enable monitoring.googleapis.com
```

2. Просмотр метрик в Google Cloud Console:
- Использование CPU
- Использование памяти
- Задержка запросов
- Частота ошибок

### Горизонтальное автомасштабирование подов
```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: translation-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: translation-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 70
```

## Устранение неполадок
1. Проверка статуса пода:
```bash
kubectl get pods -l app=translation-service
```

2. Просмотр логов пода:
```bash
kubectl logs <имя-пода>
```

3. Проверка конечных точек сервиса:
```bash
kubectl get endpoints translation-service
```

## Поддержка
По вопросам и проблемам создавайте issue в репозитории или обращайтесь к команде разработки. 