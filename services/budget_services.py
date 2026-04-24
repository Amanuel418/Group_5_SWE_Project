from models.budget import Budget


class BudgetService:
    def __init__(self, budget_repository):
        self.budget_repository = budget_repository

    def set_monthly_budget(self, user_id, monthly_limit, warning_threshold=80.0):
        budget = Budget(
            user_id=user_id,
            monthly_limit=monthly_limit,
            warning_threshold=warning_threshold
        )
        return self.budget_repository.save_budget(budget)

    def view_budget(self, user_id):
        budget = self.budget_repository.get_budget_by_user_id(user_id)
        if budget is None:
            raise ValueError("Budget not found")
        return budget

    def update_budget(self, user_id, monthly_limit=None, warning_threshold=None):
        budget = self.view_budget(user_id)

        new_limit = budget.monthly_limit if monthly_limit is None else monthly_limit
        new_threshold = budget.warning_threshold if warning_threshold is None else warning_threshold

        updated_budget = Budget(
            user_id=user_id,
            monthly_limit=new_limit,
            warning_threshold=new_threshold
        )

        return self.budget_repository.save_budget(updated_budget)

    def compare_spending_to_budget(self, user_id, current_spending):
        if not isinstance(current_spending, (int, float)):
            raise ValueError("Current spending must be a number")

        if current_spending < 0:
            raise ValueError("Current spending cannot be negative")

        budget = self.view_budget(user_id)

        percentage_used = round((current_spending / budget.monthly_limit) * 100, 2) if budget.monthly_limit > 0 else 0

        if current_spending > budget.monthly_limit:
            status = "Over Budget"
        elif percentage_used >= budget.warning_threshold:
            status = "Warning"
        else:
            status = "Within Budget"

        return {
            "monthly_limit": budget.monthly_limit,
            "current_spending": current_spending,
            "percentage_used": percentage_used,
            "status": status
        }

    def delete_budget(self, user_id):
        return self.budget_repository.delete_budget(user_id)