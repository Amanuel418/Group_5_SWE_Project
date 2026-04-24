# The data model for a financial summary
# Stores the list of subscription costs for a user

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FinancialSummary:
    user_id: str
    subscription_costs: List[Optional[float]]  # list of subscription costs

    def __post_init__(self):
        # Make sure user_id is a non-empty string
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID is required")

        # Make sure subscription_costs is provided (not None)
        if self.subscription_costs is None:
            raise ValueError("Error: Subscription data is required.")

        # Check each cost in the list
        for cost in self.subscription_costs:
            if cost is None:
                raise ValueError("Error: Cost value is required.")
            if not isinstance(cost, (int, float)):
                raise ValueError("Error: Invalid cost value.")
            if cost < 0:
                raise ValueError("Error: Invalid cost value.")