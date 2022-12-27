


from pulumi import ResourceOptions
from pulumi_gcp import compute



def prov_network(network_name="default-network"):
    return compute.Network(resource_name=network_name, name=network_name)



#default_network = compute.Network("default-network")
PORTS = [
                "80",
                "22",
                "8080",
                "1000-2000",
                # check necessary ports for kube https://kubernetes.io/docs/reference/networking/ports-and-protocols/
                "6443", #important for api server kubernetes
                "2379-2380",
                "10250",
                "10259",
                "10257",
                "30000-32767",
                "10250"
            ]
def prov_firewall(network, firewall_name="default-firewall", ports=PORTS):
    return compute.Firewall(firewall_name,
    network=network.name,
    name=firewall_name,
    allows=[
        compute.FirewallAllowArgs(
            protocol="icmp",
        ),
        compute.FirewallAllowArgs(
            protocol="tcp",
            ports=ports,
        ),
           compute.FirewallAllowArgs(
            protocol="udp",
        )
    ],
    source_tags=["web"],
    source_ranges=["0.0.0.0/0"],
    )

def prov_address(instance_name):
    return  compute.address.Address(f"address-{instance_name}")


def prov_instance(instance_name, network, firewall, instance_address, machine_type="e2-standard-2"):
    return compute.Instance(
        f"instance-{instance_name}",
        name=instance_name,
        machine_type=machine_type,
        # metadata_startup_script=startup_script,
        boot_disk=compute.InstanceBootDiskArgs(
            initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
                image="debian-cloud/debian-11"
            )
        ),
        network_interfaces=[compute.InstanceNetworkInterfaceArgs(
                network=network.id,
                access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs(
                    nat_ip=instance_address.address
                )],
        )],
        service_account=compute.InstanceServiceAccountArgs(
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        ),
        opts=ResourceOptions(depends_on=[firewall]),
    )