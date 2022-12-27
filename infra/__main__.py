import pulumi
from helper import prov_firewall, prov_network, prov_instance, prov_address

MACHINE_NAMES = ["controle-plane", "worker-1", "worker-2", "load-balancer"]

network = prov_network(network_name="default-network")
firewall = prov_firewall(network=network, firewall_name="default-firewall")



for instance_name in MACHINE_NAMES:
    instance_address = prov_address(instance_name=instance_name)
    compute_instance = prov_instance(instance_name=instance_name, network=network, firewall=firewall, instance_address=instance_address, machine_type="e2-standard-2")
    pulumi.export(f"{instance_name}-instance_ip", instance_address.address)

pulumi.export("network", network.name)
# compute_network = compute.Network(
#     "network",
#     auto_create_subnetworks=True,
# )

# compute_firewall = compute.Firewall(
#     "firewall",
#     network=compute_network.self_link,
#     allows=[compute.FirewallAllowArgs(
#         protocol="tcp",
#         ports=["22", "80"],
#     )],
#     source_tags=["my-network"]
# )

# default_network = compute.Network("default-network")
# default_firewall = compute.Firewall("default-firewall",
#     network=default_network.name,
#     allows=[
#         compute.FirewallAllowArgs(
#             protocol="icmp",
#         ),
#         compute.FirewallAllowArgs(
#             protocol="tcp",
#             ports=[
#                 "80",
#                 "22",
#                 "8080",
#                 "1000-2000",
#             ],
#         ),
#     ],
#     source_tags=["web"],
#     source_ranges=["0.0.0.0/0"],
#     )
# for instance_name in ["worker1", "worker2", "master"]:print(instance_name)
# # A simple bash script that will run when the webserver is initalized
# startup_script = """#!/bin/bash
# echo "Hello, World!" > index.html
# nohup python -m SimpleHTTPServer 80 &"""

# instance_addr = compute.address.Address(
#     "address")
# compute_instance = compute.Instance(
#     "instance",
#     name="worker",
#     machine_type="e2-medium",
#     metadata_startup_script=startup_script,
#     boot_disk=compute.InstanceBootDiskArgs(
#         initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
#             image="debian-cloud/debian-11"
#         )
#     ),
#     network_interfaces=[compute.InstanceNetworkInterfaceArgs(
#             network=default_network.id,
#             access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs(
#                 nat_ip=instance_addr.address
#             )],
#     )],
#     service_account=compute.InstanceServiceAccountArgs(
#         scopes=["https://www.googleapis.com/auth/cloud-platform"],
#     ),
#     opts=ResourceOptions(depends_on=[default_firewall]),
# )

# pulumi.export("instanceName", compute_instance.name)
# pulumi.export("instanceIP", instance_addr.address)
