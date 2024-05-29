from pydantic import BaseModel

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