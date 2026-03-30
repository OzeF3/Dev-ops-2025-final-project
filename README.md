
# Seyoawe Community - DevOps Final Project

## Architecture Overview

This project implements a full DevOps lifecycle around the Seyoawe automation engine.

### Components

- **GitHub** - source control
- **Jenkins** - CI/CD pipelines
- **Docker** - containerization
- **Docker Hub** - container registry (devoeoe23ops)
- **Terraform** - AWS EC2 provisioning
- **Ansible** - server configuration
- **Kubernetes** - application orchestration
- **Prometheus & Grafana** - monitoring

---

## Repository Structure

```
seyoawe-community/
├── docker/          # Dockerfiles for engine and CLI
├── jenkins/         # CI/CD pipeline definitions
│   ├── engine/      # CI pipeline for the engine
│   ├── cli/         # CI pipeline for the CLI
│   ├── cd/          # CD pipeline (Terraform + Ansible + K8s)
│   └── version-check.sh
├── k8s/             # Kubernetes manifests
├── terraform/       # AWS infrastructure provisioning
├── ansible/         # Server configuration playbooks
├── monitoring/      # Prometheus & Grafana setup
├── modules/         # Seyoawe engine modules
├── sawectl/         # CLI tool
├── workflows/       # Sample workflows
└── version.txt      # Shared semantic version
```

---

## Pipeline Flow

### CI Pipeline (Engine)

1. Checkout code
2. Version check - detect changed components
3. Lint Python modules
4. Build Docker image
5. Push to Docker Hub as `devoeoe23ops/seyoawe-engine:<version>`

### CI Pipeline (CLI)

1. Checkout code
2. Version check - detect changed components
3. Install dependencies
4. Lint & unit tests
5. Build Docker image
6. Push to Docker Hub as `devoeoe23ops/seyoawe-cli:<version>`
7. Tag Git with version

### CD Pipeline

1. Checkout code
2. Terraform init, plan, apply → provision EC2 on AWS (us-west-2)
3. Update Ansible inventory with EC2 IP
4. Wait for EC2 to be ready
5. Run Ansible playbook → install Docker & kubectl, pull image
6. Deploy to Kubernetes using manifests

---

## Version Coupling

Both engine and CLI share the same semantic version defined in `version.txt`.
The `jenkins/version-check.sh` script detects which components changed and
sets build flags to avoid unnecessary rebuilds.

---

## Monitoring

Prometheus scrapes metrics from the engine on port 5000.
Grafana runs on port 3000 with dashboards for engine health.

To start monitoring:

```bash
cd monitoring
docker-compose up -d
```

---

## AWS Infrastructure

- **Region:** us-west-2
- **Instance type:** t2.micro
- **AMI:** Ubuntu 24.04 LTS
- **Key pair:** oz-seyoawe-key
