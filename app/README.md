# **🚀 AI-Powered Data Extraction Pipeline**


## 🌟 Introduction
This project implements a robust API for processing textual data using advanced language models (LLMs). It addresses two critical use cases :
1. **Text classification** : Dynamic categorization based on provided themes with explanation of reasoning.
2. **Entity extraction (Form Completion)** : Transforming a conversation transcript into a structured JSON form.

### ⚙️ Technical stack 
* **Infrastructure** : [UV](https://docs.astral.sh/uv/) for modern and deterministic project management.
* **LLM Inference** : [AWS Bedrock](https://aws.amazon.com/fr/bedrock/) With **Claude Haiku 4.5, Claude Opus 4.5 and Claude Sonnet 4.5**.
* **Structured generation** : [BAML](https://docs.boundaryml.com/) to ensure JSON schema compliance and prompt separation.
* **API Framework** : [FastAPI](https://fastapi.tiangolo.com/)
* **Observability & Tracing** : [Langfuse](https://langfuse.com/) to monitor LLM calls, trace reasoning steps, and track token consumption in real time.
* **Unit Testing** : [PyTest](https://docs.pytest.org/en/stable/) for comprehensive, automated unit testing of our FastAPI endpoints.
* **Linter And Code Formatter** : [Ruff](https://docs.astral.sh/ruff/) to detects unused variables, sorts imports alphabetically, and formats code.

---

## 📂  Project structure

The project is organised in such a way as to strictly separate the transport layer (API), business logic (Services) and AI model definition (BAML).

```text
.
├── baml_src/                # Core LLM logic (Boundary ML)
│   ├── classify.baml        # Logic and prompts for Use Case 1
│   ├── clients.baml         # AWS Bedrock clients configuration
│   ├── common.baml          # Reusable instructions (Global Guardrails)
│   ├── dynamic_extraction.baml # Logic and prompts for Bonus 2
│   ├── extraction.baml      # Logic and prompts for Use Case 2
│   └── types.baml           # Data schema definitions
├── src/                     # FastAPI Application
│   ├── main.py              # API initialization and middlewares
│   ├── routes.py            # API endpoints definition
│   └── services.py          # Orchestration between API and BAML client
├── Dockerfile               # Containerisation
├── pyproject.toml           # Dependency manifest (managed by UV)
├── uv.lock                  # Dependency lockfile for reproducibility
└── README.md                # Project documentation

```

## ⚙️ Environnement Configuration

The project uses `uv` to ensure that the environment is identical on all machines.

### 1. Prerequisites
* **Python 3.12** installed
* **UV** installed : `curl -LsSf https://astral.sh/uv/install.sh | sh`
* **AWS CLI** configured : `aws configure` (with `bedrock:InvokeModel` permissions enabled).
* **BAML** : BAML extension for improved structured generation development.
* **Docker** installed and running.

### 2. Installation and Build
Since the repository contains `pyproject.toml` and `uv.lock`, installation is simplified. :

```bash
# Install the environment and dependencies
uv sync

# Generate the BAML client (required for Python import)
uv run baml generate

# Check that everything is in order(Optional but recommended)
uv run baml check
```

=> Running **BAML commands** produces a baml_client/ folder. This directory contains the generated SDK that bridges your .baml schemas and the Python application. It provides an asynchronous interface and Pydantic models that guarantee compile-time type safety.

**⚠️ Warning** : This folder is an automatic build artefact. Any manual changes will be overwritten during the next generation.


## 🚀 Lancement et Tests locaux

**Starting the API**

```bash
uv run python -m src.main
```

* The API is now available at http://localhost:8000. Go to http://localhost:8000/docs to test it via the Swagger interface.

**Testing with Python code examples**

* You can use the `tests.py` file located at the root of the project to run tests against all implemented APIs. Feel free to extend or modify these tests as needed.

* Once the application is running, open a new terminal and execute: 

```bash
uv run python tests.py
```


**Testing With cURL**

**Use Case 1 : Text Classification**

```bash
curl -X POST http://localhost:8000/api/v1/classify \
-H "Content-Type: application/json" \
-d '{
    "text": "I am calling because I have a problem with my internet connection",
    "themes": [
        {"title": "Technical support", "description": "The customer is calling for technical support"},
        {"title": "Billing", "description": "The customer is calling for billing issues"},
        {"title": "Refund", "description": "The customer is calling for a refund"}
    ]
}'
```

**Use Case 2 : Form Completion**

```bash
curl -X POST http://localhost:8000/api/v1/complete-form \
-H "Content-Type: application/json" \
-d '{
    "text": "Agent: Good morning! I need your name. Customer: My name is John Doe. Agent: Your gender? Customer: I prefer not to share. Agent: Email? Customer: johndoe@example.com. Agent: Preferred contact? Customer: Email."
}'
```

**🧪 Unit Testing**

* You can execute unit tests using the following command : 

```bash
uv run pytest unit_tests.py
```

**🔍 Code Quality (Linting & Formatting)**

* To ensure high readability and maintain standards, I use Ruff. It identifies unused variables, sorts imports alphabetically, and enforces a consistent code style.

```bash
# Analyze linting errors
uv run ruff check . --fix
# Automatically fixes detected errors
uv run ruff check . --fix
# Format the code
uv run ruff format .       
```


## 💡 Design Choices

### A. Structured Generation with BAML
Rather than using raw text prompts within the Python code, I opted for **BAML**. This allows :
* **Type-Safety** : The types defined in `.baml` generate a typed Python client, reducing runtime errors.
* **Separation of concerns** : `Prompt Engineering` has its own lifecycle, independent of the FastAPI application logic.

### B. Advanced Prompt Engineering
To ensure the reliability of the LLM's responses, I implemented :
* **Few-Shot Learning** : Inclusion of reference examples to guide the model on the expected format and tone.
* **Chain of Thought (CoT)** : The model is forced to generate a `model_reasoning` field before the final result, which significantly improves the accuracy of complex classifications.

### C. AWS-Native Architecture
* **AWS Bedrock** : Chosen for its security and compliance.
* **IAM Roles** : The application is configured to use local AWS credentials or instance roles, thus avoiding the storage of API keys in plain text.

### D. Data Quality Management
* **Universal Guardrails** : Using `template_string` to inject security and privacy guidelines across the board.
* **Handling of Nulls** : Strict management of optional values has been implemented to differentiate between data that is missing and data that has been explicitly refused by the user.

## 📈 Potential improvements

- **Agentic Workflows** : Transitioning from simple extraction to a reasoning agent capable of self-correcting extraction errors.
- **Advanced Memory Management** : Using persistent memory to handle context across multiple sessions.
- **LLM Evaluation** : Implementing a dedicated evaluation suite to benchmark extraction precision across different models.
- **PII Redaction**: Adding a pre-processing layer to detect and mask Personally Identifiable Information (PII) before sending data to the LLM provider, ensuring GDPR compliance.
- **Multi-modal Support**: Extending the pipeline to process unstructured data from images or PDFs using Vision models, rather than relying solely on raw text.
