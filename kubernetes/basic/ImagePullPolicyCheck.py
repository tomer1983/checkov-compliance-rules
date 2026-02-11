"""
Checkov Custom Check: Ensure image pull policy is not set to Always or is explicitly set
This check ensures that containers have imagePullPolicy set appropriately.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class ImagePullPolicyCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure containers have imagePullPolicy explicitly set"
        id = "CKV_K8S_CUSTOM_010"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for imagePullPolicy in container configurations
        """
        spec = None
        
        if entity_type == "Pod":
            spec = conf.get("spec", {})
        else:
            spec = conf.get("spec", {}).get("template", {}).get("spec", {})
        
        if not spec:
            return CheckResult.FAILED
        
        containers = spec.get("containers", [])
        init_containers = spec.get("initContainers", [])
        
        all_containers = containers + init_containers
        
        if not all_containers:
            return CheckResult.FAILED
        
        # Check all containers have imagePullPolicy explicitly set
        for container in all_containers:
            if not container.get("imagePullPolicy"):
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = ImagePullPolicyCheck()
