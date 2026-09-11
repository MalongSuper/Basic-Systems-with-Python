# Subnetting - Borrowed Hosts


def borrowed_bits(subnets):
    if subnets < 1:
        raise ValueError("Number of subnets must be at least 1")
    bits = 0
    while 2 ** bits < subnets:
        bits += 1
    return bits


def usable_subnets(subnets, network):
    s = borrowed_bits(subnets)
    if network == 'A':
        prefix = 8
    elif network == 'B':
        prefix = 16
    elif network == 'C':
        prefix = 24
    else:
        raise ValueError("Invalid Class for network, must be A, B, or C")

    cidr = prefix + s
    if cidr > 32:
        raise ValueError("Too many subnets for this class: resulting CIDR exceeds /32")
    return cidr, 2 ** s, 2 ** (32 - cidr) - 2


def main():
    network = str(input("Enter Network Class: ").upper())
    if network not in ['A', 'B', 'C']:
        raise ValueError("Invalid Class for network, must be A, B, or C")

    subnets = int(input("Enter the number of subnets required: "))
    if subnets < 1:
        raise ValueError("Invalid Input for number of subnets as integer")

    print("Borrowed Bits:", borrowed_bits(subnets))
    print("CIDR:", usable_subnets(subnets, network)[0])
    print("Usable number of subnets:", usable_subnets(subnets, network)[1])
    print("Usable number of hosts for each subnet:", usable_subnets(subnets, network)[2])


if __name__ == "__main__":
    main()
