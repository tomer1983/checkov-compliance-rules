"""
Checkov Custom Check: Ensure containers run with read-only root filesystem
This check ensures that containers have readOnlyRootFilesystem set to true for enhanced security.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class ReadOnlyRootFilesystemCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers have readOnlyRootFilesystem enabled"
        id = "CKV_K8S_CUSTOM_002"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for readOnlyRootFilesystem in container security contexts
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        containers = spec.get("containers", [])
        init_containers = spec.get("initContainers", [])
        
        all_containers = containers + init_containers
        
        if not all_containers:
            return CheckResult.FAILED
        
        # Check all containers have readOnlyRootFilesystem set to true
        for container in all_containers:
            security_context = container.get("securityContext", {})
            if not security_context.get("readOnlyRootFilesystem", False):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = ReadOnlyRootFilesystemCheck()
