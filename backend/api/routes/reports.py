"""
API routes for managing reports
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime

from database import get_reports_collection, get_users_collection
from models.schemas import (
    ReportCreate, ReportResponse, ReportInDB, ReportUpdate,
    UserInDB, ReportStatus
)
from utils.auth import get_current_user, get_officer_or_admin_user

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    current_user: Optional[UserInDB] = Depends(get_current_user)
):
    """
    Create a new report
    """
    reports_collection = get_reports_collection()
    
    # Create report document
    report = ReportInDB(
        title=report_data.title,
        description=report_data.description,
        category=report_data.category,
        location=report_data.location,
        address=report_data.address,
        latitude=report_data.latitude,
        longitude=report_data.longitude,
        priority=report_data.priority.lower(),
        department=report_data.department.lower(),
        reporter_id=current_user.id if current_user else "anonymous",
        reporter_name=report_data.reporter_name,
        reporter_email=report_data.reporter_email,
        reporter_phone=report_data.reporter_phone
    )
    
    # Insert into database
    report_dict = report.dict()
    result = await reports_collection.insert_one(report_dict)
    
    if result.inserted_id:
        return {
            "message": "Report created successfully",
            "report_id": report.id,
            "status": "submitted"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create report"
        )

@router.get("/", response_model=List[ReportResponse])
async def get_all_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None),
    category_filter: Optional[str] = Query(None),
    department_filter: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get all reports with optional filtering and pagination
    """
    reports_collection = get_reports_collection()
    
    # Build filter query
    filter_query = {}
    
    # Filter by user role
    if current_user.user_type == "public":
        # Public users can only see their own reports
        filter_query["reporter_id"] = current_user.id
    elif current_user.user_type == "officer":
        # Officers can see reports from their department or assigned to them
        if current_user.department:
            filter_query["$or"] = [
                {"department": current_user.department.lower()},
                {"assigned_officer_id": current_user.id}
            ]
    # Admins can see all reports (no additional filter)
    
    # Apply optional filters
    if status_filter:
        filter_query["status"] = status_filter.lower()
    if category_filter:
        filter_query["category"] = category_filter.lower()
    if department_filter:
        filter_query["department"] = department_filter.lower()
    
    # Query database
    cursor = reports_collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
    reports_docs = await cursor.to_list(length=limit)
    
    # Convert to response models
    reports = []
    for report_doc in reports_docs:
        report = ReportInDB(**report_doc)
        reports.append(ReportResponse(
            id=report.id,
            title=report.title,
            description=report.description,
            category=report.category,
            location=report.location,
            address=report.address,
            latitude=report.latitude,
            longitude=report.longitude,
            created_at=report.created_at,
            updated_at=report.updated_at,
            status=report.status,
            reporter_id=report.reporter_id,
            reporter_name=report.reporter_name,
            reporter_email=report.reporter_email,
            reporter_phone=report.reporter_phone,
            assigned_officer_id=report.assigned_officer_id,
            assigned_officer_name=report.assigned_officer_name,
            image_urls=report.image_urls,
            priority=report.priority,
            department=report.department,
            estimated_resolution_time=report.estimated_resolution_time,
            department_contact=report.department_contact,
            updates=report.updates
        ))
    
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a specific report by ID
    """
    reports_collection = get_reports_collection()
    
    # Find report
    report_doc = await reports_collection.find_one({"id": report_id})
    if not report_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    report = ReportInDB(**report_doc)
    
    # Check permissions
    if current_user.user_type == "public" and report.reporter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own reports"
        )
    elif (current_user.user_type == "officer" and 
          report.department != current_user.department.lower() and 
          report.assigned_officer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view reports from your department or assigned to you"
        )
    
    return ReportResponse(
        id=report.id,
        title=report.title,
        description=report.description,
        category=report.category,
        location=report.location,
        address=report.address,
        latitude=report.latitude,
        longitude=report.longitude,
        created_at=report.created_at,
        updated_at=report.updated_at,
        status=report.status,
        reporter_id=report.reporter_id,
        reporter_name=report.reporter_name,
        reporter_email=report.reporter_email,
        reporter_phone=report.reporter_phone,
        assigned_officer_id=report.assigned_officer_id,
        assigned_officer_name=report.assigned_officer_name,
        image_urls=report.image_urls,
        priority=report.priority,
        department=report.department,
        estimated_resolution_time=report.estimated_resolution_time,
        department_contact=report.department_contact,
        updates=report.updates
    )

@router.put("/{report_id}/status")
async def update_report_status(
    report_id: str,
    new_status: ReportStatus,
    update_message: str = "",
    current_user: UserInDB = Depends(get_officer_or_admin_user)
):
    """
    Update report status (officers and admins only)
    """
    reports_collection = get_reports_collection()
    
    # Find report
    report_doc = await reports_collection.find_one({"id": report_id})
    if not report_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    report = ReportInDB(**report_doc)
    
    # Check permissions for officers
    if (current_user.user_type == "officer" and 
        report.department != current_user.department.lower() and 
        report.assigned_officer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update reports from your department or assigned to you"
        )
    
    # Create update record
    update_record = ReportUpdate(
        message=update_message or f"Status changed to {new_status.value}",
        status=new_status,
        updated_by=current_user.id,
        updated_by_name=current_user.name
    )
    
    # Update report
    update_data = {
        "status": new_status.value,
        "updated_at": datetime.utcnow(),
        "$push": {"updates": update_record.dict()}
    }
    
    # If assigning, set officer information
    if new_status in [ReportStatus.IN_PROGRESS, ReportStatus.RESOLVE_SOON]:
        update_data.update({
            "assigned_officer_id": current_user.id,
            "assigned_officer_name": current_user.name
        })
    
    result = await reports_collection.update_one(
        {"id": report_id},
        update_data
    )
    
    if result.modified_count:
        return {
            "message": "Report status updated successfully",
            "new_status": new_status.value,
            "updated_by": current_user.name
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update report status"
        )

@router.get("/stats/summary")
async def get_report_stats(
    current_user: UserInDB = Depends(get_officer_or_admin_user)
):
    """
    Get report statistics summary (officers and admins only)
    """
    reports_collection = get_reports_collection()
    
    # Build base filter for user role
    base_filter = {}
    if current_user.user_type == "officer" and current_user.department:
        base_filter["department"] = current_user.department.lower()
    
    # Aggregate statistics
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]
    
    stats_cursor = reports_collection.aggregate(pipeline)
    stats_result = await stats_cursor.to_list(length=None)
    
    # Process results
    stats = {
        "total": 0,
        "submitted": 0,
        "in_progress": 0,
        "done": 0,
        "rejected": 0
    }
    
    for stat in stats_result:
        status = stat["_id"]
        count = stat["count"]
        stats["total"] += count
        
        if status in stats:
            stats[status] = count
    
    return stats