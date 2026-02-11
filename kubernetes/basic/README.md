# Basic Kubernetes Security Checks

This directory contains custom Checkov checks for basic Kubernetes security and best practices that apply to any Kubernetes cluster.

## Checks Overview

### Security Context Checks

#### CKV_K8S_CUSTOM_001: Pod Security Context
**Purpose**: Ensures pods have security context defined at the pod level.

**Why it matters**: Security contexts define privilege and access control settings. Without them, pods may run with unnecessary privileges.

**How to fix**:
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
```

---

#### CKV_K8S_CUSTOM_002: Read-Only Root Filesystem
**Purpose**: Ensures containers have `readOnlyRootFilesystem: true`.

**Why it matters**: Prevents containers from writing to their filesystem, reducing attack surface and preventing persistence of malicious changes.

**How to fix**:
```yaml
containers:
- name: app
  securityContext:
    readOnlyRootFilesystem: true
  volumeMounts:
  - name: tmp
    mountPath: /tmp
volumes:
- name: tmp
  emptyDir: {}
```

---

#### CKV_K8S_CUSTOM_003: Run as Non-Root
**Purpose**: Ensures containers run as non-root user.

**Why it matters**: Running as root increases security risk. If a container is compromised, the attacker has root privileges.

**How to fix**:
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
```

---

#### CKV_K8S_CUSTOM_004: No Privileged Containers
**Purpose**: Ensures containers don't run in privileged mode.

**Why it matters**: Privileged containers have access to all host devices and can perform system administration tasks, significantly increasing security risk.

**How to fix**: Remove or set to false:
```yaml
containers:
- name: app
  securityContext:
    privileged: false
```

---

#### CKV_K8S_CUSTOM_007: Drop All Capabilities
**Purpose**: Ensures containers drop all Linux capabilities.

**Why it matters**: Linux capabilities provide fine-grained privileges. Dropping all and adding only necessary ones follows the principle of least privilege.

**How to fix**:
```yaml
containers:
- name: app
  securityContext:
    capabilities:
      drop:
        - ALL
      add:
        - NET_BIND_SERVICE  # Only add if needed
```

---

### Resource Management Checks

#### CKV_K8S_CUSTOM_005: Resource Limits
**Purpose**: Ensures containers have CPU and memory limits defined.

**Why it matters**: Prevents resource exhaustion and ensures fair resource distribution across pods.

**How to fix**:
```yaml
containers:
- name: app
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
```

---

#### CKV_K8S_CUSTOM_006: Resource Requests
**Purpose**: Ensures containers have CPU and memory requests defined.

**Why it matters**: Helps Kubernetes scheduler make informed decisions about pod placement.

**How to fix**:
```yaml
containers:
- name: app
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
```

---

### Health Check Probes

#### CKV_K8S_CUSTOM_008: Liveness Probe
**Purpose**: Ensures containers have liveness probes configured.

**Why it matters**: Liveness probes allow Kubernetes to restart unhealthy containers automatically.

**How to fix**:
```yaml
containers:
- name: app
  livenessProbe:
    httpGet:
      path: /health
      port: 8080
    initialDelaySeconds: 30
    periodSeconds: 10
```

---

#### CKV_K8S_CUSTOM_009: Readiness Probe
**Purpose**: Ensures containers have readiness probes configured.

**Why it matters**: Readiness probes prevent traffic from being sent to pods that aren't ready to handle requests.

**How to fix**:
```yaml
containers:
- name: app
  readinessProbe:
    httpGet:
      path: /ready
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
```

---

### Image Security Checks

#### CKV_K8S_CUSTOM_010: Image Pull Policy
**Purpose**: Ensures `imagePullPolicy` is explicitly set.

**Why it matters**: Explicit pull policies ensure predictable behavior and prevent using outdated images.

**How to fix**:
```yaml
containers:
- name: app
  imagePullPolicy: IfNotPresent  # or Always, Never
```

---

#### CKV_K8S_CUSTOM_011: Image Tag
**Purpose**: Ensures images use specific tags, not `latest`.

**Why it matters**: Using `latest` makes deployments unpredictable and makes rollbacks difficult.

**How to fix**:
```yaml
containers:
- name: app
  image: myapp:1.0.0  # Use specific version tag
```

---

### Network Security Checks

#### CKV_K8S_CUSTOM_012: No Host Network
**Purpose**: Ensures pods don't use `hostNetwork`.

**Why it matters**: Host network mode gives pods access to the host's network stack, bypassing network policies and increasing attack surface.

**How to fix**: Remove or set to false:
```yaml
spec:
  hostNetwork: false
```

---

## Running These Checks

```bash
# Check all manifests in current directory
checkov -d . --external-checks-dir /path/to/kubernetes/basic

# Check specific file
checkov -f deployment.yaml --external-checks-dir /path/to/kubernetes/basic

# Output in JSON format
checkov -d . --external-checks-dir /path/to/kubernetes/basic --output json
```

## Further Reading

- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [NSA Kubernetes Hardening Guide](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2716980/nsa-cisa-release-kubernetes-hardening-guidance/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
