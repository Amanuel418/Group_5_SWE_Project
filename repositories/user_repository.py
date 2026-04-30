from typing import Optional
from datetime import datetime
from models.user import User
from database import get_connection


class UserRepository:
    def add_user(self, user: User) -> None:
        conn = get_connection()
        try:
            conn.execute(
                """
                INSERT INTO USERS (user_id, email, password_hash, created_at, is_active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user.user_id,
                    user.email,
                    user.password_hash,
                    user.created_at.isoformat(),
                    int(user.is_active),
                ),
            )
            conn.commit()
        except Exception:
            conn.close()
            raise ValueError("A user with this email already exists.")
        conn.close()

    def get_by_email(self, email: str) -> Optional[User]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM USERS WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return self._row_to_user(row)

    def get_by_id(self, user_id: str) -> Optional[User]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM USERS WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return self._row_to_user(row)

    def _row_to_user(self, row) -> User:
        return User(
            email=row["email"],
            password_hash=row["password_hash"],
            user_id=row["user_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            is_active=bool(row["is_active"]),
        )