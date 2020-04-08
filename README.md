## TL;DR

This repo is followed k8s guide of:

https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/

 Optimization has been made under the circumstances of Chinese networkThe vagrant/ansible will do three thinges:

1. Setup a k8s cluster with 1 master and 2 slaves.
2. Setup a private docker image on k8s master.

We also provide some config sample for other services such as `consul`, `ingress-nginx`.

## Simple build

```
vagrant up
kubectl get node -o wide
```

## Depoly a services

We have a docker registry running on `k8s-master` as `192.168.50.10:5000`, so you can create a development by push a docker repo to our private docker registry first.

## Control with `kubectl` from your host machine

Simply copy `k8s-master:~/.kube/config` to your `~/.kube/config`.


## Install Consul as mesh

1. Pre-create `PV` and `PVC` by (on host):
```
mkdir -p data
kubectl apply -f ./components/consul/storageclass.yaml
kubectl apply -f ./components/consul/pv.yaml
kubectl apply -f ./components/consul/pvc.yaml
```

2. Install consul with `helm` (on host):

```
curl https://github.com/hashicorp/consul-helm/archive/v0.18.0.zip | unzip
helm install consul v0.18.0 -f ./consul_src/consul_src.yml
```

3. Interact with consul cluster (on host):

```
kubectl port-forward services/consul-consul-server 8500:8500
export CONSUL_HTTP_ADDR="http://localhost:18500"
consul members

```

## Install ingress

```
kubectl apply -f ./components/ingress/ingress-nginx.yaml
kubectl apply -f ./components/ingress/service-nodeport.yaml

```

## Install MetalLIB

```
# ref https://metallb.universe.tf/installation/
kubectl apply -f ./compoents/metallb/namespace.yaml
kubectl apply -f ./compoents/metallb/metallb/metallb.yaml
# On first install only
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
```
