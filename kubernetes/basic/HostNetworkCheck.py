"""
Checkov Custom Check: Ensure hostNetwork is not set to true
This check ensures that pods do not use hostNetwork.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class HostNetworkCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure pods do not use hostNetwork"
        id = "CKV_K8S_CUSTOM_012"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for hostNetwork in pod spec
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.PASSED
        
        if spec.get("hostNetwork", False):
            return CheckResult.FAILED
        
        return CheckResult.PASSED


check = HostNetworkCheck()
