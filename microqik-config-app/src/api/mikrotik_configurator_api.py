from routeros_api import RouterOsApiPool

class MicroTikConfiguratorApi: 
                
    def __init__(self, ip_address, username, password): 
        self.connection = RouterOsApiPool(ip_address, username=username, password=password)
        self.api = self.connection.get_api()

    def __del__(self):
        self.connection.disconnect()

    def login(self, username, password):
        self.api.login(login=username, password=password, plaintext_login='True')

    def disconnect(self):
        self.connection.disconnect()

    def delete_firewall_rules(self):
        rules = self.api.get_resource('/ip/firewall/filter').get()
    
        for rule in rules:
            if rule['id'] != '*C':
                self.api.get_resource('/ip/firewall/filter').remove(id=rule['id'])

    def set_bridge_mode(self):
        # Configure bridge mode
        self.api.get_resource('/interface/bridge').call('add', {
            'name': 'bridge1'})
        self.api.get_resource('/interface/ethernet').call('set', {
            'numbers': '1', 'master-port': 'bridge1'})
        self.api.get_resource('/ip/dhcp-client').call('remove', 
            [x['.id'] for x in self.api.get_binary_resource('/ip/dhcp-client').call('print')])
        self.api.get_resource('/ip/pool').call('remove', 
            [x['.id'] for x in self.api.get_binary_resource('/ip/pool').call('print')])
        self.api.get_resource('/ip/dhcp-server').call('remove', 
            [x['.id'] for x in self.api.get_binary_resource('/ip/dhcp-server').call('print')])
        self.api.get_resource('/ip/address').call('remove', 
            [x['.id'] for x in self.api.get_binary_resource('/ip/address').call('print')])
        self.api.get_resource('/ip/firewall/filter').call('add', {
            'chain': 'forward', 'action': 'accept'})
        self.api.get_resource('/ip/firewall/filter').call('add', {
            'chain': 'input', 'action': 'accept'})

    def set_vlan_900(self):
        # Enable ingress filtering on the bridge
        self.api.get_binary_resource('/interface/bridge').call('set', {
            'numbers': 'bridge1', 'ingress-filtering': 'yes'})

        # Call the VLAN add function
        vlan_params = {'numbers': '900', 'interface': 'bridge1', 'tagged': 'ether1', 'untagged': 'ether4,ether5'}
        response = self.api.get_resource('/interface/vlan').call('add', **vlan_params)

        # set the PVID of ether4 and ether5 to 900
        self.api.get_resource('/interface/ethernet/set').set(params={
            '.id': 'ether4',
            'pvid': '900',
        })
        self.api.get_resource('/interface/ethernet/set').set(params={
            '.id': 'ether5',
            'pvid': '900',
        })

    def set_tcp_firewall_rule(self, chain_type, port_type, port, action_type, comment):

        if port_type == "destination" or port_type == "dst":
            self.api.get_resource('/ip/firewall/filter').call('add', {
                'chain': chain_type,
                'protocol': 'tcp',
                'dst-port': port,
                'action': action_type,
                'comment': comment
            })

        elif port_type == "source" or port_type == "src":
            self.api.get_resource('/ip/firewall/filter').call('add', {
                'chain': chain_type,
                'protocol': 'tcp',
                'src-port': port,
                'action': action_type,
                'comment': comment
            })

    def set_8291_tcp_firewall_rule(self):
    
        self.api.get_resource('/ip/firewall/filter').call('add', {
            'chain': 'input',
            'protocol': 'tcp',
            'dst-port': '8291',
            'action': 'accept',
            'comment': 'WinBox'
        })

    def set_router_identity(self, router_identity):
        self.api.get_resource('/system/identity').call('set', {
            'name': router_identity
        })

    def set_router_password(self, router_password):
        self.api.get_resource('/user').call('set', {
        '.id':'admin',
        'password': router_password
    })

    def set_ip_address_of_interface(self, interface_name, ip_address, network_address, broadcast_address, interface_comment):
        self.api.get_resource('/ip/address').call('add', {
            'interface': interface_name,
            'address': ip_address + '/24',
            'network': network_address,
            'broadcast': broadcast_address,
            'comment': interface_comment
        })

    def set_wan_ip_address(self, ip_address, network_address, broadcast_address):
        self.api.get_resource('/ip/address').call('add', {
            'interface': 'ether1',
            'address': ip_address + '/24',
            'network': network_address,
            'broadcast': broadcast_address,
            'comment': 'WAN static IP address',
        })

    def set_default_gateway(self, default_gateway):
        # set gateway IP address
        self.api.get_resource('/ip/route').call('add', {'dst-address': '0.0.0.0/0', 'gateway': default_gateway})

    def set_dns(self, *dns_servers):

        # declare variable for figuring out the number of arguments passed to the method
        number_of_servers = 0

        # step through number of arguments passed through method
        for dns_server in dns_servers:
            number_of_servers += 1

        # set DNS server
        if number_of_servers == 1:
            self.api.get_resource('/ip').call('dns', {'servers': dns_servers})
        elif number_of_servers == 2:
            self.api.get_resource('/ip').call('dns', {'servers': dns_servers[0] + ', ' + dns_servers[1]})

    def set_wireless_interface(self, interface_id, ssid, wireless_mode, frequency, channel_width, disabled, security_profile):
        self.api.get_resource('/interface/wireless').call('set', {
            '.id': interface_id,
            'ssid': ssid,
            'mode': wireless_mode,
            'frequency': frequency,
            'channel-width': channel_width,
            'disabled': disabled,
            'security-profile': security_profile
        })

    def set_ssid_2ghz(self, ssid_2ghz):
        self.api.get_resource('/interface/wireless').call('set', {
            '.id': 'wlan1',
            'ssid': ssid_2ghz,
            'mode': 'ap-bridge',
            'frequency': 'auto',
            'channel-width': '20mhz',
            'disabled': 'no',
            'security-profile': 'default'
        })

    def set_ssid_5ghz(self, ssid_5ghz):
        self.api.get_resource('/interface/wireless').call('set', {
            '.id': 'wlan2',
            'ssid': ssid_5ghz,
            'mode': 'ap-bridge',
            'frequency': 'auto',
            'channel-width': '20mhz',
            'disabled': 'no',
            'security-profile': 'default'
        })

    def set_ssid_password(self, ssid_password):
        self.api.get_resource('/interface/wireless/security-profiles').call('set', {
            '.id': 'default',
            'mode': 'dynamic-keys',
            'authentication-types': 'wpa2-psk',
            'wpa2-pre-shared-key': ssid_password
    })

    def set_and_run_script(self, script_txt):
        
        with open('script.txt', 'w') as file:
            file.write(script_txt) 

        with open('script.txt', 'r') as file:
            script_txt = file.read()

        self.api.get_resource('/system/script').call('add', {
            'source': script_txt
        })

        self.api.get_resource('/system/script').call('run', {
            'number': '0'
        })
    
    def set_script(self, script_txt):
        
        with open('script.txt', 'w') as file:
            file.write(script_txt) 

        with open('script.txt', 'r') as file:
            script_txt = file.read()

        self.api.get_resource('/system/script').call('add', {
            'source': script_txt
        })

    def run_script(self, script_id):
        self.api.get_resource('/system/script').call('run', { 
            'number': script_id
        })
