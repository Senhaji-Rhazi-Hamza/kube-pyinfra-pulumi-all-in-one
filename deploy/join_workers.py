from pathlib import Path

from pyinfra import host
from pyinfra.operations import server


ROOT = Path(__file__).parent.parent

with open(ROOT / "secrets/k8s/join_cmd.txt", "r") as f:
    join_cmd = f.read()



if "workers" in host.groups:
    # TODO shoul check if the workers are already joined or not
    server.shell(
        _sudo=True,
        name="join node",
        commands=[f"{join_cmd}"]
    )