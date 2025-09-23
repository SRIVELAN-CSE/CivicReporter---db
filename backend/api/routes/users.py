"""
API routes for user management
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime

from database import (
    get_users_collection, 
    get_registration_requests_collection,
    get_password_reset_requests_collection
)
from models.schemas import (
    UserResponse, UserInDB, UserType,
    RegistrationRequestResponse, RegistrationRequestInDB, RegistrationStatus,
    PasswordResetRequestCreate, PasswordResetRequestResponse, PasswordResetRequestInDB
)
from utils.auth import get_current_user, get_admin_user, get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_type_filter: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Get all users (admin only)
    """
    users_collection = get_users_collection()
    
    # Build filter
    filter_query = {}
    if user_type_filter:
        filter_query["user_type"] = user_type_filter.lower()
    
    # Query database
    cursor = users_collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
    users_docs = await cursor.to_list(length=limit)
    
    # Convert to response models
    users = []
    for user_doc in users_docs:
        user = UserInDB(**user_doc)
        users.append(UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            user_type=user.user_type,
            location=user.location,
            department=user.department,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
            profile_image_url=user.profile_image_url
        ))
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a specific user by ID
    """
    # Users can only view their own profile unless they're admin
    if current_user.id != user_id and current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )
    
    users_collection = get_users_collection()
    user_doc = await users_collection.find_one({"id": user_id})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = UserInDB(**user_doc)
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        user_type=user.user_type,
        location=user.location,
        department=user.department,
        is_active=user.is_active,
        created_at=user.created_at,
        last_login_at=user.last_login_at,
        profile_image_url=user.profile_image_url
    )

@router.put("/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Activate a user (admin only)
    """
    users_collection = get_users_collection()
    
    result = await users_collection.update_one(
        {"id": user_id},
        {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User activated successfully"}

@router.put("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Deactivate a user (admin only)
    """
    users_collection = get_users_collection()
    
    result = await users_collection.update_one(
        {"id": user_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}

# Registration Requests Management
@router.get("/registration-requests/", response_model=List[RegistrationRequestResponse])
async def get_registration_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Get all registration requests (admin only)
    """
    registration_requests_collection = get_registration_requests_collection()
    
    # Build filter
    filter_query = {}
    if status_filter:
        filter_query["status"] = status_filter.lower()
    
    # Query database
    cursor = registration_requests_collection.find(filter_query).skip(skip).limit(limit).sort("request_date", -1)
    requests_docs = await cursor.to_list(length=limit)
    
    # Convert to response models
    requests = []
    for request_doc in requests_docs:
        request = RegistrationRequestInDB(**request_doc)
        requests.append(RegistrationRequestResponse(
            id=request.id,
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            id_number=request.id_number,
            reason=request.reason,
            request_date=request.request_date,
            status=request.status,
            admin_response=request.admin_response,
            response_date=request.response_date,
            responded_by=request.responded_by,
            user_type=request.user_type,
            department=request.department,
            designation=request.designation
        ))
    
    return requests

@router.post("/registration-requests/{request_id}/approve")
async def approve_registration_request(
    request_id: str,
    admin_response: str = "",
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Approve a registration request and create the user (admin only)
    """
    registration_requests_collection = get_registration_requests_collection()
    users_collection = get_users_collection()
    
    # Find the registration request
    request_doc = await registration_requests_collection.find_one({"id": request_id})
    if not request_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration request not found"
        )
    
    request = RegistrationRequestInDB(**request_doc)
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create the user
    user = UserInDB(
        name=request.full_name,
        email=request.email,
        phone=request.phone,
        user_type=request.user_type,
        location=request.address,
        department=request.department,
        password_hash=request.password_hash
    )
    
    user_dict = user.dict()
    await users_collection.insert_one(user_dict)
    
    # Update the registration request
    await registration_requests_collection.update_one(
        {"id": request_id},
        {
            "$set": {
                "status": RegistrationStatus.REGISTERED,
                "admin_response": admin_response or "Registration approved",
                "response_date": datetime.utcnow(),
                "responded_by": current_user.id
            }
        }
    )
    
    return {
        "message": "Registration request approved and user created",
        "user_id": user.id,
        "user_email": user.email
    }

@router.post("/registration-requests/{request_id}/reject")
async def reject_registration_request(
    request_id: str,
    admin_response: str,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Reject a registration request (admin only)
    """
    registration_requests_collection = get_registration_requests_collection()
    
    result = await registration_requests_collection.update_one(
        {"id": request_id},
        {
            "$set": {
                "status": RegistrationStatus.ARCHIVED,
                "admin_response": admin_response,
                "response_date": datetime.utcnow(),
                "responded_by": current_user.id
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration request not found"
        )
    
    return {"message": "Registration request rejected"}

# Password Reset Requests
@router.post("/password-reset-requests/", status_code=status.HTTP_201_CREATED)
async def create_password_reset_request(request_data: PasswordResetRequestCreate):
    """
    Create a password reset request
    """
    password_reset_requests_collection = get_password_reset_requests_collection()
    users_collection = get_users_collection()
    
    # Check if user exists
    user_doc = await users_collection.find_one({"email": request_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create password reset request
    reset_request = PasswordResetRequestInDB(
        email=request_data.email,
        reason=request_data.reason,
        new_password_hash=get_password_hash(request_data.new_password)
    )
    
    request_dict = reset_request.dict()
    await password_reset_requests_collection.insert_one(request_dict)
    
    return {
        "message": "Password reset request created. Please wait for admin approval.",
        "request_id": reset_request.id
    }

@router.get("/password-reset-requests/", response_model=List[PasswordResetRequestResponse])
async def get_password_reset_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Get all password reset requests (admin only)
    """
    password_reset_requests_collection = get_password_reset_requests_collection()
    
    cursor = password_reset_requests_collection.find({}).skip(skip).limit(limit).sort("request_date", -1)
    requests_docs = await cursor.to_list(length=limit)
    
    requests = []
    for request_doc in requests_docs:
        request = PasswordResetRequestInDB(**request_doc)
        requests.append(PasswordResetRequestResponse(
            id=request.id,
            email=request.email,
            reason=request.reason,
            request_date=request.request_date,
            status=request.status,
            admin_response=request.admin_response,
            response_date=request.response_date,
            responded_by=request.responded_by
        ))
    
    return requests

@router.post("/password-reset-requests/{request_id}/approve")
async def approve_password_reset(
    request_id: str,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Approve password reset request (admin only)
    """
    password_reset_requests_collection = get_password_reset_requests_collection()
    users_collection = get_users_collection()
    
    # Find the request
    request_doc = await password_reset_requests_collection.find_one({"id": request_id})
    if not request_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password reset request not found"
        )
    
    request = PasswordResetRequestInDB(**request_doc)
    
    # Update user's password
    await users_collection.update_one(
        {"email": request.email},
        {"$set": {"password_hash": request.new_password_hash}}
    )
    
    # Update the request status
    await password_reset_requests_collection.update_one(
        {"id": request_id},
        {
            "$set": {
                "status": "approved",
                "admin_response": "Password reset approved",
                "response_date": datetime.utcnow(),
                "responded_by": current_user.id
            }
        }
    )
    
    return {"message": "Password reset approved and user password updated"}

@router.post("/password-reset-requests/{request_id}/reject")
async def reject_password_reset(
    request_id: str,
    admin_response: str,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Reject password reset request (admin only)
    """
    password_reset_requests_collection = get_password_reset_requests_collection()
    
    result = await password_reset_requests_collection.update_one(
        {"id": request_id},
        {
            "$set": {
                "status": "rejected",
                "admin_response": admin_response,
                "response_date": datetime.utcnow(),
                "responded_by": current_user.id
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password reset request not found"
        )
    
    return {"message": "Password reset request rejected"}