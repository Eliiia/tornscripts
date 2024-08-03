import os
# from dotenv import load_dotenv
import requests
import json
# import time

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TORN_KEY")

if TOKEN == "":
    print("API token not found")

def req(url):
    # add token to URL
    if "?" in url: url += "&"
    else: url += "?"
    request = json.loads(requests.get(url+f"key={TOKEN}").content)
    
    # check for error
    if "error" in request:
        print(f"\nError:\n{request}")
        exit()
    else:
        return request

# get torn items list
tornitems = req("https://api.torn.com/torn/?selections=items")["items"].items()

def getitemdetails(itemlookingfor):
    # find first match using startswith() and lower()
    return next(
            (
                { # return these details...
                    "id": item_id,
                    "name": item_details["name"],
                    "market_value": item_details["market_value"],
                    "circulation": item_details["circulation"],
                }
                for item_id, item_details in tornitems # ...by looping in this loop...
                if item_details["name"].lower().startswith(itemlookingfor.lower()) # ...and checking for this
            ),
            None, # return none if no valid result found
        )

    #out = next((item for item in tornitems if item["name"].lower().startswith(itemname.lower())), None)
    #if out == None: return None
    #else: return out[0]["id"]


# tornitems = json.loads(requests.get(f"https://api.torn.com/torn/?selections=items&key={TOKEN}").content)
# if "error" in tornitems:
#     print(f"\nError:\n{tornitems}")
#     exit()
# else: tornitems = tornitems["bazaar"][:5]