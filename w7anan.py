import re
import sys

def validate_ip(ip):
    """Validate IP address format."""
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    
    if not match:
        return False

    for octet in match.groups():
        if not 0 <= int(octet) <= 255:
            return False
    return True

def validate_subnet_mask(mask):
    """Validasi subnett yang benar!"""

    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, mask)
    
    if not match:
        return False

    binary = ""
    for octet in match.groups():
        if not 0 <= int(octet) <= 255:
            return False
        binary += format(int(octet), '08b')

    if '01' in binary:
        return False
    
    return True

def get_ip_class(first_octet):
    """Determine IP address class."""
    if 1 <= first_octet <= 126:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "E (Eksperimental)"
    else:
        return "Tidak Valid"

def get_default_subnet_mask(ip_class):
    """Get default subnet mask based on IP class."""
    if ip_class == "A":
        return "255.0.0.0"
    elif ip_class == "B":
        return "255.255.0.0"
    elif ip_class == "C":
        return "255.255.255.0"
    else:
        return "N/A"

def get_ip_type(ip_octets):
    """Determine if IP address is private or public."""
    first, second, third, fourth = ip_octets
    
    if first == 10:
        return "Privat"
 
    elif first == 172 and 16 <= second <= 31:
        return "Privat"

    elif first == 192 and second == 168:
        return "Privat"

    elif first == 127:
        return "Loopback"
 
    elif first == 169 and second == 254:
        return "Link-local"
    # Reserved for documentation
    elif (first == 192 and second == 0 and third == 2) or \
         (first == 198 and second == 51 and third == 100) or \
         (first == 203 and second == 0 and third == 113):
        return "Direservasi untuk dokumentasi"
    else:
        return "Publik"

def get_network_address(ip_octets, mask_octets):
    """Calculate network address."""
    network_octets = [ip_octets[i] & mask_octets[i] for i in range(4)]
    return '.'.join(map(str, network_octets))

def count_subnet_mask_bits(subnet_mask):
    """Count the number of '1' bits in the subnet mask."""
    binary = ""
    for octet in subnet_mask:
        binary += format(octet, '08b')
    return binary.count('1')

def calculate_subnet_info(ip_address, subnet_mask):
    """Calculate all required subnet information."""
    if not validate_ip(ip_address) or not validate_subnet_mask(subnet_mask):
        return "Alamat IP atau subnet mask tidak valid!"
    
    # Parse IP and subnet mask
    ip_octets = list(map(int, ip_address.split('.')))
    mask_octets = list(map(int, subnet_mask.split('.')))
    
    # Get IP class
    ip_class = get_ip_class(ip_octets[0])
    
    # Get IP type (private/public)
    ip_type = get_ip_type(ip_octets)
    
    # Get default subnet mask
    default_mask = get_default_subnet_mask(ip_class)
    
    # Calculate network address
    network_address = get_network_address(ip_octets, mask_octets)
    
    # Calculate number of subnet mask bits
    subnet_mask_bits = count_subnet_mask_bits(mask_octets)
    
    # Calculate bits borrowed
    default_mask_bits = count_subnet_mask_bits(list(map(int, default_mask.split('.'))))
    borrowed_bits = subnet_mask_bits - default_mask_bits
    
    # Calculate total subnets
    if borrowed_bits >= 0:
        total_subnets = 2 ** borrowed_bits
    else:
        total_subnets = "N/A"
    
    # Calculate host addresses
    total_host_addresses = 2 ** (32 - subnet_mask_bits)
    usable_host_addresses = max(0, total_host_addresses - 2)  # Subtract network and broadcast addresses
    
    return {
        "Kelas": ip_class,
        "Tipe": ip_type,
        "Alamat Jaringan": network_address,
        "Subnet Mask Default": default_mask,
        "Jumlah Bit yang Dipinjam": borrowed_bits if borrowed_bits >= 0 else "N/A",
        "Total Jumlah Subnet": total_subnets,
        "Total Jumlah Alamat Host": total_host_addresses,
        "Jumlah Alamat yang Dapat Digunakan": usable_host_addresses
    }

def main():
    print("Kalkulator Alamat IP dan Subnet")
    print("--------------------------------")
    
    while True:
        ip_address = input("Masukkan Alamat IP (contoh: 192.168.1.1): ")
        if not validate_ip(ip_address):
            print("Format alamat IP tidak valid! Silakan coba lagi.")
            continue
        
        subnet_mask = input("Masukkan Subnet Mask (contoh: 255.255.255.0): ")
        if not validate_subnet_mask(subnet_mask):
            print("Subnet mask tidak valid! Silakan coba lagi.")
            continue
        
        result = calculate_subnet_info(ip_address, subnet_mask)
        
        if isinstance(result, str):
            print(result)
        else:
            print("\nHasil:")
            print("-" * 40)
            for key, value in result.items():
                print(f"{key}: {value}")
        
        again = input("\nHitung lagi? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    main()