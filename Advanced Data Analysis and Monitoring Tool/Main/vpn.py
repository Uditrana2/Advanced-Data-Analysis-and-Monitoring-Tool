#import the actual scraper
import requests

url = "http://ip-api.com/json/"
key = requests.get(url)
#print(key.text)
if "Croatia" in key.text or "Zagreb" in key.text or "Hrvatska" in key.text:
    print("VPN might not be on !!")
    safe = False
else:
    safe = True

if safe == True:
    import Upro.ahmiascraper as ahmiascraper
    ahmiascraper.Scraper()
else:
    print("IP change failed, try again later.")
