import requests
from bs4 import BeautifulSoup
import os

def getlocalInfo(): #get Router INFO and update inventory 
    router_ip_address1 = os.popen("netstat -rn | grep eth0.101 | grep UG | awk '{print $2}'")
    router_ip_address = router_ip_address1.readline().strip()
    url = f"https://{router_ip_address}/cgi-bin/index.cgi"
    infoGet = requests.get(url, verify=False, timeout=10).content
    infoSoup = BeautifulSoup(infoGet, 'html.parser')
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
    'model' : infoSoup.find(id='Model').get_text()
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
    elif model == "SAX2V1S":
        model = 26
    elif model == "RAC2V1A":
        model = 30
    elif model == "RAC2V1K":
        model = 31
    elif model == "SAX2V1R":
        model = 38
    elif model == "RAC2V2S":
        model = 40
    elif model == "RAC2V1S":
        model = 42
    elif model == "MAX2V1K":
        model = 51
    
    print(model)
    print(mac_address)
    print(serial)
    
    
    #Creates The Asset and gets the Asset ID
    url = "https://inventory.scp-lab.dev-charter.net:8443/api/v1/hardware"
    payload={"status_id": "11",
    "model_id": f"{model}",
    "serial": f"{serial}",
    "_snipeit_mac_address_1": f"{mac_address}",
    "_snipeit_serial_connection_2": "Yes"}
    headers = {
      "Authorization": your_api_token"}
    response = requests.post(url, headers=headers, data=payload).json()
    print(response)
    


getlocalInfo()

