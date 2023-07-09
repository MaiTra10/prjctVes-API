# get
import boto3
from boto3.dynamodb.conditions import Key

dynamoDB = boto3.resource("dynamodb")
table_name = "prjctVes-DB"
table = dynamoDB.Table(table_name)

def lambda_get(event, ctx):

    params = event["queryStringParameters"]

    event_for = params["for"]
    user = int(params["user"])
    retrieve = params["retrieve"]

    if event_for == "both":

        both_query_resp = table.query(KeyConditionExpression = Key("userID").eq(user) & Key("ctx").begins_with("."))

        if int(both_query_resp["Count"]) == 0:

            return return_msg(403, "Error: Table is Empty")

        return return_msg(200, both_query_resp["Items"])

    if event_for == "steam":

        prefix = ".v-"

    else:

        prefix = ".s-"

    if retrieve == "all":

        query_resp = table.query(KeyConditionExpression = Key("userID").eq(user) & Key("ctx").begins_with(prefix))

        if int(query_resp["Count"]) == 0:

            return return_msg(403, "Error: Table is Empty")

        return return_msg(200, query_resp["Items"])
    
    else: # 'retrieve' is 'specific' and needs 'index' parameter

        index = int(params["index"])

        query_resp = table.query(KeyConditionExpression = Key("userID").eq(user) & Key("ctx").begins_with(prefix))

        count = int(query_resp["Count"])

        if count == 0:

            return return_msg(403, f"Error: Table is Empty")

        elif index not in range(1, count + 1):

            return return_msg(400, f"Error: Index is Out of Range (1 - {count})")

        item_id = query_resp["Items"][index - 1]["ctx"]

        get_resp = table.get_item(Key = {

            "userID": user,
            "ctx": item_id

        })

        return return_msg(200, get_resp["Item"])



def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg