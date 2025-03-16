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

@router.put("/me", response_model=schemas.UserOut)
def update_user(updated_info: schemas.UserBase, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    
    if updated_info.email != current_user.email:
        # Check if new email already exists
        existing_email = db.query(models.User).filter(models.User.email == updated_info.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user_query.update(updated_info.dict(), synchronize_session=False)
    db.commit()
    
    return user_query.first()

@router.put("/me/password")
def change_password(password_data: dict, 
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):
    
    # Verify current password
    if not utils.verify_password(password_data["current_password"], current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Hash new password
    hashed_password = utils.hash_password(password_data["new_password"])
    
    # Update password
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.update({"password": hashed_password}, synchronize_session=False)
    db.commit()
    
    return {"message": "Password updated successfully"}

