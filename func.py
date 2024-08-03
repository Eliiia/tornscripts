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


# tornitems = json.loads(requests.get(f"https://api.torn.com/torn/?selections=items&key={TOKEN}").content)
# if "error" in tornitems:
#     print(f"\nError:\n{tornitems}")
#     exit()
# else: tornitems = tornitems["bazaar"][:5]