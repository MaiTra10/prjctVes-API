# get-steam
import requests
import boto3
import json
from bs4 import BeautifulSoup
from urllib.parse import quote

def lambda_get_steam(event, ctx):

    item_name = quote(event["queryStringParameters"]["itemName"])
    request_type = event["queryStringParameters"]["requestType"]

    price_url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=20&market_hash_name=" + item_name

    price_resp = requests.get(price_url).json()

    if price_resp["success"] == False:

        return return_msg(404, "Error: Item not Found")

    if request_type == "validate":
        
        return return_msg(200, "Valid")

    if request_type == "advanced":

        ssm = boto3.client("ssm", region_name="us-west-2")

        ssm_resp = ssm.get_parameter(
            Name = "Steam_Session_Cookie",
            WithDecryption=True
        )
        
        price_history_url = "https://steamcommunity.com/market/pricehistory/?country=DE&currency=3&appid=730&market_hash_name=" + item_name

        cookie = {"steamLoginSecure": ssm_resp["Parameter"]["Value"]}

        price_history_resp = requests.get(price_history_url, cookies = cookie).json()

        try :
            
            prices = price_history_resp["prices"]

            price_resp["prices"] = get_history(prices)
            
            price_resp["historyAvailable"] = True
                
        except:
            
            price_resp["historyAvailable"] = False
            
        page_url = "https://steamcommunity.com/market/listings/730/" + item_name
        
        html = requests.get(page_url).text
        
        soup = BeautifulSoup(html)
        
        item_img_url = soup.find("div", "market_listing_largeimage").img["src"]
        
        price_resp["imgURL"] = item_img_url

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
    
def get_history(prices):
    
    if len(prices) < 750:
        
        return prices[-len(prices):]

    else:
        
        return prices[-750:]