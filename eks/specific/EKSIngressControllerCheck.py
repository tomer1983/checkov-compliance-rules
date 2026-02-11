"""
Checkov Custom Check: Ensure Ingress uses AWS Load Balancer Controller
This check ensures that Ingress resources use the AWS Load Balancer Controller.
"""
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EKSIngressControllerCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure Ingress uses AWS Load Balancer Controller class"
        id = "CKV_EKS_CUSTOM_005"
        supported_resources = ["Ingress"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        """
        Looks for ingressClassName or annotations for AWS Load Balancer Controller
        """
        spec = conf.get("spec", {})
        ingress_class_name = spec.get("ingressClassName")
        
        # Check for ingressClassName (preferred method in newer k8s versions)
        if ingress_class_name == "alb":
            return CheckResult.PASSED
        
        # Check annotations for legacy support
        metadata = conf.get("metadata", {})
        annotations = metadata.get("annotations", {})
        
        ingress_class = annotations.get("kubernetes.io/ingress.class")
        alb_annotation = annotations.get("alb.ingress.kubernetes.io/scheme")
        
        if ingress_class == "alb" or alb_annotation:
            return CheckResult.PASSED
        
        return CheckResult.FAILED


check = EKSIngressControllerCheck()
