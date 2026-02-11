"""
Checkov Custom Check: Ensure containers drop all capabilities
This check ensures that containers drop all capabilities and only add necessary ones.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class DropAllCapabilitiesCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers drop all capabilities"
        id = "CKV_K8S_CUSTOM_007"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for capabilities drop ALL in container security contexts
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
        
        # Check all containers drop all capabilities
        for container in all_containers:
            security_context = container.get("securityContext", {})
            capabilities = security_context.get("capabilities", {})
            drop = capabilities.get("drop", [])
            
            if "ALL" not in drop:
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = DropAllCapabilitiesCheck()
