"""
Checkov Custom Check: Ensure containers do not run in privileged mode
This check ensures that containers are not running in privileged mode.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class PrivilegedContainerCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers do not run in privileged mode"
        id = "CKV_K8S_CUSTOM_004"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for privileged: true in container security contexts
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.PASSED  # No spec, no privileged containers
        
        containers = spec.get("containers", [])
        init_containers = spec.get("initContainers", [])
        
        all_containers = containers + init_containers
        
        # Check all containers are not privileged
        for container in all_containers:
            security_context = container.get("securityContext", {})
            if security_context.get("privileged", False):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = PrivilegedContainerCheck()
