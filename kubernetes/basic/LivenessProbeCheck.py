"""
Checkov Custom Check: Ensure liveness probe is configured
This check ensures that containers have liveness probes configured for health checking.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class LivenessProbeCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers have liveness probe configured"
        id = "CKV_K8S_CUSTOM_008"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for livenessProbe in container configurations
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
        
        # Check all containers have liveness probe
        for container in containers:
            if not container.get("livenessProbe"):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = LivenessProbeCheck()
