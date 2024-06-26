from pydantic import BaseModel
from decimal import Decimal

# Assuming these models are for request bodies
class User(BaseModel):
    username: str
    email: str
    password: str
    # Add other fields as needed

class Alarm(BaseModel):
    user_id: str
    alarm_name: str
    alarm_time: str
    days_of_week: str
    enabled: bool
    # Add other fields as needed

class AuthDetails(BaseModel):
    username: str
    password: str

class Transaction(BaseModel):
    user_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    description: str
    category: str

class Category(BaseModel):
    user_id: str
    category_name: str

class Withdrawal(BaseModel):
    user_id: str
    amount: Decimal

class Budget(BaseModel):
    user_id: str
    category: str
    amount: Decimal