import json

class DynamoService:
    def __init__(self, session, table):
        self.client = session.client('dynamodb')
        self.table = table
    
    def get_item(self, key):
        response = self.client.get_item(TableName=self.table,Key=key)
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    
    def put_item(self, item):
        self.client.put_item(TableName=self.table,Item=item)
        return {
            "statusCode": 200,
            "body":"Registro inserido com sucesso"
        }
    
    def update_item(self, key, update_expression, att_values):
        self.client.update_item(TableName=self.table, Key=key, UpdateExpression=update_expression, ExpressionAttributeValues=att_values)
        return {
            "statusCode": 200,
            "body":"Registro atualizado com sucesso"
        }
    
    def delete_item(self, key):
        self.client.delete_item(TableName=self.table, Key=key)
        return {
            "statusCode": 200,
            "body":"Registro deletado com sucesso"
        }