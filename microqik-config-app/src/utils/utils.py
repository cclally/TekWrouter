import re

def validate_ip_address(ip_address):
    # Regular expression pattern to match an IPv4 address
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    
    if re.match(pattern, ip_address):
        # Split the IP address into its component octets
        octets = ip_address.split('.')
        
        # Check that each octet is a number between 0 and 255
        for octet in octets:
            if int(octet) < 0 or int(octet) > 255:
                return False
        
        return True
    else:
        return False
    
def get_network_address_24_cidr(ip_address):
    # split the IP address into components of octets
    octets = ip_address.split(".")
    # bind variable of network address of a /24 IP
    network_address = ".".join(octets[:3]) + ".0"
    return network_address

def get_broadcast_address_24_cidr(ip_address):
    # split the IP address into components of octets
    octets = ip_address.split(".")
    # bind variable of broadcast address of a /24 IP
    broadcast_add = ".".join(octets[:3]) + ".255"
