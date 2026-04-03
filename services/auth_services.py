from typing import Dict, Optional
import hashlib

from models.user import User
from models.session import Session
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
        self.active_sessions: Dict[str, Session] = {}

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register_user(self, email: str, password: str) -> User:
        if not email or not email.strip():
            raise ValueError("Email is required.")

        if not password or not password.strip():
            raise ValueError("Password is required.")

        if self.user_repository.get_by_email(email) is not None:
            raise ValueError("Email is already registered.")

        user = User(
            email=email.strip().lower(),
            password_hash=self._hash_password(password)
        )
        self.user_repository.add_user(user)
        return user

    def login(self, email: str, password: str) -> Session:
        if not email or not password:
            raise ValueError("Email and password are required.")

        user = self.user_repository.get_by_email(email.strip().lower())
        if user is None:
            raise ValueError("Invalid email or password.")

        hashed_password = self._hash_password(password)
        if user.password_hash != hashed_password:
            raise ValueError("Invalid email or password.")

        session = Session(user_id=user.user_id)
        self.active_sessions[session.session_id] = session
        return session

    def logout(self, session_id: str) -> bool:
        session = self.active_sessions.get(session_id)
        if session is None:
            raise ValueError("Session not found.")

        session.is_active = False
        return True

    def is_authenticated(self, session_id: str) -> bool:
        session = self.active_sessions.get(session_id)
        return session is not None and session.is_valid()

    def get_user_id_from_session(self, session_id: str) -> str:
        if not self.is_authenticated(session_id):
            raise ValueError("User is not authenticated.")
        return self.active_sessions[session_id].user_id