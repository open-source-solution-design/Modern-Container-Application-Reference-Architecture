#!/bin/bash

export secret=$3
export key_file=$1
export cert_file=$2
export namespace=$3

kubectl create namespace $namespace || echo true
kubectl delete secret tls $secret -n $namespace || echo true
kubectl create secret tls $secret --cert=$cert_file --key=$key_file -n $namespace
