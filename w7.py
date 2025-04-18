import ipaddress

def get_ip_input():
    ip_input = input("Masukkan IP Address: ").strip()
    mask_input = input("Masukkan Subnet Mask: ").strip()
    return ip_input, mask_input

def validate_ip(ip_str):
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except:
        return False

def validate_netmask(mask_str):
    try:
        ipaddress.IPv4Network(f"0.0.0.0/{mask_str}")
        return True
    except:
        return False

def get_ip_class(ip):
    first_octet = int(str(ip).split('.')[0])
    if 1 <= first_octet <= 126:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "E (Experimental)"
    else:
        return "Tidak ada"

def get_default_prefix(ip_class):
    return {"A": 8, "B": 16, "C": 24}.get(ip_class, 0)

def analyze_ip(ip_str, subnet_mask_str):
    if not validate_ip(ip_str):
        return {"error": "IP Address tidak valid"}
    if not validate_netmask(subnet_mask_str):
        return {"error": "subnet mask tidak valid"}

    netmask = ipaddress.IPv4Network(f'0.0.0.0/{subnet_mask_str}').prefixlen
    network = ipaddress.IPv4Network(f'{ip_str}/{netmask}', strict=False)

    ip = ipaddress.IPv4Address(ip_str)
    ip_class = get_ip_class(ip)
    ip_type = "Public IP"
    if ip.is_private:
        ip_type = "Private IP"

    default_prefix = get_default_prefix(ip_class)
    bits_borrowed = netmask - default_prefix
    total_subnets = 2 ** bits_borrowed if bits_borrowed >= 0 else 0
    total_hosts = 2 ** (32 - netmask)
    usable_hosts = max(0, total_hosts - 2)

    return {
        "Class": ip_class,
        "Type": ip_type,
        "Network Address": str(network.network_address),
        "Default subnet mask": str(ipaddress.IPv4Network(f'0.0.0.0/{default_prefix}').netmask),
        "Bits borrowed": bits_borrowed,
        "Total number of subnets": total_subnets,
        "Total number of host addresses": total_hosts,
        "Total number of usable host addresses": usable_hosts
    }

if __name__ == "__main__":
    ip_input, mask_input = get_ip_input()
    result = analyze_ip(ip_input, mask_input)

    print()
    for key, value in result.items():
        print(f"{key}: {value}")