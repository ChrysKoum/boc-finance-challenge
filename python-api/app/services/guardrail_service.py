class GuardrailService:
    BLOCKED_TERMS = (
        "hack",
        "fraud",
        "scam",
        "steal",
        "money laundering",
    )

    def is_blocked(self, message: str) -> bool:
        normalized_message = message.lower()
        return any(term in normalized_message for term in self.BLOCKED_TERMS)
