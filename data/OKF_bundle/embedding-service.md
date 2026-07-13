---
type: Service
title: embedding-service
description: Converts text into vector representations for retrieval and similarity search.
tags: [ml, embeddings, platform]
timestamp: 2026-07-01T00:00:00Z
---

# embedding-service

## Overview
The embedding-service converts text into vector representations for use in retrieval and similarity search. It is used by agent-orchestrator for RAG-based agent tasks and by internal search tooling.

## Owner
Platform Team - ML Infrastructure squad

## Dependencies
- None (stateless compute service; loads model weights on startup)

## Endpoints
- POST /embed - convert a batch of text inputs into vectors
- GET /embed/model-info - return the currently loaded model name and version

## Related
- Depended on by [agent-orchestrator](agent-orchestrator.md)
- See [embedding-service-throughput](embedding-service-throughput.md) for current performance
- See [scale-embedding-service](scale-embedding-service.md) for scaling procedure
- See [incident-high-latency](incident-high-latency.md) for known incident history