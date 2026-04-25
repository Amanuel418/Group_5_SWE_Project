# Handles the business logic for UC11 - View Financial Summary
# Uses the repository to save/retrieve and calculates the total cost

from models.FinancialSummary import FinancialSummary

class FinancialSummaryService:
    def __init__(self, financial_summary_repository):
        self.financial_summary_repository = financial_summary_repository

    def create_summary(self, user_id, subscription_costs):
        # Create a new FinancialSummary object (validation happens inside the model)
        summary = FinancialSummary(
            user_id=user_id,
            subscription_costs=subscription_costs
        )
        return self.financial_summary_repository.save_summary(summary)

    def view_summary(self, user_id):
        # Get the saved summary for a user
        summary = self.financial_summary_repository.get_summary_by_user_id(user_id)
        if summary is None:
            raise ValueError("Summary not found")
        return summary

    def calculate_total(self, user_id):
        # Add up all subscription costs and return the total
        summary = self.view_summary(user_id)
        total = round(sum(summary.subscription_costs), 2)
        return {
            "user_id": user_id,
            "subscription_costs": summary.subscription_costs,
            "total_cost": total
        }

    def delete_summary(self, user_id):
        # Delete the summary for a user
        return self.financial_summary_repository.delete_summary(user_id)
