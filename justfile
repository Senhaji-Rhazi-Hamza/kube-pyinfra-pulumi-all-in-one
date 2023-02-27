set dotenv-load := true


# Clean python dependencies
clean: 
  find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
# Install python dependencies
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
# Provision the infrastructure with pulumi
stack_up: local_state install-python-dependencies
  pulumi --cwd infra up --stack dev
# Destroy the infrastructure with pulumi
stack_destroy:
  pulumi --cwd infra destroy --stack dev -y
  pulumi --cwd infra stack rm dev     

# Print output stack
stack_output:
  pulumi stack -s dev output

install_kube_deps_on_nodes:
  poetry run pyinfra deploy/inventory.py deploy/main.py

# Add workers to the kubernetes cluster
join_workers:
  poetry run pyinfra deploy/inventory.py deploy/join_workers.py

# Configure an nginx on a server as a loadbalancer
configure_loadbalancer:
  poetry run pyinfra deploy/inventory.py deploy/configure_loadbalancer.py

# Deploy the ingress nginx controller 
deploy_nginx_ingress_controller:
  poetry run pyinfra deploy/inventory.py deploy/deploy_ingress_controller.py 


expose_k8s: deploy_nginx_ingress_controller configure_loadbalancer

# Make kubectl works from your local machine 
configure_remote_kubectl:
  poetry run pyinfra deploy/inventory.py deploy/remote_kubectl.py  --limit controlplanes

install_kube_fully: install_kube_deps_on_nodes join_workers configure_remote_kubectl expose_k8s 

git_add_update:
  git add -u

commit message: git_add_update
  git commit -m "{{message}}"

ammend:
  git commit --amend --no-edit
