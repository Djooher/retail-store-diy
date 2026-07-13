# Retail Store Microservices Application

A cloud-native retail store application built using a **microservices architecture**.
The project demonstrates containerization, service communication, Kubernetes deployment, and DevOps practices.

##  Architecture Overview

The application is composed of multiple independent services:

* **UI Service** → Frontend web interface
* **Catalog Service** → Product catalog management
* **Cart Service** → Shopping cart management
* **Checkout Service** → Checkout process
* **Orders Service** → Order processing

Each service runs inside its own container and communicates with other services through internal networking.

##  Tech Stack

### Application

* Python Flask
* HTML/CSS/JavaScript

### Containers

* Docker
* Docker Compose (local testing)

### Kubernetes

* Kubernetes Deployments
* Services
* ConfigMaps
* Secrets
* Probes (liveness/readiness)
* Resource requests and limits

### DevOps Tools

* Git & GitHub
* GitHub Actions CI/CD
* ArgoCD GitOps deployment

##  Project Structure

```
retail-store-final/
│
├── services/
│   ├── cart/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── catalog/
│   ├── checkout/
│   ├── orders/
│   └── ui/
│
├── k8s/
│   ├── namespace.yaml
│   ├── cart.yaml
│   ├── catalog.yaml
│   ├── checkout.yaml
│   ├── orders.yaml
│   └── ui.yaml
│
├── argocd/
│   └── application.yaml
│
├── kind-config.yaml
└── README.md
```

# Running Locally With Docker

## 1. Create Docker Network

```bash
docker network create retail-net
```

## 2. Build Images

Example:

```bash
docker build -t catalog ./services/catalog
docker build -t cart ./services/cart
docker build -t checkout ./services/checkout
docker build -t orders ./services/orders
docker build -t ui ./services/ui
```

## 3. Run Containers

Example:

```bash
docker run -d \
--name catalog \
--network retail-net \
-p 5002:5000 \
catalog
```

Repeat for other services.

Check running containers:

```bash
docker ps
```

## 4. Access Application

Open:

```
http://localhost:8080
```

##  Kubernetes Deployment

## 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

## 2. Deploy Services

```bash
kubectl apply -f k8s/
```

Check pods:

```bash
kubectl get pods -n retail
```

Check services:

```bash
kubectl get svc -n retail
```

##  CI/CD Pipeline

The project follows a modern DevOps workflow:

```
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    v
Docker Image Build
    |
    v
Container Registry
    |
    v
ArgoCD
    |
    v
Kubernetes Cluster
```

##  Kubernetes Features Used

### Deployments

Provide:

* Scaling
* Self-healing
* Rolling updates

Example:

```yaml
replicas: 3
```

### Readiness Probe

Checks if the application is ready to receive traffic.

### Liveness Probe

Restarts unhealthy containers automatically.

### Resource Management

Containers have CPU and memory limits:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

## Troubleshooting

### Check Logs

```bash
docker logs <container-name>
```

or Kubernetes:

```bash
kubectl logs <pod-name> -n retail
```

### Enter Container

```bash
docker exec -it <container-name> bash
```

### Test Service Communication

Example:

```bash
curl http://catalog:5000/catalog
```

##  Project Goals

This project demonstrates:

 Microservices architecture
 Docker containerization
 Kubernetes orchestration
 Service discovery
 CI/CD automation
 GitOps deployment using ArgoCD
 Cloud-native application practices

##  Author

Hadjer Boubegra (Djo)

Cloud / DevOps Engineering Project
