from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, User, UserLoginInput,  TokenResponse
from services.user_service import create_user, login_user, get_current_user, get_user_by_id, assign_role
from config.db_config import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


# User registration
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# User login
@router.post("/login", response_model=TokenResponse)
def login(user: UserLoginInput, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_authorization = UserLoginInput(email=form_data.username, password=form_data.password) 
    return login_user(user_authorization, db)


@router.post("/assign-admin-role")
def assign_admin_role(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return assign_role(user_id, current_user, db)
    
