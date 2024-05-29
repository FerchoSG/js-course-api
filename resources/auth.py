import json
import boto3
import os
import hashlib
import jwt
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

SECRET_KEY = "g2K#Z!9W3n@0X$LqR5s*tp&Fb1DcEaH8"
ALGORITHM = "HS256"

from models import AuthDetails

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Set your region

table = dynamodb.Table("Users")

def authenticate(auth_details: AuthDetails):
    username_or_email = auth_details.username
    password = auth_details.password
    try:
        # Query the DynamoDB Users table to find the user by username or email
        response = table.scan(
            FilterExpression='username = :u or email = :e',
            ExpressionAttributeValues={
                ':u': username_or_email,
                ':e': username_or_email
            }
        )
        if response['Count'] == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = response['Items'][0]

        # Verify the provided password against the stored hashed password
        stored_hashed_password = user['password']
        if verify_password(password, stored_hashed_password):
            # Set expiration time for the token (optional)
            expiration_time = datetime.now() + timedelta(hours=1)

            # Add expiration time to the data
            user["iat"] = expiration_time
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
