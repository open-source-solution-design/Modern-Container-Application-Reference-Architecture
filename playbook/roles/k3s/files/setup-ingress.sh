#!/bin/bash
ingress=$1
ingress_ip=$2

if [[ $ingress_type == nginx ]]; then
cat > value.yaml <<EOF
controller:
  nginxplus: false
  ingressClass: nginx
  replicaCount: 2
  service:
    enabled: true
    type: NodePort
    externalIPs:
      - $ingress_ip
EOF

cat > nginx-cm.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-nginx-ingress
  namespace: ingress
data:
  external-status-address: $ingress_ip
  proxy-connect-timeout: 10s
  proxy-read-timeout: 10s
  client-header-buffer-size: 64k
  client-body-buffer-size: 64k
  client-max-body-size: 1000m
  proxy-buffers: 8 32k
  proxy-body-size: 1024m
  proxy-buffer-size: 32k
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

helm repo add nginx-stable https://helm.nginx.com/stable || echo true
helm repo up
kubectl create namespace ingress || echo true
helm upgrade --install nginx nginx-stable/nginx-ingress --version=0.15.0 --namespace ingress -f value.yaml
kubectl apply -f nginx-cm.yaml
kubectl patch svc nginx-nginx-ingress -n ingress --patch-file nginx-svc-patch.yaml

elif [[ $ingress_type == apisix ]]; then

export ingress_ip=$1
helm repo add apisix https://charts.apiseven.com || echo true
helm repo update
kubectl create ns ingress || echo true
helm upgrade --install apisix apisix/apisix \
  --set etcd.replicaCount=1                 \
  --set gateway.type=NodePort               \
  --set gateway.http.enabled=true           \
  --set gateway.http.nodePort=80            \
  --set gateway.tls.enabled=true            \
  --set gateway.tls.nodePort=443            \
  --set gateway.externalIPs[0]=$ingress_ip  \
  --set ingress-controller.enabled=true     \
  --namespace ingress                       \
  --set ingress-controller.config.apisix.serviceNamespace=ingress \
  --kubeconfig /etc/rancher/k3s/k3s.yaml
kubectl get service --namespace ingress
fi
