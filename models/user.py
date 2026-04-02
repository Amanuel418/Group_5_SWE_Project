from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    email: str
    password_hash: str
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True