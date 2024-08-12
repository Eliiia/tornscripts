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
    itemlookingfor = itemlookingfor.lower()
    # loop through three algorithms and return none if nothing at all found
    return (
        # first criteria: exact result
        next(
            (
                { # return these details...
                    "id": item_id,
                    "name": item_details["name"],
                    "market_value": item_details["market_value"],
                    "circulation": item_details["circulation"],
                }
                for item_id, item_details in tornitems # ...by looping in this loop...
                if item_details["name"].lower() == itemlookingfor # ...and checking for this
            ),
            None, # return none if no valid result found
        )
        # second criteria: startswith
        or next(
            (
                { 
                    "id": item_id,
                    "name": item_details["name"],
                    "market_value": item_details["market_value"],
                    "circulation": item_details["circulation"],
                }
                for item_id, item_details in tornitems
                if item_details["name"].lower().startswith(itemlookingfor) 
            ),
            None, 
        )
        # third criteria: in
        or next(
            (
                { 
                    "id": item_id,
                    "name": item_details["name"],
                    "market_value": item_details["market_value"],
                    "circulation": item_details["circulation"],
                }
                for item_id, item_details in tornitems 
                if itemlookingfor in item_details["name"].lower() 
            ),
            None, 
        )
    )


def abbrvcheck(num, f): 
    # check for "k" or "m" in a number
    # "f" is a type function to specify type of output
    # being able to specify allows for user input to be fed directly in and then processed after
    if num.endswith("k"):
        num = f(int(float(num.replace("k", "")) * 1000))
    elif num.endswith("m"):
        num = f(int(float(num.replace("m", "")) * 1000000))
    # todo: if k or m not at the end, tell program it is invalid number?
    return num
