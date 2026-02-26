---
name: k8s-diagnostic-skill
description: Kubernetes diagnostic workflow that checks logs, lists pods, and provides pod details. Use when users ask about pod status, troubleshooting, or cluster diagnostics.
---

# Kubernetes Diagnostic Workflow

This skill implements a structured diagnostic workflow for Kubernetes pod analysis.

## Workflow Steps

When a user requests information about Kubernetes pods or cluster status, follow this exact sequence:

### Step 1: Check Logs First
Always start by checking logs from recent pod activity. This provides context about what's happening in the cluster.

**Tool to use**: `get_pod_logs`
- If a specific pod is mentioned, get logs for that pod
- If no pod is specified, skip this step or check logs from the most recent pod in the default namespace
- Use `tail_lines: 50` to get the most recent 50 log lines

### Step 2: Get List of Pods
After checking logs (or if logs aren't available), retrieve the list of pods.

**Tool to use**: `list_pods`
- Default to the "default" namespace unless specified otherwise
- This returns a list of all pods with their basic information

### Step 3: Conditional Pod Details

**Case A: User asks about a specific pod**
- Use the tool `get_pod_details` with the specific pod name
- Return comprehensive details about that pod including:
  - Status and conditions
  - Container information
  - Labels and annotations
  - Resource configuration

**Case B: User asks general question or no specific pod mentioned**
- Return the list of all pods
- **Additionally**, get detailed information for ONLY the first pod in the list using `get_pod_details`
- Present the pod list followed by detailed information about the first pod

## Tools Available

You have access to these Kubernetes tools:

1. **list_pods(namespace: str = "default")**
   - Lists all pods in a namespace
   - Returns: List of pod information dictionaries

2. **get_pod_details(pod_name: str, namespace: str = "default")**
   - Gets detailed information about a specific pod
   - Returns: Dictionary with comprehensive pod details

3. **get_pod_logs(pod_name: str, namespace: str = "default", container: str = None, tail_lines: int = None)**
   - Retrieves logs from a pod
   - Returns: String containing log output

4. **list_namespaces()**
   - Lists all namespaces in the cluster
   - Returns: List of namespace information

## Response Format

Structure your response as follows:

```
## Logs Review
[Log output from get_pod_logs if available]

## Pod List
[List of all pods from list_pods]

## Detailed Pod Information
[Details from get_pod_details for specific pod or first pod]
```

## Example Scenarios

### Scenario 1: General Pod Status Request
**User**: "Show me the pods in my cluster"

**Action Sequence**:
1. Call `list_pods()` to get all pods
2. Call `get_pod_details(pod_name=<first_pod_name>)` for the first pod in the list
3. Present both the full list and details of the first pod

### Scenario 2: Specific Pod Request
**User**: "Tell me about the nginx-pod"

**Action Sequence**:
1. Optional: Call `get_pod_logs(pod_name="nginx-pod", tail_lines=50)` to check recent activity
2. Call `list_pods()` to show context
3. Call `get_pod_details(pod_name="nginx-pod")` for specific details
4. Present logs (if retrieved), pod list, and detailed information about nginx-pod

### Scenario 3: Troubleshooting Request
**User**: "Why is my pod failing?"

**Action Sequence**:
1. Call `list_pods()` to identify which pods might be failing
2. For the first pod (or mentioned pod), call `get_pod_logs(pod_name=<pod_name>, tail_lines=100)` to see recent errors
3. Call `get_pod_details(pod_name=<pod_name>)` to check status and conditions
4. Analyze the information and provide diagnostic insights

## Important Notes

- **Always follow the workflow order**: logs → list → details
- **Namespace context**: Default to "default" namespace unless specified
- **Error handling**: If a tool call fails, explain the error and proceed with remaining steps
- **First pod priority**: When no specific pod is mentioned, always include details of the first pod
- **Structured output**: Present information in a clear, organized format

## Safety Considerations

- This skill is read-only and diagnostic in nature
- No modifications are made to the cluster
- Always indicate which namespace you're querying
- If sensitive information appears in logs, remind users to review security policies
