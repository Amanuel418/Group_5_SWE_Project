from dataclasses import dataclass
from datetime import datetime


@dataclass
class Budget:
    user_id: str
    monthly_limit: float
    warning_threshold: float = 80.0
    created_at: datetime = datetime.now()

    def __post_init__(self):
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID is required")

        if not isinstance(self.monthly_limit, (int, float)):
            raise ValueError("Monthly budget must be a number")

        if self.monthly_limit < 0:
            raise ValueError("Monthly budget cannot be negative")

        if not isinstance(self.warning_threshold, (int, float)):
            raise ValueError("Warning threshold must be a number")

        if self.warning_threshold < 0 or self.warning_threshold > 100:
            raise ValueError("Warning threshold must be between 0 and 100")