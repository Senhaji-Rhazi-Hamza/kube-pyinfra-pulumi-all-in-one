from pathlib import Path

from pyinfra import host
from pyinfra import local
from pyinfra.operations import server, apt, python
from deploy.facts.k8s_facts import K8sInitialized


ROOT = Path(__file__).parent.parent

if "workers" in host.groups or "controlplanes" in host.groups:
    apt.packages(
        update=True,
        name="Ensure packages installed",
        packages=["curl"],
        _sudo=True,  # use sudo when installing the packages
    )


    local.include((ROOT / "deploy/tasks/install_docker.py").as_posix())


    server.shell(
        name="Add apt repository for kube binaries",
        commands=[
            "curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg",
            'echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list',
        ],
        _sudo=True,  # use sudo when installing the packages
    )


    apt.packages(
        update=True,
        force=True,
        name="Ensure packages installed (kubelet, kubeadm)",
        packages=["kubelet=1.22.4-00", "kubeadm=1.22.4-00"],
        _sudo=True,  # useudo when installing the packages
    )

if "controlplanes" in host.groups:
    apt.packages(
        update=True,
        force=True,
        name="Ensure packages installed (kubectl)",
        packages=["kubectl=1.22.4-00"],
        _sudo=True,  # useudo when installing the packages
    )

    if not host.get_fact(K8sInitialized):

        server.shell(
            _sudo=True,
            name="initialize cluster if not",
            commands=[
                "cd",
                "kubeadm init --pod-network-cidr=10.244.0.0/16 >> cluster_initialized.txt ",
            ],
        )

        server.shell(
            _sudo=True,
            name="install pod network",
            commands=[
                "cd",
                "kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml >> pod_network_setup.txt",
            ],
        )

        server.shell(
            _sudo=True,
            name="allow user to use kubectl conf withoutsudo",
            commands=[
                "mkdir -p $HOME/.kube",
                "sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config",
                "sudo chown $(id -u):$(id -g) $HOME/.kube/config",
            ],
        )

    def callback():

        if "controlplanes" in host.groups:
            result = server.shell(
                name="generate token cmd",
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




# from pyinfra.operations import python, server

# def callback():
#     result = server.shell(
#         commands=["echo output"],
#     )

#     logger.info(f"Got result: {result.stdout}")

# python.call(
#     name="Execute callback function",
#     function=callback,
# )
