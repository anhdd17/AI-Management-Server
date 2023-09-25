import jwt
from sqlalchemy.orm import Session
from models.user import User as UserModel
from schemas.user_schema import UserCreate, UserLoginInput
from fastapi import HTTPException, Depends
from utils.password_utils import hash_password, verify_password
from utils.errors import ( EmailAlreadyExistsException, IncorrectEmailOrPasswordException,
                           InvalidCredentialsException, UserNotFoundException, TokenExpiresException, 
                           TokenValidationFailedException
                        )
from datetime import datetime, timedelta
from config.app_settings import secret_key
from config.db_config import get_db
from utils.security import oauth2_scheme

def create_user(db: Session, user: UserCreate):
    if get_user_by_email(db, user.email) is not None:
        raise EmailAlreadyExistsException()
    hashed_password = hash_password(user.password)
    db_user = UserModel(
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(input_data: UserLoginInput, db: Session):
    user = get_user_by_email(db, input_data.email)
    if not user or not verify_password(input_data.password, user.password):
        raise IncorrectEmailOrPasswordException
    expiration = datetime.utcnow() + timedelta(minutes=2)
    token = jwt.encode(
        {"email": user.email, "exp": expiration},
        secret_key,
        algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer"}

def get_user_by_email(db: Session, email: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    return user

def get_user_by_id(db: Session, id: int):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])   
        email: str = payload.get("email")
        if email is None:
            raise InvalidCredentialsException
        user = get_user_by_email(db, email)
        if user is None:
            raise UserNotFoundException
        return user
    except jwt.ExpiredSignatureError:
        raise TokenExpiresException
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise TokenValidationFailedException
    

def assign_role(user_id: int, current_user: UserModel, db: Session):
    if current_user.role != "super-admin":
        raise HTTPException(status_code=403, detail="Permission denied") 
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user.role = "admin"
    db.commit()
    return {"message": "Admin role assigned successfully"}





