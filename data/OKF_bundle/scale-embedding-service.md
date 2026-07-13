---
type: Runbook
title: scale-embedding-service
description: Procedure for scaling embedding-service horizontally.
tags: [runbook, scaling, embedding-service]
timestamp: 2026-07-01T00:00:00Z
---

# scale-embedding-service

## Overview
Procedure for scaling embedding-service horizontally when throughput approaches capacity.

## Owner
Platform Team - ML Infrastructure squad

## Steps
1. Check [embedding-service-throughput](embedding-service-throughput.md) to confirm the service is near its target ceiling.
2. Increase the replica count for embedding-service in the Kubernetes deployment config.
3. Confirm new replicas pass health checks and are receiving traffic via the load balancer.
4. Re-run the load testing suite to confirm the new throughput ceiling.
5. Update [embedding-service-throughput](embedding-service-throughput.md) with the new baseline once confirmed.

## Related
- See [embedding-service](embedding-service.md) for the owning service
- See [incident-high-latency](incident-high-latency.md) — a past incident where this procedure was triggered