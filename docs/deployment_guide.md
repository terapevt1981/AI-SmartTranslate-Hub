# Руководство по развертыванию

## Предварительные требования

1. Google Cloud Platform аккаунт
2. Установленные инструменты:
   - gcloud CLI
   - kubectl
   - docker 

## Настройка окружения

1. Создание кластера GKE:
''
bash
gcloud container clusters create ai-translate-cluster \
--num-nodes=3 \
--zone=us-central1-a \
--machine-type=e2-standard-2
'''

2. Настройка доступа к кластеру:
```bash
gcloud container clusters get-credentials ai-translate-cluster --zone=us-central1-a
```

3. Создание секретов:
```bash
kubectl create secret generic telegram-bot-secret \
    --from-literal=token=YOUR_BOT_TOKEN

kubectl create secret generic postgres-secrets \
    --from-literal=POSTGRES_USER=admin \
    --from-literal=POSTGRES_PASSWORD=secure_password
```

## Развертывание приложения

1. Применение конфигураций базы данных:
```bash
kubectl apply -f k8s/database/

# Дождитесь готовности PostgreSQL
kubectl wait --for=condition=ready pod -l app=postgres
```

2. Развертывание сервисов:
```bash
kubectl apply -f k8s/transport-service/
kubectl apply -f k8s/translation-service/
kubectl apply -f k8s/telegram-bot/
```

3. Настройка мониторинга:
```bash
kubectl apply -f k8s/monitoring/
```

## Проверка развертывания

1. Проверка статуса подов:
```bash
kubectl get pods
```

2. Проверка логов:
```bash
kubectl logs -f deployment/telegram-bot-service
kubectl logs -f deployment/translation-service
kubectl logs -f deployment/transport-service
```

## Мониторинг

1. Доступ к Grafana:
```bash
kubectl port-forward svc/grafana 3000:3000
```

2. Доступ к Prometheus:
```bash
kubectl port-forward svc/prometheus 9090:9090
```

## Обновление приложения

1. Обновление образов:
```bash
kubectl set image deployment/telegram-bot-service \
    telegram-bot=gcr.io/PROJECT_ID/telegram-bot:new-version
```

2. Проверка статуса обновления:
```bash
kubectl rollout status deployment/telegram-bot-service
```

## Устранение неполадок

1. Проверка событий:
```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

2. Описание пода:
```bash
kubectl describe pod <pod-name>
```

3. Проверка логов:
```bash
kubectl logs <pod-name> --previous
```
```

Это завершает основную конфигурацию проекта. Все компоненты готовы к развертыванию. Есть ли какие-то конкретные части, которые нужно детализировать или дополнить?
