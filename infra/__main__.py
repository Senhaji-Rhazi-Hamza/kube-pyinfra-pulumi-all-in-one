import pulumi

from helper import prov_firewall, prov_network, prov_instance, prov_address

MACHINE_NAMES = ["control-plane", "worker-1", "worker-2", "load-balancer"]

network = prov_network(network_name="default-network")
firewall = prov_firewall(network=network, firewall_name="default-firewall")



for instance_name in MACHINE_NAMES:
    instance_address = prov_address(instance_name=instance_name)
    compute_instance = prov_instance(instance_name=instance_name, network=network, firewall=firewall, instance_address=instance_address, machine_type="e2-standard-2")
    pulumi.export(f"{instance_name}-instance_ip", instance_address.address)

pulumi.export("network", network.name)