"""
Checkov Custom Check: Ensure StorageClass uses AWS EBS CSI driver
This check ensures that StorageClass uses the AWS EBS CSI driver for EKS.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSStorageClassCSICheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure StorageClass uses AWS EBS CSI driver"
        id = "CKV_EKS_CUSTOM_006"
        supported_resources = ["StorageClass"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for AWS EBS CSI driver provisioner
        """
        provisioner = conf.get("provisioner", "")
        
        # Check for EBS CSI driver
        if provisioner == "ebs.csi.aws.com":
            return CheckResult.PASSED
        
        # Legacy in-tree provisioner (deprecated)
        if provisioner == "kubernetes.io/aws-ebs":
            return CheckResult.FAILED
        
        return CheckResult.FAILED


check = EKSStorageClassCSICheck()
