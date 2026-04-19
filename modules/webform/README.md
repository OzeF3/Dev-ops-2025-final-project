
---
## 🚀 How to Use the App

### Prerequisites
- Python 3.x installed
- Install dependencies:
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
## ⚙️ Pipeline Flow

### CI Pipeline - Engine

1. Checkout code
2. Version check - detect changed components
3. Lint Python modules
4. Build Docker image
5. Push to Docker Hub as `devoeoe23ops/seyoawe-engine:<version>`

### CI Pipeline - CLI

1. Checkout code
2. Version check
3. Install dependencies
4. Lint
5. Unit tests
6. Build Linux binary with PyInstaller
7. Build Docker image
8. Push to Docker Hub as `devoeoe23ops/seyoawe-cli:<version>`
9. Tag Git with version

### CD Pipeline

1. Checkout code
2. Terraform init, plan, apply → provision EC2 on AWS
3. Update Ansible inventory with EC2 IP
4. Wait for EC2 to be ready
5. Run Ansible playbook → install Docker & kubectl, pull image
6. Deploy to Kubernetes

---

## ✅ Pipeline Success

> Screenshot will be added after first successful pipeline run

---

## ❌ Pipeline Failure

> Screenshot will be added after first pipeline run

---

## 📊 Version Coupling

Both engine and CLI share the same semantic version defined in `version.txt`.
`jenkins/version-check.sh` detects which components changed and sets build
flags to avoid unnecessary rebuilds.

---

## 📈 Monitoring

- Prometheus scrapes metrics from the engine on port 8080
- Grafana dashboard runs on port 3000

To start monitoring:

```bash
cd monitoring
docker-compose up -d
```

---

## ☁️ AWS Infrastructure

- **Region:** us-west-2
- **Instance type:** t2.micro
- **AMI:** Ubuntu 24.04 LTS (ami-0d76b909de1a0595d)
- **Key pair:** oz-seyoawe-key
- **Jenkins server:** http://52.12.194.132:8080
