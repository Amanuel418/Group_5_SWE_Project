from datetime import date
from typing import List, Optional

from models.subscription import Subscription
from repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.subscription_repository = subscription_repository

    def create_subscription(
        self,
        user_id: str,
        name: str,
        cost: float,
        billing_frequency: str,
        renewal_date: date,
        category: str
    ) -> Subscription:
        if not name or not name.strip():
            raise ValueError("Subscription name cannot be empty.")

        if cost < 0:
            raise ValueError("Subscription cost cannot be negative.")

        if billing_frequency not in {"monthly", "yearly", "weekly"}:
            raise ValueError("Invalid billing frequency.")

        duplicate = self.subscription_repository.find_duplicate(user_id, name)
        if duplicate is not None:
            raise ValueError("Duplicate subscription already exists.")

        subscription = Subscription(
            user_id=user_id,
            name=name,
            cost=cost,
            billing_frequency=billing_frequency,
            renewal_date=renewal_date,
            category=category
        )
        self.subscription_repository.add_subscription(subscription)
        return subscription

    def view_subscriptions(self, user_id: str) -> List[Subscription]:
        return self.subscription_repository.get_by_user_id(user_id)

    def update_subscription(
        self,
        subscription_id: str,
        name: Optional[str] = None,
        cost: Optional[float] = None,
        billing_frequency: Optional[str] = None,
        renewal_date: Optional[date] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Subscription:
        subscription = self.subscription_repository.get_by_id(subscription_id)
        if subscription is None:
            raise ValueError("Subscription not found.")

        if name is not None:
            if not name.strip():
                raise ValueError("Subscription name cannot be empty.")
            subscription.name = name

        if cost is not None:
            if cost < 0:
                raise ValueError("Subscription cost cannot be negative.")
            subscription.cost = cost

        if billing_frequency is not None:
            if billing_frequency not in {"monthly", "yearly", "weekly"}:
                raise ValueError("Invalid billing frequency.")
            subscription.billing_frequency = billing_frequency

        if renewal_date is not None:
            subscription.renewal_date = renewal_date

        if category is not None:
            if not category.strip():
                raise ValueError("Category cannot be empty.")
            subscription.category = category

        if is_active is not None:
            subscription.is_active = is_active

        self.subscription_repository.update_subscription(subscription)
        return subscription

    def delete_subscription(self, subscription_id: str) -> bool:
        self.subscription_repository.delete_subscription(subscription_id)
        return True