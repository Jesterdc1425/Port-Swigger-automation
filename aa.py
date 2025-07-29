import requests

# Bitbucket Server URL
url = "http://localhost:7990/rest/api/1.0/projects"

# Base64 encoded "username:password" => "fred:fred"
headers = {
    "Authorization": "Basic ZnJlZDpmcmVk",
    "Content-Type": "application/json"
}

# Send GET request
response = requests.get(url, headers=headers)

# Print status and response
print("Status Code:", response.status_code)
print("Headers:\n", response.headers)
print("Body:\n", response.text)
