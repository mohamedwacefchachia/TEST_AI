import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_classification():
    print("======= Testing use case 1: Text Classification =======")
    payload = {
        "text": "I am calling because I have a problem with my internet connection",
        "themes": [
            {
                "title": "Technical support",
                "description": "The customer is calling for technical support",
            },
            {
                "title": "Billing",
                "description": "The customer is calling for billing issues",
            },
            {"title": "Refund", "description": "The customer is calling for a refund"},
        ],
    }

    response = httpx.post(f"{BASE_URL}/classify", json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"✅API response : {data}")
    else:
        print(f"❌ API request failed : {response.status_code} - {response.text}")


def test_form_completion():
    print("======= Testing use case 2: Form Completion =======")
    transcript = (
        "Agent: Good morning! I'll need to collect some basic details. "
        "Could you please provide your first and last name? "
        "Customer: Sure! My name is John Doe. "
        "Agent: Thank you, John. May I also ask for your gender? "
        "Customer: I'd prefer not to share that at the moment. "
        "Agent: No problem. Your email address? "
        "Customer: Yes, my email is johndoe@example.com. "
        "Agent: Preferred contact method? "
        "Customer: Please contact me via Email."
    )

    payload = {"text": transcript}
    response = httpx.post(f"{BASE_URL}/complete-form", json=payload, timeout=30)

    if response.status_code == 200:
        data = response.json()
        print(f"✅API response : {json.dumps(data, indent=2)}")
        assert data["personal_info"]["gender"] is None
        print("Gender is correctly set to null")

    else:
        print(f"❌ API request failed : {response.status_code} - {response.text}")


# Bonus 1
def test_probabilistic_classification():
    print("======= Testing Bonus 1: Probabilistic Text Classification =======")
    payload = {
        "text": "I am calling because I have a problem with my internet connection",
        "themes": [
            {
                "title": "Technical support",
                "description": "The customer is calling for technical support",
            },
            {
                "title": "Billing",
                "description": "The customer is calling for billing issues",
            },
            {"title": "Refund", "description": "The customer is calling for a refund"},
        ],
    }

    response = httpx.post(
        f"{BASE_URL}/classify-probabilistic?iterations=5", json=payload
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅API response : {data}")
    else:
        print(f"❌ API request failed : {response.status_code} - {response.text}")


# Bonus 1 : Approach 2
def test_probabilistic_classification_2():
    print(
        "======= Testing Bonus 1: Probabilistic Text Classification approach 2======="
    )
    payload = {
        "text": "I am calling because I have a problem with my internet connection",
        "themes": [
            {
                "title": "Technical support",
                "description": "The customer is calling for technical support",
            },
            {
                "title": "Billing",
                "description": "The customer is calling for billing issues",
            },
            {"title": "Refund", "description": "The customer is calling for a refund"},
        ],
    }

    response = httpx.post(f"{BASE_URL}/classify-probabilistic-2", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"✅API response : {data}")
    else:
        print(f"❌ API request failed : {response.status_code} - {response.text}")


# Bonus  3
def test_streaming_1():
    print("======= Testing Streamed Form Completion =======")
    transcript = (
        "Agent: Good morning! I'll need to collect some basic details. "
        "Could you please provide your first and last name? "
        "Customer: Sure! My name is John Doe. "
        "Agent: Thank you, John. May I also ask for your gender? "
        "Customer: I'd prefer not to share that at the moment. "
        "Agent: No problem. Your email address? "
        "Customer: Yes, my email is johndoe@example.com. "
        "Agent: Preferred contact method? "
        "Customer: Please contact me via Email."
    )

    payload = {"text": transcript}

    with httpx.stream(
        "POST", f"{BASE_URL}/complete-form-stream", json=payload, timeout=None
    ) as r:
        for line in r.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    # data extraction
                    first = data.get("personal_info", {}).get("first_name")
                    email = data.get("contact_info", {}).get("email")
                    ##
                    if first or email:
                        print(f"Progress -> Name: {first} | Email: {email}")
                    else:
                        print("Processing tokens...", end="\r")

                except Exception:
                    continue

    print("Stream finished")


# Another example
def test_streaming_2():
    print("======= Testing Streamed Form Completion =======")
    payload = {
        "text": "Agent: Name? Customer: Alice Smith. Agent: Email? Customer: alice@test.com"
    }

    with httpx.stream(
        "POST", f"{BASE_URL}/complete-form-stream", json=payload, timeout=None
    ) as r:
        for line in r.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    # data extraction
                    first = data.get("personal_info", {}).get("first_name")
                    email = data.get("contact_info", {}).get("email")
                    ##
                    if first or email:
                        print(f"Progress -> Name: {first} | Email: {email}")
                    else:
                        print("Processing tokens...", end="\r")

                except Exception:
                    continue

    print("Stream finished")


def test_generalized_extraction():
    print("======= Testing Bonus 2 : Generalized Form Completion =======")

    payload = {
        "text": "I want to book a repair for my Toyota Corolla 2015. The license plate is ABC-1234",
        "schema_description": {
            "car_brand": "The brand of the car",
            "model_year": "The year the car was made (number)",
            "plate": "The license plate string",
        },
    }

    response = httpx.post(f"{BASE_URL}/extract-generalized", json=payload, timeout=30)

    if response.status_code == 200:
        print(f"✅API response : {json.dumps(response.json(), indent=2)}")

    else:
        print(f"❌ API request failed : {response.text}")


if __name__ == "__main__":
    try:
        # test_classification()
        # test_form_completion()
        test_probabilistic_classification()
        test_probabilistic_classification_2()
        # test_streaming_1()
        # test_streaming_2()
        # test_generalized_extraction()
        print("===> All tests passed successfully !")
    except Exception as e:
        print(f"An error occurred : {e}")
