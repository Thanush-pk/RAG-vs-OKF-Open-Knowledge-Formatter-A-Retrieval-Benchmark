---
type: Metric
title: embedding-service-throughput
description: Requests per second embedding-service can process.
tags: [metric, throughput, embedding-service]
timestamp: 2026-07-01T00:00:00Z
---

# embedding-service-throughput

## Overview
Number of text embedding requests the embedding-service can process per second under normal load.

## Current Value
850 requests/sec

## Target
1000 requests/sec (to support projected agent growth)

## Measured By
Load testing suite, run weekly against a staging replica

## Related
- Metric for [embedding-service](embedding-service.md)
- See [scale-embedding-service](scale-embedding-service.md) — scaling procedure to increase this