from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_agent_uses_weather_tool_then_finishes() -> None:
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "What is the weather in Melbourne?", "max_steps": 4},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["steps_used"] == 2
    assert body["trace"][0]["tool_name"] == "weather"
    assert "Tool result" in body["answer"]


def test_direct_answer_uses_one_step() -> None:
    response = client.post("/api/v1/agent/run", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json()["steps_used"] == 1
