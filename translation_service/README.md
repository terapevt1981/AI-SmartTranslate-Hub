# Translation Service

## Overview
Translation Service is a FastAPI-based microservice that handles text translation requests using OpenAI API. It's part of the AI SmartTranslate Hub project.

## Features
- REST API for text translation
- OpenAI API integration
- Async request processing
- Error handling and validation
- Docker support
- Kubernetes deployment ready

## Prerequisites
- Python 3.9+
- OpenAI API key
- Docker
- FastAPI

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
OPENAI_API_KEY=your_api_key
```

4. Run the service:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation
After running the service, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment
1. Build image:
```bash
docker build -t translation_service:latest .
```

2. Run container:
```bash
docker run -d \
  --name translation_service \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  translation_service:latest
```

## GKE Deployment

### Prerequisites
- Google Cloud SDK installed
- Access to Google Cloud Project
- kubectl configured

### Steps

1. Tag and push Docker image:
```bash
export PROJECT_ID=your-project-id
docker tag translation_service:latest gcr.io/${PROJECT_ID}/translation_service:latest
docker push gcr.io/${PROJECT_ID}/translation_service:latest
```

2. Create Kubernetes secret for OpenAI API key:
```bash
kubectl create secret generic openai-secret \
  --from-literal=api_key=your_openai_api_key
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

## Monitoring and Scaling

### Monitoring
1. Enable Google Cloud Monitoring:
```bash
gcloud services enable monitoring.googleapis.com
```

2. View metrics in Google Cloud Console:
- CPU usage
- Memory usage
- Request latency
- Error rates

### Horizontal Pod Autoscaling
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

## Troubleshooting
1. Check pod status:
```bash
kubectl get pods -l app=translation-service
```

2. View pod logs:
```bash
kubectl logs <pod-name>
```

3. Check service endpoints:
```bash
kubectl get endpoints translation-service
```

## Support
For issues and questions, please create an issue in the repository or contact the development team. 