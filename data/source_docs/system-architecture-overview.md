# system-architecture-overview

## Overview
High-level overview of how the AI Platform Team's services fit together.

## Core Services
- [auth-service](auth-service.md) — validates identity for every other service
- [orders-api](orders-api.md) — handles the e-commerce checkout write path
- [agent-orchestrator](agent-orchestrator.md) — manages AI agent lifecycle and task routing
- [embedding-service](embedding-service.md) — provides vector embeddings for agents and search
- [notification-service](notification-service.md) — sends emails and push notifications

## Request Flow
A typical request enters through orders-api or agent-orchestrator, is authenticated by auth-service, and may trigger downstream calls to embedding-service (for agent tasks) or notification-service (for order confirmations).

## Related
- See [data-flow-orders](data-flow-orders.md) for a detailed walkthrough of one request path
- See [agent-lifecycle](agent-lifecycle.md) for how agents move through the system
- See [on-call-process](on-call-process.md) for how incidents are handled across these services