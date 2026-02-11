"""
Checkov Custom Check: Ensure pods reference a ServiceAccount for EKS IRSA
This check ensures that pods specify a serviceAccountName for IAM role assumption.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSPodServiceAccountCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure pods specify a serviceAccountName for EKS IRSA"
        id = "CKV_EKS_CUSTOM_002"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for serviceAccountName in pod spec
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        service_account_name = spec.get("serviceAccountName")
        
        # Check that serviceAccountName is specified and not "default"
        if service_account_name and service_account_name != "default":
            return CheckResult.PASSED
        
        return CheckResult.FAILED


check = EKSPodServiceAccountCheck()
