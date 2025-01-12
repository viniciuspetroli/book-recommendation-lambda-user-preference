import json
from src.dynamo import DynamoService

def process(event, dynamo_service: DynamoService):
    http_method = event["httpMethod"]
    body = json.loads(event["body"]) if "body" in event else {}

    if http_method == "POST":
        item = {
            'user_id': {'N': body["user_id"]},
            'user_name': {'S': body["user_name"]},
            'user_fav_cat': {'S': body["user_fav_cat"]},
            'user_fav_aut': {'S': body["user_fav_aut"]}
        }
        result = dynamo_service.put_item(item=item)
    elif http_method == "PUT":
        key = {
            'user_id': {'N': body["user_id"]},
        }
        update_expression = "set nome = :nome"
        expression_attribute_values = {
            ':user_name': {'S': body["user_name"]},
        }
        result = dynamo_service.update_item(key=key, update_expression=update_expression, att_values=expression_attribute_values)
    elif http_method == "GET":
        user_id = event["queryStringParameters"]["user_id"]
        result = dynamo_service.get_item(key={"user_id": {"N": user_id}})
    elif http_method == "DELETE":
        user_id = event["queryStringParameters"]["user_id"]
        result = dynamo_service.delete_item(key={"user_id": {"N": user_id}})
    else:
        raise Exception("Invalid HTTP method")
    return result

#Just a comment to push the code