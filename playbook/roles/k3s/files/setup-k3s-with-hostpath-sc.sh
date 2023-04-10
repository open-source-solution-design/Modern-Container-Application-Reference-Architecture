#!/bin/bash

mkdir -pv /opt/rancher/k3s
curl -sfL https://get.k3s.io | sh -s - \
	--disable=traefik,servicelb                          \
	--write-kubeconfig-mode 644                          \
	--write-kubeconfig ~/.kube/config                    \
	--data-dir=/opt/rancher/k3s                          \
	--kube-apiserver-arg service-node-port-range=0-50000

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

case `uname -m` in
	x86_64) ARCH=amd64; ;;
        aarch64) ARCH=arm64; ;;
        loongarch64) ARCH=loongarch64; ;;
        *) echo "un-supported arch, exit ..."; exit 1; ;;
esac
rm -rf helm.tar.gz* /usr/local/bin/helm || echo true 
sudo wget --no-check-certificate https://mirrors.onwalk.net/tools/linux-${ARCH}/helm.tar.gz && sudo tar -xvpf helm.tar.gz -C /usr/local/bin/
sudo chmod 755 /usr/local/bin/helm

helm repo add artifact https://artifact.onwalk.net/chartrepo/k8s/ | echo true
helm repo up
