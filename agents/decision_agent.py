class DecisionAgent:
    def decide(self, score, fraud, fraud_reason):

        # Fraud always rejected
        if fraud:
            return "Rejected", fraud_reason

        # Skill threshold
        if score >= 60:
            return "Shortlisted", "Qualified"

        return "Rejected", "Insufficient skill match"
