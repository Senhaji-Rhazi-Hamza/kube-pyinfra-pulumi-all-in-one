# behold a recipe
fun:
  echo "hi" > tmp.txt
  cat tmp.txt
  rm tmp.txt

set dotenv-load := true

# This command aims to
install-python-dependencies:
  poetry install 
  poetry config virtualenvs.in-project true --local

kube-debug:
  kubectl run -i --rm --tty debug --image=busybox --restart=Never -- sh
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

install_kube: install_kube_deps_on_nodes join_workers

git_add_update:
  git add -u

commit message: git_add_update
  git commit -m "{{message}}"

ammend:
  git commit --amend --no-edit
