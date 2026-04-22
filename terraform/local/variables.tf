# ---------------------------------------------------------------------------
# Cluster access
# ---------------------------------------------------------------------------

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "Kubernetes context to use (e.g. minikube)"
  type        = string
  default     = "minikube"
}

# ---------------------------------------------------------------------------
# App config
# ---------------------------------------------------------------------------

variable "namespace" {
  description = "Kubernetes namespace for SeyoAWE resources"
  type        = string
  default     = "seyoawe"
}

variable "app_env" {
  description = "Application environment (local/dev/prod)"
  type        = string
  default     = "local"
}

# ---------------------------------------------------------------------------
# Release-app / 4-function configuration (non-sensitive)
# ---------------------------------------------------------------------------

variable "jira_base_url" {
  description = "Jira base URL"
  type        = string
  default     = "https://oefraty.atlassian.net"
}

variable "jira_project" {
  description = "Jira project key"
  type        = string
  default     = "SEY"
}

variable "github_repo" {
  description = "GitHub repo in owner/name format"
  type        = string
  default     = "OzeF3/Dev-ops-2025-final-project"
}

# ---------------------------------------------------------------------------
# Release-app / 4-function secrets (populated from Jenkins credentials)
# ---------------------------------------------------------------------------

variable "gmail_user" {
  description = "Gmail account for email release function"
  type        = string
  default     = ""
  sensitive   = true
}

variable "gmail_password" {
  description = "Gmail app password"
  type        = string
  default     = ""
  sensitive   = true
}

variable "jira_email" {
  description = "Jira user email"
  type        = string
  default     = ""
  sensitive   = true
}

variable "jira_token" {
  description = "Jira API token"
  type        = string
  default     = ""
  sensitive   = true
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  default     = ""
  sensitive   = true
}
