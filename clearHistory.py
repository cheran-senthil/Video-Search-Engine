import json

x = []
with open("history.json", 'w') as jsonfile:
    json.dump(x, jsonfile)
