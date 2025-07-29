import requests
from bs4 import BeautifulSoup
import re
import urllib3

# === Configuration ===
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === User Inputs ===
total_runs = int(input("Enter number of times to run the request: "))
user_name = input("Enter your name: ")
whatsapp_number = input("Enter your WhatsApp number: ")
funds_value = input("Enter funds value: ")

# === Start Session ===
url = "https://sharegenius.in/contact"
post_url = url
session = requests.Session()

for run in range(1, total_runs + 1):
    print(f"\n=== Run {run} of {total_runs} ===")

    # Step 1: GET request to fetch CAPTCHA
    response = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 2: Extract the CAPTCHA expression and token
    captcha_box = soup.find("div", class_="captcha-box")
    captcha_text = captcha_box.text.strip() if captcha_box else ""
    captcha_token_input = soup.find("input", {"name": "captcha_token"})
    captcha_token = captcha_token_input["value"] if captcha_token_input else ""

    print(f"CAPTCHA Question: {captcha_text}")

    # Step 3: Solve the CAPTCHA
    match = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", captcha_text)
    if not match:
        print("Failed to parse CAPTCHA.")
        continue

    a, operator, b = match.groups()
    a, b = int(a), int(b)

    if operator == "+":
        captcha_answer = a + b
    elif operator == "-":
        captcha_answer = a - b
    elif operator == "*":
        captcha_answer = a * b
    elif operator == "/":
        captcha_answer = a / b
    else:
        print("Unknown operator in CAPTCHA.")
        continue

    print(f"Solved CAPTCHA Answer: {captcha_answer}")

    # Step 4: POST request
    payload = {
        "name": user_name,
        "whatsapp": whatsapp_number,
        "funds": funds_value,
        "captcha_answer": str(int(captcha_answer)),
        "captcha_token": captcha_token
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    post_response = session.post(post_url, data=payload, headers=headers, verify=False, proxies=proxies)

    print("POST Request Status Code:", post_response.status_code)
    # Optional: print response body
    print("Server Response:\n", post_response.text.strip())
