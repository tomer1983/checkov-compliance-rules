"""
Checkov Custom Check: Ensure LoadBalancer services are internal in EKS
This check ensures that LoadBalancer services are configured as internal by default.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSInternalLoadBalancerCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure LoadBalancer services are internal (not internet-facing)"
        id = "CKV_EKS_CUSTOM_004"
        supported_resources = ["Service"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for internal load balancer annotation
        """
        spec = conf.get("spec", {})
        service_type = spec.get("type")
        
        # Only check LoadBalancer services
        if service_type != "LoadBalancer":
            return CheckResult.PASSED
        
        metadata = conf.get("metadata", {})
        annotations = metadata.get("annotations", {})
        
        # Check for internal annotation (both old and new styles)
        scheme = annotations.get("service.beta.kubernetes.io/aws-load-balancer-scheme", "")
        is_internal_legacy = annotations.get("service.beta.kubernetes.io/aws-load-balancer-internal", "")
        
        if scheme == "internal" or is_internal_legacy == "true":
            return CheckResult.PASSED
        
        return CheckResult.FAILED


check = EKSInternalLoadBalancerCheck()
