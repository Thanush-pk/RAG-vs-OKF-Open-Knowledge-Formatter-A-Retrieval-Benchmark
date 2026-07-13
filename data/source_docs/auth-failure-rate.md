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