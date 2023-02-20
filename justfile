# define build_docker_image
# 	docker image build --rm -t $(1):$(2) -f $(3) .
# 	docker tag $(1):$(2) $(1):latest
# endef


set dotenv-load := true


clean:
  find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
# This command aims to
install-python-dependencies:
  poetry install
  poetry config virtualenvs.in-project true --local

ssh-docker:
  docker exec -it my-apo /bin/bash

build-image:
  docker image build --rm -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f Dockerfile .
  docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USERNAMESPACE}/${DOCKER_IMAGE}:latest
  docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USERNAMESPACE}/${DOCKER_IMAGE}:${DOCKER_TAG}

  

kube-debug:
  kubectl run -i --rm --tty debug --image=johnajimenez/busyboxplus  --restart=Never -- sh


local_state:
  pulumi login file:///$(pwd)/secrets/iac

stack_up: local_state install-python-dependencies
  pulumi --cwd infra up --stack dev

stack_output:
  pulumi stack -s dev output

install_kube_deps_on_nodes:
  poetry run pyinfra deploy/inventory.py deploy/main.py

join_workers:
  poetry run pyinfra deploy/inventory.py deploy/join_workers.py

configure_loadbalancer:
  poetry run pyinfra deploy/inventory.py deploy/loadbalancer.py

configure_nginx_controller:
  poetry run pyinfra deploy/inventory.py deploy/expose_k8s.py 
  
reg_certs_kubeadm:
  poetry run pyinfra deploy/inventory.py deploy/remote_kubectl.py  --limit controlplanes


install_kube: install_kube_deps_on_nodes join_workers

git_add_update:
  git add -u

commit message: git_add_update
  git commit -m "{{message}}"

ammend:
  git commit --amend --no-edit
