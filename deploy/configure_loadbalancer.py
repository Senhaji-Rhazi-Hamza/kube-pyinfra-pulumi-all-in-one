from pathlib import Path

from pyinfra import host
from pyinfra import inventory
from pyinfra.operations import systemd, apt, files

ROOT = Path(__file__).parent.parent

if "loadbalancers" in host.groups:
    apt.packages(
        update=True,
        force=True,
        name="Ensure nginx package installed",
        packages=["nginx"],
        _sudo=True,
    )

    files.template(
        name="Copy and render config nginx for loadbalancer",
        src=ROOT / "deploy/assets/nginx/default.conf.j2",
        dest="/etc/nginx/nginx.conf",
        workers_ips=inventory.groups["workers"],
        _sudo=True,
    )

    systemd.service(
        service="nginx",
        running=True,
        reloaded=True,
        _sudo=True,
    )
