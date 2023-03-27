#!/bin/bash
ip=$1

cat > /tmp/egress.yaml << EOF
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: egress-nat
spec:
  endpointSelector:
    matchLabels:
      role: egress-gateway
  egress:
  - {}
  egressNAT:
  - source: 10.42.0.0/16
    translation: $ip
EOF
kubectl apply -f /tmp/egress.yaml
