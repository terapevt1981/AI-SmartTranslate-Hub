# Telegram Bot Service

## Overview
Telegram Bot Service is a component of AI SmartTranslate Hub that handles message processing and translation requests through Telegram interface.

## Features
- Real-time message processing
- Text translation support
- Error handling and logging
- Multiple language support
- Docker containerization
- Kubernetes deployment ready

## Prerequisites
- Python 3.9+
- Docker
- Telegram Bot Token
- Access to Translation Service

## Local Development Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
TRANSLATION_SERVICE_URL=http://localhost:8000/translate
```

4. Run the bot:
```bash
python bot.py
```

## Docker Deployment
1. Build image:
```bash
docker build -t telegram_bot_service:latest .
```

2. Run container:
```bash
docker run -d \
  --name telegram_bot_service \
  -e TELEGRAM_BOT_TOKEN=your_bot_token \
  -e TRANSLATION_SERVICE_URL=http://translation_service:8000/translate \
  telegram_bot_service:latest
```

## GKE Deployment

### Prerequisites
- Google Cloud SDK installed
- Access to Google Cloud Project
- kubectl configured

### Steps

1. Tag and push Docker image to Google Container Registry:
```bash
export PROJECT_ID=your-project-id
docker tag telegram_bot_service:latest gcr.io/${PROJECT_ID}/telegram_bot_service:latest
docker push gcr.io/${PROJECT_ID}/telegram_bot_service:latest
```

2. Create Kubernetes secret for bot token:
```bash
kubectl create secret generic telegram-bot-secret \
  --from-literal=token=your_bot_token
```

3. Apply Kubernetes manifests:
```bash
# Create deployment
kubectl apply -f k8s/deployment.yaml

# Create service
kubectl apply -f k8s/service.yaml
```

### Kubernetes Manifests Example

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

## Monitoring and Logging
- Use Google Cloud Monitoring for metrics
- Access logs through Google Cloud Logging:
```bash
kubectl logs -f deployment/telegram-bot-service
```

## Troubleshooting
1. Check pod status:
```bash
kubectl get pods
```

2. View pod logs:
```bash
kubectl logs <pod-name>
```

3. Check service status:
```bash
kubectl get services
```

## Support
For issues and questions, please create an issue in the repository or contact the development team. 