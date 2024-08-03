import time
import math

from func import req, getitemdetails, abbrvcheck

items = [] 

# main loop per item
while True:
    # get item name
    itemname = input("\nWhat is the item name? ")
    if itemname == "quit": break

    # get item ID and other details
    itemdetails = getitemdetails(itemname)
    if itemdetails == None: # if not found, tell user
        print("Unable to find item, going back to name input...")
        continue
    print(f"{itemdetails["name"]}\n\tMarket value: ${itemdetails["market_value"]} | Circulation: {itemdetails["circulation"]}")

    # get market info
    bazaarreq = req(f"https://api.torn.com/market/{itemdetails["id"]}/?selections=bazaar")["bazaar"]
    imarketreq = req(f"https://api.torn.com/market/{itemdetails["id"]}/?selections=itemmarket")["itemmarket"]

    # check for empty bazaar and imarket info, then print market info
    # TODO: do not add last "|" on output
    marketinfo = ""

    if bazaarreq == None:
        print("\tBazaar information not found")
    else:
        bazaarreq = bazaarreq[:5]
        marketinfo += "\tBazaar:\n\t"
        for x in bazaarreq:
            marketinfo += f"${x["cost"]} ({x["quantity"]}) | "

    if imarketreq == None:
        print("\tItem market information not found")
    else:
        imarketreq = imarketreq[:10]
        if marketinfo != "": marketinfo += "\n"
        marketinfo += "\tItem market:"
        for (i, x) in enumerate(imarketreq):
            if(i % 5 == 0): marketinfo += "\n\t"
            marketinfo += f"${x["cost"]} ({x["quantity"]}) | "

    # ask for quantity and price
    # TODO: allow user to input "k" and "m"
    price = input("How much do you wish to charge? ")
    price = abbrvcheck(price)
    if price == "quit" or not price.isdigit(): # if did not enter a number, assume incorrect item found
        print("Non-number detected, going back to name input...")
        continue 
    else: price = int(price)
    itemquan = int(input("How many? "))

    # save
    items.append({
        "name": itemdetails["name"],
        "quantity": itemquan,
        "price": price,
        "market_value": itemdetails["market_value"]
        })

print("\n---\n") # separator

# print receipt per-item; market value and given
totaltocharge = 0
totalmarketvalue = 0
for x in items:
    itemtotal = x["quantity"]*x["price"]
    totaltocharge += itemtotal
    totalmarketvalue += x["quantity"]*x["market_value"]
    print(f"{x["quantity"]} {x["name"]} at ${x["price"]} = ${itemtotal}")

# print totals; market value and given
print() # empty line
print(f"Total: ${totaltocharge/1000}k ~= ${math.floor(totaltocharge/1000)}k (${math.floor(totaltocharge/1000)/1000}m)")
print(f"Total market value: ${totalmarketvalue/1000}k (${totaltocharge/1000000}m)")

# Allow user to manually input rounded number
input("Rounded to: $")