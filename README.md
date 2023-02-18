# kube-pyinfra-pulumi-all-in-one


This project aims to show a code pattern example that you cans use as a boilerplate on how you can in one repo handle infrastructure provisioning, configuration management, app deployment and the source code of the application itself

In more details the code present in the repo will allow you to :
1.  Provision an infrastructure on GCP with pulumi
2.  Deploy a cluster kubernetes with pyinfra
3.  Expose your cluster to the outside world
4.  Deploy a python app into the kubernetes cluster

We will deploy the following architecture :

![schema](assets/schema-Page-3.png)
See the architecture schema below : 


Pre-requisite installs:

* **Justfile** : Makefile alternative written on rust, a bit more flexible, see how to instal it [here](https://just.systems/man/en/chapter_1.html) 
* **Docker** : Container runtime we use for our tutorial + image builder see how to install it [here](https://www.docker.com/get-started/) 
* **Pulumi CLI** : Pulumi will provision our infrastructure in GCP see how to download it [here](https://www.pulumi.com/docs/get-started/install/)
* **Gcloud CLI** : Google cloud cli that authenticate & authorize the interaction with the gcp project
* **Poetry**
## Usage : 

### Preparation steps :
1 - Clone the repo and delete the content of secrets/iac/* and secrets/k8s/* (your own secrets will be generated)

2 - Init & configure gcloud cli 
```
# if gcloud it's not yet associated to a project, init gcloud & select a project where your want to provision your vms
gcloud init
# Then authorize the lib apis to interact with your GCP project (Pulumi needs this step)
gcloud auth application-default login
```

3 - create a .env at the root dir with following keys and fill values of your own
```
# create a .env with theses values and put your own values
GOOGLE_PROJECT=<YOUR_GCP_PROJECT: example -> gifted-cooler-370220>
GOOGLE_REGION=<YOUR_GCP_REGION: example -> europe-west9>
GOOGLE_ZONE=<YOUR_GCP_ZONE: example -> europe-west9-a>
KUBECONFIG=${PWD}/secrets/k8s/kubeconfig
DOCKER_IMAGE=<DOCKER_IMG_NAME: example -> my-app>
DOCKER_TAG=0.0.0
DOCKER_USERNAMESPACE=<DOCKER_USER_NAME: example -> senhajirhazi>
```
### Step 1 : Provision compute engines
````
# run cmd 
just stack_up 
# this will 
# 1. include .env file as env variables
# 2. install the app dependencies with poetry
# 3. configure pulumi to store the state file locally at <root>/secrets/iac/
# 4. open a prompt with pulumi asking you if you want to provision the infrastructure of 4 linux machines + network (tap yes if you agree)

# At the end you should have an output like this
(your ips will be differents)
Outputs:
    control-plane-instance_ip: "34.155.173.159"
    load-balancer-instance_ip : "34.163.165.22"
    network                   : "default-network"
    worker-1-instance_ip      : "34.155.150.176"
    worker-2-instance_ip      : "34.155.230.196"

Resources:
    + 11 created
````


Usage 
Clone repo
create a .env 
```
GOOGLE_PROJECT=gifted-cooler-370220
GOOGLE_REGION=europe-west9
GOOGLE_ZONE=europe-west9-a
KUBECONFIG=${PWD}/secrets/k8s/kubeconfig
PULUMI_CONFIG_PASSPHRASE=<personal_value>
DOCKER_IMAGE=my-app
DOCKER_TAG=0.0.0
DOCKER_USERNAMESPACE=senhajirhazi
```
### Step 2 : Install the kubernetes cluster

# Dependencies 
‘‘‘
* https://buddy.works/guides/git-crypt
‘‘‘
