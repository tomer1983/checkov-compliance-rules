# Implementation Guide

This guide provides step-by-step instructions for implementing Checkov compliance rules in your Kubernetes environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Local Development Setup](#local-development-setup)
4. [CI/CD Integration](#cicd-integration)
5. [Customizing Policies](#customizing-policies)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

- Python 3.7 or higher installed
- pip package manager
- Access to your Kubernetes manifests
- (Optional) Git for version control
- (Optional) CI/CD system (GitHub Actions, GitLab CI, Jenkins, etc.)

## Quick Start

### Step 1: Install Checkov

Install Checkov using pip:

```bash
pip install checkov
```

Verify the installation:

```bash
checkov --version
```

### Step 2: Get the Compliance Rules

Clone this repository:

```bash
git clone https://github.com/tomer1983/checkov-compliance-rules.git
cd checkov-compliance-rules
```

Or download as a ZIP and extract it.

### Step 3: Run Your First Scan

Scan a single manifest:

```bash
checkov -f /path/to/your/deployment.yaml --external-checks-dir ./policies
```

Scan a directory:

```bash
checkov -d /path/to/your/manifests/ --external-checks-dir ./policies
```

### Step 4: Review Results

Checkov will output:
- ✅ Passed checks (green)
- ❌ Failed checks (red)
- ⚠️ Skipped checks (yellow)

Example output:
```
Passed checks: 15, Failed checks: 3, Skipped checks: 0

Check: CKV_K8S_CUSTOM_001: "Ensure container does not run as root user"
	FAILED for resource: Deployment.default.nginx-deployment
	File: /deployment.yaml:1-25
	Guide: Running containers as root increases the risk of privilege escalation attacks.

		1  | apiVersion: apps/v1
		2  | kind: Deployment
		...
```

## Local Development Setup

### Option 1: Install System-wide

```bash
pip install checkov
```

### Option 2: Use Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv checkov-env

# Activate it
source checkov-env/bin/activate  # On Linux/Mac
# OR
checkov-env\Scripts\activate  # On Windows

# Install Checkov
pip install checkov
```

### Option 3: Use Docker

```bash
# Pull the Checkov image
docker pull bridgecrew/checkov:latest

# Run Checkov with Docker
docker run -v /path/to/manifests:/manifests \
           -v /path/to/checkov-compliance-rules:/rules \
           bridgecrew/checkov:latest \
           -d /manifests \
           --external-checks-dir /rules/policies
```

## CI/CD Integration

### GitHub Actions

1. Create workflow file `.github/workflows/checkov.yml`:

```yaml
name: Checkov Security Scan

on:
  pull_request:
    branches: [ main, develop ]
  push:
    branches: [ main ]

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Checkout compliance rules
        uses: actions/checkout@v3
        with:
          repository: tomer1983/checkov-compliance-rules
          path: compliance-rules

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov scan
        run: |
          checkov -d k8s/ \
            --external-checks-dir compliance-rules/policies \
            --output cli \
            --output json \
            --output-file-path console,checkov-results.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: checkov-results
          path: checkov-results.json
```

2. Commit and push the workflow file
3. Check the Actions tab in your GitHub repository

### GitLab CI/CD

1. Add to `.gitlab-ci.yml`:

```yaml
stages:
  - security

checkov-scan:
  stage: security
  image: python:3.10
  before_script:
    - pip install checkov
    - git clone https://github.com/tomer1983/checkov-compliance-rules.git
  script:
    - checkov -d k8s-manifests/ 
        --external-checks-dir checkov-compliance-rules/policies 
        --output cli 
        --output json 
        --output-file-path console,checkov-results.json
  artifacts:
    reports:
      junit: checkov-results.json
    paths:
      - checkov-results.json
    expire_in: 1 week
  allow_failure: false
```

2. Commit and push to trigger the pipeline

### Jenkins

1. Create a Jenkinsfile:

```groovy
pipeline {
    agent any
    
    environment {
        CHECKOV_VERSION = '2.3.187'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install checkov==${CHECKOV_VERSION}
                '''
            }
        }
        
        stage('Get Compliance Rules') {
            steps {
                dir('compliance-rules') {
                    git url: 'https://github.com/tomer1983/checkov-compliance-rules.git', 
                        branch: 'main'
                }
            }
        }
        
        stage('Run Checkov') {
            steps {
                sh '''
                    . venv/bin/activate
                    checkov -d k8s-manifests/ \
                        --external-checks-dir compliance-rules/policies \
                        --output cli \
                        --output junitxml \
                        --output-file-path console,checkov-results.xml
                '''
            }
        }
    }
    
    post {
        always {
            junit 'checkov-results.xml'
            archiveArtifacts artifacts: 'checkov-results.xml', allowEmptyArchive: true
        }
    }
}
```

2. Create a new Jenkins job using this Jenkinsfile

### Azure DevOps

1. Create `azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pr:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.10'
    addToPath: true

- script: |
    pip install checkov
  displayName: 'Install Checkov'

- checkout: self
- checkout: git://ProjectName/checkov-compliance-rules

- script: |
    checkov -d $(Build.SourcesDirectory)/k8s-manifests \
      --external-checks-dir $(Build.SourcesDirectory)/checkov-compliance-rules/policies \
      --output cli \
      --output junitxml \
      --output-file-path console,$(Common.TestResultsDirectory)/checkov-results.xml
  displayName: 'Run Checkov Scan'
  continueOnError: true

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: '**/checkov-results.xml'
    testRunTitle: 'Checkov Security Scan'
  condition: always()
```

## Customizing Policies

### Adjusting Severity Levels

Edit a policy file to change severity:

```yaml
metadata:
  id: "CKV_K8S_CUSTOM_001"
  name: "Ensure container does not run as root user"
  severity: "CRITICAL"  # Change from HIGH to CRITICAL
```

### Creating Custom Policies

1. Choose the appropriate directory:
   - `policies/kubernetes/security/` - Security-related checks
   - `policies/kubernetes/resource-management/` - Resource limits/requests
   - `policies/kubernetes/configuration/` - Configuration best practices
   - `policies/kubernetes/networking/` - Network policies
   - `policies/aws-eks/` - AWS EKS-specific checks

2. Create a new YAML file:

```yaml
---
metadata:
  id: "CKV_K8S_CUSTOM_XXX"  # Use next available number
  name: "Your custom check name"
  category: "KUBERNETES_SECURITY"
  severity: "HIGH"
  guideline: "Detailed explanation of why this check is important"
definition:
  cond_type: "attribute"
  resource_types:
    - "Deployment"
    - "StatefulSet"
  attribute: "spec.template.spec.containers[*].securityContext.runAsNonRoot"
  operator: "equals"
  value: true
```

3. Test your policy:

```bash
checkov -f examples/kubernetes/secure-deployment.yaml --external-checks-dir ./policies
```

### Skipping Checks

#### Method 1: Inline Skip (Recommended for specific resources)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: special-deployment
  annotations:
    checkov.io/skip1: CKV_K8S_CUSTOM_001=This is a legacy system, approved by security team
    checkov.io/skip2: CKV_K8S_CUSTOM_007=Resource limits not needed for this workload
spec:
  # ... rest of manifest
```

#### Method 2: Command-line Skip

```bash
checkov -d manifests/ \
  --external-checks-dir ./policies \
  --skip-check CKV_K8S_CUSTOM_001,CKV_K8S_CUSTOM_002
```

#### Method 3: Skip File

Create `.checkov.yaml`:

```yaml
skip-check:
  - CKV_K8S_CUSTOM_001  # Skip root user check
  - CKV_K8S_CUSTOM_013  # Skip liveness probe check
```

Then run:

```bash
checkov -d manifests/ --external-checks-dir ./policies --config-file .checkov.yaml
```

## Troubleshooting

### Issue: Policies Not Loading

**Symptom**: Checkov runs but doesn't execute custom policies

**Solutions**:
1. Verify path: `--external-checks-dir` should point to the `policies` directory
2. Check YAML syntax: Run `yamllint policies/` to validate
3. Ensure Python version: Checkov requires Python 3.7+

### Issue: False Positives

**Symptom**: Policy fails but configuration is correct

**Solutions**:
1. Check the attribute path in the policy definition
2. Verify the operator matches your use case
3. Test with simplified manifest
4. Skip the check if it's not applicable

### Issue: Performance Problems

**Symptom**: Scans take too long

**Solutions**:
1. Scan only specific directories: Use `-d` with precise paths
2. Use specific policy categories: Point to subdirectories like `policies/kubernetes/security`
3. Enable compact output: Use `--compact` flag
4. Scan in parallel: Split manifests into groups and scan concurrently

### Issue: Integration with Git Pre-commit

**Setup**:

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/bridgecrewio/checkov.git
    rev: '2.3.187'
    hooks:
      - id: checkov
        args: ['--external-checks-dir=./compliance-rules/policies', '-d=k8s/']
        additional_dependencies: ['checkov']
```

3. Install the hook:
```bash
pre-commit install
```

### Getting Help

If you encounter issues:

1. Check [Checkov documentation](https://www.checkov.io/)
2. Review [GitHub Issues](https://github.com/tomer1983/checkov-compliance-rules/issues)
3. Run with verbose output: `checkov -d manifests/ --external-checks-dir ./policies -v`
4. Test with example manifests from this repository

## Best Practices

1. **Start Small**: Begin with security policies, then expand to other categories
2. **Review Results**: Don't blindly fix all issues; understand each recommendation
3. **Document Skips**: Always add a reason when skipping checks
4. **Regular Updates**: Keep Checkov and policies updated
5. **Team Training**: Ensure team understands the policies and their purpose
6. **Incremental Adoption**: Apply to new projects first, then gradually to existing ones
7. **Customize Policies**: Adapt policies to your organization's specific needs
8. **Automate**: Integrate into CI/CD pipelines for continuous validation

## Next Steps

- Review the [Policy Reference](POLICIES.md) for detailed information on each check
- Check out [CI/CD Integration](CI_CD_INTEGRATION.md) for advanced integration scenarios
- Explore the `examples/` directory for sample manifests
- Consider contributing new policies or improvements

## Additional Resources

- [Checkov CLI Reference](https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [YAML Custom Policies Documentation](https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html)
