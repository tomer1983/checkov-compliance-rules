# Checkov Compliance Rules for Kubernetes

A comprehensive collection of custom Checkov policies for ensuring Kubernetes manifest compliance with security and operational best practices. This repository includes dedicated rule sets for both standard Kubernetes deployments and AWS EKS-specific configurations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Policy Categories](#policy-categories)
- [Examples](#examples)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository provides battle-tested Checkov custom policies to enforce security, compliance, and operational best practices for Kubernetes workloads. The policies are organized into logical categories and split between generic Kubernetes rules and AWS EKS-specific checks.

### What is Checkov?

Checkov is a static code analysis tool for infrastructure-as-code. It scans cloud infrastructure configurations to find misconfigurations before deployment. This repository extends Checkov's built-in capabilities with custom rules tailored for Kubernetes environments.

## ✨ Features

- **30+ Custom Policies**: Comprehensive coverage of Kubernetes security and best practices
- **Organized by Category**: Easy to navigate and selectively apply policies
- **AWS EKS Support**: Dedicated policies for EKS-specific features (IRSA, ALB, EBS CSI, etc.)
- **Production Ready**: Based on real-world enterprise requirements
- **Well Documented**: Each policy includes clear guidelines and rationale
- **Example Manifests**: Both compliant and non-compliant examples for testing
- **CI/CD Ready**: Easy integration into existing pipelines

## 📁 Repository Structure

```
checkov-compliance-rules/
├── policies/
│   ├── kubernetes/              # Generic Kubernetes policies
│   │   ├── security/
│   │   │   └── container-security-context.yaml
│   │   ├── resource-management/
│   │   │   └── resource-limits.yaml
│   │   ├── configuration/
│   │   │   ├── health-checks.yaml
│   │   │   ├── image-policies.yaml
│   │   │   └── deployment-best-practices.yaml
│   │   └── networking/
│   │       └── network-policies.yaml
│   └── aws-eks/                 # AWS EKS-specific policies
│       ├── iam-and-security.yaml
│       ├── load-balancer-configuration.yaml
│       └── storage-configuration.yaml
├── examples/
│   ├── kubernetes/              # Example Kubernetes manifests
│   │   ├── secure-deployment.yaml
│   │   ├── insecure-deployment.yaml
│   │   └── namespace-with-policies.yaml
│   └── aws-eks/                 # Example EKS manifests
│       ├── deployment-with-irsa.yaml
│       ├── alb-nlb-ingress.yaml
│       └── storage-classes.yaml
├── docs/
│   ├── USAGE.md
│   ├── POLICIES.md
│   └── CI_CD_INTEGRATION.md
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Install Checkov**

```bash
pip install checkov
```

2. **Clone this repository**

```bash
git clone https://github.com/tomer1983/checkov-compliance-rules.git
cd checkov-compliance-rules
```

3. **Verify installation**

```bash
checkov --version
```

## 💻 Usage

### Basic Scan

Scan a single Kubernetes manifest:

```bash
checkov -f path/to/your/manifest.yaml --external-checks-dir ./policies
```

Scan a directory of manifests:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies
```

### Scan with Specific Policy Categories

Scan only with Kubernetes security policies:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies/kubernetes/security
```

Scan only with AWS EKS policies:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies/aws-eks
```

### Output Formats

Generate JSON output:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies --output json
```

Generate JUnit XML for CI/CD:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies --output junitxml
```

Generate SARIF for GitHub Security:

```bash
checkov -d path/to/manifests/ --external-checks-dir ./policies --output sarif
```

### Skip Specific Checks

Skip a specific check inline in your manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  annotations:
    checkov.io/skip1: CKV_K8S_CUSTOM_001=Development environment only
spec:
  # ... rest of manifest
```

Skip checks via command line:

```bash
checkov -f manifest.yaml --external-checks-dir ./policies --skip-check CKV_K8S_CUSTOM_001,CKV_K8S_CUSTOM_002
```

### Test with Example Manifests

Run against the provided examples to see the policies in action:

```bash
# Test with compliant manifest
checkov -f examples/kubernetes/secure-deployment.yaml --external-checks-dir ./policies

# Test with non-compliant manifest
checkov -f examples/kubernetes/insecure-deployment.yaml --external-checks-dir ./policies
```

## 📚 Policy Categories

### Kubernetes Security Policies

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_K8S_CUSTOM_001 | Container does not run as root | HIGH | Ensures runAsNonRoot is set to true |
| CKV_K8S_CUSTOM_002 | Container not in privileged mode | CRITICAL | Prevents privileged containers |
| CKV_K8S_CUSTOM_003 | Containers drop all capabilities | HIGH | Ensures all capabilities are dropped |
| CKV_K8S_CUSTOM_004 | Read-only root filesystem | MEDIUM | Enforces read-only root filesystem |
| CKV_K8S_CUSTOM_005 | No privilege escalation | HIGH | Prevents privilege escalation |
| CKV_K8S_CUSTOM_006 | High UID for pod user | MEDIUM | Ensures runAsUser > 10000 |

### Resource Management Policies

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_K8S_CUSTOM_007 | CPU limits defined | MEDIUM | Ensures CPU limits are set |
| CKV_K8S_CUSTOM_008 | Memory limits defined | MEDIUM | Ensures memory limits are set |
| CKV_K8S_CUSTOM_009 | CPU requests defined | MEDIUM | Ensures CPU requests are set |
| CKV_K8S_CUSTOM_010 | Memory requests defined | MEDIUM | Ensures memory requests are set |
| CKV_K8S_CUSTOM_011 | ResourceQuota exists | LOW | Validates namespace ResourceQuota |
| CKV_K8S_CUSTOM_012 | LimitRange exists | LOW | Validates namespace LimitRange |

### Configuration Best Practices

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_K8S_CUSTOM_013 | Liveness probe defined | MEDIUM | Ensures liveness probe exists |
| CKV_K8S_CUSTOM_014 | Readiness probe defined | MEDIUM | Ensures readiness probe exists |
| CKV_K8S_CUSTOM_015 | Startup probe for slow containers | LOW | Validates startup probe |
| CKV_K8S_CUSTOM_016 | No latest image tag | MEDIUM | Prevents use of :latest tag |
| CKV_K8S_CUSTOM_017 | Proper imagePullPolicy | LOW | Validates imagePullPolicy |
| CKV_K8S_CUSTOM_018 | Trusted registry | HIGH | Ensures images from trusted registries |
| CKV_K8S_CUSTOM_025 | Appropriate replica count | LOW | Ensures >= 2 replicas for HA |
| CKV_K8S_CUSTOM_026 | PodDisruptionBudget exists | LOW | Validates PDB for HA apps |
| CKV_K8S_CUSTOM_027 | Pod anti-affinity | LOW | Ensures pod distribution |
| CKV_K8S_CUSTOM_028 | RollingUpdate strategy | LOW | Validates deployment strategy |
| CKV_K8S_CUSTOM_029 | Labels defined | LOW | Ensures labels exist |
| CKV_K8S_CUSTOM_030 | App label defined | LOW | Ensures app label exists |

### Networking Policies

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_K8S_CUSTOM_019 | NetworkPolicy exists | MEDIUM | Validates NetworkPolicy presence |
| CKV_K8S_CUSTOM_020 | Ingress and egress rules | MEDIUM | Ensures both rules are defined |
| CKV_K8S_CUSTOM_021 | hostNetwork disabled | HIGH | Prevents hostNetwork usage |
| CKV_K8S_CUSTOM_022 | hostPID disabled | HIGH | Prevents hostPID usage |
| CKV_K8S_CUSTOM_023 | hostIPC disabled | HIGH | Prevents hostIPC usage |
| CKV_K8S_CUSTOM_024 | Not using default namespace | LOW | Prevents default namespace use |

### AWS EKS Policies

#### IAM and Security

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_EKS_CUSTOM_001 | IRSA role annotation | HIGH | Ensures ServiceAccount has IAM role |
| CKV_EKS_CUSTOM_002 | Valid IAM role ARN | MEDIUM | Validates ARN format |
| CKV_EKS_CUSTOM_003 | Uses ServiceAccount | HIGH | Ensures pod uses ServiceAccount |
| CKV_EKS_CUSTOM_004 | No AWS credentials in env | CRITICAL | Prevents embedded credentials |
| CKV_EKS_CUSTOM_005 | FSx encryption | HIGH | Ensures FSx volumes are encrypted |
| CKV_EKS_CUSTOM_006 | EBS encryption | HIGH | Ensures EBS volumes are encrypted |

#### Load Balancer Configuration

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_EKS_CUSTOM_007 | ALB uses HTTPS | HIGH | Ensures certificate is configured |
| CKV_EKS_CUSTOM_008 | SSL redirect enabled | MEDIUM | Validates HTTPS redirect |
| CKV_EKS_CUSTOM_009 | Security groups defined | MEDIUM | Ensures SG configuration |
| CKV_EKS_CUSTOM_010 | Internal ALB scheme | MEDIUM | Validates internal ALB usage |
| CKV_EKS_CUSTOM_011 | WAF enabled | MEDIUM | Ensures WAF protection |
| CKV_EKS_CUSTOM_012 | Cross-zone LB | LOW | Validates cross-zone LB |
| CKV_EKS_CUSTOM_013 | Internal NLB | MEDIUM | Ensures internal NLB for private APIs |

#### Storage Configuration

| Policy ID | Name | Severity | Description |
|-----------|------|----------|-------------|
| CKV_EKS_CUSTOM_014 | EBS CSI driver | MEDIUM | Ensures EBS CSI driver usage |
| CKV_EKS_CUSTOM_015 | Proper EBS volume type | LOW | Validates gp3 or io2 usage |
| CKV_EKS_CUSTOM_016 | EFS CSI driver | LOW | Validates EFS CSI driver |
| CKV_EKS_CUSTOM_017 | Proper reclaim policy | MEDIUM | Ensures proper reclaim policy |
| CKV_EKS_CUSTOM_018 | PVC storage request | LOW | Validates storage request |

For detailed information about each policy, see [docs/POLICIES.md](docs/POLICIES.md).

## 📖 Examples

### Example 1: Secure Kubernetes Deployment

See `examples/kubernetes/secure-deployment.yaml` for a complete example of a deployment that passes all security checks:

- Runs as non-root user with high UID
- Drops all capabilities
- Uses read-only root filesystem
- Has resource limits and requests
- Includes health checks
- Uses specific image tags from trusted registry

### Example 2: AWS EKS with IRSA

See `examples/aws-eks/deployment-with-irsa.yaml` for an example using:

- IAM Roles for Service Accounts (IRSA)
- Encrypted EBS storage with CSI driver
- Proper security contexts

### Example 3: Namespace with Policies

See `examples/kubernetes/namespace-with-policies.yaml` for:

- ResourceQuota configuration
- LimitRange setup
- NetworkPolicy examples
- PodDisruptionBudget

## 🔄 CI/CD Integration

### GitHub Actions

Create `.github/workflows/checkov.yml`:

```yaml
name: Checkov Security Scan

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  checkov-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Checkout compliance rules
        uses: actions/checkout@v3
        with:
          repository: tomer1983/checkov-compliance-rules
          path: compliance-rules

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: k8s-manifests/
          external_checks_dirs: compliance-rules/policies
          output_format: sarif
          output_file_path: results.sarif

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: results.sarif
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
checkov:
  stage: test
  image: bridgecrew/checkov:latest
  before_script:
    - git clone https://github.com/tomer1983/checkov-compliance-rules.git
  script:
    - checkov -d k8s-manifests/ --external-checks-dir checkov-compliance-rules/policies --output junitxml --output-file-path results.xml
  artifacts:
    reports:
      junit: results.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                dir('compliance-rules') {
                    git 'https://github.com/tomer1983/checkov-compliance-rules.git'
                }
            }
        }
        
        stage('Checkov Scan') {
            steps {
                sh '''
                    pip install checkov
                    checkov -d k8s-manifests/ \
                        --external-checks-dir compliance-rules/policies \
                        --output junitxml \
                        --output-file-path results.xml
                '''
            }
        }
    }
    
    post {
        always {
            junit 'results.xml'
        }
    }
}
```

### Azure DevOps

Add to `azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- checkout: self
- checkout: git://MyProject/checkov-compliance-rules

- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x'

- script: |
    pip install checkov
    checkov -d $(Build.SourcesDirectory)/k8s-manifests \
      --external-checks-dir $(Build.SourcesDirectory)/checkov-compliance-rules/policies \
      --output junitxml \
      --output-file-path $(Common.TestResultsDirectory)/checkov-results.xml
  displayName: 'Run Checkov'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: '**/checkov-results.xml'
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bridgecrewio/checkov.git
    rev: '2.3.187'  # Use latest version
    hooks:
      - id: checkov
        args: 
          - --external-checks-dir=path/to/checkov-compliance-rules/policies
          - -d=k8s-manifests/
```

For more detailed CI/CD integration examples, see [docs/CI_CD_INTEGRATION.md](docs/CI_CD_INTEGRATION.md).

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug or have a suggestion? Open an issue
2. **Add Policies**: Create new policies following the existing structure
3. **Improve Documentation**: Help us make the docs better
4. **Share Examples**: Add more example manifests

### Adding a New Policy

1. Create a new YAML file in the appropriate directory
2. Follow the Checkov YAML policy format:

```yaml
---
metadata:
  id: "CKV_K8S_CUSTOM_XXX"
  name: "Your policy name"
  category: "CATEGORY"
  severity: "HIGH|MEDIUM|LOW|CRITICAL"
  guideline: "Clear explanation of the policy"
definition:
  cond_type: "attribute"
  resource_types:
    - "Pod"
    - "Deployment"
  attribute: "spec.path.to.attribute"
  operator: "equals|exists|not_exists|contains|regex_match"
  value: "expected_value"
```

3. Add example manifests demonstrating the policy
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Checkov](https://www.checkov.io/) - The amazing open-source IaC scanning tool
- Kubernetes community for security best practices
- AWS EKS documentation and best practices

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/tomer1983/checkov-compliance-rules/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tomer1983/checkov-compliance-rules/discussions)

## 🔗 Useful Links

- [Checkov Documentation](https://www.checkov.io/1.Welcome/What%20is%20Checkov.html)
- [Checkov Custom Policies Guide](https://www.checkov.io/3.Custom%20Policies/Custom%20Policies%20Overview.html)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [AWS EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)

---

**Note**: These policies are provided as-is and should be reviewed and customized based on your organization's specific security requirements and compliance needs.