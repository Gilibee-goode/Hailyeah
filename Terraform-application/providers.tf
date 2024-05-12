 provider "aws" {
  region = var.region
}

# https://github.com/terraform-aws-modules/terraform-aws-eks/issues/2009
data "aws_eks_cluster" "default" {
  name = var.cluster_name
}

# data "aws_eks_cluster_auth" "cluster_auth" {
#   name = var.cluster_name
# }


provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.default.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
    # token                  = data.aws_eks_cluster_auth.cluster_auth.token

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", var.cluster_name]
      command     = "aws"
    }
  }
}

provider "kubernetes" {
    host                   = data.aws_eks_cluster.default.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
    
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", var.cluster_name]
      command     = "aws"
  }
}


# data "aws_eks_cluster_auth" "cluster_auth" {
#   name = var.cluster_name
# }

# provider "kubernetes" {
#   host                   = data.aws_eks_cluster.default.endpoint
#   cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
#   token                  = data.aws_eks_cluster_auth.cluster_auth.token
# }

# provider "kubectl" {
#   host                   = data.aws_eks_cluster.default.endpoint
#   cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
#   load_config_file       = false
#   token                  = data.aws_eks_cluster_auth.cluster_auth.token
# }

# provider "helm" {
#   kubernetes {
#     # host                   = data.aws_eks_cluster.default.endpoint
#     # cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
#     # token                  = data.aws_eks_cluster_auth.cluster_auth.token
#     # token                  = data.aws_eks_cluster.cluster_auth.token
#     config_path            = var.kubeconfig
#   }
# }

