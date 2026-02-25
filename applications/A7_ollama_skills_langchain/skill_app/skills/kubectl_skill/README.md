# kubectl Skill

A comprehensive skill for helping with Kubernetes kubectl commands and cluster operations.

## Purpose

This skill provides the agent with detailed knowledge about:
- Common kubectl commands for resource management
- Debugging and troubleshooting Kubernetes pods and deployments
- Best practices for safe cluster operations
- Context and namespace management
- Service and networking commands

## When to Use

The agent will automatically consider this skill when users ask about:
- kubectl commands
- Kubernetes operations
- Pod, deployment, or service management
- Container logs and debugging
- Cluster troubleshooting

## Coverage

### Resource Management
- Viewing and listing resources (pods, deployments, services)
- Creating and updating resources
- Scaling and managing deployments
- Rollout and rollback operations

### Debugging
- Viewing logs
- Describing resources
- Checking events
- Executing commands in containers
- Port forwarding

### Configuration
- Context switching
- Namespace management
- Cluster configuration

### Safety Features
- Warns about destructive operations
- Reminds about namespace context
- Suggests dry-run previews
- Provides rollback instructions

## Format

Uses Anthropic skill format with YAML frontmatter for automatic loading and discovery.
