# incident-high-latency

## Overview
Runbook and historical record for diagnosing and resolving high-latency incidents on orders-api.

## Owner
Platform Team - on-call engineer

## Last Occurrence
orders-api p99 latency breached 400ms threshold for over 20 minutes, traced to a slow downstream call to embedding-service during a load spike.

## Diagnosis Steps
1. Check [p99-latency-orders-api](p99-latency-orders-api.md) to confirm the breach.
2. Check [embedding-service-throughput](embedding-service-throughput.md) for signs of saturation.
3. If embedding-service is saturated, follow [scale-embedding-service](scale-embedding-service.md).
4. If the cause is a bad orders-api deployment instead, follow [rollback-procedure](rollback-procedure.md).

## Related
- See [orders-api](orders-api.md) for the affected service
- See [embedding-service](embedding-service.md) for the dependency involved in the last occurrence