from pydantic import BaseModel
from typing import Optional


# Assuming these models are for request bodies
class UserResponse(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    created_at: Optional[str]
    user_id: Optional[str]
    # Add other fields as needed

class AlarmResponse(BaseModel):
    user_id: Optional[str]
    alarm_name: Optional[str]
    alarm_time: Optional[str]
    days_of_week: Optional[str]
    enabled: Optional[bool]

class UserAlarmsResponse(BaseModel):
    password: Optional[str]
    user_id: Optional[str]
    username: Optional[str]
    created_at: Optional[str]
    email: Optional[str]
    alarms: list[AlarmResponse]

class AuthDetailsResponse(BaseModel):
    username: Optional[str]
    email: Optional[str]
    iat: Optional[str]
    exp: Optional[str]
    token: Optional[str]
    sub: Optional[str]
    created_at: Optional[str]

class TransactionResponse(BaseModel):
    user_id: Optional[str]
    amount: float
    currency: Optional[str]
    transaction_id: Optional[str]
    transaction_type: Optional[str]
    description: Optional[str]
    category: Optional[str]
    created_at: Optional[str]


class Response(BaseModel):
    message: str

class CategoryResponse(BaseModel):
    user_id: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    category_type: Optional[str]
    created_at: Optional[str]

class WithdrawalResponse(BaseModel):
    user_id: Optional[str]
    withdrawal_id: Optional[str]
    amount: float
    created_at: Optional[str]

class BudgetResponse(BaseModel):
    user_id: Optional[str]
    bugdet_id: Optional[str]
    category: Optional[str]
    amount: float
    created_at: Optional[str]