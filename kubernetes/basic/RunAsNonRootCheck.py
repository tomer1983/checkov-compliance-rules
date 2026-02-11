"""
Checkov Custom Check: Ensure containers run as non-root user
This check ensures that containers run as non-root user for better security.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class RunAsNonRootCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers run as non-root user"
        id = "CKV_K8S_CUSTOM_003"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for runAsNonRoot in container or pod security contexts
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        # Check pod-level security context
        pod_security_context = spec.get("securityContext", {})
        pod_run_as_non_root = pod_security_context.get("runAsNonRoot", False)
        
        containers = spec.get("containers", [])
        init_containers = spec.get("initContainers", [])
        
        all_containers = containers + init_containers
        
        if not all_containers:
            return CheckResult.FAILED
        
        # If pod-level is set to true, it applies to all containers
        if pod_run_as_non_root:
            return CheckResult.PASSED
        
        # Otherwise, check each container
        for container in all_containers:
            security_context = container.get("securityContext", {})
            if not security_context.get("runAsNonRoot", False):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = RunAsNonRootCheck()
