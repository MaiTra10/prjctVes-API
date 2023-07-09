# add
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamoDB = boto3.resource("dynamodb")
table_name = "prjctVes-DB"
table = dynamoDB.Table(table_name)

def lambda_add(event, ctx):

    params = event["queryStringParameters"]

    event_for = params["for"]

    if event_for == "steam":

        prefix = "v-"
        context = f"{prefix}{uuid.uuid4()}"

    else:

        prefix = "s-"
        context = f"{prefix}{uuid.uuid4()}"

    user = params["user"]
    item_to_add = params["itemToAdd"]

    query_resp = table.query(KeyConditionExpression = Key("userID").eq(user) & Key("ctx").begins_with(prefix))

    if query_resp["Count"] != 0 and query_resp["Count"] < 10:

        for item in query_resp["Items"]:

            if item["item"] == item_to_add:

                return return_msg(409, "Error: Duplicate Entry")
            
    elif query_resp["Count"] >= 10:

        return return_msg(403, "Error: Max Number of Watchlist Items")
    
    put_resp = table.put_item(Item = {
        "userID": user,
        "ctx": context,
        "item": item_to_add
    })

    return return_msg(put_resp["ResponseMetadata"]["HTTPStatusCode"], " ")

def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg