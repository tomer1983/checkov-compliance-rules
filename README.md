# Checkov Compliance Rules for Kubernetes

A comprehensive collection of Checkov custom checks for ensuring Kubernetes manifest compliance with security best practices and cloud-native standards.

## 📋 Overview

This repository provides custom Checkov policies for validating Kubernetes manifests, split into two main categories:

1. **Basic Kubernetes Checks** - Universal security and best practice checks applicable to any Kubernetes cluster
2. **AWS EKS Specific Checks** - Checks tailored for Amazon EKS environments

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Checkov installed (`pip install checkov`)

### Installation

```bash
# Clone the repository
git clone https://github.com/tomer1983/checkov-compliance-rules.git
cd checkov-compliance-rules

# Run checks on your manifests
checkov -d /path/to/your/manifests --external-checks-dir kubernetes/basic
checkov -d /path/to/your/manifests --external-checks-dir eks/specific
```

### Running All Checks

```bash
# Check both basic and EKS-specific rules
checkov -d /path/to/your/manifests \
  --external-checks-dir kubernetes/basic \
  --external-checks-dir eks/specific
```

## 📚 Check Categories

### Basic Kubernetes Checks (`kubernetes/basic/`)

These checks apply to any Kubernetes cluster and enforce fundamental security best practices:

| Check ID | Check Name | Description |
|----------|------------|-------------|
| CKV_K8S_CUSTOM_001 | Pod Security Context | Ensures pods have security context defined |
| CKV_K8S_CUSTOM_002 | Read-Only Root Filesystem | Ensures containers have readOnlyRootFilesystem enabled |
| CKV_K8S_CUSTOM_003 | Run as Non-Root | Ensures containers run as non-root user |
| CKV_K8S_CUSTOM_004 | No Privileged Containers | Ensures containers don't run in privileged mode |
| CKV_K8S_CUSTOM_005 | Resource Limits | Ensures containers have CPU and memory limits |
| CKV_K8S_CUSTOM_006 | Resource Requests | Ensures containers have CPU and memory requests |
| CKV_K8S_CUSTOM_007 | Drop All Capabilities | Ensures containers drop all Linux capabilities |
| CKV_K8S_CUSTOM_008 | Liveness Probe | Ensures containers have liveness probes configured |
| CKV_K8S_CUSTOM_009 | Readiness Probe | Ensures containers have readiness probes configured |
| CKV_K8S_CUSTOM_010 | Image Pull Policy | Ensures imagePullPolicy is explicitly set |
| CKV_K8S_CUSTOM_011 | Image Tag | Ensures images use specific tags (not 'latest') |
| CKV_K8S_CUSTOM_012 | No Host Network | Ensures pods don't use hostNetwork |

### AWS EKS Specific Checks (`eks/specific/`)

These checks are tailored for Amazon EKS environments:

| Check ID | Check Name | Description |
|----------|------------|-------------|
| CKV_EKS_CUSTOM_001 | IRSA Annotation | Ensures ServiceAccounts have IAM role annotations |
| CKV_EKS_CUSTOM_002 | Pod ServiceAccount | Ensures pods specify non-default ServiceAccount |
| CKV_EKS_CUSTOM_003 | LoadBalancer Annotations | Ensures LoadBalancers have AWS annotations |
| CKV_EKS_CUSTOM_004 | Internal LoadBalancer | Ensures LoadBalancers are internal by default |
| CKV_EKS_CUSTOM_005 | Ingress Controller | Ensures Ingress uses AWS Load Balancer Controller |
| CKV_EKS_CUSTOM_006 | StorageClass CSI | Ensures StorageClass uses EBS CSI driver |
| CKV_EKS_CUSTOM_007 | PersistentVolume CSI | Ensures PersistentVolumes use EBS CSI driver |
| CKV_EKS_CUSTOM_008 | IMDSv2 Compliance | Ensures pods comply with IMDSv2 requirements |

## 📖 Usage Examples

### Example 1: Check a Single Manifest

```bash
checkov -f examples/compliant-deployment.yaml \
  --external-checks-dir kubernetes/basic
```

### Example 2: Check All Manifests in a Directory

```bash
checkov -d ./k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --external-checks-dir eks/specific \
  --compact
```

### Example 3: Output Results in JSON

```bash
checkov -d ./k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --output json \
  --output-file-path ./results.json
```

### Example 4: Skip Specific Checks

```bash
checkov -d ./k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --skip-check CKV_K8S_CUSTOM_008,CKV_K8S_CUSTOM_009
```

### Example 5: CI/CD Integration

```bash
# Exit with error code if checks fail (useful for CI/CD)
checkov -d ./k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --external-checks-dir eks/specific \
  --compact \
  || exit 1
```

## 🏗️ Repository Structure

```
checkov-compliance-rules/
├── kubernetes/
│   └── basic/                    # Basic Kubernetes security checks
│       ├── SecurityContextCheck.py
│       ├── ReadOnlyRootFilesystemCheck.py
│       ├── RunAsNonRootCheck.py
│       ├── PrivilegedContainerCheck.py
│       ├── ResourceLimitsCheck.py
│       ├── ResourceRequestsCheck.py
│       ├── DropAllCapabilitiesCheck.py
│       ├── LivenessProbeCheck.py
│       ├── ReadinessProbeCheck.py
│       ├── ImagePullPolicyCheck.py
│       ├── ImageTagCheck.py
│       └── HostNetworkCheck.py
├── eks/
│   └── specific/                 # AWS EKS specific checks
│       ├── EKSIRSAAnnotationCheck.py
│       ├── EKSPodServiceAccountCheck.py
│       ├── EKSLoadBalancerAnnotationsCheck.py
│       ├── EKSInternalLoadBalancerCheck.py
│       ├── EKSIngressControllerCheck.py
│       ├── EKSStorageClassCSICheck.py
│       ├── EKSPersistentVolumeCSICheck.py
│       └── EKSIMDSv2Check.py
└── examples/                     # Example manifests
    ├── compliant-deployment.yaml
    ├── non-compliant-deployment.yaml
    └── eks-compliant-resources.yaml
```

## 🔍 Testing the Checks

Test the checks against the provided example manifests:

```bash
# Test compliant deployment (should pass most checks)
checkov -f examples/compliant-deployment.yaml \
  --external-checks-dir kubernetes/basic

# Test non-compliant deployment (should fail multiple checks)
checkov -f examples/non-compliant-deployment.yaml \
  --external-checks-dir kubernetes/basic

# Test EKS-specific resources
checkov -f examples/eks-compliant-resources.yaml \
  --external-checks-dir eks/specific
```

## 🛠️ Customization

### Adding Your Own Checks

1. Create a new Python file in the appropriate directory
2. Extend `BaseResourceCheck` from Checkov
3. Implement the `scan_resource_conf` method
4. Define supported resources and categories

Example:

```python
from checkov.kubernetes.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class MyCustomCheck(BaseResourceCheck):
    def __init__(self):
        name = "My custom check description"
        id = "CKV_K8S_CUSTOM_XXX"
        supported_resources = ["Deployment"]
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf, entity_type):
        # Your check logic here
        return CheckResult.PASSED

check = MyCustomCheck()
```

## 🔐 Security Best Practices

These checks enforce the following security principles:

### Defense in Depth
- Multiple layers of security controls
- Principle of least privilege
- Fail-safe defaults

### Container Security
- Non-root user execution
- Read-only root filesystems
- Dropped Linux capabilities
- No privileged containers

### Resource Management
- CPU and memory limits
- CPU and memory requests
- Prevent resource exhaustion

### Network Security
- No host network access
- Internal load balancers by default
- Proper ingress configuration

### AWS EKS Best Practices
- IAM Roles for Service Accounts (IRSA)
- AWS Load Balancer Controller integration
- EBS CSI driver for persistent storage
- IMDSv2 compliance

## 📊 CI/CD Integration

### GitHub Actions

```yaml
name: Checkov Scan
on: [push, pull_request]

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install Checkov
        run: pip install checkov
      
      - name: Checkout compliance rules
        uses: actions/checkout@v2
        with:
          repository: tomer1983/checkov-compliance-rules
          path: compliance-rules
      
      - name: Run Checkov
        run: |
          checkov -d ./k8s-manifests \
            --external-checks-dir ./compliance-rules/kubernetes/basic \
            --external-checks-dir ./compliance-rules/eks/specific \
            --compact
```

### GitLab CI

```yaml
checkov:
  image: bridgecrew/checkov:latest
  script:
    - git clone https://github.com/tomer1983/checkov-compliance-rules.git
    - |
      checkov -d ./k8s-manifests \
        --external-checks-dir ./checkov-compliance-rules/kubernetes/basic \
        --external-checks-dir ./checkov-compliance-rules/eks/specific \
        --compact
  only:
    - branches
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Related Resources

- [Checkov Documentation](https://www.checkov.io/1.Welcome/Quick%20Start.html)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [AWS EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)

## 📞 Support

For issues, questions, or contributions, please open an issue in the GitHub repository.