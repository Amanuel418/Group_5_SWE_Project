import json
from models.FinancialSummary import FinancialSummary
from database import get_connection


class FinancialSummaryRepository:
    def save_summary(self, summary: FinancialSummary) -> FinancialSummary:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO FINANCIAL_SUMMARIES (user_id, subscription_costs)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                subscription_costs = excluded.subscription_costs
            """,
            (summary.user_id, json.dumps(summary.subscription_costs)),
        )
        conn.commit()
        conn.close()
        return summary

    def get_summary_by_user_id(self, user_id: str) -> FinancialSummary | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM FINANCIAL_SUMMARIES WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return FinancialSummary(
            user_id=row["user_id"],
            subscription_costs=json.loads(row["subscription_costs"]),
        )

    def delete_summary(self, user_id: str) -> bool:
        conn = get_connection()
        cur = conn.execute(
            "SELECT user_id FROM FINANCIAL_SUMMARIES WHERE user_id = ?", (user_id,)
        )
        if cur.fetchone() is None:
            conn.close()
            raise ValueError("Summary not found")
        conn.execute(
            "DELETE FROM FINANCIAL_SUMMARIES WHERE user_id = ?", (user_id,)
        )
        conn.commit()
        conn.close()
        return True