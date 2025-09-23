"""
API routes for notification management
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime

from database import get_notifications_collection
from models.schemas import (
    NotificationCreate, NotificationResponse, NotificationInDB,
    NotificationType, UserInDB
)
from utils.auth import get_current_user, get_admin_user

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Create a new notification (admin only)
    """
    notifications_collection = get_notifications_collection()
    
    # Create notification document
    notification = NotificationInDB(
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        user_id=notification_data.user_id,
        issue_id=notification_data.issue_id,
        data=notification_data.data
    )
    
    # Insert into database
    notification_dict = notification.dict()
    result = await notifications_collection.insert_one(notification_dict)
    
    if result.inserted_id:
        return {
            "message": "Notification created successfully",
            "notification_id": notification.id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification"
        )

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    unread_only: bool = Query(False),
    notification_type: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get notifications for the current user
    """
    notifications_collection = get_notifications_collection()
    
    # Build filter query
    filter_query = {
        "$or": [
            {"user_id": current_user.id},  # User-specific notifications
            {"user_id": None}  # System-wide notifications
        ]
    }
    
    # Add filters
    if unread_only:
        filter_query["is_read"] = False
    
    if notification_type:
        filter_query["type"] = notification_type.lower()
    
    # Query database
    cursor = notifications_collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
    notifications_docs = await cursor.to_list(length=limit)
    
    # Convert to response models
    notifications = []
    for notification_doc in notifications_docs:
        notification = NotificationInDB(**notification_doc)
        notifications.append(NotificationResponse(
            id=notification.id,
            title=notification.title,
            message=notification.message,
            type=notification.type,
            user_id=notification.user_id,
            issue_id=notification.issue_id,
            data=notification.data,
            is_read=notification.is_read,
            created_at=notification.created_at,
            read_at=notification.read_at
        ))
    
    return notifications

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a specific notification by ID
    """
    notifications_collection = get_notifications_collection()
    
    # Find notification
    notification_doc = await notifications_collection.find_one({"id": notification_id})
    if not notification_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification = NotificationInDB(**notification_doc)
    
    # Check permissions
    if notification.user_id and notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own notifications"
        )
    
    return NotificationResponse(
        id=notification.id,
        title=notification.title,
        message=notification.message,
        type=notification.type,
        user_id=notification.user_id,
        issue_id=notification.issue_id,
        data=notification.data,
        is_read=notification.is_read,
        created_at=notification.created_at,
        read_at=notification.read_at
    )

@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Mark a notification as read
    """
    notifications_collection = get_notifications_collection()
    
    # Find notification first to check permissions
    notification_doc = await notifications_collection.find_one({"id": notification_id})
    if not notification_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification = NotificationInDB(**notification_doc)
    
    # Check permissions
    if notification.user_id and notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark your own notifications as read"
        )
    
    # Update notification
    result = await notifications_collection.update_one(
        {"id": notification_id},
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count:
        return {"message": "Notification marked as read"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notification as read"
        )

@router.put("/mark-all-read")
async def mark_all_notifications_as_read(
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Mark all notifications as read for the current user
    """
    notifications_collection = get_notifications_collection()
    
    # Update all unread notifications for the user
    result = await notifications_collection.update_many(
        {
            "$or": [
                {"user_id": current_user.id},
                {"user_id": None}
            ],
            "is_read": False
        },
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "message": f"Marked {result.modified_count} notifications as read"
    }

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Delete a notification (user can delete their own, admin can delete any)
    """
    notifications_collection = get_notifications_collection()
    
    # Find notification first to check permissions
    notification_doc = await notifications_collection.find_one({"id": notification_id})
    if not notification_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification = NotificationInDB(**notification_doc)
    
    # Check permissions
    if (current_user.user_type != "admin" and 
        notification.user_id and notification.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own notifications"
        )
    
    # Delete notification
    result = await notifications_collection.delete_one({"id": notification_id})
    
    if result.deleted_count:
        return {"message": "Notification deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification"
        )

@router.get("/stats/unread-count")
async def get_unread_count(
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get count of unread notifications for the current user
    """
    notifications_collection = get_notifications_collection()
    
    # Count unread notifications
    count = await notifications_collection.count_documents({
        "$or": [
            {"user_id": current_user.id},
            {"user_id": None}
        ],
        "is_read": False
    })
    
    return {"unread_count": count}

# Admin-only routes
@router.post("/broadcast", status_code=status.HTTP_201_CREATED)
async def broadcast_notification(
    notification_data: NotificationCreate,
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Send a broadcast notification to all users (admin only)
    """
    notifications_collection = get_notifications_collection()
    
    # Create system-wide notification (user_id = None)
    notification = NotificationInDB(
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        user_id=None,  # System-wide notification
        issue_id=notification_data.issue_id,
        data=notification_data.data
    )
    
    # Insert into database
    notification_dict = notification.dict()
    result = await notifications_collection.insert_one(notification_dict)
    
    if result.inserted_id:
        return {
            "message": "Broadcast notification created successfully",
            "notification_id": notification.id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create broadcast notification"
        )

@router.get("/admin/all", response_model=List[NotificationResponse])
async def get_all_notifications_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserInDB = Depends(get_admin_user)
):
    """
    Get all notifications in the system (admin only)
    """
    notifications_collection = get_notifications_collection()
    
    # Query all notifications
    cursor = notifications_collection.find({}).skip(skip).limit(limit).sort("created_at", -1)
    notifications_docs = await cursor.to_list(length=limit)
    
    # Convert to response models
    notifications = []
    for notification_doc in notifications_docs:
        notification = NotificationInDB(**notification_doc)
        notifications.append(NotificationResponse(
            id=notification.id,
            title=notification.title,
            message=notification.message,
            type=notification.type,
            user_id=notification.user_id,
            issue_id=notification.issue_id,
            data=notification.data,
            is_read=notification.is_read,
            created_at=notification.created_at,
            read_at=notification.read_at
        ))
    
    return notifications