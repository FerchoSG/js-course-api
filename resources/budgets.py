import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Budget

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
table = dynamodb.Table("Budgets")

def create_budget(budget: Budget):
    try:
        budget_id = str(uuid.uuid4())
        user_id = budget.user_id
        amount = budget.amount
        category = budget.category
        created_at = datetime.now().isoformat()

        item = {
            'budget_id': budget_id,
            'user_id': user_id,
            'amount': amount,
            'category': category,
            'created_at': created_at
        }

        table.put_item(Item=item)
        return {'message': 'Budget created successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_budgets(user_id: str):
    try:
        response = table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_budget(budget_id: str):
    try:
        response = table.get_item(Key={'budget_id': budget_id})
        item = response.get('Item')
        if item:
            return item
        else:
            return {'message': 'Budget not found'}
    except Exception as e:
        return str(e)

def update_budget(budget_id: str, budget: Budget):
    try:
        budget_dict = budget.dict()
        expression_attribute_values = {f":{k}": v for k, v in budget_dict.items()}

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in budget_dict.keys())

        logger.debug(f"Update expression: {update_expression}")

        table.update_item(
            Key={'budget_id': budget_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {'message': 'Budget updated successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_budget(budget_id: str):
    try:
        table.delete_item(Key={'budget_id': budget_id})
        return {'message': 'Budget deleted successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
