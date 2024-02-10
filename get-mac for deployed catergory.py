import requests


####This script gets mac addresses and the location for all Routers and Modems from Snipe-IT################

# Set up the API endpoint and API key
api_endpoint = "http://inventory.scp-lab.dev-charter.net/api/v1"
api_key = your_api_token
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
params = {
    "limit": 1000  # Increase the limit to retrieve all categories
}

# Make the API request to retrieve the list of categories
response = requests.get(f"{api_endpoint}/categories", headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON to get the list of categories
    categories = response.json()["rows"]

    # Create a dictionary to map category IDs to category names
    category_id_to_name = {category["id"]: category["name"] for category in categories}

    # Set up the headers and parameters for the API request to retrieve assets
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    params = {
        "status": "deployed"
    }

    # Make the API request to retrieve the list of assets
    response = requests.get(f"{api_endpoint}/hardware", headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON to get the list of assets
        assets = response.json()["rows"]

        # Initialize the dictionaries for MAC addresses and locations for each category
        cable_modem_data = {}
        router_data = {}

        # Iterate through the list of assets and retrieve the MAC address and location for each modem or router
        for asset in assets:
            category_id = asset["category"]["id"]
            if category_id in category_id_to_name:
                category_name = category_id_to_name[category_id]
                if category_name == "Cable Modem":
                    mac_address = asset["custom_fields"].get("MAC Address")
                    if mac_address is not None:
                        mac_address_value = mac_address["value"].replace(":", "").replace(" ", "")
                        if asset["location"] is not None:
                            cable_modem_data[mac_address_value] = asset["location"].get("name")
                elif category_name == "ROUTER":
                    mac_address = asset["custom_fields"].get("MAC Address")
                    if mac_address is not None:
                        mac_address_value = mac_address["value"].replace(":", "").replace(" ", "")
                        if asset["location"] is not None:
                            router_data[mac_address_value] = asset["location"].get("name")

        # Print the MAC addresses and locations for each category
        print("Cable modem data:", cable_modem_data)
        print("Router data:", router_data)

    else:
        print("Error retrieving list of assets")
else:
    print("Error retrieving list of categories")

# Loop over the MAC addresses in cable_modem_data dictionary
for mac_address in cable_modem_data:
    # Do something with the MAC address, for example print it
    print(mac_address)

# Loop over the MAC addresses in router_data dictionary
for mac_address in router_data:
    # Do something with the MAC address, for example print it
    print(mac_address)
