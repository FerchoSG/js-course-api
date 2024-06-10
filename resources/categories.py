import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Category

import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'
)
table = dynamodb.Table("Categories")
transaction_table = dynamodb.Table("Transactions")

def create_category(category: Category):
    try:
        category_id = str(uuid.uuid4())
        user_id = category.user_id
        category_name = category.category_name
        category_type = category.category_type
        created_at = datetime.now().isoformat()

        item = {
            'category_id': category_id,
            'user_id': user_id,
            'category_name': category_name,
            'category_type': category_type.lower(),
            'created_at': created_at
        }

        table.put_item(Item=item)
        return {'message': 'Category created successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_categories(user_id: str):
    try:
        response = table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_category(category_id: str):
    try:
        response = table.get_item(Key={'category_id': category_id})
        item = response.get('Item')
        if item:
            return item
        else:
            return {'message': 'Category not found'}
    except Exception as e:
        return str(e)

def get_category_by_type(category_type: str):
    try:
        logger.info(f"Category type: {category_type}")
        response = table.scan(FilterExpression='category_type = :u', ExpressionAttributeValues={':u': category_type.lower()})
        logger.info(f"Response: {response}")
        return response.get('Items', [])
    except Exception as e:
        return str(e)

def update_category(category_id: str, category: Category):
    try:
        category_dict = category.dict()
        expression_attribute_values = {f":{k}": v for k, v in category_dict.items()}

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in category_dict.keys())

        logger.debug(f"Update expression: {update_expression}")

        table.update_item(
            Key={'category_id': category_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {'message': 'Category updated successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_category(category_id: str):
    try:
        transactions = transaction_table.scan(FilterExpression='category = :c', ExpressionAttributeValues={':c': category_id})
        data = transactions.get('Items', [])
        if len(data) > 0:
            return {'message': 'Category cannot be deleted as it is associated with transactions'}
        
        table.delete_item(Key={'category_id': category_id})
        return {'message': 'Category deleted successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
