from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from . import schemas,database,token as token_utils,models
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return token_utils.verify_token(data,credentials_exception)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = token_utils.verify_token(token, credentials_exception)  # ← returns TokenData
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user  # ← full ORM User



