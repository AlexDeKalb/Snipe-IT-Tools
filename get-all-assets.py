import requests

# Set up the API endpoint and API key
api_endpoint = "http://inventory.scp-lab.dev-charter.net/api/v1/hardware?search=0c%3Ab9%3A37%3A59%3A38%3A80"
api_key = your_api_token

# Set up the headers and parameters for the API request to retrieve categories
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
params = {
    "limit": 1000  # Increase the limit to retrieve all categories
}

with open("assetlist.txt", "w") as f:
    response = requests.get(f"{api_endpoint}", headers=headers, params=params) 
    f.write(response.text)
    print(response.text)

