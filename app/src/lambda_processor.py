import re
import json
from src.dynamo import DynamoService

def process(event, dynamo_service: DynamoService):
    http_method = event["httpMethod"]
    if http_method != "GET":
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
    
        update_expression = "set "
        expression_attribute_values = {}

        if "user_name" in body:
            update_expression += "user_name = :user_name, "
            expression_attribute_values[':user_name'] = {'S': body["user_name"]}

        if "user_fav_cat" in body:
            update_expression += "user_fav_cat = :user_fav_cat, "
            expression_attribute_values[':user_fav_cat'] = {'S': body["user_fav_cat"]}

        if "user_fav_aut" in body:
            update_expression += "user_fav_aut = :user_fav_aut, "
            expression_attribute_values[':user_fav_aut'] = {'S': body["user_fav_aut"]}

        update_expression = update_expression.rstrip(", ")

        result = dynamo_service.update_item(key=key, update_expression=update_expression, att_values=expression_attribute_values)
    elif http_method == "GET":
        user_id = event["pathParameters"]["user_id"]
        key = {
            'user_id': {'N': user_id},
        }
        result = dynamo_service.get_item(key=key)
    elif http_method == "DELETE":
        key = {
            'user_id': {'N': body["user_id"]},
        }
        result = dynamo_service.delete_item(key=key)
    else:
        raise Exception("Invalid HTTP method")
    return result