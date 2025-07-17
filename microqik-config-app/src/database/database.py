import sqlite3

'''

  ** Not currently implemented in the application itself. **
** Future plans to recall configurations for users routers. **

  MikroTik Database module for storing router configurations
'''


class MikroTikDB:

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def __del__(self):
        self.cursor.execute("DROP TABLE mikrotik_config")
        self.connection.close()

    def create_table(self):
        # If table doesn't exist create a new table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mikrotik_config (
                id INTEGER PRIMARY KEY,
                ip_address TINYTEXT,
                gateway_address TINYTEXT,
                broadcast_address TINYTEXT,
                network_address TINYTEXT,
                router_username TINYTEXT,
                router_password TINYTEXT,
                router_identity TINYTEXT,
                ssid_2g TINYTEXT,
                ssid_5g TINYTEXT,
                ssid_password TINYTEXT,
                remote_winbox_script LONGTEXT
                )
        ''')
        
        self.connection.commit()

    def insert_mikrotik_config(self, mikrotik_config):
        # store data into mikrotik_config table
        self.cursor.execute(''' 
            INSERT INTO mikrotik_config (
                id, ip_address, gateway_address, broadcast_address, 
                network_address, router_username, router_password_hash, 
                router_identity, ssid_2g, ssid_5g, ssid_password, 
                remote_winbox_script
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (mikrotik_config['id'], mikrotik_config['ip_address'], mikrotik_config['gateway_address'], 
            mikrotik_config['broadcast_address'], mikrotik_config['network_address'], mikrotik_config['router_username'], 
            mikrotik_config['router_password_hash'], mikrotik_config['router_identity'], mikrotik_config['ssid_2g'], 
            mikrotik_config['ssid_5g'], mikrotik_config['ssid_password'], mikrotik_config['remote_winbox_script']))

        self.connection.commit()
    
    def update_mikrotik_config_rwb_script(self, mikrotik_config):
        # update remote winbox script in the mikrotik_config table
        self.cursor.execute(''' 
            UPDATE mikrotik_config SET remote_winbox_script = ? WHERE id = ?
            ''', (mikrotik_config['remote_winbox_script'], mikrotik_config['id']))

        self.connection.commit()

    def get_mikrotik_config_ip_address(self, mikrotik_config_id):
        # select ip address in the mikrotik_config table
        self.cursor.execute("SELECT ip_address FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the ip address
        result = self.cursor.fetchone()

        return result
    
    def get_mikrotik_config_gateway_address(self, mikrotik_config_id):
        # select gateway address in the mikrotik_config table
        self.cursor.execute("SELECT gateway_address FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the gateway address
        result = self.cursor.fetchone()

        return result
    
    def get_mikrotik_config_broadcast_address(self, mikrotik_config_id):
        # select broadcast address in the mikrotik_config table
        self.cursor.execute("SELECT broadcast_address FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the broadcast address
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_network_address(self, mikrotik_config_id):
        # select network address in the mikrotik_config table
        self.cursor.execute("SELECT network_address FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the network address
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_router_username(self, mikrotik_config_id):
        # select router username in the mikrotik_config table
        self.cursor.execute("SELECT router_username FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the router_username
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_router_password_hash(self, mikrotik_config_id):
        # select router password hash in the mikrotik_config table
        self.cursor.execute("SELECT router_password_hash FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the router_password_hash
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_router_identity(self, mikrotik_config_id):
        # select router identity in the mikrotik_config table
        self.cursor.execute("SELECT router_identity FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the router identity
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_ssid_2g(self, mikrotik_config_id):
        # select ssid 2.4ghz band in the mikrotik_config table
        self.cursor.execute("SELECT ssid_2g FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the ssid 2.4ghz band
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_ssid_5g(self, mikrotik_config_id):
        # select ssid 5ghz band in the mikrotik_config table
        self.cursor.execute("SELECT ssid_5g FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the ssid 5ghz band
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_ssid_password(self, mikrotik_config_id):
        # select ssid password in the mikrotik_config table
        self.cursor.execute("SELECT ssid_password FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the ssid password
        result = self.cursor.fetchone()

        return result

def get_mikrotik_config_remote_winbox_script(self, mikrotik_config_id):
        # select remote winbox script in the mikrotik_config table
        self.cursor.execute("SELECT remote_winbox_script FROM mikrotik_config WHERE id = ?", (mikrotik_config_id))

        self.connection.commit()
        # retrieve the remote winbox script
        result = self.cursor.fetchone()

        return result
