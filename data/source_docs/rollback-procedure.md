# rollback-procedure

## Overview
Standard procedure for rolling back a bad deployment across platform services.

## Owner
Platform Team - on-call engineer

## Applies To
- [orders-api](orders-api.md)
- [agent-orchestrator](agent-orchestrator.md)

## Steps
1. Identify the last known-good version from the CI/CD deployment history.
2. Trigger a rollback via the deployment pipeline to that version.
3. Confirm the rollback completed by checking the service's health endpoint.
4. Monitor the relevant metric for the affected service (e.g. [p99-latency-orders-api](p99-latency-orders-api.md) or [agent-success-rate](agent-success-rate.md)) for 15 minutes post-rollback.
5. Notify the on-call channel and update the incident log.

## Related
- See [incident-high-latency](incident-high-latency.md) — an example incident where this procedure was used
- See [on-call-process](on-call-process.md) for escalation context