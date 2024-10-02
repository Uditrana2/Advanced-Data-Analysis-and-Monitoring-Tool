import requests
import random
import time
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

def check_vpn():
    try:
        # Attempt to connect to the Tor proxy
        response = requests.get('http://localhost:9050')
        if response.status_code == 200:
            print("Tor proxy is running and configured correctly.")
            return True
        else:
            print("Tor proxy is not running or not configured correctly.")
            return False
    except requests.exceptions.ConnectionError:
        print("Tor proxy is not running or not configured correctly.")
        return False

def deep_web_scraper():
    # Ask for the URL of the deep web
    url = "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page"

    try:
        # Make the request to the URL using Tor proxy
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        request = requests.get(url, proxies=proxies)
        status_code = request.status_code

        if status_code == 200:
            print("Request went through.\n")
            content = request.content
            soup = BeautifulSoup(content, 'html.parser')
            body_content = soup.find('body')
            
            if body_content:
                # Function to write HTML body content to a text file
                def write_content_to_file(content):
                    timestamp = int(time.time())
                    filename = "content_{}.txt".format(timestamp)
                    print("Saving to ... ", filename)

                    with open(filename, "w") as newfile:
                        newfile.write(content)

                    print("Content written to a text file:", filename)
                
                write_content_to_file(body_content.text)
            else:
                print("Body content not found on the page.")
                
        else:
            print("Request failed with status code:", status_code)

    except Exception as e:
        print("An error occurred:", e)

if check_vpn():
    deep_web_scraper()
else:
    print("Tor proxy is not running or not configured correctly.")
