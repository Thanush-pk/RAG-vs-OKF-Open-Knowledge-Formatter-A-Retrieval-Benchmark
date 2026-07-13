---
type: Service
title: auth-service
description: Handles user authentication and session management for the platform.
tags: [identity, security, platform]
timestamp: 2026-07-01T00:00:00Z
---

# auth-service

## Overview
The auth-service handles user authentication and session management — login, logout, account creation, and account deletion. It is the security gatekeeper for the platform: every request to orders-api, agent-orchestrator, and notification-service must first be validated here.

## Owner
Platform Team - Identity & Security squad

## Dependencies
- user-database (stores credentials and account records)

## Manages
- OAuth token issuance and validation
- Session credentials
- Account security policies

## Endpoints
- POST /auth/login
- POST /auth/logout
- POST /auth/accounts
- DELETE /auth/accounts/{id}

## Related
- Depended on by [orders-api](orders-api.md), [agent-orchestrator](agent-orchestrator.md), [notification-service](notification-service.md)
- See [rotate-api-keys](rotate-api-keys.md) for credential rotation procedure
- See [auth-failure-rate](auth-failure-rate.md) for current metrics