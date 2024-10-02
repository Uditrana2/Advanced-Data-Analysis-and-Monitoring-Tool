import requests
import random
import re
import string
import sys
import os

# Function to scrape ahmia.fi for onion links
def ahmia_scraper(query):
    if " " in query:
        query = query.replace(" ", "+")

    url = "https://ahmia.fi/search/?q={}".format(query)

    ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
               "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
               "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
               "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
               "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
    ua = random.choice(ua_list)
    headers = {'User-Agent': ua}

    request = requests.get(url, headers=headers)
    content = request.text

    regex_query = "\w+\.onion"
    mined_data = re.findall(regex_query, content)
    mined_data = list(dict.fromkeys(mined_data))

    n = random.randint(1, 9999)
    filename = "sites{}.txt".format(str(n))
    print("Saving to ... ", filename)

    with open(filename, "w+") as file:
        for link in mined_data:
            file.write(link + "\n")

    print("All the links written to a text file:", filename)

# Function to search for onion links using Tor
def tor_searcher(url):
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}

    print("Getting ...", url)
    result = session.get(url).text

    # Extract site name from URL
    site_name = url.split("/")[-1].replace(".onion", "").replace("/", "")

    with open(f"{site_name}.txt", "w+", encoding="utf-8") as file:
        file.write(result)

    print("Data from the page saved as:", f"{site_name}.txt")

# Function to run the scraper based on IP location
def run_scraper():
    url = "http://ip-api.com/json/"
    key = requests.get(url)

    if "Croatia" in key.text or "Zagreb" in key.text or "Hrvatska" in key.text:
        print("Your VPN might not be on!")
        return

    import ahmiascraper
    ahmiascraper.Scraper()

if __name__ == "__main__":
    program_name = os.path.basename(sys.argv[0])

    if len(sys.argv) < 2:
        print("Usage: {} <command> [args]".format(program_name))
        sys.exit(1)

    command = sys.argv[1]

    if command == "scrape":
        if len(sys.argv) != 3:
            print("Usage: {} scrape <query>".format(program_name))
            sys.exit(1)
        query = sys.argv[2]
        ahmia_scraper(query)

    elif command == "search":
        if len(sys.argv) != 3:
            print("Usage: {} search <url_list>".format(program_name))
            sys.exit(1)
        url_list = sys.argv[2]
        try:
            with open(url_list, "r", encoding="utf-8") as file:
                data = file.readlines()
                for url in data:
                    url = url.replace("\n", "")
                    url = "http://" + url
                    tor_searcher(url)
        except Exception as e:
            print(e)

    elif command == "run":
        run_scraper()

    else:
        print("Unknown command:", command)
        print("Usage: {} <command> [args]".format(program_name))
