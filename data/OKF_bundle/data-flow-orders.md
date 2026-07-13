---
type: Architecture
title: data-flow-orders
description: Walks through how a single customer order moves through the platform.
tags: [architecture, orders, data-flow]
timestamp: 2026-07-01T00:00:00Z
---

# data-flow-orders

## Overview
Walks through how a single customer order moves through the platform, end to end.

## Flow
1. A client sends a request to orders-api to create a new order.
2. orders-api calls auth-service to validate the request token.
3. Once validated, orders-api writes the order record and returns a confirmation.
4. orders-api triggers notification-service to send an order confirmation email.
5. Order status updates are available via orders-api's GET endpoint for the lifetime of the order.

## Related
- See [orders-api](orders-api.md), [auth-service](auth-service.md), [notification-service](notification-service.md) for the services involved
- See [system-architecture-overview](system-architecture-overview.md) for the broader platform context