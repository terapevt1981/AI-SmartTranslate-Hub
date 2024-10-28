# Telegram Bot Service

## Обзор
Telegram Bot Service - компонент AI SmartTranslate Hub, обрабатывающий сообщения и запросы на перевод через интерфейс Telegram.

## Возможности
- Обработка сообщений в реальном времени
- Поддержка перевода текста
- Обработка ошибок и логирование
- Поддержка нескольких языков
- Контейнеризация Docker
- Готовность к развертыванию в Kubernetes

## Предварительные требования
- Python 3.9+
- Docker
- Токен Telegram Bot
- Доступ к Translation Service

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
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TRANSLATION_SERVICE_URL=http://localhost:8000/translate
```

4. Запуск бота:
```bash
python bot.py
```

## Развертывание с Docker
1. Сборка образа:
```bash
docker build -t telegram_bot_service:latest .
```

2. Запуск контейнера:
```bash
docker run -d \
  --name telegram_bot_service \
  -e TELEGRAM_BOT_TOKEN=ваш_токен_бота \
  -e TRANSLATION_SERVICE_URL=http://translation_service:8000/translate \
  telegram_bot_service:latest
```

## Развертывание в GKE

### Предварительные требования
- Установленный Google Cloud SDK
- Доступ к проекту Google Cloud
- Настроенный kubectl

### Шаги

1. Пометить и отправить Docker-образ в Google Container Registry:
```bash
export PROJECT_ID=ваш-project-id
docker tag telegram_bot_service:latest gcr.io/${PROJECT_ID}/telegram_bot_service:latest
docker push gcr.io/${PROJECT_ID}/telegram_bot_service:latest
```

2. Создание секрета Kubernetes для токена бота:
```bash
kubectl create secret generic telegram-bot-secret \
  --from-literal=token=ваш_токен_бота
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
  name: telegram-bot-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: telegram-bot-service
  template:
    metadata:
      labels:
        app: telegram-bot-service
    spec:
      containers:
      - name: telegram-bot-service
        image: gcr.io/PROJECT_ID/telegram_bot_service:latest
        env:
        - name: TELEGRAM_BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegram-bot-secret
              key: token
        - name: TRANSLATION_SERVICE_URL
          value: http://translation-service:8000/translate
```

service.yaml:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: telegram-bot-service
spec:
  selector:
    app: telegram-bot-service
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

## Мониторинг и логирование
- Используйте Google Cloud Monitoring для метрик
- Доступ к логам через Google Cloud Logging:
```bash
kubectl logs -f deployment/telegram-bot-service
```

## Устранение неполадок
1. Проверка статуса пода:
```bash
kubectl get pods
```

2. Просмотр логов пода:
```bash
kubectl logs <имя-пода>
```

3. Проверка статуса сервиса:
```bash
kubectl get services
```

## Поддержка
По вопросам и проблемам создавайте issue в репозитории или обращайтесь к команде разработки. 