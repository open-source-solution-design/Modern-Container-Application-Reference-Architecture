helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo up
kubectl create ns database
helm upgrade --install mysql bitnami/mysql -n database
