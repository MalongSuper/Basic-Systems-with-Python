# Network of IP Addresses - Subnetting
from ipaddress import IPv4Network
from math import log2


def get_required_hosts(hosts):
    # Minimum block size is 2^2, then 2^3, 2^4, ...
    required_hosts = []
    for host in hosts.values():
        size = 4
        while size <= host:
            size *= 2
            if size > 2 ** 32:
                raise ValueError(f"Host requirement {host} is too large")
        required_hosts.append(size)
    return required_hosts


def get_cidr(required_hosts):
    return [32 - int(log2(hosts)) for hosts in required_hosts]


def subnetting_plan(network, hosts):
    # Optional: Sort the subnets in descending order
    # Prioritize the one with the largest required hosts
    required_hosts = get_required_hosts(hosts)
    cidr = get_cidr(required_hosts)
    current_address = network.network_address
    results = []
    for c, name, block in zip(cidr, hosts, required_hosts):
        subnet = IPv4Network(f"{current_address}/{c}", strict=False)
        network_addr = subnet.network_address
        broadcast_addr = subnet.network_address + (2 ** (32 - c) - 1)
        first_addr, last_addr = network_addr + 1, broadcast_addr - 1
        results.append({
            "name": name,
            "requested_hosts": hosts[name],
            "block_size": block,
            "cidr": c,
            "network": str(network_addr),
            "broadcast": str(broadcast_addr),
            "first": str(first_addr),
            "last": str(last_addr),
            "usable": (2 ** (32 - c)) - 2,
        })
        current_address = last_addr + 2
    return results


def subnetting(network, hosts):
    for row in subnetting_plan(network, hosts):
        print(f"{row['name']}: {row['first']} - {row['last']}")


def main():
    print("+ Example 1")
    network = IPv4Network("192.168.10.0/24")
    hosts = {"Network A": 60, "Network B": 30,
             "Network C": 14, "Network D": 6}
    subnetting(network, hosts)
    print("+ Example 2")
    network = IPv4Network("172.16.0.0/20")
    hosts = {"Network A": 400, "Network B": 200,
             "Network C": 100, "Network D": 50,
             "Network E": 25}
    subnetting(network, hosts)


if __name__ == "__main__":
    main()
