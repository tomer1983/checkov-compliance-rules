"""
Checkov Custom Check: Ensure pods use IAM roles for service accounts (IRSA)
This check ensures that pods have the appropriate annotations for IRSA in EKS.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSIRSAAnnotationCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure ServiceAccount has IAM role annotation for EKS IRSA"
        id = "CKV_EKS_CUSTOM_001"
        supported_resources = ["ServiceAccount"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for eks.amazonaws.com/role-arn annotation in ServiceAccount
        """
        metadata = conf.get("metadata", {})
        annotations = metadata.get("annotations", {})
        
        # Check for IRSA annotation
        if "eks.amazonaws.com/role-arn" in annotations:
            return CheckResult.PASSED
        
        return CheckResult.FAILED


check = EKSIRSAAnnotationCheck()
