"""
Checkov Custom Check: Ensure PersistentVolume uses AWS EBS CSI driver
This check ensures that PersistentVolumes use the AWS EBS CSI driver.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSPersistentVolumeCSICheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure PersistentVolume uses AWS EBS CSI driver"
        id = "CKV_EKS_CUSTOM_007"
        supported_resources = ["PersistentVolume"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for AWS EBS CSI driver in PersistentVolume spec
        """
        spec = conf.get("spec", {})
        
        # Check for CSI volume source
        csi = spec.get("csi", {})
        if csi:
            driver = csi.get("driver", "")
            if driver == "ebs.csi.aws.com":
                return CheckResult.PASSED
        
        # Check for deprecated awsElasticBlockStore
        if spec.get("awsElasticBlockStore"):
            return CheckResult.FAILED
        
        # If neither CSI nor legacy, might be using different storage - pass
        return CheckResult.PASSED


check = EKSPersistentVolumeCSICheck()
