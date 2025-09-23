"""
Authentication routes for user registration, login, and token management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

from database import get_users_collection, get_registration_requests_collection
from models.schemas import (
    UserCreate, UserResponse, UserInDB, Token, TokenData,
    RegistrationRequestCreate, RegistrationRequestInDB
)
from utils.auth import (
    get_password_hash, verify_password, create_access_token, 
    authenticate_user, get_current_user
)

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    location: Optional[str] = None
    user_type: str = "public"
    department: Optional[str] = None

@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return access token
    """
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login time
    users_collection = get_users_collection()
    await users_collection.update_one(
        {"id": user.id},
        {"$set": {"last_login_at": datetime.utcnow()}}
    )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
            "department": user.department,
            "is_active": user.is_active
        }
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(register_data: RegisterRequest):
    """
    Register a new user (creates registration request for admin approval)
    """
    users_collection = get_users_collection()
    registration_requests_collection = get_registration_requests_collection()
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": register_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Check if registration request already exists
    existing_request = await registration_requests_collection.find_one(
        {"email": register_data.email}
    )
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration request for this email already exists"
        )
    
    # For public users, auto-approve and create user directly
    if register_data.user_type.lower() == "public":
        # Create user directly
        user = UserInDB(
            name=register_data.name,
            email=register_data.email,
            phone=register_data.phone,
            user_type="public",
            location=register_data.location,
            password_hash=get_password_hash(register_data.password),
        )
        
        user_dict = user.dict()
        await users_collection.insert_one(user_dict)
        
        return {
            "message": "Registration successful! You can now login.",
            "user_id": user.id,
            "status": "approved"
        }
    
    else:
        # For officers/admins, create registration request for admin approval
        registration_request = RegistrationRequestInDB(
            full_name=register_data.name,
            email=register_data.email,
            phone=register_data.phone,
            address=register_data.location or "",
            id_number="",  # Would be provided in a full registration form
            reason=f"Registration as {register_data.user_type}",
            password_hash=get_password_hash(register_data.password),
            user_type=register_data.user_type.lower(),
            department=register_data.department
        )
        
        request_dict = registration_request.dict()
        await registration_requests_collection.insert_one(request_dict)
        
        return {
            "message": "Registration request submitted. Please wait for admin approval.",
            "request_id": registration_request.id,
            "status": "pending_approval"
        }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current user profile information
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        user_type=current_user.user_type,
        location=current_user.location,
        department=current_user.department,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login_at=current_user.last_login_at,
        profile_image_url=current_user.profile_image_url
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: UserInDB = Depends(get_current_user)):
    """
    Refresh access token for authenticated user
    """
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout():
    """
    Logout user (client should remove token)
    """
    return {"message": "Successfully logged out"}