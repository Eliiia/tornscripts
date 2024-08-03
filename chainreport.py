# Developed together with DemandingSloth
# See https://github.com/DemandingSloth/Torn

import time

from func import req

# TODO check if faction currently chaining

# get time inputs
timefrom = int(input("When from? "))
timeto = input("When to? ")
if timeto == "now": timeto = int(time.time()) # if user says "now", get current time
else: timeto = int(timeto)

# get list of chains!
print("Getting chain info...")
chains = req(f"https://api.torn.com/faction/?selections=chains&from={timefrom}&to={timeto}")["chains"]
print(f"Loaded {len(chains)} chains")

contribs = {}

for chainid in chains:
    print(f"Processing chain {chainid}")
    members = req(f"https://api.torn.com/torn/{chainid}/?selections=chainreport")["chainreport"]["members"]

    for member_id, mdata in members.items():
        if mdata["attacks"] >= 3:  
            if member_id not in contribs.keys():
                contribs[member_id] = mdata["attacks"]
            else:
                contribs[member_id] += mdata["attacks"]

print("Getting usernames...\n")
time.sleep(1) # in case nearing API limit

# Get member profiles and print results
print(f"Attacks\tName") 
for member_id, attacks in contribs.items():
    name = req(f"https://api.torn.com/user/{member_id}/")["name"]
    print(f"{attacks}\t{name}") 

print(f"'to' time: {timeto}")