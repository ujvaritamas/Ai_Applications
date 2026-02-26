"""Customer Notification tools for interacting with K8s customer notification resources."""

from typing import List, Dict, Any
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
def list_customer_notification_pods(namespace: str = "kcp-system") -> List[Dict[str, Any]]:
    """
    List all customer notification operator pods in the kcp-system namespace.
    Specifically looks for pods matching 'customer-notification' pattern.

    Args:
        namespace: The Kubernetes namespace to query (default: "kcp-system")

    Returns:
        List of dictionaries containing customer notification pod information
    """
    load_k8s_config()
    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(namespace=namespace)

        # Filter pods specifically for customer-notification operator
        cn_pods = []
        for pod in pods.items:
            # Only include pods with "customer-notification" in the name
            if "customer-notification" in pod.metadata.name.lower():
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
                cn_pods.append(pod_info)

        return cn_pods

    except ApiException as e:
        raise Exception(f"Error listing customer notification pods in namespace '{namespace}': {e}")


@tool
def list_customer_notifications(namespace: str = "kcp-system") -> List[Dict[str, Any]]:
    """
    List all customer notification custom resources in the kcp-system namespace.
    This shows CustomerNotification, MajorUpgrade, and PlannedMaintenance resources.

    Args:
        namespace: The Kubernetes namespace to query (default: "kcp-system")

    Returns:
        List of dictionaries containing customer notification custom resource information
    """
    load_k8s_config()
    custom_api = client.CustomObjectsApi()

    try:
        # Query the custom resource based on the CRD definition
        group = "operator.kyma-project.io"
        version = "v1alpha1"  # Common version for Kyma operators, adjust if needed
        plural = "customernotifications"

        crs = custom_api.list_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural
        )

        notifications = []
        for item in crs.get("items", []):
            metadata = item.get("metadata", {})
            status = item.get("status", {})
            spec = item.get("spec", {})

            # Extract nested fields based on the CRD structure
            notification_params = spec.get("notificationparameters", {})
            parameters = spec.get("parameters", {})

            notification_info = {
                "name": metadata.get("name"),
                "namespace": metadata.get("namespace"),
                "status": status.get("mainstate", "Unknown"),
                "type": notification_params.get("type", "Unknown"),
                "schedule": parameters.get("schedule", ""),
                "creation_timestamp": metadata.get("creationTimestamp", ""),
                "labels": metadata.get("labels", {}),
                "annotations": metadata.get("annotations", {}),
            }
            notifications.append(notification_info)

        return notifications

    except ApiException as e:
        raise Exception(f"Error listing customer notifications in namespace '{namespace}': {e}")


@tool
def get_customer_notification_details(
    name: str,
    namespace: str = "kcp-system"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific customer notification custom resource.

    Args:
        name: Name of the customer notification resource
        namespace: The Kubernetes namespace (default: "kcp-system")

    Returns:
        Dictionary containing detailed customer notification information
    """
    load_k8s_config()
    custom_api = client.CustomObjectsApi()

    try:
        # Query the specific custom resource based on the CRD definition
        group = "operator.kyma-project.io"
        version = "v1alpha1"  # Common version for Kyma operators, adjust if needed
        plural = "customernotifications"

        cr = custom_api.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name
        )

        metadata = cr.get("metadata", {})
        status = cr.get("status", {})
        spec = cr.get("spec", {})

        # Extract nested fields based on the CRD structure
        notification_params = spec.get("notificationparameters", {})
        parameters = spec.get("parameters", {})

        return {
            "name": metadata.get("name"),
            "namespace": metadata.get("namespace"),
            "status": status.get("mainstate", "Unknown"),
            "type": notification_params.get("type", "Unknown"),
            "schedule": parameters.get("schedule", ""),
            "creation_timestamp": metadata.get("creationTimestamp", ""),
            "labels": metadata.get("labels", {}),
            "annotations": metadata.get("annotations", {}),
            "spec": spec,
            "status_details": status,
        }

    except ApiException as e:
        raise Exception(f"Error getting customer notification '{name}' in namespace '{namespace}': {e}")


tools = [
    list_customer_notification_pods,
    list_customer_notifications,
    get_customer_notification_details
]
