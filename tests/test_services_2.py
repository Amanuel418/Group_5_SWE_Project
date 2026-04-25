import pytest
from datetime import date
from models.budget import Budget
from models.FinancialSummary import FinancialSummary
from repositories.budget_repository import BudgetRepository
from repositories.FinancialSummary_repository import FinancialSummaryRepository
from services.budget_services import BudgetService
from services.FinancialSummary_service import FinancialSummaryService

@pytest.fixture
def budget_service():
    budget_repo = BudgetRepository()
    return BudgetService(budget_repo)

@pytest.fixture
def financial_summary_service():
    financial_summary_repo = FinancialSummaryRepository()
    return FinancialSummaryService(financial_summary_repo)

# --- Use Case 6: Manage Budget ---
def test_budget_success_under_limit(budget_service):
    budget_service.set_monthly_budget("newuser@gmail.com", 100.00)
    assert budget_service.compare_spending_to_budget("newuser@gmail.com", 70.00)["status"] == "Within Budget"

def test_budget_success_under_limit_threshold_warning(budget_service):
    budget_service.set_monthly_budget("newuser@gmail.com", 100.00)
    assert budget_service.compare_spending_to_budget("newuser@gmail.com", 80.00)["status"] == "Warning"

def test_budget_success_over_limit(budget_service):
    budget_service.set_monthly_budget("newuser@gmail.com", 100.00)
    assert budget_service.compare_spending_to_budget("newuser@gmail.com", 120.00)["status"] == "Over Budget"

def test_budget_negative_budget(budget_service):
    with pytest.raises(ValueError, match="Monthly budget cannot be negative"):
        budget_service.set_monthly_budget("newuser@gmail.com", -500.00)

def test_budget_negative_spending(budget_service):
    budget_service.set_monthly_budget("newuser@gmail.com", 200.00)
    with pytest.raises(ValueError, match="Current spending cannot be negative"):
        budget_service.compare_spending_to_budget("newuser@gmail.com", -10.00)

def test_budget_invalid_budget(budget_service):
    with pytest.raises(ValueError, match="Monthly budget must be a number"):
        budget_service.set_monthly_budget("newuser@gmail.com", None)

def test_budget_invalid_spending(budget_service):
    budget_service.set_monthly_budget("newuser@gmail.com", 100.00)
    with pytest.raises(ValueError, match="Current spending must be a number"):
        budget_service.compare_spending_to_budget("newuser@gmail.com", None)

# --- Use Case 11: Budget Summary --- 
def test_financial_summary_success(financial_summary_service):
    financial_summary_service.create_summary("newuser@gmail.com", [15.99, 9.99, 54.99])
    assert financial_summary_service.calculate_total("newuser@gmail.com")["total_cost"] == 80.97

def test_financial_summary_success_v2(financial_summary_service):
    financial_summary_service.create_summary("newuser@gmail.com", [])
    assert financial_summary_service.calculate_total("newuser@gmail.com")["total_cost"] == 0.00

def test_financial_summary_success_v3(financial_summary_service):
    financial_summary_service.create_summary("newuser@gmail.com", [20.00, 30.00])
    assert financial_summary_service.calculate_total("newuser@gmail.com")["total_cost"] == 50.00

def test_financial_summary_invalid_cost(financial_summary_service):
    with pytest.raises(ValueError, match="Error: Invalid cost value"):
        financial_summary_service.create_summary("newuser@gmail.com", [15.99, -5.00])

def test_financial_summary_missing_cost(financial_summary_service):
    with pytest.raises(ValueError, match="Error: Cost value is required."):
        financial_summary_service.create_summary("newuser@gmail.com", [15.99, None])

def test_financial_summary_missing_data(financial_summary_service):
    with pytest.raises(ValueError, match="Error: Subscription data is required"):
        financial_summary_service.create_summary("newuser@gmail.com", None)