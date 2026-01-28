<!-- Sync Impact Report:
- Version change: 3.0.0 → 4.0.0
- Modified principles: Updated for Phase IV cloud-native deployment focus
- Added sections: Containerization, Helm Charts, Minikube Cluster, AI DevOps Tools, Security & Hardening
- Removed sections: Phase III specific requirements
- Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Local Kubernetes Deployment Constitution - Phase IV: Cloud-Native Todo Chatbot

## Project Overview

From AI Chatbot to local cloud-native deployment, the objective is to achieve production-grade local excellence. The Evolution of Todo continues from Phase III (Full-Stack Web Application with AI Chatbot) to Phase IV, transforming the existing application into a fully containerized, cloud-native deployment using Kubernetes. The objective is to provide a production-grade local deployment on Minikube with containerized frontend (Next.js) and backend (FastAPI + Cohere chatbot) services, ensuring enterprise-level observability, resilience, and operational excellence through AI-powered DevOps tools.

## Core Requirements

### I. Containerization and Orchestration
Both frontend (Next.js) and backend (FastAPI + Cohere chatbot) services must be containerized with optimized multi-stage Dockerfiles, deployed as Kubernetes deployments with replica sets, resource limits/requests, and health probes to ensure reliable operation in the cluster.

### II. AI-Generated Infrastructure as Code
All infrastructure must be AI-generated using agentic tools with production-ready Helm charts that include all necessary components: Deployments, Services, Ingress controllers, ConfigMaps, and Secrets. No manual YAML or kubectl commands are permitted - everything must be AI-generated only.

### III. Minikube Cluster Deployment
The application must deploy successfully on Minikube with ingress-enabled access and port-forward fallback, utilizing the docker driver with ingress addon enabled to provide local access to both frontend and backend services.

### IV. AIOps Validation and Resilience
The system must leverage kubectl-ai and kagent for intelligent creation, troubleshooting, and scaling operations. Full observability (logs, events, pod status) and resilience (self-healing, restarts) must be ensured through proper monitoring and alerting configurations.

## Containerization Strategy

### Multi-Stage Dockerfiles
Frontend and backend services must use optimized multi-stage Dockerfiles that:
- Implement security best practices (non-root user, minimal base images)
- Apply Gordon-first strategy for container security scanning
- Include proper build optimizations and caching layers
- Follow Docker security guidelines (no secrets in images, proper layer ordering)

### Gordon Security Integration
All Docker builds must utilize Gordon Beta for security scanning and compliance verification. Container images must pass security scans before deployment to ensure no vulnerabilities exist in the base images or dependencies.

### Image Optimization
Docker images must be optimized for size and security with:
- Minimal base images (alpine or distroless where possible)
- Multi-stage builds to separate build and runtime environments
- Proper cleanup of build artifacts and package managers
- Non-root user execution within containers

## Helm Charts Architecture

### Umbrella Chart Structure
The system must implement an umbrella Helm chart with subcharts for:
- Frontend service (Next.js application)
- Backend service (FastAPI + Cohere API)
- Database (PostgreSQL/Neon connector)
- Ingress controller
- Monitoring and observability components

### Values Configuration
Values.yaml files must be fully configurable with defaults for local development and production-like settings, supporting environment-specific overrides and secret management through Kubernetes Secrets.

### Template Requirements
Helm templates must include:
- Deployments with replica sets (minimum 1, scalable to 3+)
- Services with proper selectors and ports
- Ingress resources with TLS termination (where applicable)
- Health probes (liveness and readiness)
- Resource limits and requests (CPU/memory)
- Horizontal Pod Autoscaler configurations
- Proper security contexts and RBAC where needed

## Minikube Cluster Operations

### Cluster Setup
Minikube must be started with docker driver and ingress addon enabled, with proper resource allocation (4GB+ RAM, 2+ CPUs) to handle the multi-service application workload.

### Access Patterns
The system must support both ingress-based access and port-forward fallback for service connectivity, with proper host alias configuration for local development access.

### Tunneling and Networking
Network policies and service discovery must work properly within the Minikube environment, with clear documentation on accessing services both internally and externally through various methods (ingress, port-forward, minikube tunnel).

## AI DevOps Tools Integration

### Gordon Usage Examples
Gordon must be leveraged for:
- Container security scanning and compliance checking
- Multi-stage Dockerfile generation and optimization
- Automated vulnerability remediation recommendations

### kubectl-ai Prompt Patterns
Standard prompt patterns must be established for:
- Resource creation and configuration
- Troubleshooting and debugging
- Scaling operations and performance optimization
- Monitoring and alerting setup

### kagent Operations
kagent tools must be used for:
- Cluster health monitoring and optimization
- Pod status and performance analysis
- Automatic scaling and self-healing operations
- Event correlation and incident response

## Security & Hardening

### Kubernetes Secrets Management
All sensitive environment variables (BETTER_AUTH_SECRET, COHERE_API_KEY, DATABASE_URL) must be stored as Kubernetes Secrets and mounted as environment variables or volumes, with no plaintext secrets in configuration files or Docker images.

### Least-Privilege Security
Pod security contexts must be configured with minimal required privileges, following least-privilege principles for container execution and resource access.

### Health Probes Enforcement
Liveness and readiness probes must be implemented for all services to ensure application health and proper traffic routing within the cluster.

## Development Workflow

### Agentic Development Process
Strict adherence to constitution → specs → plans → agents/skills → validation → iteration workflow, with all infrastructure changes performed through Claude Code agents and Spec-Kit Plus skills.

### AI-Powered Operations
All Kubernetes operations must utilize AI tools (kubectl-ai, kagent) for creation, troubleshooting, and optimization, avoiding manual kubectl commands or YAML creation.

### Continuous Validation
Regular validation of cluster health, security posture, and application functionality through automated testing and monitoring tools.

## Monorepo Updates

### Directory Structure
New directories must be added to maintain infrastructure code:
- `docker/` - Contains multi-stage Dockerfiles for frontend and backend
- `charts/` - Helm chart definitions with subcharts and values
- `k8s/manifests/` - Generated manifests for CI/CD (if needed)
- Update `.specify/config` to reflect new project structure

### Documentation Updates
All new infrastructure components must be documented with clear deployment and troubleshooting guides, including AI tool usage examples and cluster maintenance procedures.

## Guiding Principles

### Spec-Driven Infrastructure
All infrastructure changes must be defined in specifications before implementation, with clear requirements and validation criteria before any code is written.

### AI-First DevOps Approach
Prioritize AI-powered DevOps tools (kubectl-ai, kagent, Gordon) for all infrastructure operations, treating them as primary tools rather than supplementary.

### Resilience and Observability
Design for failure with proper health checks, logging, and monitoring to ensure applications can self-heal and remain observable under all conditions.

### Back to Basics
Return to fundamental DevOps principles while leveraging modern AI tools, ensuring that automation serves to enhance rather than replace understanding.

### Enterprise-Level Quality
Maintain production-grade standards for all infrastructure components, with proper security, monitoring, and operational procedures from day one.

## Deliverables and Success Criteria

### Running Minikube Cluster
Successfully deployed application on local Minikube cluster with all services accessible and functioning properly.

### AI-Generated Artifacts
Complete set of AI-generated Dockerfiles, Helm charts, and Kubernetes configurations with no manually created YAML files.

### Kubernetes Secrets
Properly configured Kubernetes Secrets for all sensitive environment variables with secure mounting in pods.

### Demo Commands
Comprehensive set of commands and procedures for demoing the cloud-native deployment with screenshots showing cluster status and application functionality.

### Screenshots and Documentation
Visual evidence of successful deployment with cluster metrics, pod statuses, and application accessibility through ingress.

## Governance

This constitution supersedes all other practices and development guidelines for Phase IV implementation. All infrastructure must be AI-generated, with no manual kubectl commands or YAML creation permitted. Amendments require explicit documentation and approval process. All pull requests and code reviews must verify constitution compliance. Specifications serve as the authoritative source for all implementation decisions.

**Version**: 4.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26