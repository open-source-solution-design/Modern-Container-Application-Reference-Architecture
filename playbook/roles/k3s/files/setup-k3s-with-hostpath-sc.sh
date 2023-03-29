mkdir -pv /opt/rancher/k3s
curl -sfL https://get.k3s.io | sh -s - \
	--disable=traefik                                    \
	--flannel-backend=none                               \
	--disable-network-policy                             \
	--disable-kube-proxy                                 \
	--write-kubeconfig-mode 644                          \
	--write-kubeconfig ~/.kube/config                    \
	--node-external-ip 42.xx.xx.12                       \
	--advertise-address 42.xx.xx.12                      \
	--node-ip 192.168.1.1                                \
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

helm repo add cilium https://helm.cilium.io/
helm repo add artifact https://artifact.onwalk.net/chartrepo/k8s/ | echo true
helm repo up

helm install cilium cilium/cilium --version 1.13.1 \
	--namespace kube-system             \
	--set bpf.masquerade=true           \
	--set egressGateway.enabled=true    \
	--set kubeProxyReplacement=strict   \
	--set operator.replicas=1           \
	--set devices=eth0                  \
	--set k8sServiceHost=192.168.31.254 \
	--set k8sServicePort=6443           \
	--set ipv4NativeRoutingCIDR=192.168.31.254/32 \
	--set l7Proxy=false
