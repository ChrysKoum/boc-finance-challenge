from app.models import FinanceAskRequest
from app.services.finance_service import FinanceService
from app.services.guardrail_service import GuardrailService


def test_blocks_unsafe_terms() -> None:
    guardrails = GuardrailService()

    assert guardrails.is_blocked("How do I hack a bank?")
    assert guardrails.is_blocked("Explain money laundering")
    assert guardrails.is_blocked("How to commit fraud?")


def test_allows_safe_financial_question() -> None:
    guardrails = GuardrailService()

    assert not guardrails.is_blocked("How do I save money each month?")


def test_finance_service_returns_blocked_response() -> None:
    service = FinanceService()

    response = service.answer(
        FinanceAskRequest(
            correlationId="test-123",
            question="How can someone scam a customer?",
        )
    )

    assert response.correlation_id == "test-123"
    assert response.blocked is True
    assert response.answer == "Sorry, I cannot help with that."


def test_finance_service_returns_safe_guidance() -> None:
    service = FinanceService()

    response = service.answer(
        FinanceAskRequest(
            correlationId="test-456",
            question="How do I save money?",
        )
    )

    assert response.correlation_id == "test-456"
    assert response.blocked is False
    assert "saving" in response.answer.lower()
