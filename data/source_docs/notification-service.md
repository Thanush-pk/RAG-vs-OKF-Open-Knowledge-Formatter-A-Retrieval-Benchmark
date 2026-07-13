# notification-service

## Overview
The notification-service sends transactional emails and push notifications — order confirmations, account changes, and agent task completion alerts. It is a downstream consumer of events from orders-api and agent-orchestrator.

## Owner
Platform Team - Comms squad

## Dependencies
- auth-service (validates internal service requests)

## Endpoints
- POST /notifications/email - send a transactional email
- POST /notifications/push - send a push notification
- GET /notifications/{id}/status - check delivery status

## Related
- Depended on by [orders-api](orders-api.md)
- See [on-call-process](on-call-process.md) for escalation if delivery failures spike