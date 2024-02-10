import requests
import json

# Function to identify duplicates
def identify_duplicates(assets):
    mac_dict = {}
    
    for asset in assets:
        # Check if the MAC Address field exists
        if "MAC Address" in asset.get("custom_fields", {}):
            mac_address = asset["custom_fields"]["MAC Address"]["value"]
            asset_tag_numeric = ''.join(filter(str.isdigit, asset["asset_tag"]))
            
            # Skip assets that have no numeric parts in their asset tags
            if not asset_tag_numeric:
                continue
            
            asset_tag = int(asset_tag_numeric)
            
            if mac_address in mac_dict:
                existing_asset_tag = int(''.join(filter(str.isdigit, mac_dict[mac_address]["asset_tag"])))
                if asset_tag < existing_asset_tag:
                    mac_dict[mac_address] = asset
            else:
                mac_dict[mac_address] = asset
    
    original_assets = list(mac_dict.values())
    duplicates = [asset for asset in assets if asset not in original_assets]
    
    return original_assets, duplicates


# Fetching all assets
url = "https://inventory.scp-lab.dev-charter.net:8443/api/v1/hardware"
headers = {
  'Authorization': your_api_token
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Cookie': 'snipeit_session=WyyVLSmEJzg2EB4hz7rtDlJBnWyCESHSNB9SLtuT'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    assets = response.json()["rows"]
    _, duplicates = identify_duplicates(assets)
    
    # Deleting duplicates
    for duplicate in duplicates:
        mac_address = duplicate.get("custom_fields", {}).get('MAC Address', {}).get('value')
        if mac_address:
            response = requests.request("DELETE", f"{url}/{duplicate['id']}", headers=headers)
            if response.status_code == 200:  # Assuming 200 is the success status code for deletion
                print(f"Deleted asset with ID {duplicate['id']} and MAC Address {mac_address}")
            else:
                print(f"Failed to delete asset with ID {duplicate['id']}. Reason: {response.text}")
        else:
            print(f"Skipped asset with ID {duplicate['id']} because it doesn't have a valid MAC Address.")



else:
    print(f"Failed to fetch assets. Reason: {response.text}")
