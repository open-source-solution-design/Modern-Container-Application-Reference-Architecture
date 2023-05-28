#!/bin/bash
export ingress_ip=$1
helm repo add apisix https://charts.apiseven.com || echo true
helm repo update
kubectl create ns ingress || echo true
helm upgrade --install apisix apisix/apisix \
  --set etcd.replicaCount=1                 \
  --set gateway.type=NodePort               \
  --set gateway.externalIPs[0]=$ingress_ip  \
  --set ingress-controller.enabled=true     \
  --namespace ingress                       \
  --set ingress-controller.config.apisix.serviceNamespace=ingress \
  --kubeconfig /etc/rancher/k3s/k3s.yaml
kubectl get service --namespace ingress
