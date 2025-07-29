# Send 2 POST request in www-url-encoded form and application/json 


import requests 
import urllib3


# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://jsonplaceholder.typicode.com/posts"
data = {
    "id": 1,
    "title": 'foo',
    "body": 'bar',
    "userId": 1,
  }

headers = {
    'Content-type': 'application/json; charset=UTF-8',
  }

r = requests.post(url,verify=False,headers=headers,json=data)
print(r.json())


r = requests.post(url,verify=False,data=data)
print(r.text)