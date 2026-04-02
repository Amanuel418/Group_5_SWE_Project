from typing import Dict, List, Optional
from models.subscription import Subscription


class SubscriptionRepository:
    def __init__(self) -> None:
        self._subscriptions: Dict[str, Subscription] = {}

    def add_subscription(self, subscription: Subscription) -> None:
        self._subscriptions[subscription.subscription_id] = subscription

    def get_by_id(self, subscription_id: str) -> Optional[Subscription]:
        return self._subscriptions.get(subscription_id)

    def get_by_user_id(self, user_id: str) -> List[Subscription]:
        return [
            subscription
            for subscription in self._subscriptions.values()
            if subscription.user_id == user_id
        ]

    def update_subscription(self, subscription: Subscription) -> None:
        if subscription.subscription_id not in self._subscriptions:
            raise ValueError("Subscription does not exist.")
        self._subscriptions[subscription.subscription_id] = subscription

    def delete_subscription(self, subscription_id: str) -> None:
        if subscription_id not in self._subscriptions:
            raise ValueError("Subscription does not exist.")
        del self._subscriptions[subscription_id]

    def find_duplicate(self, user_id: str, name: str) -> Optional[Subscription]:
        normalized_name = name.strip().lower()
        for subscription in self._subscriptions.values():
            if (
                subscription.user_id == user_id
                and subscription.name.strip().lower() == normalized_name
                and subscription.is_active
            ):
                return subscription
        return None