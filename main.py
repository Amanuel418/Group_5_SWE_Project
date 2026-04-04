from datetime import date

from repositories.user_repository import UserRepository
from repositories.subscription_repository import SubscriptionRepository
from services.auth_services import AuthService
from services.subscription_services import SubscriptionService
from services.dashboard_service import DashboardService


def main():
    # Initialize everything
    user_repo = UserRepository()
    sub_repo = SubscriptionRepository()

    auth_service = AuthService(user_repo)
    sub_service = SubscriptionService(sub_repo)
    dashboard_service = DashboardService(sub_repo)

    print("=== REGISTER USER ===")
    user = auth_service.register_user("amanuel@test.com", "password123", "password123")
    print("User created:", user)

    print("\n=== LOGIN ===")
    session = auth_service.login("amanuel@test.com", "password123")
    print("Session:", session.session_id)

    user_id = auth_service.get_user_id_from_session(session.session_id)

    print("\n=== ADD SUBSCRIPTIONS ===")
    sub1 = sub_service.create_subscription(
        user_id=user_id,
        name="Netflix",
        cost=15.99,
        billing_frequency="monthly",
        renewal_date=date(2026, 3, 10),
        category="Entertainment"
    )

    sub2 = sub_service.create_subscription(
        user_id=user_id,
        name="Spotify",
        cost=120,
        billing_frequency="yearly",
        renewal_date=date(2026, 8, 1),
        category="Music"
    )

    print("Subscriptions added!")

    print("\n=== VIEW SUBSCRIPTIONS ===")
    subs = sub_service.view_subscriptions(user_id)
    for s in subs:
        print(s)

    print("\n=== DASHBOARD ===")
    dashboard = dashboard_service.get_dashboard_summary(user_id)
    print(dashboard)

    print("\n=== LOGOUT ===")
    auth_service.logout(session.session_id)
    print("Logged out successfully")


if __name__ == "__main__":
    main()