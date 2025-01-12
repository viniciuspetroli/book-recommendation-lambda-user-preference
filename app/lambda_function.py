import json
from db import DynamoDBIntegration
from src.utils.utils import create_gemini_payload
import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

dynamodb = DynamoDBIntegration('db_host', 'db_user')

@tracer.capture_lambda_handler
def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        preferred_books = body['preference_books']['books']

        dynamodb.insert(
            {
                'user_id': user_id,
                'preference_books': preferred_books
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Preferencias do usuario atualizadas'
            })
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao atualizar preferencias do usuario'
            })
        }