from app.models import FinanceAskRequest, FinanceAskResponse
from app.services.guardrail_service import GuardrailService


class FinanceService:
    def __init__(self, guardrail_service: GuardrailService | None = None) -> None:
        self._guardrail_service = guardrail_service or GuardrailService()

    def answer(self, request: FinanceAskRequest) -> FinanceAskResponse:
        if self._guardrail_service.is_blocked(request.question):
            return FinanceAskResponse(
                correlation_id=request.correlation_id,
                answer="Sorry, I cannot help with that.",
                blocked=True,
            )

        return FinanceAskResponse(
            correlation_id=request.correlation_id,
            answer=self._get_guidance(request.question),
            blocked=False,
        )

    def _get_guidance(self, question: str) -> str:
        normalized_question = question.lower()

        if "save" in normalized_question or "saving" in normalized_question:
            return "Start by saving a small amount regularly and build an emergency fund."

        if "budget" in normalized_question:
            return "Create a simple monthly budget that tracks income, essentials, savings, and discretionary spending."

        if "invest" in normalized_question or "investment" in normalized_question:
            return "Consider your goals, time horizon, and risk tolerance before investing."

        if "loan" in normalized_question or "debt" in normalized_question:
            return "Review interest rates, repayment terms, and affordability before taking on debt."

        return "For general financial wellbeing, track your spending, save regularly, and seek professional advice for important decisions."
