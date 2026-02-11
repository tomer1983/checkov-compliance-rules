"""
Checkov Custom Check: Ensure containers have resource requests defined
This check ensures that containers have CPU and memory requests defined.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class ResourceRequestsCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers have CPU and memory requests defined"
        id = "CKV_K8S_CUSTOM_006"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for resource requests in container configurations
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        containers = spec.get("containers", [])
        
        if not containers:
            return CheckResult.FAILED
        
        # Check all containers have resource requests
        for container in containers:
            resources = container.get("resources", {})
            requests = resources.get("requests", {})
            
            # Check for both CPU and memory requests
            if not requests.get("cpu") or not requests.get("memory"):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = ResourceRequestsCheck()
