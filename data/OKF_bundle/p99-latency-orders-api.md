---
type: Metric
title: p99-latency-orders-api
description: 99th-percentile response latency for orders-api.
tags: [metric, latency, orders-api]
timestamp: 2026-07-01T00:00:00Z
---

# p99-latency-orders-api

## Overview
99th-percentile response latency for the orders-api service, measured across all endpoints.

## Current Value
420ms (as of last measurement window)

## Target
Under 300ms

## Measured By
Platform observability stack, sampled every 60 seconds from orders-api request logs

## Related
- Metric for [orders-api](orders-api.md)
- See [incident-high-latency](incident-high-latency.md) — this metric breached target during the last incident