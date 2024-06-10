import os
import jwt
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Alarm, AuthDetails, User, Budget, Transaction, Category, Withdrawal
from resources.alarms import create_alarm, delete_alarm, get_alarm, get_alarms, update_alarm
from resources.auth import authenticate
from resources.users import add_user, delete_user, get_user, get_user_alarms, get_users, update_user, get_user_budgets, get_user_categories, get_user_transactions, get_user_withdrawals
from resources.budgets import create_budget, get_budget, get_budgets, update_budget, delete_budget
from resources.transactions import create_transaction, delete_transaction, get_transaction, get_transactions, update_transaction
from resources.categories import create_category, delete_category, get_category, get_categories, update_category
from resources.withdrawals import create_withdrawal, delete_withdrawal, get_withdrawal, get_withdrawals, update_withdrawal
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

        return username
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token has expired -> {e}")
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token -> {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def read_root():
    return {"message": "Health check passed!"}

@app.get("/users", response_model=list[User])
def read_users(current_user: str = Depends(get_current_user)):
    return get_users()

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user(user_id)

@app.get("/users/{user_id}/alarms")
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_alarms(user_id)

@app.get("/users/{user_id}/transactions", response_model=list[Transaction])
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_transactions(user_id)

@app.get("/users/{user_id}/categories", response_model=list[Category])
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_categories(user_id)

@app.get("/users/{user_id}/budgets", response_model=list[Budget])
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_budgets(user_id)

@app.get("/users/{user_id}/withdrawals", response_model=list[Withdrawal])
def read_user(user_id: str, current_user: str = Depends(get_current_user)):
    return get_user_withdrawals(user_id)

@app.post("/users", response_model=User)
def create_user(user: User):
    return add_user(user)

@app.put("/users/{user_id}", response_model=User)
def modify_user(user_id: str, user: User, current_user: str = Depends(get_current_user)):
    return update_user(user_id, user)

@app.delete("/users/{user_id}", response_model=User)
def remove_user(user_id: str, current_user: str = Depends(get_current_user)):
    return delete_user(user_id)

@app.get("/alarms", response_model=list[Alarm])
def read_alarms(current_user: str = Depends(get_current_user)):
    return get_alarms()

@app.get("/alarms/{alarm_id}", response_model=Alarm)
def read_alarm(alarm_id: str, current_user: str = Depends(get_current_user)):
    return get_alarm(alarm_id)

@app.post("/alarms", response_model=Alarm)
def create_new_alarm(alarm: Alarm, current_user: str = Depends(get_current_user)):
    return create_alarm(alarm)

@app.put("/alarms/{alarm_id}", response_model=Alarm)
def modify_alarm(alarm_id: str, alarm: Alarm, current_user: str = Depends(get_current_user)):
    return update_alarm(alarm_id, alarm)

@app.delete("/alarms/{alarm_id}", response_model=Alarm)
def remove_alarm(alarm_id: str, current_user: str = Depends(get_current_user)):
    return delete_alarm(alarm_id)

@app.post("/auth")
def authenticate_user(auth_details: AuthDetails):
    return authenticate(auth_details)

@app.get("/budgets", response_model=list[Budget])
def read_budgets(current_user: str = Depends(get_current_user)):
    return get_budgets(current_user)

@app.get("/budgets/{budget_id}", response_model=Budget)
def read_budget(budget_id: str, current_user: str = Depends(get_current_user)):
    return get_budget(budget_id)

@app.post("/budgets", response_model=Budget)
def create_new_budget(budget: Budget, current_user: str = Depends(get_current_user)):
    return create_budget(budget)

@app.put("/budgets/{budget_id}", response_model=Budget)
def modify_budget(budget_id: str, budget: Budget, current_user: str = Depends(get_current_user)):
    return update_budget(budget_id, budget)

@app.delete("/budgets/{budget_id}", response_model=Budget)
def remove_budget(budget_id: str, current_user: str = Depends(get_current_user)):
    return delete_budget(budget_id)

@app.get("/transactions", response_model=list[Transaction])
def read_transactions(current_user: str = Depends(get_current_user)):
    return get_transactions(current_user)

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: str, current_user: str = Depends(get_current_user)):
    return get_transaction(transaction_id)

@app.post("/transactions", response_model=Transaction)
def create_new_transaction(transaction: Transaction, current_user: str = Depends(get_current_user)):
    return create_transaction(transaction)

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def modify_transaction(transaction_id: str, transaction: Transaction, current_user: str = Depends(get_current_user)):
    return update_transaction(transaction_id, transaction)

@app.delete("/transactions/{transaction_id}", response_model=Transaction)
def remove_transaction(transaction_id: str, current_user: str = Depends(get_current_user)):
    return delete_transaction(transaction_id)

@app.get("/categories", response_model=list[Category])
def read_categories(current_user: str = Depends(get_current_user)):
    return get_categories(current_user)

@app.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: str, current_user: str = Depends(get_current_user)):
    return get_category(category_id)

@app.post("/categories", response_model=Category)
def create_new_category(category: Category, current_user: str = Depends(get_current_user)):
    return create_category(category)

@app.put("/categories/{category_id}", response_model=Category)
def modify_category(category_id: str, category: Category, current_user: str = Depends(get_current_user)):
    return update_category(category_id, category)

@app.delete("/categories/{category_id}", response_model=Category)
def remove_category(category_id: str, current_user: str = Depends(get_current_user)):
    return delete_category(category_id)

@app.get("/withdrawals", response_model=list[Withdrawal])
def read_withdrawals(current_user: str = Depends(get_current_user)):
    return get_withdrawals(current_user)

@app.get("/withdrawals/{withdrawal_id}", response_model=Withdrawal)
def read_withdrawal(withdrawal_id: str, current_user: str = Depends(get_current_user)):
    return get_withdrawal(withdrawal_id)

@app.post("/withdrawals", response_model=Withdrawal)
def create_new_withdrawal(withdrawal: Withdrawal, current_user: str = Depends(get_current_user)):
    return create_withdrawal(withdrawal)

@app.put("/withdrawals/{withdrawal_id}", response_model=Withdrawal)
def modify_withdrawal(withdrawal_id: str, withdrawal: Withdrawal, current_user: str = Depends(get_current_user)):
    return update_withdrawal(withdrawal_id, withdrawal)

@app.delete("/withdrawals/{withdrawal_id}", response_model=Withdrawal)
def remove_withdrawal(withdrawal_id: str, current_user: str = Depends(get_current_user)):
    return delete_withdrawal(withdrawal_id)




# Optionally, you can add custom exception handlers if needed
@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
