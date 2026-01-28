# Research: Local Kubernetes Deployment for Todo Chatbot

## Overview
This document captures research findings for the Kubernetes deployment of the Todo Chatbot application, addressing all "NEEDS CLARIFICATION" items from the Technical Context.

## Current Application Architecture
Based on examining the existing codebase:

### Frontend (Next.js)
- Located in `frontend/` directory
- Uses React with TypeScript
- API calls to backend via `/api` endpoints
- Environment variables for API URLs and authentication

### Backend (FastAPI)
- Located in `backend/` directory
- FastAPI web framework with Pydantic models
- Database connection to SQLite (todoapp.db) or Neon PostgreSQL
- Authentication with JWT tokens
- Cohere API integration for AI chatbot functionality
- Environment variables: `BETTER_AUTH_SECRET`, `COHERE_API_KEY`, `DATABASE_URL`

### Key Dependencies
- Frontend: React, Next.js, axios/fetch for API calls
- Backend: FastAPI, uvicorn, cohere, psycopg2-binary, python-jose, passlib

## Docker Strategy Decision
**Decision**: Gordon-first approach for Dockerfile generation, with fallback to optimized multi-stage Dockerfiles
**Rationale**: The constitution mandates Gordon-first strategy for container security and optimization. Gordon will generate secure, optimized multi-stage Dockerfiles with proper layer caching and minimal base images.
**Alternatives considered**:
- Manual Dockerfile creation (rejected - violates constitution requirement for AI-generated infrastructure)
- Standard templates without Gordon (rejected - doesn't meet security optimization goals)

## Helm Chart Generation Strategy
**Decision**: kubectl-ai for initial chart generation, kagent for optimization and hardening
**Rationale**: This follows the constitution's mandate for AI-first DevOps approach while allowing for iterative improvement of the generated charts.
**Alternatives considered**:
- Manual chart creation (rejected - violates constitution requirement for AI-generated infrastructure)
- Direct kubectl commands (rejected - bypasses AI tooling requirements)

## Minikube Configuration
**Decision**: Use docker driver with --cpus=4 --memory=8192 as specified in requirements
**Rationale**: Provides sufficient resources for running both frontend and backend services with AI chatbot functionality
**Configuration**:
- Driver: docker (for consistent local experience)
- CPUs: 4 (to handle concurrent AI requests and database operations)
- Memory: 8192MB (to accommodate both services and potential scaling)

## Ingress Strategy
**Decision**: Enable ingress addon with minikube tunnel for production-like access
**Rationale**: Enables proper hostname routing and prepares for future TLS implementation as specified in requirements
**Fallback**: Port-forward if ingress issues arise during development

## Secret Management
**Decision**: Single Kubernetes Secret containing all sensitive environment variables
**Rationale**: Simpler management for local deployment while maintaining security requirements
**Secret name**: `todo-secrets`
**Variables included**:
- BETTER_AUTH_SECRET
- COHERE_API_KEY
- DATABASE_URL

## Health Probes Configuration
**Decision**: Full health probe implementation (startup, liveness, readiness) with specified timeouts
**Configuration**:
- startupProbe: 30s timeout (for initial container startup)
- livenessProbe: 10s timeout (to detect deadlocks/failures)
- readinessProbe: 5s timeout (to control traffic routing)

## Resource Requests and Limits
**Decision**: Start with conservative values, optimize with kagent as needed
**Initial values**:
- Requests: 256Mi memory, 0.2 CPU
- Limits: 512Mi memory, 0.5 CPU
**Rationale**: Conservative values ensure cluster stability while allowing kagent to optimize based on actual usage patterns

## AI Tool Integration Points
### Gordon (Docker AI)
- Generate optimized multi-stage Dockerfiles for both frontend and backend
- Security scanning and vulnerability assessment
- Image size optimization

### kubectl-ai
- Generate initial Kubernetes manifests and Helm chart structure
- Troubleshooting and diagnosis ("why pod crashing?")
- Scaling operations and performance optimization

### kagent
- Cluster health analysis and resource optimization
- Real-time monitoring and performance suggestions
- Failure root-cause analysis and remediation

## Deployment Sequence
Based on the feature specification requirements:

1. **Phase 1**: Minikube & Cluster Foundation
   - Start Minikube with docker driver
   - Enable ingress addon
   - Run initial cluster health analysis

2. **Phase 2**: Containerization
   - Generate Dockerfiles using Gordon
   - Build and tag images for both services
   - Local smoke testing

3. **Phase 3**: Secrets Creation
   - Create Kubernetes Secret with environment variables
   - Verify secret creation

4. **Phase 4**: Helm Chart Generation
   - Generate umbrella chart with kubectl-ai
   - Optimize with kagent
   - Configure values and templates

5. **Phase 5**: Deployment
   - Install Helm chart to cluster
   - Wait for readiness

6. **Phase 6**: Validation & Optimization
   - Run AIOps validation
   - Apply optimizations suggested by kagent

7. **Phase 7**: Access & Observability
   - Set up ingress access
   - Configure monitoring

8. **Phase 8**: Full Testing
   - End-to-end functionality validation
   - Resilience testing

9. **Phase 9**: Documentation
   - Create deployment guide
   - Prepare demo assets

## Potential Challenges & Mitigations
1. **Gordon Availability**: If Gordon is region-locked or unavailable, fall back to ultra-optimized multi-stage Dockerfiles generated by Docker Engineer Agent
2. **Resource Constraints**: Monitor resource usage and adjust limits based on actual consumption
3. **Ingress Issues**: Have port-forward as backup access method
4. **AI Tool Limitations**: Maintain manual override capability while prioritizing AI tools

## Environment Variables Mapping
For Kubernetes Secret creation:
- BETTER_AUTH_SECRET: From local environment or .env file
- COHERE_API_KEY: From local environment or .env file
- DATABASE_URL: From local environment or .env file (Neon PostgreSQL connection string)