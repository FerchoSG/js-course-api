import json
import boto3
import os
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

import logging

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

SECRET_KEY = "g2K#Z!9W3n@0X$LqR5s*tp&Fb1DcEaH8"
ALGORITHM = "HS256"

from models import AuthDetails

logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-2'
)

table = dynamodb.Table("Users")

def authenticate(auth_details: AuthDetails):
    username_or_email = auth_details.username
    password = auth_details.password

    logger.info(f"Authenticating user: {username_or_email}")
    try:
        # Query the DynamoDB Users table to find the user by username or email
        response = table.scan(
            FilterExpression='username = :u or email = :e',
            ExpressionAttributeValues={
                ':u': username_or_email,
                ':e': username_or_email
            }
        )

        logger.info(f"Response: {response}")
        if response['Count'] == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        logger.info(f"User found: {response['Items'][0]}")

        user = response['Items'][0]

        # Verify the provided password against the stored hashed password
        stored_hashed_password = user['password']
        if verify_password(password, stored_hashed_password):
            # Set expiration time for the token (optional)
            current_time_utc = datetime.now(timezone.utc)
            expiration_time_utc = current_time_utc + timedelta(days=1)

            # Add expiration time to the data
            user["iat"] = current_time_utc
            user["exp"] = expiration_time_utc
            user["sub"] = user['username']

            # Encode the data into a JWT token
            token = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

            user['token'] = token
            # remove password from the response
            user.pop('password')
            
            return {
                'statusCode': 200,
                'body': user
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def verify_password(plain_password, hashed_password):
    """
    Verify if a plain text password matches its hashed version.
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password stored in the database.
    Returns:
        bool: True if the plain text password matches its hashed version, False otherwise.
    """
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
