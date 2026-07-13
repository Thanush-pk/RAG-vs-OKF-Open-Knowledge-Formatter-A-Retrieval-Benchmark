---
type: Service
title: orders-api
description: Handles creation, retrieval, and status updates for customer orders.
tags: [orders, checkout, platform]
timestamp: 2026-07-01T00:00:00Z
---

# orders-api

## Overview
The orders-api service handles creation, retrieval, and status updates for customer orders. It is the primary write path for the e-commerce checkout flow.

## Owner
Platform Team - Order Processing squad

## Dependencies
- auth-service (validates request tokens before processing)
- notification-service (triggers order confirmation emails)

## Endpoints
- POST /orders - create a new order
- GET /orders/{id} - retrieve order status
- PATCH /orders/{id} - update order status

## Related
- See [p99-latency-orders-api](p99-latency-orders-api.md) for current performance
- See [incident-high-latency](incident-high-latency.md) for known incident history
- See [rollback-procedure](rollback-procedure.md) for deployment rollback steps
- See [data-flow-orders](data-flow-orders.md) for how orders move through the system