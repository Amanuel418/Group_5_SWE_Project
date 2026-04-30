from datetime import datetime
from models.budget import Budget
from database import get_connection


class BudgetRepository:
    def save_budget(self, budget: Budget) -> Budget:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO BUDGETS (user_id, monthly_limit, warning_threshold, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                monthly_limit     = excluded.monthly_limit,
                warning_threshold = excluded.warning_threshold,
                created_at        = excluded.created_at
            """,
            (
                budget.user_id,
                budget.monthly_limit,
                budget.warning_threshold,
                budget.created_at.isoformat(),
            ),
        )
        conn.commit()
        conn.close()
        return budget

    def get_budget_by_user_id(self, user_id: str) -> Budget | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM BUDGETS WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return Budget(
            user_id=row["user_id"],
            monthly_limit=row["monthly_limit"],
            warning_threshold=row["warning_threshold"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def delete_budget(self, user_id: str) -> bool:
        conn = get_connection()
        cur = conn.execute(
            "SELECT user_id FROM BUDGETS WHERE user_id = ?", (user_id,)
        )
        if cur.fetchone() is None:
            conn.close()
            raise ValueError("Budget not found")
        conn.execute("DELETE FROM BUDGETS WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True