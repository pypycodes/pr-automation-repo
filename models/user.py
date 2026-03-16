"""
User model for the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from utils.helpers import validate_email, generate_hash

@dataclass
class User:
    """User data model."""
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    roles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate user data after initialization."""
        if not validate_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")
        
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")
    
    @property
    def user_hash(self) -> str:
        """Generate unique hash for user."""
        return generate_hash(f"{self.id}:{self.username}:{self.email}")
    
    def add_role(self, role: str) -> None:
        """Add a role to the user."""
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.utcnow()
    
    def remove_role(self, role: str) -> None:
        """Remove a role from the user."""
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'roles': self.roles,
            'user_hash': self.user_hash
        }
