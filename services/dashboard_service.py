from datetime import date
from typing import Dict, List

from models.subscription import Subscription
from repositories.subscription_repository import SubscriptionRepository


class DashboardService:
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.subscription_repository = subscription_repository

    def _monthly_equivalent(self, subscription: Subscription) -> float:
        if subscription.billing_frequency == "monthly":
            return subscription.cost
        if subscription.billing_frequency == "yearly":
            return round(subscription.cost / 12, 2)
        if subscription.billing_frequency == "weekly":
            return round(subscription.cost * 52 / 12, 2)
        return 0.0

    def get_dashboard_summary(self, user_id: str) -> Dict:
        subscriptions = [
            sub
            for sub in self.subscription_repository.get_by_user_id(user_id)
            if sub.is_active
        ]

        total_monthly_cost = round(
            sum(self._monthly_equivalent(sub) for sub in subscriptions), 2
        )

        upcoming_renewals = sorted(
            subscriptions,
            key=lambda sub: sub.renewal_date
        )

        return {
            "active_subscription_count": len(subscriptions),
            "total_monthly_cost": total_monthly_cost,
            "upcoming_renewals": [
                {
                    "name": sub.name,
                    "renewal_date": sub.renewal_date.isoformat(),
                    "cost": sub.cost,
                    "billing_frequency": sub.billing_frequency,
                }
                for sub in upcoming_renewals
            ]
        }