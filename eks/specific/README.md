# AWS EKS Specific Security Checks

This directory contains custom Checkov checks specifically designed for Amazon Elastic Kubernetes Service (EKS) environments.

## Checks Overview

### IAM and Service Account Checks

#### CKV_EKS_CUSTOM_001: IRSA Annotation
**Purpose**: Ensures ServiceAccounts have IAM role annotations for IRSA (IAM Roles for Service Accounts).

**Why it matters**: IRSA provides secure, fine-grained IAM permissions to pods without using static credentials.

**How to fix**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/my-app-role
```

**AWS Setup Required**:
```bash
# Create IAM role with trust policy for OIDC provider
eksctl create iamserviceaccount \
  --name my-app-sa \
  --namespace default \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
  --approve
```

---

#### CKV_EKS_CUSTOM_002: Pod ServiceAccount
**Purpose**: Ensures pods specify a non-default ServiceAccount.

**Why it matters**: Using custom ServiceAccounts with IRSA provides better security and auditability than the default ServiceAccount.

**How to fix**:
```yaml
spec:
  serviceAccountName: my-app-sa  # Not "default"
  containers:
  - name: app
    image: myapp:1.0.0
```

---

### Load Balancer Checks

#### CKV_EKS_CUSTOM_003: LoadBalancer Annotations
**Purpose**: Ensures LoadBalancer services have AWS-specific annotations.

**Why it matters**: AWS annotations control load balancer behavior, security groups, and network configuration.

**How to fix**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # or "external"
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
```

---

#### CKV_EKS_CUSTOM_004: Internal LoadBalancer
**Purpose**: Ensures LoadBalancer services are internal (not internet-facing) by default.

**Why it matters**: Internal load balancers are only accessible within your VPC, reducing exposure to the internet.

**How to fix**:
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-scheme: internal
    # Or for older versions:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
```

**For internet-facing services** (when needed):
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
```

---

### Ingress Controller Checks

#### CKV_EKS_CUSTOM_005: Ingress Controller
**Purpose**: Ensures Ingress resources use the AWS Load Balancer Controller.

**Why it matters**: AWS Load Balancer Controller provides better integration with AWS services, ALB features, and cost optimization.

**How to fix**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internal
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

**Prerequisites**:
```bash
# Install AWS Load Balancer Controller
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster
```

---

### Storage Checks

#### CKV_EKS_CUSTOM_006: StorageClass CSI Driver
**Purpose**: Ensures StorageClass uses the AWS EBS CSI driver.

**Why it matters**: The in-tree EBS provisioner is deprecated. The CSI driver provides better features and is the future-proof option.

**How to fix**:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com  # Not kubernetes.io/aws-ebs
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: gp3
  encrypted: "true"
```

**Prerequisites**:
```bash
# Install EBS CSI driver
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.15"
```

---

#### CKV_EKS_CUSTOM_007: PersistentVolume CSI Driver
**Purpose**: Ensures PersistentVolumes use the AWS EBS CSI driver.

**Why it matters**: Same as StorageClass - CSI driver is the modern, supported approach.

**How to fix**:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  csi:
    driver: ebs.csi.aws.com
    volumeHandle: vol-0123456789abcdef
```

---

### Instance Metadata Service Checks

#### CKV_EKS_CUSTOM_008: IMDSv2 Compliance
**Purpose**: Ensures pods don't use hostNetwork, which can bypass IMDSv2 restrictions.

**Why it matters**: IMDSv2 provides protection against SSRF attacks. Pods using hostNetwork can bypass this protection.

**How to fix**:
```yaml
spec:
  hostNetwork: false  # Don't use host networking
  serviceAccountName: my-app-sa  # Use IRSA instead
```

**EC2 Node Configuration** (required):
```bash
# Ensure nodes are configured to require IMDSv2
aws ec2 modify-instance-metadata-options \
  --instance-id i-1234567890abcdef0 \
  --http-tokens required \
  --http-put-response-hop-limit 1
```

---

## EKS-Specific Best Practices Summary

### 1. Identity and Access Management
- Use IRSA for pod-level IAM permissions
- Create dedicated IAM roles per service
- Follow principle of least privilege

### 2. Network Security
- Use internal load balancers by default
- Leverage AWS Load Balancer Controller for advanced features
- Implement Network Policies

### 3. Storage
- Migrate to CSI drivers (EBS CSI, EFS CSI)
- Enable encryption at rest
- Use VolumeBinding mode WaitForFirstConsumer

### 4. Security
- Require IMDSv2 on all nodes
- Use VPC endpoints for AWS services
- Enable EKS cluster logging

## Running These Checks

```bash
# Check all EKS manifests
checkov -d . --external-checks-dir /path/to/eks/specific

# Check both basic and EKS-specific
checkov -d . \
  --external-checks-dir /path/to/kubernetes/basic \
  --external-checks-dir /path/to/eks/specific

# Check only EKS resources (Service, Ingress, StorageClass)
checkov -f service.yaml --external-checks-dir /path/to/eks/specific
```

## EKS Setup Checklist

- [ ] Install AWS Load Balancer Controller
- [ ] Install EBS CSI Driver
- [ ] Install EFS CSI Driver (if needed)
- [ ] Configure OIDC provider for IRSA
- [ ] Enable IMDSv2 on all nodes
- [ ] Configure VPC CNI plugin
- [ ] Enable cluster logging
- [ ] Set up Pod Security Standards

## Further Reading

- [AWS EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)
- [EBS CSI Driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
- [EKS Security Best Practices](https://aws.github.io/aws-eks-best-practices/security/docs/)
