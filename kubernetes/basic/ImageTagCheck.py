"""
Checkov Custom Check: Ensure images use specific tags and not latest
This check ensures that container images use specific version tags instead of 'latest'.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class ImageTagCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure container images use specific tags and not 'latest'"
        id = "CKV_K8S_CUSTOM_011"
        supported_resources = ["Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for image tags in container configurations
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
        
        # Check all containers don't use latest tag or no tag
        for container in all_containers:
            image = container.get("image", "")
            
            if not image:
                return CheckResult.FAILED
            
            # Check if image ends with :latest or has no tag
            if image.endswith(":latest") or ":" not in image:
                return CheckResult.FAILED
        
        return CheckResult.PASSED


check = ImageTagCheck()
