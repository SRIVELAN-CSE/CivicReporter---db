"""
Pydantic models for MongoDB documents
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Generate ObjectId as string for MongoDB
def generate_id() -> str:
    return str(uuid.uuid4())

# Enums matching Flutter frontend
class UserType(str, Enum):
    PUBLIC = "public"
    OFFICER = "officer"
    ADMIN = "admin"

class Department(str, Enum):
    GARBAGE_COLLECTION = "garbageCollection"
    DRAINAGE = "drainage" 
    ROAD_MAINTENANCE = "roadMaintenance"
    STREET_LIGHTS = "streetLights"
    WATER_SUPPLY = "waterSupply"
    OTHERS = "others"

class ReportStatus(str, Enum):
    SUBMITTED = "submitted"
    NOT_SEEN = "notSeen"
    RESOLVE_SOON = "resolveSoon"
    IN_PROGRESS = "inProgress"
    DONE = "done"
    REJECTED = "rejected"
    CLOSED = "closed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationType(str, Enum):
    NEW_REPORT = "newReport"
    STATUS_UPDATE = "statusUpdate"
    ASSIGNMENT = "assignment"
    URGENT = "urgent"
    INFO = "info"
    PASSWORD_RESET_APPROVED = "passwordResetApproved"
    PASSWORD_RESET_REJECTED = "passwordResetRejected"
    PASSWORD_RESET_COMPLETED = "passwordResetCompleted"

class RegistrationStatus(str, Enum):
    REGISTERED = "registered"
    NOTIFIED = "notified"
    ARCHIVED = "archived"

# User Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    user_type: UserType
    location: Optional[str] = None
    department: Optional[Department] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    user_type: UserType
    location: Optional[str] = None
    department: Optional[Department] = None
    is_active: bool = True
    created_at: datetime
    last_login_at: Optional[datetime] = None
    profile_image_url: Optional[str] = None

class UserInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    email: EmailStr
    phone: str
    user_type: UserType
    location: Optional[str] = None
    department: Optional[Department] = None
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None
    profile_image_url: Optional[str] = None

# Report Models
class ReportUpdate(BaseModel):
    id: str = Field(default_factory=generate_id)
    message: str
    status: ReportStatus
    updated_by: str
    updated_by_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReportCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    priority: str = "medium"
    department: str = "others"
    reporter_name: str
    reporter_email: EmailStr
    reporter_phone: Optional[str] = None

class ReportResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    status: ReportStatus
    reporter_id: str
    reporter_name: str
    reporter_email: EmailStr
    reporter_phone: Optional[str] = None
    assigned_officer_id: Optional[str] = None
    assigned_officer_name: Optional[str] = None
    image_urls: List[str] = []
    priority: str
    department: str
    estimated_resolution_time: str = "Within 5 days"
    department_contact: Dict[str, str] = {}
    updates: List[ReportUpdate] = []

class ReportInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str
    category: str
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: ReportStatus = ReportStatus.SUBMITTED
    reporter_id: str
    reporter_name: str
    reporter_email: EmailStr
    reporter_phone: Optional[str] = None
    assigned_officer_id: Optional[str] = None
    assigned_officer_name: Optional[str] = None
    image_urls: List[str] = []
    priority: str = "medium"
    department: str = "others"
    estimated_resolution_time: str = "Within 5 days"
    department_contact: Dict[str, str] = {}
    updates: List[ReportUpdate] = []

# Notification Models
class NotificationCreate(BaseModel):
    title: str
    message: str
    type: NotificationType
    user_id: Optional[str] = None
    issue_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    type: NotificationType
    user_id: Optional[str] = None
    issue_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

class NotificationInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    message: str
    type: NotificationType
    user_id: Optional[str] = None
    issue_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

# Registration Request Models
class RegistrationRequestCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    address: str
    id_number: str
    reason: str
    password: str
    user_type: str = "public"
    department: Optional[str] = None
    designation: Optional[str] = None

class RegistrationRequestResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str
    address: str
    id_number: str
    reason: str
    request_date: datetime
    status: RegistrationStatus
    admin_response: Optional[str] = None
    response_date: Optional[datetime] = None
    responded_by: Optional[str] = None
    user_type: str
    department: Optional[str] = None
    designation: Optional[str] = None

class RegistrationRequestInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    full_name: str
    email: EmailStr
    phone: str
    address: str
    id_number: str
    reason: str
    password_hash: str
    request_date: datetime = Field(default_factory=datetime.utcnow)
    status: RegistrationStatus = RegistrationStatus.NOTIFIED
    admin_response: Optional[str] = None
    response_date: Optional[datetime] = None
    responded_by: Optional[str] = None
    user_type: str = "public"
    department: Optional[str] = None
    designation: Optional[str] = None

# Password Reset Request Models
class PasswordResetRequestCreate(BaseModel):
    email: EmailStr
    reason: str
    new_password: str

class PasswordResetRequestResponse(BaseModel):
    id: str
    email: EmailStr
    reason: str
    request_date: datetime
    status: str
    admin_response: Optional[str] = None
    response_date: Optional[datetime] = None
    responded_by: Optional[str] = None

class PasswordResetRequestInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    email: EmailStr
    reason: str
    new_password_hash: str
    request_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
    admin_response: Optional[str] = None
    response_date: Optional[datetime] = None
    responded_by: Optional[str] = None

# Need Request Models (for citizens requesting help)
class NeedRequestCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    urgency_level: str = "medium"
    contact_info: str
    preferred_response: str

class NeedRequestResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    location: str
    urgency_level: str
    contact_info: str
    preferred_response: str
    status: str
    created_at: datetime
    updated_at: datetime
    requester_id: str
    assigned_officer_id: Optional[str] = None

class NeedRequestInDB(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str
    category: str
    location: str
    urgency_level: str = "medium"
    contact_info: str
    preferred_response: str
    status: str = "submitted"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    requester_id: str
    assigned_officer_id: Optional[str] = None

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None