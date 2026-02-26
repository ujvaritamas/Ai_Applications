---
name: kubectl-skill
description: Helps with Kubernetes kubectl commands and cluster operations. Use when users ask about managing pods, deployments, services, debugging issues, viewing logs, or any Kubernetes cluster operations.
---

When helping with kubectl and Kubernetes operations, always include:

## Core Principles

1. **Safety first**: Remind users about namespace context and potential impact
2. **Best practices**: Suggest the most appropriate kubectl commands
3. **Clear explanations**: Explain what each command does and why
4. **Troubleshooting**: Provide diagnostic steps for common issues

## Common kubectl Commands

### Viewing Resources
- **List pods**: `kubectl get pods [-n namespace]`
- **List all resources**: `kubectl get all [-n namespace]`
- **Describe resource**: `kubectl describe <resource-type> <resource-name>`
- **View logs**: `kubectl logs <pod-name> [-c container-name] [-f]`
- **Get YAML definition**: `kubectl get <resource-type> <resource-name> -o yaml`

### Managing Deployments
- **Create from file**: `kubectl apply -f <file.yaml>`
- **Update deployment**: `kubectl set image deployment/<name> <container>=<image>`
- **Scale deployment**: `kubectl scale deployment/<name> --replicas=<count>`
- **Rollout status**: `kubectl rollout status deployment/<name>`
- **Rollback**: `kubectl rollout undo deployment/<name>`

### Debugging and Troubleshooting
- **Execute in pod**: `kubectl exec -it <pod-name> -- /bin/bash`
- **Port forwarding**: `kubectl port-forward <pod-name> <local-port>:<pod-port>`
- **View events**: `kubectl get events --sort-by=.metadata.creationTimestamp`
- **Check resource usage**: `kubectl top pods [--namespace=<namespace>]`

### Context and Configuration
- **Current context**: `kubectl config current-context`
- **List contexts**: `kubectl config get-contexts`
- **Switch context**: `kubectl config use-context <context-name>`
- **Set namespace**: `kubectl config set-context --current --namespace=<namespace>`

### Services and Networking
- **List services**: `kubectl get services`
- **Expose deployment**: `kubectl expose deployment <name> --port=<port> --type=<type>`
- **Get endpoints**: `kubectl get endpoints`

## Response Format

Structure kubectl help as:
1. **Understand the need**: Clarify what the user wants to accomplish
2. **Provide the command**: Give the exact kubectl command(s)
3. **Explain the command**: Break down what each part does
4. **Add context**: Mention important flags, options, or considerations
5. **Safety notes**: Warn about destructive operations or cluster-wide impacts

## Example Usage

**User:** "How do I check if my pods are running?"

**Response:**
To check pod status, use:
```bash
kubectl get pods
```

For pods in a specific namespace:
```bash
kubectl get pods -n <namespace>
```

For more details including node assignment and IP addresses:
```bash
kubectl get pods -o wide
```

To continuously watch pod status changes:
```bash
kubectl get pods -w
```

**User:** "My pod is crashing, how do I debug it?"

**Response:**
Here's a step-by-step debugging approach:

1. **Check pod status and events**:
```bash
kubectl describe pod <pod-name>
```
Look at the "Events" section at the bottom for error messages.

2. **View container logs**:
```bash
kubectl logs <pod-name>
```
For previous crashed container:
```bash
kubectl logs <pod-name> --previous
```

3. **If pod has multiple containers, specify which one**:
```bash
kubectl logs <pod-name> -c <container-name>
```

4. **Check resource constraints**:
```bash
kubectl top pod <pod-name>
```

Common crash causes:
- Image pull errors (check image name and registry access)
- Resource limits (memory/CPU exceeded)
- Application errors (check logs)
- Configuration issues (check environment variables and config maps)

**User:** "How do I update my deployment with a new image?"

**Response:**
To update a deployment with a new image:

```bash
kubectl set image deployment/<deployment-name> <container-name>=<new-image>:<tag>
```

Example:
```bash
kubectl set image deployment/my-app nginx=nginx:1.21
```

Monitor the rollout:
```bash
kubectl rollout status deployment/<deployment-name>
```

If something goes wrong, rollback:
```bash
kubectl rollout undo deployment/<deployment-name>
```

**Best practice**: Always tag your images with specific versions instead of using `:latest` for better version control and rollback capability.

## Common Patterns and Tips

### Filtering and Formatting
- **Filter by label**: `kubectl get pods -l app=myapp`
- **JSON path**: `kubectl get pods -o jsonpath='{.items[*].metadata.name}'`
- **Custom columns**: `kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase`

### Safety Tips
- ⚠️ **Always check your context** before running commands: `kubectl config current-context`
- ⚠️ **Use `--dry-run=client` to preview** changes: `kubectl apply -f file.yaml --dry-run=client`
- ⚠️ **Be careful with `--all-namespaces`** or `-A` flags
- ⚠️ **Double-check before deleting**: Use `kubectl get` first to verify what you're deleting

### Namespace Best Practices
- Set a default namespace to avoid accidents: `kubectl config set-context --current --namespace=dev`
- Always specify `-n <namespace>` for important operations
- Use `kubectl get ns` to list available namespaces

Keep explanations practical and command-focused. For complex scenarios, provide multiple steps with clear explanations.
