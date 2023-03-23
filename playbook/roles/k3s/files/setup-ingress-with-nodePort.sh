#!/bin/bash
ip=$1

helm repo add nginx-stable https://helm.nginx.com/stable
helm repo up

kubectl create namespace ingress
cat > value.yaml <<EOF
controller:
  nginxplus: false
  ingressClass: nginx
  replicaCount: 2
  service:
    enabled: true
    type: NodePort
    externalIPs:
      - $ip
EOF
helm upgrade --install nginx nginx-stable/nginx-ingress --version=0.15.0 --namespace ingress -f value.yaml

cat > nginx-cm.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-nginx-ingress
  namespace: ingress
data:
  client-max-body-size: 1000m
  external-status-address: $ip
  proxy-connect-timeout: 10s
  proxy-read-timeout: 10s
EOF


cat > nginx-svc-patch.yaml << EOF
spec:
  ports:
  - name: http
    nodePort: 80
    port: 80
    protocol: TCP
    targetPort: 80
  - name: https
    nodePort: 443
    port: 443
    protocol: TCP
    targetPort: 443
EOF

kubectl apply -f nginx-cm.yaml
kubectl patch svc nginx-nginx-ingress -n ingress --patch-file nginx-svc-patch.yaml

cat > tcp-service-crd.yaml << EOF
apiVersion: k8s.nginx.org/v1alpha1
kind: GlobalConfiguration
metadata:
  name: nginx-configuration
  namespace: ingress
spec:
  listeners:
  - name: gitlab-tcp
    port: 22
    protocol: TCP
---
apiVersion: k8s.nginx.org/v1alpha1
kind: TransportServer
metadata:
  name: gitlab-tcp-proxy
  namespace: gitlab
spec:
  listener:
    name: gitlab-tcp
    protocol: TCP
  upstreams:
  - name: gitlab-shell-svc
    service: gitlab-gitlab-shell
    port: 22
  action:
    pass: gitlab-shell-svc
EOF
kubectl apply -f tcp-service-crd.yaml
#
# https://www.nginx.com/blog/load-balancing-tcp-and-udp-traffic-in-kubernetes-with-nginx/
