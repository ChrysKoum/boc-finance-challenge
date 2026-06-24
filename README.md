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
├── frontend/
│   ├── src/
│   │   └── main.jsx
│   ├── Dockerfile
│   └── package.json
├── Caddyfile
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
docker compose up --build caddy
docker compose --profile tools run --rm csharp-client
docker compose --profile tools run --rm java-processor
```

The local Compose setup exposes Caddy on port `80`. The FastAPI service stays internal to Docker and is not published directly on port `8000`.

Local checks:

```bash
curl http://localhost/health
curl -X POST http://localhost/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"local-001\",\"question\":\"How do I save money?\"}"
```

## API examples

Safe question:

```bash
curl -X POST http://localhost:8000/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"12345\",\"question\":\"How do I save money?\"}"
```

When using Docker Compose through Caddy, use:

```bash
curl -X POST http://localhost/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"12345\",\"question\":\"How do I save money?\"}"
```

Live demo API example:

```bash
curl -X POST https://api-boc.chryskoum.engineer/api/v1/finance/ask \
  -H "Content-Type: application/json" \
  -d "{\"correlationId\":\"live-demo-001\",\"question\":\"How do I save money?\"}"
```

Example response:

```json
{
  "correlationId": "live-demo-001",
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

## Optional Live Demo

An optional lightweight frontend is included for manually testing the API in a browser. The main challenge scope remains the Python API, C# client, and Java processor.

Live demo:

```text
Frontend: https://boc.chryskoum.engineer/
API health: https://api-boc.chryskoum.engineer/health
API endpoint: https://api-boc.chryskoum.engineer/api/v1/finance/ask
```

Run the demo through Docker Compose:

```bash
docker compose up -d --build caddy
```

Open the frontend:

```text
http://localhost
```

Test the API through the reverse proxy:

```bash
curl http://localhost/health
```

The frontend API URL can be configured with:

```text
VITE_API_BASE_URL=https://api.example.com
```

For a hosted demo, Caddy can route:

```text
example.com -> frontend
api.example.com -> FastAPI API
```

Only Caddy should expose public ports `80` and `443`; the FastAPI container remains internal on port `8000`.

Stop the demo:

```bash
docker compose down
```

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
