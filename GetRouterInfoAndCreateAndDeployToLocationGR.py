import requests
from bs4 import BeautifulSoup
from ipaddress import ip_network, ip_address
import urllib3
import json
import os

def getlocalInfo(): #get Router INFO and update inventory 
    router_ip_address1 = os.popen("netstat -rn | grep eth0.101 | grep UG | awk '{print $2}'")
    router_ip_address = router_ip_address1.readline().strip()
    url = f"https://{router_ip_address}/cgi-bin/index.cgi"
    infoGet = requests.get(url, verify=False, timeout=10).content
    infoSoup = BeautifulSoup(infoGet, 'html.parser')
    rpi_hostname = os.environ["ANSIBLE_HOSTNAME"]
    try:
        ipv4Pull = infoSoup.find(id='IPv4').get_text()
    except:
        ipv4Pull = '10.0.0.0'#this is probably not best practice
    try:
        macAddress = ''.join(infoSoup.find(id='MAC').get_text().split(':')).lower()
    except:
        macAddress = ''.join(infoSoup.find(id='WAN MAC Address').get_text().split(':')).lower()
    facts = {
    'ipv4' : ipv4Pull,
    'mac' : macAddress,
    'serial' : infoSoup.find(id='Serial Number').get_text(),
    'model' : infoSoup.find(id='Model').get_text(),
    'cloud_status' : infoSoup.find(id='Cloud Status').get_text()
    }
    mac_address1 = facts["mac"]
    mac_address = ':'.join(format(s, '02x') for s in bytes.fromhex(mac_address1))
    serial = facts["serial"]
    model = facts["model"]
    if model == "SAC2V1K":
        model = 1
    elif model == "SAX1V1K":
        model = 5
    elif model == "SAX1V1R":
        model = 7
    elif model == "SAX1V1S":
        model = 9
    elif model == "SAC2V1A":
        model = 10
    elif model == "SAC2V2S":
        model = 11
    
    print(model)
    print(mac_address)
    print(serial)
    
    #Creates a location using the RPI hostname 
    url = "http://inventory.scp-lab.dev-charter.net/api/v1/locations"
    payload={"name": f"{rpi_hostname}",
    "parent_id": "33"} #33 is  the parent ID for CTEC1 MONDO 2 Setup
    headers = {
      "Authorization": your_api_token,
      }
    add_location = requests.post(url, headers=headers, data=payload).json()
    print(add_location)
    
    # Get Location ID for the newly created location
    response = requests.get(url, headers=headers).json()['rows']
    for responses in response:
        test = responses['id'], responses['name']
        if f"{rpi_hostname}" in test:
            location_id = test[0]              
    print(location_id)
    
    #Creates The Asset and gets the Asset ID
    url = "http://inventory.scp-lab.dev-charter.net/api/v1/hardware"
    payload={"status_id": "2",
    "model_id": f"{model}",
    "serial": f"{serial}",
    "_snipeit_mac_address_1": f"{mac_address}",
    "rtd_location_id": "2"}
    headers = {
      "Authorization": your_api_token}
    response = requests.post(url, headers=headers, data=payload).json()
    asset_id = response['payload']['id']
    print(response)
    
    # Checkout Asset to Specific Location
    url = f"http://inventory.scp-lab.dev-charter.net/api/v1/hardware/{asset_id}/checkout"
    payload={"status_id": "2",
    "checkout_to_type": "location",
    "assigned_location": f"{location_id}"}
    response = requests.post(url, headers=headers, data=payload)
    print(response)

getlocalInfo()


