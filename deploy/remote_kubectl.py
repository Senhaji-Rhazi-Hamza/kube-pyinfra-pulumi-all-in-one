import yaml

from pyinfra.operations import server, python
from pyinfra.facts.server import Home


from pyinfra import host


if "controlplanes" in host.groups:

    def callback():
        result = server.shell(
            name="kubeamd",
            commands=[
                "kubectl -n kube-system get configmap kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > kubeadm.yaml",
                "cat kubeadm.yaml",
            ],
        )
        kubeadm_yaml_dict = yaml.safe_load(result.stdout)
        kubeadm_yaml_dict["apiServer"] = {
            "certSANs": [host.connection.get_transport().getpeername()[0]]
        }

        server.shell(
            _sudo=True,
            name="Modify kubeadm config & generate new certificats to allow reach from outside",
            commands=[
                "mv /etc/kubernetes/pki/apiserver.crt "
                + f"{host.get_fact(Home)}/apiserver.crt",
                "mv /etc/kubernetes/pki/apiserver.key "
                + f"{host.get_fact(Home)}/apiserver.key",
                f"echo '{yaml.dump(kubeadm_yaml_dict)}' > kubeadm.yaml",
                "kubeadm init phase certs apiserver --config kubeadm.yaml",
            ],
        )
        server.shell(
            name="Delete pod kube-apiserver to force restart with new config",
            commands=[
                "kubectl delete pods -n kube-system -l 'component=kube-apiserver,tier=control-plane'"
            ],
        )

    python.call(
        name="Execute callback function",
        function=callback,
    )
