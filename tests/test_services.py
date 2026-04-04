import pytest
from datetime import date
from models.user import User
from models.session import Session
from models.subscription import Subscription
from repositories.user_repository import UserRepository
from repositories.subscription_repository import SubscriptionRepository
from services.auth_services import AuthService
from services.subscription_services import SubscriptionService

@pytest.fixture
def auth_service():
    user_repo = UserRepository()
    return AuthService(user_repo)

@pytest.fixture
def sub_service():
    sub_repo = SubscriptionRepository()
    return SubscriptionService(sub_repo)

# --- Use Case 1: User Registration ---

def test_register_success(auth_service):
    user = auth_service.register_user("newuser@gmail.com", "xft123%PLM", "xft123%PLM")
    assert user.email == "newuser@gmail.com"

def test_register_mismatch(auth_service):
    with pytest.raises(ValueError, match="Passwords do not match"):
        auth_service.register_user("newuser@gmail.com", "xft123%PLM", "wrongPass123")

def test_register_short_password(auth_service):
    with pytest.raises(ValueError, match="Password must be between 8 and 12 characters"):
        auth_service.register_user("newuser@gmail.com", "zzzzzzz", "zzzzzzz")

def test_register_empty_password(auth_service):
    with pytest.raises(ValueError, match="Password is required"):
        auth_service.register_user("newuser@gmail.com", "", "")

def test_register_duplicate_email(auth_service):
    auth_service.register_user("olduser@gmail.com", "xft123%PLM", "xft123%PLM")
    with pytest.raises(ValueError, match="Email is already registered"):
        auth_service.register_user("olduser@gmail.com", "xft123%PLM", "xft123%PLM")

# --- Use Case 2: Add Subscription ---

def test_add_subscription_success(sub_service):
    sub = sub_service.create_subscription("user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment")
    assert sub.name == "Netflix"
    assert sub.cost == 15.99

def test_add_subscription_empty_name(sub_service):
    with pytest.raises(ValueError, match="Subscription name cannot be empty"):
        sub_service.create_subscription("user123", "", 15.99, "monthly", date(2026, 4, 10), "Entertainment")

def test_add_subscription_duplicate(sub_service):
    sub_service.create_subscription("user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment")
    with pytest.raises(ValueError, match="Duplicate subscription already exists"):
        sub_service.create_subscription("user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment")

def test_add_subscription_negative_cost(sub_service):
    with pytest.raises(ValueError, match="Subscription cost cannot be negative"):
        sub_service.create_subscription("user123", "Disney+", -5.00, "monthly", date(2026, 5, 1), "Streaming")

def test_add_subscription_invalid_freq(sub_service):
    with pytest.raises(ValueError, match="Invalid billing frequency"):
        sub_service.create_subscription("user123", "Hulu", 10.00, "daily", date(2026, 6, 1), "Streaming")
