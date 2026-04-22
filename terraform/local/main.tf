terraform {
  required_version = ">= 1.3.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "kubernetes" {
  config_path    = var.kubeconfig_path
  config_context = var.kube_context
}

# ===========================================================================
# Infrastructure layer — what Terraform owns:
#   - Namespace (isolation boundary)
#   - ConfigMap (non-sensitive app config)
#   - Secret    (sensitive credentials for the 4 release functions)
#
# NOT owned by Terraform:
#   - StatefulSet + Service  -> k8s/ manifests, applied by Ansible
#   - PVC                    -> created automatically by the StatefulSet's
#                               volumeClaimTemplates (correct K8s pattern)
# ===========================================================================

resource "kubernetes_namespace" "seyoawe" {
  metadata {
    name = var.namespace

    labels = {
      app        = "seyoawe"
      managed_by = "terraform"
      env        = var.app_env
    }
  }
}

resource "kubernetes_config_map" "engine_config" {
  metadata {
    name      = "engine-config"
    namespace = kubernetes_namespace.seyoawe.metadata[0].name

    labels = {
      app        = "seyoawe-engine"
      managed_by = "terraform"
    }
  }

  data = {
    APP_ENV       = var.app_env
    APP_PORT      = "8080"
    LOG_LEVEL     = "DEBUG"
    JIRA_BASE_URL = var.jira_base_url
    JIRA_PROJECT  = var.jira_project
    GITHUB_REPO   = var.github_repo
  }
}

resource "kubernetes_secret" "engine_secrets" {
  metadata {
    name      = "engine-secrets"
    namespace = kubernetes_namespace.seyoawe.metadata[0].name

    labels = {
      app        = "seyoawe-engine"
      managed_by = "terraform"
    }
  }

  type = "Opaque"

  data = {
    GMAIL_USER     = var.gmail_user
    GMAIL_PASSWORD = var.gmail_password
    JIRA_EMAIL     = var.jira_email
    JIRA_TOKEN     = var.jira_token
    GITHUB_TOKEN   = var.github_token
  }
}
