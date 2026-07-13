---
type: Metric
title: daily-active-agents
description: Count of unique active agent instances in the last 24 hours.
tags: [metric, agents, growth]
timestamp: 2026-07-01T00:00:00Z
---

# daily-active-agents

## Overview
Count of unique agent instances that processed at least one task in the last 24 hours.

## Current Value
1,340

## Target
No fixed target — tracked as a leading indicator of platform growth

## Measured By
agent-orchestrator instance logs, aggregated daily at midnight UTC

## Related
- Metric for [agent-orchestrator](agent-orchestrator.md)
- See [agent-success-rate](agent-success-rate.md) for related quality metric