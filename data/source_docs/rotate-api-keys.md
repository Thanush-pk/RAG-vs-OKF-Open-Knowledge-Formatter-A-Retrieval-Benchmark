# rotate-api-keys

## Overview
Procedure for rotating credentials and API keys managed by auth-service.

## Owner
Platform Team - Identity & Security squad

## Steps
1. Generate new credentials via the auth-service admin panel.
2. Distribute new keys to dependent services ([orders-api](orders-api.md), [agent-orchestrator](agent-orchestrator.md), [notification-service](notification-service.md)) through the secrets manager.
3. Deploy dependent services to pick up the new keys.
4. Revoke the old keys after confirming all services are healthy on the new credentials.
5. Monitor [auth-failure-rate](auth-failure-rate.md) for a temporary spike during the transition window.

## Related
- See [auth-service](auth-service.md) for the owning service
- See [on-call-process](on-call-process.md) if failure rate spikes beyond expected levels