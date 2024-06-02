import os
import jwt
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Alarm, AuthDetails, User
from resources.alarms import create_alarm, delete_alarm, get_alarm, get_alarms, update_alarm
from resources.auth import authenticate
from resources.users import add_user, delete_user, get_user, get_user_alarms, get_users, update_user
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
app = FastAPI()

security_scheme = HTTPBearer()

SECRET_KEY = "g2K#Z!9W3n@0X$LqR5s*tp&Fb1DcEaH8"
ALGORITHM = "HS256"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security_scheme)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def read_root():
    return {"message": "Health check passed!"}

@app.get("/users")
def read_users(current_user: str = Depends(get_current_user)):
    return get_users()

@app.get("/users/{user_id}")
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user(user_id)

@app.get("/users/{user_id}/alarms")
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_alarms(user_id)

@app.post("/users")
def create_user(user: User):
    return add_user(user)

@app.put("/users/{user_id}")
def modify_user(user_id: str, user: User, current_user: str = Depends(get_current_user)):
    return update_user(user_id, user)

@app.delete("/users/{user_id}")
def remove_user(user_id: str, current_user: str = Depends(get_current_user)):
    return delete_user(user_id)

@app.get("/alarms")
def read_alarms(current_user: str = Depends(get_current_user)):
    return get_alarms()

@app.get("/alarms/{alarm_id}")
def read_alarm(alarm_id: str, current_user: str = Depends(get_current_user)):
    return get_alarm(alarm_id)

@app.post("/alarms")
def create_new_alarm(alarm: Alarm, current_user: str = Depends(get_current_user)):
    return create_alarm(alarm)

@app.put("/alarms/{alarm_id}")
def modify_alarm(alarm_id: str, alarm: Alarm, current_user: str = Depends(get_current_user)):
    return update_alarm(alarm_id, alarm)

@app.delete("/alarms/{alarm_id}")
def remove_alarm(alarm_id: str, current_user: str = Depends(get_current_user)):
    return delete_alarm(alarm_id)

@app.post("/auth")
def authenticate_user(auth_details: AuthDetails):
    return authenticate(auth_details)

# Optionally, you can add custom exception handlers if needed
@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
