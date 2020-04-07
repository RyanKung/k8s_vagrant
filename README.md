## Simple build

'''
vagrant up
'''

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
