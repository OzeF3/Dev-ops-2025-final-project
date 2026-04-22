output "namespace" {
  description = "Kubernetes namespace created for SeyoAWE"
  value       = kubernetes_namespace.seyoawe.metadata[0].name
}

output "configmap_name" {
  description = "Name of the engine ConfigMap"
  value       = kubernetes_config_map.engine_config.metadata[0].name
}

output "secret_name" {
  description = "Name of the engine Secret (values redacted)"
  value       = kubernetes_secret.engine_secrets.metadata[0].name
}

output "provisioned_resources" {
  description = "Summary of provisioned K8s resources (for Ansible/Jenkins)"
  value = {
    namespace = kubernetes_namespace.seyoawe.metadata[0].name
    configmap = kubernetes_config_map.engine_config.metadata[0].name
    secret    = kubernetes_secret.engine_secrets.metadata[0].name
  }
}
