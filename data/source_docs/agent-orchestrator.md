# agent-orchestrator

## Overview
The agent-orchestrator service manages the lifecycle of AI agents on the platform — spinning up new agent instances, routing tasks to them, and tearing them down when idle. It is the control plane for all agent-based workflows.

## Owner
Platform Team - Agent Infrastructure squad

## Dependencies
- auth-service (validates requests before scheduling agent tasks)
- embedding-service (agents use this for retrieval-augmented tasks)

## Endpoints
- POST /agents - launch a new agent instance
- GET /agents/{id} - get agent status
- POST /agents/{id}/tasks - assign a task to a running agent
- DELETE /agents/{id} - terminate an agent instance

## Related
- See [agent-success-rate](agent-success-rate.md) for current performance
- See [daily-active-agents](daily-active-agents.md) for usage metrics
- See [deploy-new-agent](deploy-new-agent.md) for deployment procedure
- See [agent-lifecycle](agent-lifecycle.md) for the full lifecycle process