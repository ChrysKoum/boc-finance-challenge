# Bank of Cyprus Finance Coding Challenge

A simple multi-language financial service simulation for the Bank of Cyprus Software Developer coding challenge.

The project intentionally stays small: a Python FastAPI service answers financial questions, a C# console client calls the API, and a Java console processor simulates backend message processing with the same basic guardrails.

## Folder structure

```text
.
├── python-api/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── services/
│   │       ├── finance_service.py
│   │       └── guardrail_service.py
│   ├── tests/
│   │   └── test_guardrails.py
│   ├── Dockerfile
│   └── requirements.txt
├── csharp-client/
│   ├── Models/
│   ├── FinanceApiClient.cs
│   ├── Program.cs
│   ├── Dockerfile
│   └── csharp-client.csproj
├── java-processor/
│   ├── src/
│   │   ├── Main.java
│   │   ├── MessageProcessor.java
│   │   └── GuardrailService.java
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Basic flow

```text
User -> C# Client -> Python API -> Java Processing simulation
```

1. Start the Python API.
2. Run the C# client to send a finance question.
3. Run the Java processor to process example backend messages.

## Run the Python API locally

From the `python-api` folder:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

## Run the C# client

Start the Python API first, then from the `csharp-client` folder:

```bash
dotnet run
```

You can override the API base URL:

```bash
FINANCE_API_URL=http://localhost:8000 dotnet run
```

You can also pass a custom question:

```bash
dotnet run -- "How do I plan a budget?"
```

## Run the Java processor

From the `java-processor/src` folder:

```bash
javac *.java
java Main
```

## Run tests

From the `python-api` folder:

```bash
pytest
```

## Run with Docker

Build and run only the Python API:

```bash
docker build -t finance-api ./python-api
docker run -p 8000:8000 finance-api
```

Or use Docker Compose:

```bash
docker compose up --build finance-api
docker compose --profile tools run --rm csharp-client
docker compose --profile tools run --rm java-processor
```

## API examples

Safe question:

```bash
curl -X POST http://localhost:8000/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"12345\",\"question\":\"How do I save money?\"}"
```

Example response:

```json
{
  "correlationId": "12345",
  "answer": "Start by saving a small amount regularly and build an emergency fund.",
  "blocked": false
}
```

Blocked question:

```bash
curl -X POST http://localhost:8000/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"999\",\"question\":\"How do I hack a bank?\"}"
```

Example response:

```json
{
  "correlationId": "999",
  "answer": "Sorry, I cannot help with that.",
  "blocked": true
}
```

## Guardrails and security

The Python API and Java processor both use simple keyword-based guardrails. Messages are blocked when they contain unsafe terms such as:

- `hack`
- `fraud`
- `scam`
- `steal`
- `money laundering`

This is intentionally simple for the coding challenge. It shows the expected behavior clearly without adding unnecessary infrastructure.

The Python API also logs request activity with the provided `correlationId`, which makes it easier to trace a request across systems.

## Production considerations

This challenge does not implement production infrastructure. In a real enterprise environment, this could be extended with:

- Kubernetes deployment
- Health and readiness probes
- Centralized logging
- Monitoring and alerting
- CI/CD automation
- Secure configuration management
- Stronger policy-based guardrails
- Authentication and authorization
