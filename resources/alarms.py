import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Alarm

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
table = dynamodb.Table("Alarms")

def create_alarm(alarm: Alarm):
    try:
        alarm_id = str(uuid.uuid4())
        user_id = alarm.user_id
        alarm_name = alarm.alarm_name
        alarm_time = alarm.alarm_time
        days_of_week = alarm.days_of_week
        created_at = datetime.now().isoformat()

        item = {
            'alarm_id': alarm_id,
            'user_id': user_id,
            'alarm_name': alarm_name,
            'alarm_time': alarm_time,
            'days_of_week': days_of_week,
            'enabled': True,
            'created_at': created_at
        }

        table.put_item(Item=item)
        return {'message': 'Alarm created successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_alarms():
    try:
        response = table.scan()
        data = response.get('Items', [])
        return data
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_alarm(alarm_id: str):
    try:
        response = table.get_item(Key={'alarm_id': alarm_id})
        item = response.get('Item')
        if item:
            return item
        else:
            return {'message': 'Alarm not found'}
    except Exception as e:
        return str(e)

def update_alarm(alarm_id: str, alarm: Alarm):
    try:
        alarm_dict = alarm.dict()
        expression_attribute_values = {f":{k}": v for k, v in alarm_dict.items()}

        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in alarm_dict.keys())

        logger.debug(f"Update expression: {update_expression}")

        table.update_item(
            Key={'alarm_id': alarm_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {'message': 'Alarm updated successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def delete_alarm(alarm_id: str):
    try:
        table.delete_item(Key={'alarm_id': alarm_id})
        return {'message': 'Alarm deleted successfully'}
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
