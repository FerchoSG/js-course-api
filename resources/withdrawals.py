import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Withdrawal

import logging
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'
)
table = dynamodb.Table("Withdrawals")
transaction_table = dynamodb.Table("Transactions")

def get_user_total_funds(user_id: str):
    user_transactions = transaction_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
    transactions = user_transactions['Items']
    user_total_amount = 0

    for transaction in transactions:
        if transaction['transaction_type'] == 'income':
            user_total_amount += transaction['amount']
        else:
            user_total_amount -= transaction['amount']

    return user_total_amount

def create_withdrawal(withdrawal: Withdrawal):
    try:
        # user_funds = get_user_total_funds(withdrawal.user_id)

        # if withdrawal.amount > user_funds:
        #     return {'message': 'Insufficient funds'}

        withdrawal_id = str(uuid.uuid4())
        user_id = withdrawal.user_id
        amount = withdrawal.amount
        created_at = datetime.now().isoformat()

        item = {
            'withdrawal_id': withdrawal_id,
            'user_id': user_id,
            'amount': amount,
            'created_at': created_at
        }

        table.put_item(Item=item)
        return {'message': 'Withdrawal created successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_withdrawals(user_id: str):
    try:
        response = table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_withdrawal(withdrawal_id: str):
    try:
        response = table.get_item(Key={'withdrawal_id': withdrawal_id})
        item = response.get('Item')
        if item:
            return item
        else:
            return {'message': 'Withdrawal not found'}
    except Exception as e:
        return str(e)

def update_withdrawal(withdrawal_id: str, withdrawal: Withdrawal):
    try:
        # user_funds = get_user_total_funds(withdrawal.user_id)

        # if withdrawal.amount > user_funds:
        #     return {'message': 'Insufficient funds'}
        
        withdrawal_dict = withdrawal.dict()
        expression_attribute_values = {f":{k}": v for k, v in withdrawal_dict.items()}

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in withdrawal_dict.keys())

        logger.debug(f"Update expression: {update_expression}")

        table.update_item(
            Key={'withdrawal_id': withdrawal_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {'message': 'Withdrawal updated successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_withdrawal(withdrawal_id: str):
    try:
        table.delete_item(Key={'withdrawal_id': withdrawal_id})
        return {'message': 'Withdrawal deleted successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
