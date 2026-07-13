# deploy-new-agent

## Overview
Procedure for deploying a new agent type to the agent-orchestrator platform.

## Owner
Platform Team - Agent Infrastructure squad

## Steps
1. Register the new agent's task schema with agent-orchestrator via the internal admin panel.
2. Confirm the agent's required tools are available through embedding-service and any external MCP servers it depends on.
3. Deploy the agent container image to the staging cluster.
4. Run the agent against the golden test task set to confirm baseline success rate.
5. Promote the image to production via the CI/CD pipeline.
6. Monitor [agent-success-rate](agent-success-rate.md) and [daily-active-agents](daily-active-agents.md) for the first 24 hours after rollout.

## Rollback
If success rate drops more than 5% below baseline, follow [rollback-procedure](rollback-procedure.md) immediately.

## Related
- See [agent-orchestrator](agent-orchestrator.md) for the service this deploys to
- See [agent-lifecycle](agent-lifecycle.md) for how this fits into the broader agent lifecycle