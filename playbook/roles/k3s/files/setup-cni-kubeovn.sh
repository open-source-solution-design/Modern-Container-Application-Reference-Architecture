#!/bin/bash
export NodeIP=$1
node_name=`hostname`
kubectl taint node $onde_name node-role.kubernetes.io/control-plane:NoSchedule-
kubectl label node $node_name kubernetes.io/os=linux --overwrite
kubectl label node $node_name kube-ovn/role=master --overwrite
helm repo add kubeovn https://kubeovn.github.io/kube-ovn/
helm repo up
helm upgrade --install kube-ovn kubeovn/kube-ovn --set MASTER_NODES=${NodeIP} -n kube-system
