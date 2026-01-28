# Claude Agent Context - Phase IV: Cloud-Native Kubernetes Deployment

## Project: Phase IV – Local Kubernetes Deployment for Todo Chatbot

### Tech Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with Cohere AI integration
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth (JWT)
- **Containerization**: Docker with Gordon AI optimization
- **Orchestration**: Kubernetes on Minikube
- **Package Management**: Helm 3.x charts
- **AI DevOps Tools**: kubectl-ai, kagent

### Current Phase: Kubernetes Deployment (Phase IV)
- Monorepo structure with frontend/backend directories
- AI-generated Dockerfiles for containerization (Gordon-first approach)
- AI-generated Helm charts for orchestration (kubectl-ai + kagent)
- Minikube cluster setup with ingress addon
- Kubernetes Secrets for environment variables
- Health probes (liveness, readiness, startup)
- Horizontal Pod Autoscaler configuration
- Complete AI-assisted deployment workflow

### Kubernetes Resources
- **Deployments**: Frontend and backend with replica sets
- **Services**: ClusterIP services for internal communication
- **Ingress**: External access via hostname routing
- **Secrets**: Secure storage for sensitive environment variables
- **HPA**: Horizontal Pod Autoscaler for auto-scaling
- **NetworkPolicy**: Optional network security (deny-all + allow ingress)

### File Structure
```
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
├── main.py
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
├── package.json
└── Dockerfile

docker/
├── frontend.Dockerfile     # AI-generated multi-stage Dockerfile
└── backend.Dockerfile      # AI-generated multi-stage Dockerfile

charts/
└── todo/                   # Umbrella Helm chart
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── _helpers.tpl
    │   ├── frontend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── ingress.yaml
    │   ├── backend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── hpa.yaml
    │   ├── secrets.yaml
    │   └── networkpolicy.yaml
    └── charts/             # Subcharts
        ├── frontend/
        ├── backend/

k8s/
└── manifests/              # Generated manifests for reference

specs/1-k8s-deployment/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api-contracts.md
└── tasks.md

.env (local), Kubernetes Secrets (cluster)
```

### Kubernetes Configuration
- **Minikube**: Started with --driver=docker --cpus=4 --memory=8192
- **Ingress**: Enabled with minikube tunnel for hostname access
- **Images**: todo-frontend:latest, todo-backend:latest
- **Secrets**: todo-secrets containing BETTER_AUTH_SECRET, COHERE_API_KEY, DATABASE_URL
- **Health Probes**: startupProbe (30s), liveness (10s), readiness (5s)
- **Resources**: Requests (256Mi/0.2 CPU), Limits (512Mi/0.5 CPU)

### Environment Variables in Kubernetes
- BETTER_AUTH_SECRET: From Kubernetes Secret
- COHERE_API_KEY: From Kubernetes Secret
- DATABASE_URL: From Kubernetes Secret (Neon PostgreSQL connection)
- BACKEND_API_URL: Internal service URL (http://backend-service:80)

### AI Tool Integration
- **Gordon**: Container optimization and security scanning
- **kubectl-ai**: Kubernetes manifest generation and troubleshooting
- **kagent**: Cluster health analysis and optimization suggestions
- **Helm**: Package management for Kubernetes applications

### Deployment Workflow
1. Minikube cluster initialization
2. Docker image building and tagging
3. Kubernetes Secret creation
4. Helm chart generation (AI-assisted)
5. Helm deployment to cluster
6. Health verification and scaling
7. Ingress access setup
8. Full application testing

### Security Measures
- Non-root containers with security contexts
- Read-only root filesystem where possible
- Kubernetes Secrets for sensitive data
- Network policies for service communication
- Proper RBAC and privilege separation