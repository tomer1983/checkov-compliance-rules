"""
Checkov Custom Check: Ensure pods use EC2 instance metadata service v2 (IMDSv2)
This check ensures that pods are configured to use IMDSv2 through proper settings.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSIMDSv2Check(BaseResourceCheck):
    def __init__(self):
        name = "Ensure pods have hostNetwork disabled for IMDSv2 compliance"
        id = "CKV_EKS_CUSTOM_008"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Ensures pods don't use hostNetwork which can bypass IMDSv2 restrictions
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.PASSED
        
        # Check that hostNetwork is not enabled (for IMDSv2 compliance)
        if spec.get("hostNetwork", False):
            return CheckResult.FAILED
        
        return CheckResult.PASSED


check = EKSIMDSv2Check()
