---
type: Metric
title: auth-failure-rate
description: Percentage of failed login attempts against auth-service.
tags: [metric, security, auth-service]
timestamp: 2026-07-01T00:00:00Z
---

# auth-failure-rate

## Overview
Percentage of login attempts against auth-service that fail, including both invalid credentials and system errors.

## Current Value
2.1%

## Target
Under 3% (values are expected to include normal user error; system-error failures are tracked separately)

## Measured By
auth-service request logs, aggregated hourly

## Related
- Metric for [auth-service](auth-service.md)
- See [rotate-api-keys](rotate-api-keys.md) — key rotation can cause temporary spikes in this metric