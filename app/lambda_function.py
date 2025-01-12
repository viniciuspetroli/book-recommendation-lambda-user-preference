from src.lambda_processor import process
from src.dynamo import DynamoService
import boto3
import boto3.session

# Create your own session
session = boto3.session.Session()
dynamo_service = DynamoService(session, 'Users')

def lambda_handler(event, context):
    try:
        result = process(event, dynamo_service)
        return result
    except Exception as e:
        raise e
    
#Just a comment to push the code