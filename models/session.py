from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid


@dataclass
class Session:
    user_id: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=12))
    is_active: bool = True

    def is_valid(self) -> bool:
        return self.is_active and datetime.utcnow() < self.expires_at