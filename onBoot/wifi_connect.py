import subprocess
import time

def connect_wifi(ssid, password):
    print(f"Attempting to connect to {ssid}")
    config = f'''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
'''
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(config)
    
    subprocess.call(['sudo', 'ifconfig', 'wlan0', 'down'])
    time.sleep(1)
    subprocess.call(['sudo', 'ifconfig', 'wlan0', 'up'])
    time.sleep(2)
    
    subprocess.call(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
    time.sleep(10)  # Wait for connection attempt
    
    # Check if connected
    result = subprocess.run(['iwgetid'], capture_output=True, text=True)
    return ssid in result.stdout

def is_connected():
    result = subprocess.run(['iwgetid'], capture_output=True, text=True)
    return bool(result.stdout.strip())

def connect_to_networks(priority_network, fallback_networks):
    while True:
        if is_connected():
            print("Already connected to a network")
            return

        # Try priority network first
        if connect_wifi(priority_network['ssid'], priority_network['password']):
            print(f"Successfully connected to priority network {priority_network['ssid']}")
            return

        # If priority network fails, try fallback networks
        for network in fallback_networks:
            if connect_wifi(network['ssid'], network['password']):
                print(f"Successfully connected to fallback network {network['ssid']}")
                return

        print("Failed to connect to any network. Retrying in 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    priority_network = {"ssid": "thesweetwoman-2.4Ghz", "password": "janice3byy"}
#    priority_network = {"ssid": "Yy", "password": "0183759772"}
    fallback_networks = [
#        {"ssid": "thesweetwoman-2.4Ghz", "password": "janice3byy"},
        {"ssid": "Yy's Phone", "password": "0183759772"}
    ]
    connect_to_networks(priority_network, fallback_networks)