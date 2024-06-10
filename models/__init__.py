from pydantic import BaseModel, Field

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
    transaction_id: str = Field(..., description="Este campo es auto generado")
    amount: float
    transaction_type: str
    description: str
    category: str

class Category(BaseModel):
    user_id: str
    category_id: str = Field(str, description="Este campo es auto generado")
    category_name: str
    category_type: str

class Withdrawal(BaseModel):
    user_id: str
    withdrawal_id: str = Field(str, description="Este campo es auto generado")
    amount: float

class Budget(BaseModel):
    user_id: str
    budget_id: str = Field(str, description="Este campo es auto generado")
    category: str
    amount: float