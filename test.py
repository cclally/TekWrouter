import routeros_api

routerConnection = routeros_api.RouterOsApiPool('192.168.88.1', username='admin', password='', plaintext_login=True).get_api()

with open('/Users/chaselally/Downloads/Remote Winbox Script.txt', 'r') as f:
    script_txt = f.read()


response = routerConnection.get_resource('/').call('system/script/add', {
    'source': script_txt
})

routerConnection.get_resource('/').call('system/script/run', {
    'number': '0'
})