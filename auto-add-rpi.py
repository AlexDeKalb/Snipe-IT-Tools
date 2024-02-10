import requests
import os

def getlocalInfo(): #get RPI INFO and update inventory 
    #Gets info from the RPI to update inventory with 
    rpi_mac_address1 = os.popen("/sbin/ifconfig eth0 | awk '/ether/{print $2}'")
    rpi_mac_address = rpi_mac_address1.readline().strip()
    rpi_revision1 = os.popen("cat /proc/cpuinfo | awk '/Revision/{print $3}'")
    rpi_revision = rpi_revision1.readline().strip()
    rpi_serial1 = os.popen("cat /proc/cpuinfo | awk '/Serial/{print $3}'")
    rpi_serial = rpi_serial1.readline().strip()
    rpi_hostname2 = os.popen("hostname")
    rpi_hostname1 = rpi_hostname2.readline().strip()
    rpi_hostname = rpi_hostname1.strip('-RPI')
    
    if not all([rpi_mac_address, rpi_revision, rpi_serial, rpi_hostname]):
        print("Missing information. Exiting.")
        return
    
    if rpi_revision == "b03111":
        model = 21
    elif rpi_revision == "b03112":
        model = 21
    elif rpi_revision == "b03114":
        model = 21 
    elif rpi_revision == "b03115":
        model = 21         
    elif rpi_revision == "c03111":
        model = 20
    elif rpi_revision == "c03112":
        model = 20
    elif rpi_revision == "c03114":
        model = 20
    elif rpi_revision == "c03115":
        model = 20
    print(model)
    print(rpi_mac_address)
    print(rpi_serial)
    print(rpi_hostname)
    
    
    #Creates The Asset and gets the Asset ID
    url = "http://inventory.scp-lab.dev-charter.net/api/v1/hardware"
    payload={"status_id": "11",
    "model_id": f"{model}",
    "serial": f"{rpi_serial}",
    "_snipeit_mac_address_1": f"{rpi_mac_address}"}
    headers = {
      "Authorization": your_api_token }
    response = requests.post(url, headers=headers, data=payload).json()
    print(response)
    

getlocalInfo()
