#!/bin/bash
set -e  # stop immediately if any command fails

echo "=== Retail Store — Full Local Rebuild ==="
echo "Run this from your project root (where kind-config.yaml and k8s/ live)"
echo ""

# 0. Sanity check: make sure required files exist here
if [ ! -f "kind-config.yaml" ] || [ ! -d "k8s" ]; then
  echo "ERROR: kind-config.yaml or k8s/ not found in current directory."
  echo "cd to your project root first, then re-run this script."
  exit 1
fi

# 1. Recreate the Kind cluster (safe even if one doesn't exist)
if kind get clusters | grep -q retail-store; then
  echo "--> Cluster 'retail-store' already exists, skipping creation."
else
  echo "--> Creating Kind cluster..."
  kind create cluster --name retail-store --config kind-config.yaml
fi

echo "--> Waiting for nodes to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

# 2. Load your images (uses ~/kind-tmp as TMPDIR to work around snap/Docker path issues)
mkdir -p ~/kind-tmp
export TMPDIR=~/kind-tmp

echo "--> Loading images into cluster..."
for svc in catalog cart orders checkout ui; do
  if docker images -q "$svc:latest" > /dev/null 2>&1 && [ -n "$(docker images -q $svc:latest)" ]; then
    kind load docker-image "$svc:latest" --name retail-store
  else
    echo "WARNING: image $svc:latest not found locally — build it first with:"
    echo "  docker build -t $svc services/$svc"
  fi
done

# 3. Install NGINX Ingress (Kind-specific manifest)
echo "--> Installing NGINX Ingress..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s

# 4. Deploy the app
echo "--> Deploying microservices..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/catalog.yaml -f k8s/cart.yaml -f k8s/orders.yaml -f k8s/checkout.yaml -f k8s/ui.yaml

echo ""
echo "--> Waiting for pods to be ready (this can take ~30-60s)..."
kubectl wait --namespace retail-store --for=condition=Ready pods --all --timeout=120s || true

echo ""
echo "=== Current status ==="
kubectl get pods -n retail-store

echo ""
echo "=== Test with: curl -I http://localhost ==="
echo "=== Or open http://localhost in your browser ==="
