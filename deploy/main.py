from pathlib import Path

from pyinfra import host
from pyinfra import local
from pyinfra.operations import server, apt, python, files
from pyinfra.facts.server import User, Home
from deploy.facts.k8s_facts import K8sInitialized


ROOT = Path(__file__).parent.parent

if "workers" in host.groups or "controlplanes" in host.groups:
    apt.packages(
        update=True,
        name="Ensure packages installed",
        packages=["curl", "wget", "ca-certificates", "apt-transport-https"],
        _sudo=True,
    )

    local.include((ROOT / "deploy/tasks/install_docker.py").as_posix())

    server.shell(
        name="Add apt repository for kube binaries",
        commands=[
            "sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg",
            "echo 'deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee /etc/apt/sources.list.d/kubernetes.list",
        ],
        _sudo=True,
    )

    apt.packages(
        update=True,
        force=True,
        name="Ensure packages installed (kubelet, kubeadm)",
        packages=["kubelet=1.22.4-00", "kubeadm=1.22.4-00"],
        _sudo=True,
    )

if "controlplanes" in host.groups:
    apt.packages(
        update=True,
        force=True,
        name="Ensure packages installed (kubectl)",
        packages=["kubectl=1.22.4-00"],
        _sudo=True,
    )

    if not host.get_fact(K8sInitialized):
        server.shell(
            _sudo=True,
            name="Initialize cluster if not",
            commands=[
                "cd",
                "kubeadm init --pod-network-cidr=10.244.0.0/16 >> cluster_initialized.txt ",
            ],
        )
        server.shell(
            _sudo=True,
            name="Allow user to use kubectl conf withoutsudo",
            commands=[
                f"mkdir -p {host.get_fact(Home)}/.kube",
                f"cp  /etc/kubernetes/admin.conf {host.get_fact(Home)}/.kube/config",
                f"chown $(id -u):$(id -g) {host.get_fact(Home)}/.kube/config",
            ],
        )
        files.file(
            _sudo=True, path=host.get_fact(Home) + "/.kube/config", mode=777, force=True
        )
        files.get(
            name="Download a file from a remote",
            src=host.get_fact(Home) + "/.kube/config",
            dest=(ROOT / "secrets/k8s/kubeconfig").as_posix(),
            force=True,
            _sudo=True,
        )

    server.shell(
        name="Install pod network",
        commands=[
            "cd",
            "kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml > pod_network_setup.txt",
        ],
    )

    def callback():
        if "controlplanes" in host.groups:
            result = server.shell(
                name="Generate token cmd",
                _sudo=True,
                commands=[
                    "kubeadm token create --print-join-command  > token.txt",
                    "cat token.txt && rm token.txt",
                ],
            )

            with open(ROOT / "secrets/k8s/join_cmd.txt", "w") as f:
                f.write(result.stdout)

    python.call(
        name="Execute callback function",
        function=callback,
    )
