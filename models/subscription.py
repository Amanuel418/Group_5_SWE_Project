from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid


VALID_FREQUENCIES = {"monthly", "yearly", "weekly"}


@dataclass
class Subscription:
    user_id: str
    name: str
    cost: float
    billing_frequency: str
    renewal_date: date
    category: str
    subscription_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Subscription name cannot be empty.")

        if self.cost < 0:
            raise ValueError("Subscription cost cannot be negative.")

        if self.billing_frequency not in VALID_FREQUENCIES:
            raise ValueError(
                f"Invalid billing frequency. Must be one of {VALID_FREQUENCIES}."
            )

        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty.")