import struct
import socket

def calculate_udp_checksum(ip_src, ip_dst, udp_src_port, udp_dst_port, data):
    # Konversi IP address menjadi format biner
    src_ip = socket.inet_aton(ip_src)
    dst_ip = socket.inet_aton(ip_dst)

    # Header Pseudo
    pseudo_header = src_ip + dst_ip + struct.pack('!BBH', 0, socket.IPPROTO_UDP, len(data) + 8)

    # Header UDP
    udp_header = struct.pack('!HHHH', udp_src_port, udp_dst_port, len(data) + 8, 0)

    # Gabungkan pseudo header, UDP header, dan data
    packet = pseudo_header + udp_header + data

    # Jika panjang paket ganjil, tambahkan padding byte
    if len(packet) % 2 != 0:
        packet += b'\x00'

    # Hitung checksum
    checksum = 0
    for i in range(0, len(packet), 2):
        word = (packet[i] << 8) + packet[i + 1]
        checksum += word
        while checksum > 0xFFFF:
            checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # Komplement checksum
    checksum = ~checksum & 0xFFFF
    return checksum

# Fungsi untuk menjalankan tes def calculate_udp_checksum
if __name__ == "__main__":
    test_cases = [
        ("192.168.1.1", "192.168.1.2", 12345, 80, b"Hello, UDP!"),
        ("10.0.0.1", "10.0.0.2", 5000, 8080, b"Test UDP Checksum"),
        ("172.16.100.5", "172.16.200.10", 53, 53, b"A" * 512),
        ("192.168.100.1", "192.168.100.2", 4000, 1234, b""),
        ("192.168.50.10", "192.168.50.20", 9999, 5555, bytes.fromhex("00 01 02 03 04 05 06 07 08 09"))
    ]

    for i, (src, dst, src_port, dst_port, data) in enumerate(test_cases, 1):
        checksum = calculate_udp_checksum(src, dst, src_port, dst_port, data)
        print(f"Test {i}:")
        print(f"  IP Source: {src}")
        print(f"  IP Destination: {dst}")
        print(f"  UDP Port Source: {src_port}")
        print(f"  UDP Port Destination: {dst_port}")
        print(f"  Data: {data}")
        print(f"  Checksum: {hex(checksum)}\n")
