from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date, datetime

from database import init_db
from repositories.user_repository import UserRepository
from repositories.subscription_repository import SubscriptionRepository
from repositories.budget_repository import BudgetRepository
from services.auth_services import AuthService
from services.subscription_services import SubscriptionService
from services.budget_services import BudgetService
from services.dashboard_service import DashboardService

app = Flask(__name__)
app.secret_key = "budget_optimizer_secret_key"

# ── Initialize database on startup ──────────────────────────────────────────
init_db()

# ── Set up repositories and services ────────────────────────────────────────
user_repo         = UserRepository()
sub_repo          = SubscriptionRepository()
budget_repo       = BudgetRepository()

auth_service      = AuthService(user_repo)
sub_service       = SubscriptionService(sub_repo)
budget_service    = BudgetService(budget_repo)
dashboard_service = DashboardService(sub_repo)


# ── Helper: check if user is logged in ──────────────────────────────────────
def get_current_user_id():
    """Return the logged-in user's ID from the Flask session, or None."""
    session_id = session.get("session_id")
    if not session_id:
        return None
    try:
        return auth_service.get_user_id_from_session(session_id)
    except ValueError:
        return None


# ── Auth routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Redirect to dashboard if logged in, otherwise go to login page."""
    if get_current_user_id():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email    = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")
        try:
            auth_service.register_user(email, password, confirm)
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "")
        password = request.form.get("password", "")
        try:
            user_session = auth_service.login(email, password)
            session["session_id"] = user_session.session_id
            return redirect(url_for("dashboard"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session_id = session.get("session_id")
    if session_id:
        try:
            auth_service.logout(session_id)
        except ValueError:
            pass
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ── Dashboard ────────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))

    summary = dashboard_service.get_dashboard_summary(user_id)

    # Get budget status if a budget exists
    budget_status = None
    try:
        budget = budget_service.view_budget(user_id)
        budget_status = budget_service.compare_spending_to_budget(
            user_id, summary["total_monthly_cost"]
        )
    except ValueError:
        pass  # No budget set yet

    return render_template("dashboard.html", summary=summary, budget_status=budget_status)


# ── Subscription routes ──────────────────────────────────────────────────────

@app.route("/subscriptions")
def subscriptions():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))
    subs = sub_service.view_subscriptions(user_id)
    return render_template("subscriptions.html", subscriptions=subs)


@app.route("/subscriptions/add", methods=["GET", "POST"])
def add_subscription():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            renewal_date = datetime.strptime(
                request.form.get("renewal_date", ""), "%Y-%m-%d"
            ).date()
            sub_service.create_subscription(
                user_id=user_id,
                name=request.form.get("name", ""),
                cost=float(request.form.get("cost", 0)),
                billing_frequency=request.form.get("billing_frequency", ""),
                renewal_date=renewal_date,
                category=request.form.get("category", ""),
            )
            flash("Subscription added!", "success")
            return redirect(url_for("subscriptions"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("add_subscription.html")


@app.route("/subscriptions/edit/<subscription_id>", methods=["GET", "POST"])
def edit_subscription(subscription_id):
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))

    sub = sub_repo.get_by_id(subscription_id)
    if not sub or sub.user_id != user_id:
        flash("Subscription not found.", "error")
        return redirect(url_for("subscriptions"))

    if request.method == "POST":
        try:
            renewal_date = datetime.strptime(
                request.form.get("renewal_date", ""), "%Y-%m-%d"
            ).date()
            sub_service.update_subscription(
                subscription_id=subscription_id,
                name=request.form.get("name", ""),
                cost=float(request.form.get("cost", 0)),
                billing_frequency=request.form.get("billing_frequency", ""),
                renewal_date=renewal_date,
                category=request.form.get("category", ""),
            )
            flash("Subscription updated!", "success")
            return redirect(url_for("subscriptions"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("edit_subscription.html", sub=sub)


@app.route("/subscriptions/delete/<subscription_id>", methods=["POST"])
def delete_subscription(subscription_id):
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))
    try:
        sub_service.delete_subscription(subscription_id)
        flash("Subscription deleted.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("subscriptions"))


# ── Budget routes ────────────────────────────────────────────────────────────

@app.route("/budget", methods=["GET", "POST"])
def budget():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            monthly_limit      = float(request.form.get("monthly_limit", 0))
            warning_threshold  = float(request.form.get("warning_threshold", 80))
            budget_service.set_monthly_budget(user_id, monthly_limit, warning_threshold)
            flash("Budget saved!", "success")
            return redirect(url_for("budget"))
        except ValueError as e:
            flash(str(e), "error")

    current_budget = None
    budget_status  = None
    try:
        current_budget = budget_service.view_budget(user_id)
        summary        = dashboard_service.get_dashboard_summary(user_id)
        budget_status  = budget_service.compare_spending_to_budget(
            user_id, summary["total_monthly_cost"]
        )
    except ValueError:
        pass

    return render_template("budget.html", budget=current_budget, budget_status=budget_status)


if __name__ == "__main__":
    app.run(debug=True)