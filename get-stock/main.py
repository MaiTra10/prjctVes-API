# get-stock
from bs4 import BeautifulSoup
import requests
import json

def lambda_get_stock(event, ctx):

    requestType = event["queryStringParameters"]["requestType"]
    ticker = event["queryStringParameters"]["ticker"]
    exchange = event["queryStringParameters"]["exchange"]

    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"

    html = requests.get(url).text

    soup = BeautifulSoup(html)

    try:

        price = soup.find("div", class_ = "YMlKec fxKbKc").text

    except:

        return return_msg(400, "Error: Ticker or Exchange is Invalid")

    previous_close = soup.find("div", class_ = "P6K39c").text

    if requestType == "advanced":

        data = soup.find_all("div", class_ = "P6K39c")

        advanced_data = advanced_data_bp(exchange, price, previous_close, data)

        return return_msg(200, json.dumps(advanced_data))

    return return_msg(200, json.dumps({
        "Current Price": price,
        "% Change": calculate_percent_change(price, previous_close)
    }))

def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg

def calculate_percent_change(price, previous_close):

    price_float = float(price.replace("$", "").replace(",", ""))
    previous_close_float = float(previous_close.replace("$", "").replace(",", ""))

    percent_change = ((price_float / previous_close_float) - 1) * 100

    return round(percent_change, 2)

def advanced_data_bp(exchange, price, previous_close, data):

    usa_exchange = ["NASDAQ", "NYSE"]
    canada_exchange = ["TSE"]
    futures_exchange = ["CBOT", "CME_EMINIS", "COMEX", "NYMEX"]

    if exchange in usa_exchange:

        advanced_data = {

            "Current Price": price,
            "Previous Close": previous_close,
            "Market Cap": data[3].text,
            "Average Volume": data[4].text,
            "P/E Ratio": data[5].text,
            "Dividend Yield": data[6].text,
            "% Change": calculate_percent_change(price, previous_close)

        }

    elif exchange in canada_exchange:

        advanced_data = {

            "Current Price": price,
            "Previous Close": previous_close,
            "Market Cap": data[3].text,
            "P/E Ratio": data[4].text,
            "Dividend Yield": data[5].text,
            "% Change": calculate_percent_change(price, previous_close)

        }

    elif exchange in futures_exchange:

        advanced_data = {

            "Current Price": price,
            "Previous Close": previous_close,
            "Volume": data[2].text,
            "Open Interest": data[5].text,
            "Settlement Price": data[6].text,
            "% Change": calculate_percent_change(price, previous_close)

        }

    else:

        advanced_data = {

            "Current Price": price,
            "Previous Close": previous_close,
            "% Change": calculate_percent_change(price, previous_close)

        }

    return advanced_data