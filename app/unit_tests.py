import pytest
from fastapi.testclient import TestClient
from src.main import app
import json
from httpx import AsyncClient, ASGITransport

client = TestClient(app)

# Test data
THEMES_PAYLOAD = [
    {
        "title": "Technical support",
        "description": "The customer is calling for technical support",
    },
    {"title": "Billing", "description": "The customer is calling for billing issues"},
    {"title": "Refund", "description": "The customer is calling for a refund"},
]


# Use Case 1
def test_classify_success():
    payload = {
        "text": "I am calling because I have a problem with my internet connection",
        "themes": THEMES_PAYLOAD,
    }
    response = client.post("/api/v1/classify", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "chosen_theme" in data
    assert data["chosen_theme"]["title"] == "Technical support"


# Use Case 2
def test_form_completion_logic():
    transcript = "Customer: My name is John Doe. I'd prefer not to share my gender. Email: johndoe@example.com."
    payload = {"text": transcript}

    response = client.post("/api/v1/complete-form", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["personal_info"]["first_name"] == "John"
    assert data["personal_info"]["gender"] is None


# Bonus 1 : 1
def test_probabilistic_classification():
    payload = {"text": "I have an issue with my bill", "themes": THEMES_PAYLOAD}
    # Test de l'approche avec itérations
    response = client.post("/api/v1/classify-probabilistic?iterations=3", json=payload)
    assert response.status_code == 200
    assert "confidence" in response.json()


# Bonus 1 : 2
def test_probabilistic_cross_model_voting():
    payload = {"text": "I want a refund", "themes": THEMES_PAYLOAD}

    response = client.post("/api/v1/classify-probabilistic-2", json=payload)
    assert response.status_code == 200
    assert "confidence" in response.json()


# Bonus 3
@pytest.mark.asyncio
async def test_streaming_form():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"text": "Name: Alice Smith. Email: alice@test.com"}
        async with ac.stream(
            "POST", "/api/v1/complete-form-stream", json=payload
        ) as response:
            assert response.status_code == 200

            last_chunk = None
            async for line in response.aiter_lines():
                if line:
                    clean_line = line.replace("data:", "").strip()
                    try:
                        last_chunk = json.loads(clean_line)
                    except json.JSONDecodeError:
                        continue

            assert last_chunk is not None
            assert "Alice" in last_chunk["personal_info"]["first_name"]


# Bonus 2
def test_generalized_extraction():
    payload = {
        "text": "Toyota Corolla 2015, plate ABC-1234",
        "schema_description": {"car_brand": "The brand", "plate": "The license plate"},
    }
    response = client.post("/api/v1/extract-generalized", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["car_brand"].lower() == "toyota"
    assert "plate" in data
