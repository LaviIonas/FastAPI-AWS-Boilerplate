from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:   
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    
    # Create new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/me", response_model=schemas.UserOut)
def get_current_user(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user



