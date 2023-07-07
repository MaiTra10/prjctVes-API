# get-steam
from urllib.parse import quote
import requests
import json

def lambda_get_steam(event, ctx):

    item_name = quote(event["queryStringParameters"]["itemName"])

    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=20&market_hash_name=" + item_name
    request = requests.get(url).json()

    if request["success"] == True:

        return return_msg(200, json.dumps(request))
    
    else:

        return return_msg(400, "Bad Request")

def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg