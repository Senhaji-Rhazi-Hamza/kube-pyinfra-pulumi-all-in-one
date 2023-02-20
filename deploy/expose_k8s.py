from pathlib import Path

from pyinfra import host
from pyinfra.facts.server import Home
from pyinfra.operations import files, server

ROOT = Path(__file__).parent.parent

if "controlplanes" in host.groups:
    files.template(
        name="Copy & render the nginx-controller yaml file in the controlpkane",
        src=ROOT / "deploy/assets/k8s/nginx-controller-bare-metal.yaml.j2",
        dest=f"{host.get_fact(Home)}/nginx-controller-bare-metal.yaml",
        http_node_port=30080,
        https_node_port=30443,
        _sudo=True,
    )
    # TODO add a fact to check wether or not to launch this step
    server.shell(
        name="Install the nginx controller using nginx-controller-bare-metal.yaml ",
        commands=[
            f"kubectl apply -f {host.get_fact(Home)}/nginx-controller-bare-metal.yaml",
        ],
    )

    # TODO add a fact to check if the nginx controller is running correctly
