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

# --- Use Case 2 ---

# --- Add Subscription ---
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


# ---  View Subscriptions ---

def test_view_subscriptions_success(sub_service):
    sub_service.create_subscription("user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment")
    sub_service.create_subscription("user123", "Spotify", 9.99, "monthly", date(2026, 4, 15), "Music")

    subscriptions = sub_service.view_subscriptions("user123")

    assert len(subscriptions) == 2
    assert subscriptions[0].name == "Netflix"
    assert subscriptions[1].name == "Spotify"


def test_view_subscriptions_empty(sub_service):
    subscriptions = sub_service.view_subscriptions("user999")
    assert subscriptions == []


# --- Update Subscription ---

def test_update_subscription_success(sub_service):
    sub = sub_service.create_subscription(
        "user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment"
    )

    updated_sub = sub_service.update_subscription(
        sub.subscription_id,
        name="Netflix Premium",
        cost=22.99,
        billing_frequency="monthly",
        renewal_date=date(2026, 5, 10),
        category="Streaming"
    )

    assert updated_sub.name == "Netflix Premium"
    assert updated_sub.cost == 22.99
    assert updated_sub.billing_frequency == "monthly"
    assert updated_sub.renewal_date == date(2026, 5, 10)
    assert updated_sub.category == "Streaming"


def test_update_subscription_not_found(sub_service):
    with pytest.raises(ValueError, match="Subscription not found"):
        sub_service.update_subscription(
            "fake-id",
            name="Updated Name"
        )


def test_update_subscription_invalid_name(sub_service):
    sub = sub_service.create_subscription(
        "user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment"
    )

    with pytest.raises(ValueError, match="Subscription name cannot be empty"):
        sub_service.update_subscription(
            sub.subscription_id,
            name=""
        )


def test_update_subscription_negative_cost(sub_service):
    sub = sub_service.create_subscription(
        "user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment"
    )

    with pytest.raises(ValueError, match="Subscription cost cannot be negative"):
        sub_service.update_subscription(
            sub.subscription_id,
            cost=-10.00
        )


def test_update_subscription_invalid_frequency(sub_service):
    sub = sub_service.create_subscription(
        "user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment"
    )

    with pytest.raises(ValueError, match="Invalid billing frequency"):
        sub_service.update_subscription(
            sub.subscription_id,
            billing_frequency="daily"
        )


# --- Delete Subscription ---

def test_delete_subscription_success(sub_service):
    sub = sub_service.create_subscription(
        "user123", "Netflix", 15.99, "monthly", date(2026, 4, 10), "Entertainment"
    )

    result = sub_service.delete_subscription(sub.subscription_id)

    subscriptions = sub_service.view_subscriptions("user123")

    assert result is True
    assert len(subscriptions) == 0


def test_delete_subscription_not_found(sub_service):
    with pytest.raises(ValueError, match="Subscription does not exist"):
        sub_service.delete_subscription("fake-id")