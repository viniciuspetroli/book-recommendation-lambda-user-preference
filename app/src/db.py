import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.tracing import tracer
from botocore.exceptions import ClientError

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('Users')
books_table = dynamodb.Table('Books')
recommendations_table = dynamodb.Table('Recommendations')

def ping():
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='db_credentials')['SecretString']
    return secret

class Integration:
    def __init__(self, db_host, db_user):
        self.db_host = db_host
        self.db_user = db_user
        self.engine = self.create_engine()

    def create_engine(self):
        return 'Conexão com db criada'
    
    @tracer.capture_method
    def get(self, user_id):
        try:
            response = users_table.get_item(Key={'user_id': user_id})
            return response.get['Item', {}]
        except ClientError as e:
            logger.error(f"Error in get: {user_id} | {str(e)}")
            return {}
        
    @tracer.capture_method
    def update_route_status(self, user_id, status):
        try:
            response = users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET route_status = :status',
                ExpressionAttributeValues={':status': status}
            )
            return response
        except ClientError as e:
            logger.error(f"Error in update_route_status: {user_id} | {str(e)}")
            return {}
        
    @tracer.capture_method
    def insert(self, user_data):
        try:
            response = users_table.put_item(Item=user_data)
            return response
        except ClientError as e:
            logger.error(f"Error in insert: {user_data} | {str(e)}")
            return {}
    
    @tracer.capture_method
    def delete(self, user_id):
        try:
            response = users_table.delete_item(Key={'user_id': user_id})
            return response
        except ClientError as e:
            logger.error(f"Error in delete: {user_id} | {str(e)}")
            return {}
        
    @tracer.capture_method
    def insert_books(self, books_data):
        with books_table.batch_writer() as batch:
            for book in books_data:
                batch.put_item(Item=book)
    
    @tracer.capture_method
    def get_books(self, user_id):
        try:
            response = books_table.query(KeyConditionExpression='user_id = :user_id', ExpressionAttributeValues={':user_id': user_id})
            return response.get['Items']
        except ClientError as e:
            logger.error(f"Error in get_books: {user_id} | {str(e)}")
            return []