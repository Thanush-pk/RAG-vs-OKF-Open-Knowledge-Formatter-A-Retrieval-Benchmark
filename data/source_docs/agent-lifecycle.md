# agent-lifecycle

## Overview
Describes the full lifecycle of an AI agent on the platform, from deployment to retirement.

## Lifecycle Stages
1. **Registration** — a new agent type is registered with agent-orchestrator (see [deploy-new-agent](deploy-new-agent.md)).
2. **Active** — the agent receives tasks routed by agent-orchestrator, using embedding-service for any retrieval-based work.
3. **Idle** — agent-orchestrator scales down agent instances with no assigned tasks to save resources.
4. **Retirement** — an agent type is deregistered when replaced by a newer version or no longer needed.

## Related
- See [agent-orchestrator](agent-orchestrator.md) for the service managing this lifecycle
- See [deploy-new-agent](deploy-new-agent.md) for the registration procedure
- See [agent-success-rate](agent-success-rate.md) and [daily-active-agents](daily-active-agents.md) for lifecycle-related metrics