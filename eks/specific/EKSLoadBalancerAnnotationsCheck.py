"""
Checkov Custom Check: Ensure LoadBalancer services have proper AWS annotations
This check ensures that LoadBalancer services have AWS-specific annotations for security.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSLoadBalancerAnnotationsCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure LoadBalancer services have AWS load balancer type annotation"
        id = "CKV_EKS_CUSTOM_003"
        supported_resources = ["Service"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for AWS load balancer annotations in LoadBalancer services
        """
        spec = conf.get("spec", {})
        service_type = spec.get("type")
        
        # Only check LoadBalancer services
        if service_type != "LoadBalancer":
            return CheckResult.PASSED
        
        metadata = conf.get("metadata", {})
        annotations = metadata.get("annotations", {})
        
        # Check for AWS load balancer controller annotations
        if "service.beta.kubernetes.io/aws-load-balancer-type" in annotations:
            return CheckResult.PASSED
        
        # Legacy annotation
        if "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" in annotations:
            return CheckResult.PASSED
        
        return CheckResult.FAILED


check = EKSLoadBalancerAnnotationsCheck()
