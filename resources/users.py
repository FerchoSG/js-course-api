import json
import boto3
import os
import hashlib
from datetime import datetime
from botocore.exceptions import ClientError
from helpers.data_helper import generate_uuid
from models import User

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'
)

users_table = dynamodb.Table("Users")
alarms_table = dynamodb.Table("Alarms")
transactions_table = dynamodb.Table("Transactions")
withdrawals_table = dynamodb.Table("Withdrawals")
budgets_table = dynamodb.Table("Budgets")
categories_table = dynamodb.Table("Categories")

def get_users():
    try:
        response = users_table.scan()
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_user(user_id):
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        data = response.get('Item')
        if data:
            return data
        else:
            return {
                'statusCode': 404,
                'body': "User not found"
            }
    except ClientError as e:
        return str(e)
    
def get_user_alarms(user_id):
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        data = response.get('Item')

        alarms_response = alarms_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        alarms = alarms_response.get('Items', [])

        data['alarms'] = alarms
        if data:
            return data
        else:
            return "User not found"
    except ClientError as e:
        return str(e)
    
def get_user_transactions(user_id):
    try:
        response = transactions_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        return response.get('Items', [])
    except ClientError as e:
        return str(e)
    
def get_user_budgets(user_id):
    try:
        response = budgets_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        return response.get('Items', [])
    except ClientError as e:
        return str(e)
    
def get_user_categories(user_id):
    try:
        response = categories_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        return response.get('Items', [])
    except ClientError as e:
        return str(e)
    
def get_user_withdrawals(user_id):
    try:
        response = withdrawals_table.scan(FilterExpression='user_id = :u', ExpressionAttributeValues={':u': user_id})
        return response.get('Items', [])
    except ClientError as e:
        return str(e)

def add_user(user: User):
    try:
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        user_id = generate_uuid()
        created_at = datetime.now().isoformat()

        item = {
            'user_id': user_id,
            'username': user.username,
            'email': user.email,
            'password': hashed_password,
            'created_at': created_at
        }

        username = user.username
        email = user.email

        response = users_table.scan(
            FilterExpression='username = :u or email = :e',
            ExpressionAttributeValues={
                ':u': username,
                ':e': email
            }
        )

        if response['Count'] > 0:
            return {
                'statusCode': 400,
                'body': "Username or email already exists"
            }

        users_table.put_item(Item=item)
        return {
            'statusCode': 201
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def update_user(user_id: str, user: User):
    try:
        username = user.username
        email = user.email

        user_dict = user.dict()

        response = users_table.scan(
            FilterExpression='username = :u or email = :e',
            ExpressionAttributeValues={
                ':u': username,
                ':e': email
            }
        )

        if response['Count'] > 0:
            return {
                'statusCode': 400,
                'body': "Username or email already exists"
            }

        update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in user_dict.keys())
        expression_attribute_names = {f"#{k}": k for k in user_dict.keys()}
        expression_attribute_values = {f":{k}": v for k, v in user_dict.items()}

        print(f"Update expression: {update_expression}")
        print(f"Expression attribute names: {expression_attribute_names}")
        print(f"Expression attribute values: {expression_attribute_values}")

        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {
            'statusCode': 200,
            'body': "User updated successfully"
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_user(user_id: str):
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        data = response.get('Item')

        if data:
            users_table.delete_item(Key={'user_id': user_id})
            return {
                'statusCode': 200
            }
        else:
            return {
                'statusCode': 404,
                'body': "User not found"
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
