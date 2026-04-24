# Handles storing and retrieving financial summaries
# Uses a dictionary (in-memory) to store summaries by user_id

class FinancialSummaryRepository:
    def __init__(self):
        # Dictionary to store summaries: { user_id: FinancialSummary }
        self.summaries = {}

    def save_summary(self, summary):
        # Save or overwrite the summary for a user
        self.summaries[summary.user_id] = summary
        return summary

    def get_summary_by_user_id(self, user_id):
        # Return the summary for a user, or None if not found
        return self.summaries.get(user_id)

    def delete_summary(self, user_id):
        # Delete a summary; raise an error if it doesn't exist
        if user_id not in self.summaries:
            raise ValueError("Summary not found")
        del self.summaries[user_id]
        return True
