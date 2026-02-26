"""Kubernetes tools for interacting with K8s clusters."""

from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from kubernetes import client, config
from kubernetes.client.rest import ApiException


def load_k8s_config():
    """Load Kubernetes configuration from default kubeconfig."""
    try:
        config.load_kube_config()
    except Exception:
        # Fallback to in-cluster config if running inside a pod
        config.load_incluster_config()


@tool
def list_pods(namespace: str = "default") -> List[Dict[str, Any]]:
    """
    List all pods in a specific namespace.

    Args:
        namespace: The Kubernetes namespace to query (default: "default")

    Returns:
        List of dictionaries containing pod information
    """
    load_k8s_config()
    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(namespace=namespace)

        pod_list = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "pod_ip": pod.status.pod_ip,
                "host_ip": pod.status.host_ip,
                "start_time": str(pod.status.start_time) if pod.status.start_time else None,
                "containers": [
                    {
                        "name": container.name,
                        "image": container.image,
                        "ready": container_status.ready if container_status else False,
                        "restart_count": container_status.restart_count if container_status else 0,
                    }
                    for container in pod.spec.containers
                    for container_status in (pod.status.container_statuses or [])
                    if container_status.name == container.name
                ],
                "labels": pod.metadata.labels or {},
            }
            pod_list.append(pod_info)

        return pod_list

    except ApiException as e:
        raise Exception(f"Error listing pods in namespace '{namespace}': {e}")


@tool
def get_pod_details(pod_name: str, namespace: str = "default") -> Dict[str, Any]:
    """
    Get detailed information about a specific pod.

    Args:
        pod_name: Name of the pod
        namespace: The Kubernetes namespace (default: "default")

    Returns:
        Dictionary containing detailed pod information
    """
    load_k8s_config()
    v1 = client.CoreV1Api()

    try:
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)

        return {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "conditions": [
                {
                    "type": condition.type,
                    "status": condition.status,
                    "reason": condition.reason,
                    "message": condition.message,
                }
                for condition in (pod.status.conditions or [])
            ],
            "containers": [
                {
                    "name": container.name,
                    "image": container.image,
                    "ports": [
                        {"container_port": port.container_port, "protocol": port.protocol}
                        for port in (container.ports or [])
                    ],
                }
                for container in pod.spec.containers
            ],
            "labels": pod.metadata.labels or {},
            "annotations": pod.metadata.annotations or {},
        }

    except ApiException as e:
        raise Exception(f"Error getting pod '{pod_name}' in namespace '{namespace}': {e}")


@tool
def get_pod_logs(
    pod_name: str,
    namespace: str = "default",
    container: Optional[str] = None,
    tail_lines: Optional[int] = None
) -> str:
    """
    Get logs from a specific pod.

    Args:
        pod_name: Name of the pod
        namespace: The Kubernetes namespace (default: "default")
        container: Specific container name (optional, required for multi-container pods)
        tail_lines: Number of lines to retrieve from the end of the logs

    Returns:
        String containing the pod logs
    """
    load_k8s_config()
    v1 = client.CoreV1Api()

    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container,
            tail_lines=tail_lines
        )
        return logs

    except ApiException as e:
        raise Exception(f"Error getting logs for pod '{pod_name}': {e}")


@tool
def list_namespaces() -> List[Dict[str, Any]]:
    """
    List all namespaces in the cluster.

    Returns:
        List of dictionaries containing namespace information
    """
    load_k8s_config()
    v1 = client.CoreV1Api()

    try:
        namespaces = v1.list_namespace()

        ns_list = []
        for ns in namespaces.items:
            ns_info = {
                "name": ns.metadata.name,
                "status": ns.status.phase,
                "labels": ns.metadata.labels or {},
                "creation_timestamp": str(ns.metadata.creation_timestamp),
            }
            ns_list.append(ns_info)

        return ns_list

    except ApiException as e:
        raise Exception(f"Error listing namespaces: {e}")

tools = [list_pods, get_pod_details, get_pod_logs, list_namespaces]