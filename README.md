# FastAPI AI Agent Demo — Bounded Planning and Tool Use

> Part of the **Building Reliable AI Applications** educational series. The goal is not to hide complexity behind a framework; it is to make the boundaries of a real AI application visible, testable, and replaceable.

## Overview

A small tool-using agent that makes the agent loop explicit: plan, validate, execute, observe, and either continue or finish. The design includes a maximum step limit and a trace so you can see exactly how a request moved through the system.

This repository is designed for two audiences at the same time: developers who want working source code, and technical readers who want to understand *why* the application is structured this way. The default path avoids external infrastructure wherever possible so a new reader can clone the repository, run it, inspect a request end-to-end, and then replace demo adapters with production implementations.

## What you will learn

- Understand an agent as an application loop rather than a magical model mode
- Validate tool arguments with Pydantic before execution
- Keep tool implementations ordinary Python code
- Bound execution with a maximum step count
- Return an inspectable trace for debugging and evaluation

## Architecture

```text
User -> Planner -> (ToolCall | FinalAnswer)
               | ToolCall -> Registry -> Validate args -> Execute -> Observation -> Planner
               ` FinalAnswer -> Response
```

The exact folder names are less important than the dependency direction. Transport code should not own provider SDK behavior; provider adapters should not decide authorization policy; and probabilistic model output should cross a validation boundary before deterministic application logic relies on it.

## Repository layout

```text
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── providers/
│   │   └── planner.py
│   │
│   ├── schemas/
│   │   └── agent.py
│   │
│   ├── services/
│   │   └── agent_service.py
│   │
│   ├── tools/
│   │   ├── base.py
│   │   ├── calculator.py
│   │   ├── registry.py
│   │   └── weather.py
│   │
│   ├── __init__.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   └── test_agent.py
│
├── .editorconfig
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── Makefile
├── README.md
└── pyproject.toml
```

Every project also includes a license, contribution guide, editor configuration, tests, and a CI workflow so the repository looks and behaves like a maintainable public engineering project rather than a one-file tutorial.

## Requirements

- Python 3.12+ for Python repositories.
- Git for cloning/version control.
- Node.js 20+ is recommended for the React frontend in project 07.
- A model-provider API key is **optional** unless you explicitly switch from local/mock mode to a real provider.

## Quick start

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The default mode is intentionally local/deterministic where applicable, so you can explore the project before configuring a paid provider.

To enable the included OpenAI adapter, install the optional provider extra with `pip install -e ".[openai,dev]"` (or `.[openai]` without development tools), then configure the OpenAI variables below.

## Configuration

Copy `.env.example` to `.env` when you want to override defaults. Do not commit real secrets.

| Variable | Default | Purpose |
|---|---|---|
| `APP_PLANNER_PROVIDER` | `mock` | `mock` or `openai` planner |
| `APP_OPENAI_API_KEY` | `empty` | Required for model-backed planner |
| `APP_OPENAI_MODEL` | `gpt-5` | Planner model identifier |

Environment variables are intentionally explicit. In production, load secrets from your deployment platform or secret manager rather than checking `.env` into source control.

## Main interface

**POST /api/v1/agent/run**

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the weather in Melbourne?","max_steps":4}' 
```

Example output:

```json
{"answer":"Tool result received: ...","steps_used":2,"trace":[{"step":1,"decision_type":"tool","tool_name":"weather","arguments":{"city":"Melbourne"},"observation":{"condition":"clear"}},{"step":2,"decision_type":"final"}]}
```

When the service runs under FastAPI, interactive OpenAPI documentation is available at `/docs` and the machine-readable schema at `/openapi.json`. Those pages are especially useful when experimenting with request validation and response contracts.

## How the request flows through the code

1. **Boundary validation.** User input is parsed into a typed schema before it reaches the core use case.
2. **Application service.** A service coordinates the use case without depending on browser/UI details.
3. **Adapter boundary.** Provider/tool/retrieval integrations live behind small interfaces so they can be replaced or mocked.
4. **Deterministic controls.** Validation, policy, limits, or evaluation checks remain ordinary software logic whenever they should be deterministic.
5. **Observable output.** The response includes enough metadata, tracing, sources, or reports to make failures diagnosable rather than mysterious.

The repository is intentionally explicit about these steps. AI systems become difficult to maintain when model calls, routing, policy, persistence, and HTTP behavior are mixed into a single function.

## Design decisions

- **1.** The planner may *propose* a tool call, but the registry owns validation and actual execution.
- **2.** The agent loop is bounded by `max_steps`, preventing unbounded planning/tool cycles.
- **3.** The trace is first-class output because agent systems are hard to debug without step-level observability.
- **4.** Tools expose descriptions plus argument JSON Schema, keeping the planning interface explicit.

These are not universal rules. They are useful defaults for applications where reliability, testability, and clear ownership of behavior matter more than minimizing the number of files.

## Testing

```bash
pytest
ruff check .
```

Most repositories also provide `make check` as a convenience on systems with `make`.

The tests focus on contracts and behavior rather than the internals of a specific vendor SDK. This is why the repositories default to deterministic local adapters: CI should not require network access, consume model credits, or become flaky because a third-party service is unavailable.

### What to add in a real project

A mature test strategy normally includes unit tests for services/policies, API contract tests, integration tests against non-production dependencies, and an evaluation suite for behavior that cannot be captured by ordinary deterministic assertions. For agent/RAG systems, save representative failure cases and rerun them whenever prompts, models, retrieval settings, or tool definitions change.

## Production considerations and intentional limitations

- The demo does not include authentication or tool-level authorization; the next repository focuses on that boundary.
- The mock planner uses intentionally simple heuristics. It exists to make tests and onboarding deterministic.
- A production agent may need durable state, idempotency keys, background jobs, and cancellation.

The code is therefore best viewed as a **production-shaped reference implementation**, not a claim that every production concern fits in one small repository. The point is to give each concern a clear home so it can be strengthened without rewriting unrelated layers.

## Security notes

- Never expose provider API keys to a browser or commit them to Git.
- Treat model output and tool-call arguments as untrusted input.
- Put authentication/authorization in deterministic server-side code.
- Avoid logging raw prompts by default if they may contain personal, proprietary, or regulated data.
- Rate-limit expensive or externally visible operations.
- For actions with real-world impact, use least privilege, explicit confirmation, idempotency, and auditable server-side decisions.

## Troubleshooting

**The app starts but a provider call fails.** Confirm you selected the intended provider and supplied the matching credential. Start in mock/local mode first to verify the application itself.

**Imports fail when running tests.** Run commands from the repository root and install the project with `pip install -e ".[dev]"`.

**A request returns HTTP 422.** FastAPI/Pydantic rejected the request before the application service ran. Read the validation detail; this is expected boundary protection.

**The demo behaves differently from a production model.** That is intentional. Mock components demonstrate architecture and deterministic tests; replace the adapter, not the whole application.

## Suggested extensions

Good follow-up exercises are to add authentication, persistent storage, OpenTelemetry tracing, rate limiting, provider fallback, deployment manifests, and a real evaluation dataset. Keep each addition behind the same boundaries instead of growing a single “AI service” module indefinitely.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Improvements are welcome when they preserve the repository's educational clarity and production-minded boundaries.

## License

MIT. See [LICENSE](LICENSE).
