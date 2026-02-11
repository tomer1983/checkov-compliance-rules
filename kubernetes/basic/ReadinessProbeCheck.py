"""
Checkov Custom Check: Ensure readiness probe is configured
This check ensures that containers have readiness probes configured.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class ReadinessProbeCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers have readiness probe configured"
        id = "CKV_K8S_CUSTOM_009"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for readinessProbe in container configurations
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
        
        # Check all containers have readiness probe
        for container in containers:
            if not container.get("readinessProbe"):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = ReadinessProbeCheck()
