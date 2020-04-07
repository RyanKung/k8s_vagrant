## TL;DR

This repo is followed k8s guide of:

https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/

But optimized alot for Chinese network envirement. The vagrant/ansible will do three thinges:

1. Setup a k8s cluster with 1 master and 2 slaves.
2. Setup a private docker image on k8s master.

We also provide some config sample for other services such as `consul`.

## Simple build

```
vagrant up
```

## Depoly a services

We have a docker registry running on `k8s-master` as `192.168.50.10:5000`, so you can create a development by push a docker repo to out private docker registry first.

## Control with `kubectl` from your host machine

Simply copy `k8s-master:~/.kube/config` to your `~/.kube/config`.


## Install Consul as mesh

1. Pre-create `PV` and `PVC` by:
```
mkdir -p data
kubectl apply -f ./consul_src/storageclass.yaml
kubectl apply -f ./consul_src/pv.yaml
kubectl apply -f ./consul_src/pvc.yaml
```

2. Install consul with `helm`

```
curl https://github.com/hashicorp/consul-helm/archive/v0.18.0.zip | unzip
helm install consul v0.18.0 -f ./consul_src/consul_src.yml
```
