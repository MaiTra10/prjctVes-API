# get-steam
from urllib.parse import quote
import requests
import boto3
import json

def lambda_get_steam(event, ctx):

    item_name = quote(event["queryStringParameters"]["itemName"])
    request_type = event["queryStringParameters"]["requestType"]

    price_url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=20&market_hash_name=" + item_name

    price_resp = requests.get(price_url).json()

    if price_resp["success"] == False:

        return return_msg(400, "Bad Request")

    if request_type == "advanced":

        ssm = boto3.client("ssm", region_name="us-west-2")

        ssm_resp = ssm.get_parameter(
            Name = "Steam_Session_Cookie",
            WithDecryption=True
        )
        
        price_history_url = "https://steamcommunity.com/market/pricehistory/?country=DE&currency=3&appid=730&market_hash_name=Revolution%20Case"

        cookie = {"steamLoginSecure": ssm_resp["Parameter"]["Value"]}

        price_history_resp = requests.get(price_history_url, cookies = cookie).json()

        prices = price_history_resp["prices"]

        if len(prices) < 300:

            price_resp["prices"] = prices[-len(price_history_resp):]

        else:
            
            price_resp["prices"] = prices[-300:]

        return return_msg(200, json.dumps(price_resp))

    return return_msg(200, json.dumps(price_resp))

def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg