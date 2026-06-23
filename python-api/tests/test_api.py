from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_finance_ask_endpoint_allows_safe_question() -> None:
    response = client.post(
        "/api/v1/finance/ask",
        json={
            "correlationId": "api-safe-1",
            "question": "How do I save money?",
        },
    )

    assert response.status_code == 200
    assert response.json()["correlationId"] == "api-safe-1"
    assert response.json()["blocked"] is False


def test_finance_ask_endpoint_blocks_unsafe_question() -> None:
    response = client.post(
        "/api/v1/finance/ask",
        json={
            "correlationId": "api-blocked-1",
            "question": "How do I hack a bank?",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "correlationId": "api-blocked-1",
        "answer": "Sorry, I cannot help with that.",
        "blocked": True,
    }
