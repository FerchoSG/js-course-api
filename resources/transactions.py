import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Transaction

import logging

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'
)
table = dynamodb.Table("Transactions")

def create_transaction(transaction: Transaction):
    try:
        if transaction.amount <= 0:
            return {'message': 'Amount must be greater than 0'}

        transaction_id = str(uuid.uuid4())
        user_id = transaction.user_id
        amount = transaction.amount
        transaction_type = transaction.transaction_type
        description = transaction.description
        category = transaction.category
        created_at = datetime.now().isoformat()

        item = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'amount': amount,
            'transaction_type': transaction_type,
            'description': description,
            'category': category,
            'created_at': created_at
        }

        table.put_item(Item=item)
        return {'message': 'Transaction created successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_transactions(user_id: str):
    try:
        response = table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_transaction(transaction_id: str):
    try:
        response = table.get_item(Key={'transaction_id': transaction_id})
        item = response.get('Item')
        if item:
            return item
        else:
            return {'message': 'Transaction not found'}
    except Exception as e:
        return str(e)

def update_transaction(transaction_id: str, transaction: Transaction):
    try:
        transaction_dict = transaction.dict()
        expression_attribute_values = {f":{k}": v for k, v in transaction_dict.items()}

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in transaction_dict.keys())

        logger.debug(f"Update expression: {update_expression}")

        table.update_item(
            Key={'transaction_id': transaction_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {'message': 'Transaction updated successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_transaction(transaction_id: str):
    try:
        table.delete_item(Key={'transaction_id': transaction_id})
        return {'message': 'Transaction deleted successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
