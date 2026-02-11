# Quick Start Guide

This guide will help you get started with the Checkov Compliance Rules for Kubernetes in just a few minutes.

## Prerequisites

1. **Python 3.7 or higher**
   ```bash
   python3 --version
   ```

2. **Install Checkov**
   ```bash
   pip install checkov
   # Or using pipx for isolated installation
   pipx install checkov
   ```

## 5-Minute Quickstart

### Step 1: Clone the Repository

```bash
git clone https://github.com/tomer1983/checkov-compliance-rules.git
cd checkov-compliance-rules
```

### Step 2: Test with Example Manifests

Run checks on the compliant example:
```bash
checkov -f examples/compliant-deployment.yaml \
  --external-checks-dir kubernetes/basic
```

Expected output: ✅ Most checks should pass

Run checks on the non-compliant example:
```bash
checkov -f examples/non-compliant-deployment.yaml \
  --external-checks-dir kubernetes/basic
```

Expected output: ❌ Multiple checks should fail with detailed explanations

### Step 3: Check Your Own Manifests

Point Checkov to your Kubernetes manifests directory:
```bash
checkov -d /path/to/your/k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --compact
```

### Step 4: Add EKS-Specific Checks (if using AWS EKS)

```bash
checkov -d /path/to/your/k8s-manifests \
  --external-checks-dir kubernetes/basic \
  --external-checks-dir eks/specific \
  --compact
```

## Common Use Cases

### Use Case 1: Pre-commit Hook

Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/bridgecrewio/checkov.git
    rev: 2.3.0
    hooks:
      - id: checkov
        args: [
          "-d", "k8s-manifests/",
          "--external-checks-dir", "path/to/kubernetes/basic"
        ]
```

### Use Case 2: CI/CD Pipeline

**GitHub Actions** (`.github/workflows/checkov.yml`):
```yaml
name: Kubernetes Manifest Check
on: [push, pull_request]

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Checkov
        run: pip install checkov
      
      - name: Clone compliance rules
        uses: actions/checkout@v3
        with:
          repository: tomer1983/checkov-compliance-rules
          path: compliance-rules
      
      - name: Run Checkov
        run: |
          checkov -d ./k8s/ \
            --external-checks-dir ./compliance-rules/kubernetes/basic \
            --compact
```

**GitLab CI** (`.gitlab-ci.yml`):
```yaml
checkov:
  image: bridgecrew/checkov:latest
  script:
    - git clone https://github.com/tomer1983/checkov-compliance-rules.git
    - checkov -d ./k8s/ --external-checks-dir ./checkov-compliance-rules/kubernetes/basic
```

### Use Case 3: Local Development Workflow

Create a shell script `check-manifests.sh`:
```bash
#!/bin/bash

RULES_DIR="$HOME/checkov-compliance-rules"

echo "🔍 Running Kubernetes compliance checks..."

checkov -d ./k8s-manifests \
  --external-checks-dir "$RULES_DIR/kubernetes/basic" \
  --external-checks-dir "$RULES_DIR/eks/specific" \
  --compact \
  --quiet

if [ $? -eq 0 ]; then
  echo "✅ All checks passed!"
else
  echo "❌ Some checks failed. Please review the output above."
  exit 1
fi
```

Make it executable:
```bash
chmod +x check-manifests.sh
./check-manifests.sh
```

### Use Case 4: Automated Fix Workflow

While Checkov doesn't auto-fix, you can create a workflow:

1. Run checks and save output:
   ```bash
   checkov -d ./k8s \
     --external-checks-dir kubernetes/basic \
     --output json \
     --output-file-path results.json
   ```

2. Review results:
   ```bash
   cat results.json | jq '.results.failed_checks[] | {check: .check_id, file: .file_path}'
   ```

3. Fix issues based on check IDs (refer to READMEs)

4. Re-run checks to verify fixes

## Understanding Check Results

### Passed Check ✅
```
Check: CKV_K8S_CUSTOM_003: "Ensure containers run as non-root user"
        PASSED for resource: Deployment.default.secure-app
        File: /deployment.yaml:1-50
```
**Action**: None needed - keep it this way!

### Failed Check ❌
```
Check: CKV_K8S_CUSTOM_003: "Ensure containers run as non-root user"
        FAILED for resource: Deployment.default.insecure-app
        File: /deployment.yaml:1-50
        Guide: https://docs.checkov.io/...
```
**Action**: Review the check documentation and fix the manifest

### Skipped Check ⏭️
```
Check: CKV_K8S_CUSTOM_009: "Ensure containers have readiness probe configured"
        SKIPPED for resource: Job.default.migration-job
```
**Action**: Check may not apply to this resource type

## Skipping Checks When Needed

Sometimes you need to skip specific checks (e.g., init containers don't need probes):

### Inline Skip (in YAML)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: special-pod
  annotations:
    checkov.io/skip1: CKV_K8S_CUSTOM_008=Init container doesn't need liveness probe
spec:
  # ... rest of spec
```

### Command-line Skip
```bash
checkov -d ./k8s \
  --external-checks-dir kubernetes/basic \
  --skip-check CKV_K8S_CUSTOM_008,CKV_K8S_CUSTOM_009
```

### Config File Skip (`.checkov.yaml`)
```yaml
skip-check:
  - CKV_K8S_CUSTOM_008
  - CKV_K8S_CUSTOM_009
```

## Troubleshooting

### Issue: "No checks ran"
**Solution**: Ensure you're pointing to the correct check directory
```bash
ls kubernetes/basic/*.py  # Should show check files
```

### Issue: "Module not found"
**Solution**: Ensure Checkov is installed correctly
```bash
pip show checkov
checkov --version
```

### Issue: Checks not finding resources
**Solution**: Check your YAML syntax is valid
```bash
kubectl apply --dry-run=client -f your-manifest.yaml
```

## Next Steps

1. ✅ Review the [main README](README.md) for detailed documentation
2. ✅ Check [kubernetes/basic/README.md](kubernetes/basic/README.md) for basic checks
3. ✅ Check [eks/specific/README.md](eks/specific/README.md) for EKS-specific checks
4. ✅ Integrate into your CI/CD pipeline
5. ✅ Set up pre-commit hooks
6. ✅ Customize checks for your organization

## Getting Help

- 📖 Read the detailed READMEs in each directory
- 🐛 Open an issue on GitHub
- 💬 Check [Checkov documentation](https://www.checkov.io/)
- 📚 Review [Kubernetes security best practices](https://kubernetes.io/docs/concepts/security/)

Happy checking! 🚀
