# Data Model: Local Kubernetes Deployment for Todo Chatbot

## Overview
This document defines the data models relevant to the Kubernetes deployment of the Todo Chatbot application, including both application-level entities and infrastructure-level configurations.

## Application Data Models

### Task Entity
The core entity from the existing Todo application:

```yaml
Task:
  id: UUID (primary key)
  title: string (required, max 255 chars)
  description: string (optional, max 1000 chars)
  completed: boolean (default: false)
  created_at: datetime (auto-generated)
  updated_at: datetime (auto-generated)
  user_id: UUID (foreign key to User)
```

### User Entity
Authentication user entity:

```yaml
User:
  id: UUID (primary key)
  email: string (unique, required)
  hashed_password: string (required)
  is_active: boolean (default: true)
  created_at: datetime (auto-generated)
  updated_at: datetime (auto-generated)
```

## Kubernetes Infrastructure Models

### Container Images
Docker image specifications for deployment:

#### Frontend Image
```yaml
FrontendImage:
  name: "todo-frontend"
  tag: "latest"
  base_image: "node:18-alpine" (optimized via Gordon)
  build_context: "./frontend"
  ports: [3000]
  working_directory: "/app"
  security:
    run_as_non_root: true
    read_only_root_filesystem: true
    drop_all_capabilities: true
```

#### Backend Image
```yaml
BackendImage:
  name: "todo-backend"
  tag: "latest"
  base_image: "python:3.11-slim" (optimized via Gordon)
  build_context: "./backend"
  ports: [8000]
  working_directory: "/app"
  security:
    run_as_non_root: true
    read_only_root_filesystem: true
    drop_all_capabilities: true
```

### Kubernetes Resources

#### Deployment Configuration
```yaml
Deployment:
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: string (e.g., "frontend", "backend")
    namespace: string (default: "default")
  spec:
    replicas: integer (default: 2, min: 1, max: 5)
    selector:
      matchLabels:
        app: string (deployment name)
    template:
      metadata:
        labels:
          app: string (deployment name)
      spec:
        containers:
          - name: string (container name)
            image: string (image:tag)
            ports:
              - containerPort: integer (port number)
                protocol: string (TCP)
            envFrom:
              - secretRef:
                  name: "todo-secrets"
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
            livenessProbe:
              httpGet:
                path: "/health"
                port: integer
              initialDelaySeconds: 30
              periodSeconds: 10
            readinessProbe:
              httpGet:
                path: "/ready"
                port: integer
              initialDelaySeconds: 5
              periodSeconds: 5
            startupProbe:
              httpGet:
                path: "/startup"
                port: integer
              initialDelaySeconds: 10
              periodSeconds: 5
              failureThreshold: 30
        securityContext:
          runAsNonRoot: true
          fsGroup: 1000
```

#### Service Configuration
```yaml
Service:
  apiVersion: v1
  kind: Service
  metadata:
    name: string (e.g., "frontend-service", "backend-service")
    namespace: string (default: "default")
  spec:
    selector:
      app: string (corresponding deployment name)
    ports:
      - protocol: "TCP"
        port: integer (service port)
        targetPort: integer (container port)
    type: "ClusterIP" (internal access) or "NodePort" (external access)
```

#### Ingress Configuration
```yaml
Ingress:
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: "todo-ingress"
    namespace: "default"
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
  spec:
    rules:
      - host: "todo.local"
        http:
          paths:
            - path: /
              pathType: Prefix
              backend:
                service:
                  name: "frontend-service"
                  port:
                    number: 80
            - path: /api
              pathType: Prefix
              backend:
                service:
                  name: "backend-service"
                  port:
                    number: 80
```

#### Secret Configuration
```yaml
Secret:
  apiVersion: v1
  kind: Secret
  metadata:
    name: "todo-secrets"
    namespace: "default"
  type: Opaque
  data:
    BETTER_AUTH_SECRET: base64_encoded_value
    COHERE_API_KEY: base64_encoded_value
    DATABASE_URL: base64_encoded_value
```

### Helm Chart Structure

#### Chart.yaml
```yaml
Chart:
  name: "todo"
  version: "0.1.0"
  apiVersion: "v2"
  description: "Todo Chatbot Application"
  type: "application"
  appVersion: "1.0.0"
  dependencies:
    - name: "frontend"
      version: "0.1.0"
      repository: "file://./charts/frontend"
    - name: "backend"
      version: "0.1.0"
      repository: "file://./charts/backend"
    - name: "database"
      version: "0.1.0"
      repository: "file://./charts/database"
```

#### Values.yaml (Default)
```yaml
Values:
  global:
    imageRegistry: ""
    imagePullSecrets: []
    storageClass: ""

  frontend:
    replicaCount: 2
    image:
      repository: "todo-frontend"
      pullPolicy: "IfNotPresent"
      tag: "latest"
    service:
      type: ClusterIP
      port: 80
    ingress:
      enabled: true
      hosts:
        - host: todo.local
          paths:
            - path: /
              pathType: Prefix
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 250m
        memory: 256Mi
    nodeSelector: {}
    tolerations: []
    affinity: {}

  backend:
    replicaCount: 2
    image:
      repository: "todo-backend"
      pullPolicy: "IfNotPresent"
      tag: "latest"
    service:
      type: ClusterIP
      port: 80
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 250m
        memory: 256Mi
    nodeSelector: {}
    tolerations: []
    affinity: {}

  database:
    enabled: false  # Assuming external database (Neon)
    # If internal DB needed:
    # replicaCount: 1
    # image: postgres:13
```

### Horizontal Pod Autoscaler
```yaml
HorizontalPodAutoscaler:
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: "backend-hpa"
    namespace: "default"
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: "backend"
    minReplicas: 2
    maxReplicas: 10
    metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
```

## Configuration Validation Rules

### Security Requirements
1. All containers must run as non-root users
2. Secrets must not be stored in plain text
3. Network policies should restrict unnecessary communication
4. Image scanning must pass before deployment

### Resource Constraints
1. Memory limits must be set for all deployments
2. CPU limits must prevent resource exhaustion
3. Resource requests must ensure adequate allocation
4. HPA must be configured for scaling based on load

### Health Check Requirements
1. All deployments must have liveness probes
2. All deployments must have readiness probes
3. Startup probes must be configured for applications with slow startup
4. Probe timeouts must be appropriate for application characteristics

### Deployment Requirements
1. Rolling updates must be configured for zero-downtime deployments
2. Replica counts must support high availability
3. Affinity/anti-affinity rules may be needed for distributed workloads
4. Node selectors may be needed for specific resource requirements