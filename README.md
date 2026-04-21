# Seyoawe Community - DevOps Final Project

## Architecture Overview

This project implements a full DevOps lifecycle around the Seyoawe automation engine.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DevOps Architecture                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐    push     ┌─────────────────────────────────────────┐ │
│   │  GitHub  │────────────▶│              Jenkins                    │ │
│   │  Source  │             │         CI/CD Orchestration             │ │
│   │ Control  │             └──────────────┬──────────────────────────┘ │
│   └──────────┘                            │                             │
│                              ┌────────────┴────────────┐               │
│                              │                         │               │
│                    ┌─────────▼──────────┐  ┌──────────▼─────────┐     │
│                    │   CI Pipeline      │  │   CD Pipeline       │     │
│                    │ ─────────────────  │  │ ─────────────────── │     │
│                    │ Engine: lint+build │  │ Terraform (AWS EC2) │     │
│                    │ CLI: test+package  │  │ Ansible (config)    │     │
│                    │ Version coupling   │  │ Local: Minikube     │     │
│                    └────────┬───────────┘  └──────────┬──────────┘     │
│                             │                         │               │
│                             │ push                    │ deploy        │
│                             ▼                         ▼               │
│   ┌──────────────────────┐          ┌─────────────────────────────┐  │
│   │      Docker Hub      │          │   Kubernetes (Minikube/EKS) │  │
│   │   devoeoe23ops/      │◀─ pull ──│ ─────────────────────────── │  │
│   │   seyoawe-engine     │          │  Engine StatefulSet (8080)  │  │
│   │   seyoawe-cli        │          │  PersistentVolumeClaim (1Gi) │  │
│   └──────────────────────┘          │  ClusterIP Service           │  │
│                                     │  Pod: 1/1 Running            │  │
│                                     └──────────────────────────────┘  │
│                                                      │                 │
│                                                      │ scrape          │
│                                                      ▼                 │
│                                     ┌──────────────────────────────┐  │
│                                     │         Monitoring            │  │
│                                     │  Prometheus + Grafana (3000) │  │
│                                     │  Node Exporter               │  │
│                                     └──────────────────────────────┘  │
│                                                                         │
│   ┌──────────────────┐    ┌──────────────────────────────────────────┐ │
│   │   version.txt    │    │           sawectl CLI                    │ │
│   │  Shared semver   │    │  22 unit tests · PyInstaller binary      │ │
│   └──────────────────┘    └──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Components

| Component | Tool | Purpose |
|---|---|---|
| Source control | GitHub | Code versioning, tags, webhooks |
| CI/CD | Jenkins | Automated pipelines (local) |
| Containerization | Docker | Engine & CLI containers |
| Registry | Docker Hub (devoeoe23ops) | Published images |
| Infrastructure | Terraform | AWS EC2 provisioning |
| Configuration | Ansible | Server setup & Docker install |
| Orchestration | Kubernetes (Minikube / EKS) | App deployment & scaling |
| Monitoring | Prometheus + Grafana | Metrics & dashboards |
| Version coupling | version.txt | Shared semantic version |

---

## Repository Structure

```
seyoawe-community/
├── docker/          # Dockerfiles for engine and CLI
├── jenkins/         # CI/CD pipeline definitions
│   ├── engine/      # CI pipeline for the engine
│   ├── cli/         # CI pipeline for the CLI
│   ├── cd/          # CD pipelines
│   │   ├── Jenkinsfile        # AWS production CD (Terraform + Ansible)
│   │   └── Jenkinsfile.local  # Local Minikube CD pipeline
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

## How to Use the App

### Prerequisites
Install dependencies:
```bash
pip install -r sawectl/requirements.txt
```

### Function 1 - Run a Workflow
Trigger a workflow against a running Seyoawe engine:
```bash
python3 sawectl/sawectl.py run \
  --workflow workflows/samples/command_and_slack.yaml \
  --server localhost:8080
```

### Function 2 - Validate a Workflow
Deep-validate a workflow file against schema and module manifests:
```bash
python3 sawectl/sawectl.py validate-workflow \
  --workflow workflows/samples/command_and_slack.yaml \
  --verbose
```

### Function 3 - Validate All Modules
Check all module manifests are valid:
```bash
python3 sawectl/sawectl.py validate-modules \
  --modules modules/
```

### Function 4 - Initialize a New Workflow
Create a new workflow template:
```bash
python3 sawectl/sawectl.py init workflow my_workflow \
  --full \
  --trigger api \
  --modules-path modules/
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
2. Version check
3. Install dependencies
4. Lint
5. Unit tests (22 tests)
6. Build Linux binary with PyInstaller
7. Build Docker image
8. Push to Docker Hub as `devoeoe23ops/seyoawe-cli:<version>`
9. Tag Git with version

### CD Pipeline (AWS)

1. Checkout code
2. Terraform init, plan, apply → provision EC2 on AWS (us-west-2)
3. Update Ansible inventory with EC2 IP
4. Wait for EC2 to be ready
5. Run Ansible playbook → install Docker & kubectl, pull image
6. Deploy to Kubernetes using manifests

### CD Pipeline (Local - Minikube)

1. Checkout code
2. Build Docker image
3. Push to Docker Hub
4. Deploy to Minikube using kubectl
5. Verify deployment

---

## Version Coupling

Both engine and CLI share the same semantic version defined in `version.txt`.
The `jenkins/version-check.sh` script detects which components changed and
sets build flags to avoid unnecessary rebuilds.

---

## Jenkins Dashboard

### All 3 Pipelines Green
![Jenkins Dashboard](docs/screenshots/jenkins_dashboard_.PNG)

---

## Pipeline Success

### Engine CI Pipeline - All Stages Passed
![Engine Pipeline Success](docs/screenshots/pipline_success-_engine_ci.PNG)

### CLI CI Pipeline - All Stages Passed
![CLI Pipeline Success](docs/screenshots/pipline_success-cli-_ci_.PNG)

### Local CD Pipeline - Engine Deployed to Minikube
![CD Local Pipeline Success](docs/screenshots/pipeline_success-_cd-_local.PNG)

---

## Pipeline Failure

### Engine CI Pipeline - Failed Build
![Pipeline Failure](docs/screenshots/pipline_fail-_engine_ci.PNG)

---

## Kubernetes Deployment (Local - Minikube)

### Pod Running (1/1)
![Pod Running](docs/screenshots/Pod_Running.PNG)

### Services & StatefulSet
![Services](docs/screenshots/Services.PNG)

---

## Monitoring

Prometheus scrapes metrics from the engine on port 8080.
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
- **AMI:** Ubuntu 24.04 LTS (ami-0d76b909de1a0595d)
- **Key pair:** oz-seyoawe-key
