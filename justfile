# behold a recipe
fun:
  echo "hi" > tmp.txt
  cat tmp.txt
  rm tmp.txt

local_state:
  pulumi login file:///$(pwd)/secrets/iac

init_infra_stack: local_state
  pulumi --cwd infra up --stack dev


install_kube_deps_on_nodes:
  pyinfra deploy/inventory.py deploy/main.py

install_kube: install_kube_deps_on_nodes

git_add_update:
  git add -u

commit message: git_add_update
  git commit -m "{{message}}"

ammend:
  git commit --amend --no-edit
