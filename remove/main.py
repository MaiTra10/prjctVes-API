# remove
import boto3
import simplejson as json
from boto3.dynamodb.conditions import Key

dynamoDB = boto3.resource("dynamodb")
table_name = "prjctVes-DB"
table = dynamoDB.Table(table_name)

def lambda_remove(event, ctx):

    params = event["queryStringParameters"]

    event_for = params["for"]
    user = int(params["user"])
    index = int(params["index"]) # 1-10

    if event_for == "steam":

        prefix = ".v-"

    else:

        prefix = ".s-"

    query_resp = table.query(KeyConditionExpression = Key("userID").eq(user) & Key("ctx").begins_with(prefix))

    count = int(query_resp["Count"])

    if count == 0:

        return return_msg(403, f"Error: Table is Empty")

    elif index not in range(1, count + 1):

        return return_msg(400, f"Error: Index is Out of Range (1 - {count})")

    item_id = query_resp["Items"][index - 1]["ctx"]

    delete_resp = table.delete_item(Key = {

        "userID": user,
        "ctx": item_id

    }, ReturnValues = "ALL_OLD")

    body = json.dumps(delete_resp['Attributes'])

    return return_msg(delete_resp["ResponseMetadata"]["HTTPStatusCode"], body)

def return_msg(status_code, body):
    
    msg = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    
    return msg