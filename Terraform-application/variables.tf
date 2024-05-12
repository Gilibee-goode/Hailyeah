variable "region" {
  description = "Region to use in aws"
  type        = string
  default     = "il-central-1" 
}

variable "subnet_ids" {
  description = "list of subnet ids"
  type = list
  default = []
}

variable "cluster_name" {
  description = "Cluster name"
  type        = string
  default     = "mah-clustah" 
}

variable "kubeconfig" {
  description = "Cluster name"
  type        = string
  default     = "/home/gilibee/.kube/config" 
}

# variable "cluster_endpoint" {
#   description = "Endpoint for the Kubernetes cluster"
#   type        = string
# }

# variable "cluster_ca_certificate" {
#   description = "CA Certificate for the Kubernetes cluster"
#   type        = string
# }

# variable "kubeconfig" {
#   description = "Kubeconfig file content for Kubernetes cluster access"
#   type        = string
# }
