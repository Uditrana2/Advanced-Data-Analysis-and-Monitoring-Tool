import requests
import random
import time

def Scraper():
    # Ask for the URL of the deep web
    url = "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page"

    # Check if the URL starts with "http://" or "https://", if not, add it
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    # Let's set up some fake user agents
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
        "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
    ua = random.choice(ua_list)
    headers = {'User-Agent': ua}

    try:
        # Make the request to the URL
        request = requests.get(url, headers=headers)
        status_code = request.status_code
        content = request.text

        print("Status Code:", status_code)

        # Function to write HTML body content to a text file
        def write_content_to_file(content):
            timestamp = int(time.time())
            filename = "content_{}.txt".format(timestamp)
            print("Saving to ... ", filename)

            with open(filename, "w") as newfile:
                newfile.write(content)

            print("Content written to a text file:", filename)

        if status_code == 200:
            print("Request went through.\n")
            write_content_to_file(content)
        else:
            print("Request failed with status code:", status_code)

    except Exception as e:
        print("An error occurred:", e)

# Call the Scraper function
Scraper()
