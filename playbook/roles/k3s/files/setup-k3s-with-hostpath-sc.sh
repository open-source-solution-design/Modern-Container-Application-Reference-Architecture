mkdir -pv /opt/rancher/k3s
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.24.7+k3s1 sh -s - \
	--disable=traefik \
	--write-kubeconfig-mode 644 \
	--write-kubeconfig ~/.kube/config \
	--data-dir=/opt/rancher/k3s \
	--kube-apiserver-arg service-node-port-range=0-50000

#export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
sudo wget --no-check-certificate https://mirrors.onwalk.net/tools/linux-amd64/helm.tar.gz && sudo tar -xvpf helm.tar.gz -C /usr/local/bin/
sudo chmod 755 /usr/local/bin/helm
helm repo add artifact https://artifact.onwalk.net/chartrepo/k8s/
helm repo up