from typing import List, Optional
from datetime import datetime, date
from models.subscription import Subscription
from database import get_connection


class SubscriptionRepository:
    def add_subscription(self, subscription: Subscription) -> None:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO SUBSCRIPTIONS
                (subscription_id, user_id, name, cost, billing_frequency,
                 renewal_date, category, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subscription.subscription_id,
                subscription.user_id,
                subscription.name,
                subscription.cost,
                subscription.billing_frequency,
                subscription.renewal_date.isoformat(),
                subscription.category,
                int(subscription.is_active),
                subscription.created_at.isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def get_by_id(self, subscription_id: str) -> Optional[Subscription]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM SUBSCRIPTIONS WHERE subscription_id = ?",
            (subscription_id,),
        ).fetchone()
        conn.close()
        return self._row_to_sub(row) if row else None

    def get_by_user_id(self, user_id: str) -> List[Subscription]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM SUBSCRIPTIONS WHERE user_id = ?", (user_id,)
        ).fetchall()
        conn.close()
        return [self._row_to_sub(r) for r in rows]

    def update_subscription(self, subscription: Subscription) -> None:
        conn = get_connection()
        cur = conn.execute(
            "SELECT subscription_id FROM SUBSCRIPTIONS WHERE subscription_id = ?",
            (subscription.subscription_id,),
        )
        if cur.fetchone() is None:
            conn.close()
            raise ValueError("Subscription does not exist.")
        conn.execute(
            """
            UPDATE SUBSCRIPTIONS
            SET name = ?, cost = ?, billing_frequency = ?,
                renewal_date = ?, category = ?, is_active = ?
            WHERE subscription_id = ?
            """,
            (
                subscription.name,
                subscription.cost,
                subscription.billing_frequency,
                subscription.renewal_date.isoformat(),
                subscription.category,
                int(subscription.is_active),
                subscription.subscription_id,
            ),
        )
        conn.commit()
        conn.close()

    def delete_subscription(self, subscription_id: str) -> None:
        conn = get_connection()
        cur = conn.execute(
            "SELECT subscription_id FROM SUBSCRIPTIONS WHERE subscription_id = ?",
            (subscription_id,),
        )
        if cur.fetchone() is None:
            conn.close()
            raise ValueError("Subscription does not exist.")
        conn.execute(
            "DELETE FROM SUBSCRIPTIONS WHERE subscription_id = ?",
            (subscription_id,),
        )
        conn.commit()
        conn.close()

    def find_duplicate(self, user_id: str, name: str) -> Optional[Subscription]:
        normalized = name.strip().lower()
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT * FROM SUBSCRIPTIONS
            WHERE user_id = ? AND is_active = 1
            """,
            (user_id,),
        ).fetchall()
        conn.close()
        for row in rows:
            if row["name"].strip().lower() == normalized:
                return self._row_to_sub(row)
        return None

    def _row_to_sub(self, row) -> Subscription:
        return Subscription(
            subscription_id=row["subscription_id"],
            user_id=row["user_id"],
            name=row["name"],
            cost=row["cost"],
            billing_frequency=row["billing_frequency"],
            renewal_date=date.fromisoformat(row["renewal_date"]),
            category=row["category"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )