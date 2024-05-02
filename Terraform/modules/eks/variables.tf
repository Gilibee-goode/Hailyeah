variable "region" {
  description = "Region to use in aws"
  type        = string
}

variable "iam_role_name" {
  description = "The name of the IAM role"
  type        = string
  default     = "aws-load-balancer-controller"
}

# variable "name" {
#   description = "module.eks.cluster_id"
#   type        = string
# }

# variable "availability_zone" {
#   description = "AZ to use in aws"
#   type        = string
#   default     = "il-central-1a" 
# }

variable "cluster_name" {
  description = "Cluster name"
  type        = string
  default     = "mah-clustah" 
}

variable "private_subnet_ids" {
  description = "list of subnet ids"
  type = list
}

variable "vpc_id" {
  description = "id of the vpc"
  type = string
}

