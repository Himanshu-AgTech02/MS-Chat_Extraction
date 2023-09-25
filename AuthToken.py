import ConfigFile
import requests

token_url = ConfigFile.Token_url

data = {
    "client_id": ConfigFile.Client_id,
    "client_secret": ConfigFile.Client_secret,
    "grant_type": ConfigFile.Grant_type,
    "scope": ConfigFile.Scope
}

response = requests.post(token_url, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response to get the access token
    token_data = response.json()
    access_token = token_data.get("access_token")
    print(f"Access Token: {access_token}")
else:
    print(f"Token request failed with status code {response.status_code}")