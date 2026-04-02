from typing import Dict, Optional
from models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._users_by_id: Dict[str, User] = {}
        self._users_by_email: Dict[str, User] = {}

    def add_user(self, user: User) -> None:
        if user.email in self._users_by_email:
            raise ValueError("A user with this email already exists.")
        self._users_by_id[user.user_id] = user
        self._users_by_email[user.email] = user

    def get_by_email(self, email: str) -> Optional[User]:
        return self._users_by_email.get(email)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users_by_id.get(user_id)