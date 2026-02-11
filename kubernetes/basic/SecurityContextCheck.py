"""
Checkov Custom Check: Ensure pods have security context defined
This check ensures that pods have security context configurations to enforce security policies.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class PodSecurityContextCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure pod has security context defined"
        id = "CKV_K8S_CUSTOM_001"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for security context configuration in pod spec:
        https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
        """
        spec = None
        
        # Handle different resource types
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        # Check for pod-level security context
        security_context = spec.get("securityContext", {})
        
        if not security_context:
            return CheckResult.FAILED
        
        return CheckResult.PASSED


check = PodSecurityContextCheck()
