class BudgetRepository:
    def __init__(self):
        self.budgets = {}

    def save_budget(self, budget):
        self.budgets[budget.user_id] = budget
        return budget

    def get_budget_by_user_id(self, user_id):
        return self.budgets.get(user_id)

    def delete_budget(self, user_id):
        if user_id not in self.budgets:
            raise ValueError("Budget not found")
        del self.budgets[user_id]
        return True