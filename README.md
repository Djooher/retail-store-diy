#  Retail Store Microservices - Cloud Native DevOps Project

##  Project Overview

This project demonstrates how a traditional online store application can be transformed into a **cloud-native microservices application** using modern DevOps practices.

The goal is not only to run an application, but to understand how real companies build, package, deploy, update, and manage applications at scale.

The project covers:

* Microservices architecture
* Docker containerization
* Kubernetes orchestration
* CI/CD automation
* GitOps deployment with ArgoCD

---

#  Application Architecture

A retail store application usually contains multiple functionalities:

* User interface
* Product catalog
* Shopping cart
* Checkout process
* Order management

Instead of building everything as one large application, we split it into independent services.

## Before: Monolithic Architecture

A traditional application could look like this:

```
                Retail Store Application

                       |
        ---------------------------------
        |        |        |             |
       UI      Cart    Checkout      Orders
```

All features are inside one application.

### Problems:

* A bug in one feature can affect the entire application
* Updating one part requires redeploying everything
* Scaling specific features is difficult

---

# After: Microservices Architecture

The application is divided into independent services:

```
                  Retail Store

                      |
 ------------------------------------------------
 |          |          |          |              |
UI       Catalog      Cart     Checkout       Orders
```

Each service:

* Has its own source code
* Has its own Docker image
* Can be deployed independently
* Can be scaled independently

Example:

If the checkout service has a problem:

```
Checkout Service 

Catalog Service 
Cart Service 
Orders Service 
```

The entire application does not need to stop.

---

# Project Structure
```
retail-store-final/

│
├── services/
│   ├── ui/
│   ├── cart/
│   ├── catalog/
│   ├── checkout/
│   └── orders/
│
├── k8s/
│   ├── namespace.yaml
│   ├── ui.yaml
│   ├── cart.yaml
│   ├── catalog.yaml
│   ├── checkout.yaml
│   └── orders.yaml
│
├── argocd/
│   └── application.yaml
│
└── README.md
```

---

#  Docker: Packaging Each Service

Docker allows each service to run in an isolated environment.

A Docker image contains:

```
Application Code
        +
Dependencies
        +
Runtime Environment
        |
        |
     Docker Image
        |
        |
     Container
```

Example:

The catalog service becomes:

```
catalog:v1

Contains:
- Python
- Flask
- Catalog code
- Required libraries
```

When Docker runs the image, it creates a container.

---

#  Container Communication

Although services are separated, they still need to communicate.

Example:

```
User

 |
 |
UI Container

 |
 |
Checkout Container

 |
 |
Cart Container

 |
 |
Orders Container
```

Docker networking allows containers to find each other.

Instead of using IP addresses:

```
localhost:5000
```

services communicate using names:

```
catalog:5000
cart:5000
orders:5000
```

Docker DNS automatically resolves these names.

---

#  Why Kubernetes?

Docker can run containers, but managing many containers manually becomes difficult.

Imagine having:

```
50 containers
```

Who will:

* Restart failed containers?
* Create new containers?
* Scale applications?
* Update versions?
* Distribute traffic?

Kubernetes solves these problems.

---

# Kubernetes Responsibilities

## 1. Self-Healing

If a container crashes:

```
Application Pod 

Kubernetes:

Create a new Pod 
```

---

## 2. Scaling

Example:

High traffic on catalog service:

Before:

```
Catalog

1 Pod
```

After:

```
Catalog

Pod 1
Pod 2
Pod 3
```

Only the required service is scaled.

---

## 3. Deployment Management

Kubernetes manages application versions.

Example:

Old version:

```
catalog:v1
```

New version:

```
catalog:v2
```

Kubernetes gradually replaces old containers with new ones.

---

# Kubernetes YAML Files

The YAML files describe what Kubernetes should create.

Example:

```
catalog.yaml
```

tells Kubernetes:

* Which Docker image to use
* How many replicas are needed
* Which ports are open
* Resource limits
* Health checks

---

#  CI/CD Pipeline

CI/CD means automatically building, testing, and deploying application changes.

The workflow:

```
Developer

    |
    |
Writes Code

    |
    |
GitHub Repository

    |
    |
GitHub Actions

    |
    |
Build Docker Image

    |
    |
Push Image to Registry

    |
    |
Deploy New Version

    |
    |
Kubernetes Cluster
```

---

# ⚙️ GitHub Actions

GitHub Actions acts like a robot.

When code changes are pushed:

It automatically:

1. Downloads the new code
2. Builds Docker images
3. Runs tests
4. Pushes images to a container registry
5. Deploys the new version

Example:

Before:

```
catalog:v1
```

After a code update:

```
catalog:v2
```

---

# Important: CI/CD Does Not Mean No Bugs

CI/CD automates the process, but it cannot guarantee perfect code.

It can:

 Build applications automatically
 Run automated tests
 Deploy changes faster

But problems can still happen because of:

* Programming errors
* Database issues
* Configuration mistakes

That is why production systems also use:

* Monitoring
* Logging
* Alerts

---

# 🚀 GitOps with ArgoCD

ArgoCD introduces a GitOps workflow.

Instead of manually deploying applications:

```
Developer

   |
   |
GitHub

   |
   |
ArgoCD

   |
   |
Kubernetes
```

ArgoCD continuously watches the Git repository.

If the desired state changes in Git:

Example:

```
image: catalog:v2
```

ArgoCD updates Kubernetes automatically.

---

# Complete Project Workflow

```
Developer
    |
    |
Git Push
    |
    |
GitHub Repository
    |
    |
GitHub Actions
    |
    |
Docker Image Build
    |
    |
Container Registry
    |
    |
ArgoCD
    |
    |
Kubernetes Cluster
    |
    |
Running Application
```

---

# 🎯 What This Project Teaches

After completing this project, you understand:

## Application Architecture

✅ Microservices
✅ Service communication
✅ Independent deployments

## Containers

✅ Docker images
✅ Docker containers
✅ Container networking

## Kubernetes

✅ Pods
✅ Deployments
✅ Services
✅ Scaling
✅ Self-healing

## DevOps

✅ CI/CD pipelines
✅ Automated deployments
✅ GitOps with ArgoCD

---

# Future Improvements

Possible improvements:

* Add Terraform for Infrastructure as Code
* Deploy on Azure Kubernetes Service (AKS)
* Add Prometheus and Grafana monitoring
* Add NGINX Ingress Controller
* Add automated testing
* Add security scanning for Docker images

---

# Author

Hadjer Boubegra (Djo)

Cloud / DevOps Learning Project
