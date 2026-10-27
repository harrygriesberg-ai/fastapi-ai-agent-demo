# Architecture Notes

This document complements the main README with the architectural intent behind the example. The repository is deliberately compact, but dependencies point inward toward application behavior and outward integrations stay behind adapters.

## Flow

```text
User -> Planner -> ToolCall -> Registry -> Validation -> Tool -> Observation -> Planner -> FinalAnswer
```

## Module ownership

| Module | Owns |
|---|---|
| `providers/planner.py` | Planning decision interface |
| `tools/` | Allowlisted capabilities and argument schemas |
| `services/agent_service.py` | Bounded execution loop |
| `schemas/agent.py` | Decision, response, and trace contracts |

## Boundary rules

1. Validate untrusted data at the boundary closest to where it enters.
2. Keep provider/tool/database SDK objects out of public API schemas and core application services.
3. Prefer deterministic code for authorization, validation, limits, and invariants.
4. Make important AI behavior observable through source metadata, traces, reports, request IDs, or audit events.
5. Make local tests independent of paid/network services whenever possible.

## How to evolve this repository

Add tools by registering ordinary typed capabilities. Keep policy/authorization outside the planner; repository 05 demonstrates that boundary.

When adding a new concern, first decide which layer owns it. For example, HTTP authentication belongs near the transport/application boundary; provider retry classification belongs around the provider call; and business policy belongs in deterministic application code. Avoid solving every new requirement by expanding the prompt or adding conditions to one route handler.

## Production-shape vs. production-complete

This repository demonstrates maintainable boundaries, not a universal deployment blueprint. Real systems may need persistent databases, queues, secret managers, distributed tracing, tenant-aware authorization, rate limits, model routing, content policies, and deployment-specific health checks. Those additions should strengthen the existing boundaries rather than collapse them.
