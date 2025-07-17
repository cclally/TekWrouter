import tkinter
import customtkinter
import routeros_api

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")


root = customtkinter.CTk()
root.geometry(f"{1100}x{580}")

root.title("TekWrouter.exe")

IP_Add_txt = ""
gateway_txt = ""
ssid_txt = ""
ssid5_txt = ""
ssid_pass_txt = ""
router_name_txt = ""
router_pass_txt = ""
network_add = ""
broadcast_add = ""
script_txt = ""


routerConnection = routeros_api.RouterOsApiPool('192.168.88.1', username='admin', password='', plaintext_login=True).get_api()

def doBaseRouterConfig():
    routerConnection.get_resource('/').call('system/identity/set', {
        'name': router_name_entry.get()
    })
    rules = routerConnection.get_resource('/ip/firewall/filter').get()
    
    for rule in rules:
        if rule['id'] != '*C':
            routerConnection.get_resource('/ip/firewall/filter').remove(id=rule['id'])

    routerConnection.get_resource('/').call('ip/firewall/filter/add', {
        'chain': 'input',
        'protocol': 'tcp',
        'dst-port': '8291',
        'action': 'accept',
        'comment': 'WinBox'
    })
    octets = address_entry.get().split(".")

    network_add = ".".join(octets[:3]) + ".0"
    broadcast_add = ".".join(octets[:3]) + ".255"

    if radio_var.get() == 1:
        routerConnection.get_resource('/').call('ip/address/add', {
        'interface': 'ether1',
        'address': address_entry.get() + '/24',
        'network': network_add,
        'broadcast': broadcast_add,
        'comment': 'WAN static IP address',
        })
    
    # set gateway IP address
    routerConnection.get_resource('/ip/route').call('add', {'dst-address': '0.0.0.0/0', 'gateway': gateway_entry.get()})

    # set DNS servers
    routerConnection.get_resource('/').call('ip/dns', {'servers': '23.151.80.5, 23.151.80.6'})

    routerConnection.get_resource('/').call('interface/wireless/set', {
        '.id': 'wlan1',
        'ssid': ssid_2_entry.get(),
        'mode': 'ap-bridge',
        'frequency': 'auto',
        'channel-width': '20mhz',
        'disabled': 'no',
        'security-profile': 'default',
    })
    routerConnection.get_resource('/').call('interface/wireless/set', {
        '.id': 'wlan2',
        'ssid': ssid_5_entry.get(),
        'mode': 'ap-bridge',
        'frequency': 'auto',
        'channel-width': '20mhz',
        'disabled': 'no',
        'security-profile': 'default',
    })
    routerConnection.get_resource('/').call('interface/wireless/security-profiles/set', {
        '.id': 'default',
        'mode': 'dynamic-keys',
        'authentication-types': 'wpa2-psk',
        'wpa2-pre-shared-key': ssid_pass_entry.get()
    })

def finishRouterConfig(router_pass, script_txt):
    #routerConnection.get_binary_resource('/').call('new_terminal/terminal')
    with open('script.txt', 'w') as file:
        file.write(script_txt) 

    with open('script.txt', 'r') as file:
        script_txt = file.read()

    routerConnection.get_resource('/').call('system/script/add', {
        'source': script_txt
    })

    routerConnection.get_resource('/').call('system/script/run', {
        'number': '0'
    })
    
    routerConnection.get_resource('/').call('user/set', {
        '.id':'admin',
        'password': router_pass
    })

def finished_config(router_pass):
    script_txt = script_tb.get("1.0", "end-1c")
    

    frame3.destroy()
    frame4.pack(padx=20, pady=20)
    
    finishRouterConfig(router_pass, script_txt)
    label = customtkinter.CTkLabel(master=frame4, text="config complete!")
    label.pack(padx=10, pady=10)


def remote_winbox_config():

    IP_Add_txt = address_entry.get()
    gateway_txt = gateway_entry.get()
    ssid_txt = ssid_2_entry.get()
    ssid5_txt = ssid_5_entry.get()
    ssid_pass_txt = ssid_pass_entry.get()
    router_name_txt = router_name_entry.get()
    router_pass_txt = router_pass_entry.get()
    octets = IP_Add_txt.split(".")

    network_add = ".".join(octets[:3]) + ".0"
    broadcast_add = ".".join(octets[:3]) + ".255"

    doBaseRouterConfig()

    frame2.destroy()

    frame3.pack(padx=20, pady=20)
    label = customtkinter.CTkLabel(master=frame3, text="Paste your remote winbox script:")
    label.pack(padx=10, pady=10)

    script_tb.pack(padx=10, pady=10)
    button = customtkinter.CTkButton(master=frame3, text="Finish config", command=lambda: finished_config(router_pass_txt))
    button.pack(padx=10, pady=10)
        
frame2 = customtkinter.CTkFrame(master=root)
frame3 = customtkinter.CTkFrame(master=root)
frame4 = customtkinter.CTkFrame(master=root)

radio_var = tkinter.IntVar(value=1)

script_tb = customtkinter.CTkTextbox(master=frame3, height=400, width=400)
address_entry = customtkinter.CTkEntry(master=frame2)
gateway_entry = customtkinter.CTkEntry(master=frame2)

ssid_2_entry = customtkinter.CTkEntry(master=frame2)
ssid_5_entry = customtkinter.CTkEntry(master=frame2)
ssid_pass_entry = customtkinter.CTkEntry(master=frame2)

router_name_entry = customtkinter.CTkEntry(master=frame2)
router_pass_entry = customtkinter.CTkEntry(master=frame2)

def toggle_entry_state():
        if radio_var.get() == 2:
            address_entry.configure(state="disabled", fg_color="lightgrey")
            gateway_entry.configure(state="disabled", fg_color="lightgrey")
        else:
            address_entry.configure(state="normal", fg_color="white")
            gateway_entry.configure(state="normal", fg_color="white")

frame2.pack(padx=20, pady=20, fill="both", expand=True, anchor="c")
frame2.grid_rowconfigure(18, weight=1)
frame2.grid_columnconfigure(8, weight=1)

label = customtkinter.CTkLabel(master=frame2, text="Connected to the router. \n Enter router config below:")
label.grid(row=1, column=3, columnspan=3, rowspan=3, padx=10, pady=10)

network_label = customtkinter.CTkLabel(master=frame2, text="Network")
network_label.grid(row=4, column=2, padx=10, pady=10)

static_radio = customtkinter.CTkRadioButton(master=frame2, text="Static", variable=radio_var, value=1, command=toggle_entry_state)
static_radio.grid(row=4, column=4, sticky='n', pady=10)
dhcp_radio = customtkinter.CTkRadioButton(master=frame2, text="DHCP", variable=radio_var, value=2, command=toggle_entry_state)
dhcp_radio.grid(row=4, column=5, sticky='n', pady=10)

address_label = customtkinter.CTkLabel(master=frame2, text="IP Address:")
address_label.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
gateway_label = customtkinter.CTkLabel(master=frame2, text="Gateway:")
gateway_label.grid(row=6, column=2, columnspan=2, padx=5, pady=5)


address_entry = customtkinter.CTkEntry(master=frame2)
gateway_entry = customtkinter.CTkEntry(master=frame2)

address_entry.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
gateway_entry.grid(row=6, column=4, columnspan=2, padx=5, pady=5)
    

wireless_label = customtkinter.CTkLabel(master=frame2, text="Wireless Settings")
wireless_label.grid(row=8, column=2, padx=10, pady=10)

ssid_2_label = customtkinter.CTkLabel(master=frame2, text="2.4Ghz SSID:")
ssid_2_label.grid(row=9, column=2, columnspan=2, padx=5, pady=5)
ssid_2_entry.grid(row=9, column=4, columnspan=2, padx=5, pady=5)
ssid_5_label = customtkinter.CTkLabel(master=frame2, text="5Ghz SSID:")
ssid_5_label.grid(row=10, column=2, columnspan=2, padx=5, pady=5)
ssid_5_entry.grid(row=10, column=4, columnspan=2, padx=5, pady=5)
ssid_pass_label = customtkinter.CTkLabel(master=frame2, text="Password:")
ssid_pass_label.grid(row=11, column=2, columnspan=2, padx=5, pady=5)
ssid_pass_entry.grid(row=11, column=4, columnspan=2, padx=5, pady=5)

system_label = customtkinter.CTkLabel(master=frame2, text="System Settings")
system_label.grid(row=13, column=2, padx=10, pady=10)

router_name_label = customtkinter.CTkLabel(master=frame2, text="Router Name:")
router_name_label.grid(row=14, column=2, columnspan=2, padx=5, pady=5)
router_name_entry.grid(row=14, column=4, columnspan=2, padx=5, pady=5)
router_pass_label = customtkinter.CTkLabel(master=frame2, text="Router password:")
router_pass_label.grid(row=15, column=2, columnspan=2, padx=5, pady=5)
router_pass_entry.grid(row=15, column=4, columnspan=2, padx=5, pady=5)

button = customtkinter.CTkButton(master=frame2, text="Configure Router", command=remote_winbox_config)
button.grid(row=17, column=6, columnspan=2, padx=10, pady=10)

root.mainloop()

