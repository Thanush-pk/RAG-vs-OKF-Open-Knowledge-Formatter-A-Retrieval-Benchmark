---
type: Architecture
title: on-call-process
description: Describes how the Platform Team handles incident escalation.
tags: [architecture, on-call, process]
timestamp: 2026-07-01T00:00:00Z
---

# on-call-process

## Overview
Describes how the Platform Team handles incident escalation outside of business hours.

## Escalation Steps
1. An alert fires from the observability stack when a metric breaches its target (e.g. [p99-latency-orders-api](p99-latency-orders-api.md) or [auth-failure-rate](auth-failure-rate.md)).
2. The on-call engineer acknowledges the alert within 10 minutes.
3. The engineer follows the relevant runbook — [incident-high-latency](incident-high-latency.md), [rollback-procedure](rollback-procedure.md), or [rotate-api-keys](rotate-api-keys.md) depending on the alert type.
4. If unresolved within 30 minutes, the engineer escalates to the squad lead for the affected service.
5. A post-incident summary is logged after resolution.

## Related
- See [system-architecture-overview](system-architecture-overview.md) for the services this process covers
- See [notification-service](notification-service.md) — delivery failures here also trigger this process