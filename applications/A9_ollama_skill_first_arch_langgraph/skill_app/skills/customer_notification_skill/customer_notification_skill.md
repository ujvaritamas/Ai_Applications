---
name: customer_notification_skill
description: Manages and troubleshoots the customer notification service. Use this skill when users ask about customer notification service diagnostics, health checks, or any related operations.
---

# Customer Notification Service Health Check

## Required Actions (Execute Immediately):

1. Call `list_customer_notifications` with namespace="kcp-system"
2. Call `list_customer_notification_pods` with namespace="kcp-system"

## After Getting Results:

Analyze the results:
- ✅ Service is OK if: pod is Running AND all CRs have status "Succeeded"
- ❌ Service has issues if: pod is not Running OR any CR has status "Error", "InProgress", or "Cancelled"

Report:
- Pod status
- List of CRs with non-Succeeded status (if any)
- Overall health: OK or Issues
- If overall health is "Issues", include all tool response details

## Output Formatting (Terminal Display):

**Table Format for Custom Resources:**
```
┌─────────────────────────────┬────────────┐
│ CR Name                     │ Status     │
├─────────────────────────────┼────────────┤
│ notification-config-001     │ Succeeded  │
│ notification-config-002     │ Error      │
└─────────────────────────────┴────────────┘
```

**Color Coding:**
- Overall Health Status: Use 🔴 RED/❌ for "Issues", 🟢 GREEN/✅ for "OK"
- Use ANSI color codes for terminal output:
  - Green (`\033[92m`) for healthy/succeeded
  - Red (`\033[91m`) for issues/errors
  - Reset (`\033[0m`) after colored text

**Summary Format:**
```
Overall Health: [🟢 OK | 🔴 Issues]
Pod Status: [Running/Not Running]
CR Issues: [count] of [total]
```