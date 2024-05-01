data "aws_availability_zones" "available" {}
data "aws_caller_identity" "current" {}


locals {
  # name   = var.cluster_name  #not needed

  tags = {
    Example    = var.cluster_name
    GithubRepo = "terraform-aws-eks"
    GithubOrg  = "terraform-aws-modules"
    }
}


module "eks" {
  # source  = "terraform-aws-modules/eks/aws"
  source = "https://github.com/terraform-aws-modules/terraform-aws-eks.git?ref=afadb14e44d1cdbd852dbae815be377c4034e82a"
  version = "20.8.5"

  cluster_name                   = var.cluster_name

  # cluster_endpoint_private_access = true  #no need, there is no access from within the VPC
  cluster_endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true
  authentication_mode = "API_AND_CONFIG_MAP"

  vpc_id                   = var.vpc_id
  subnet_ids               = var.private_subnet_ids

  enable_irsa = true  #iam role for service accounts (configs OIDC)

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }


  # EKS Managed Node Group(s)
  # eks_managed_node_group_defaults = {
  #   ami_type       = "AL2_x86_64"
  #   instance_types = ["t3.small"]
  #   disk_size = 20

  #   attach_cluster_primary_security_group = true
  # }

  eks_managed_node_groups = {
    hailyeah-weatherapp = {
      min_size     = 1
      max_size     = 2
      desired_size = 1

      instance_types = ["t3.small"]
      # capacity_type  = "SPOT"
      capacity_type  = "ON_DEMAND"

      tags = {
        ExtraTag = "hailyeah"
      }
    }
  }


  tags = local.tags
}




# https://github.com/terraform-aws-modules/terraform-aws-eks/issues/2009
data "aws_eks_cluster" "default" {
  name = var.cluster_name

  depends_on = [module.eks]
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.default.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.default.id]
      command     = "aws"
    }
  }
}

module "aws_load_balancer_controller_irsa_role" {
  # source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  source  = "https://github.com/terraform-aws-modules/terraform-aws-iam/tree/v5.39.0/modules/iam-role-for-service-accounts-eks?ref=f9d5e28996ca282af4c09cb97f6291cf77ac03ea"
  # version = "5.3.1"
  version = "~> 5.0"

  role_name = "aws-load-balancer-controller"

  attach_load_balancer_controller_policy = true

  oidc_providers = {
    ex = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-load-balancer-controller"]
    }
  }

  depends_on = [module.eks]
}


resource "helm_release" "aws_load_balancer_controller" {
  name = "aws-load-balancer-controller"

  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  version    = "1.4.4"

  set {
    name  = "replicaCount"
    value = "2"  #default is 2
  }

  set {
    name  = "clusterName"
    value = var.cluster_name
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.aws_load_balancer_controller_irsa_role.iam_role_arn
  }

  depends_on = [module.eks]
}



resource "helm_release" "my_local_chart" {
  name      = "hailyeah"
  namespace = "default"
  chart     = "./Helm"

  # set {
  #   name  = "key"
  #   value = "value"
  # }

  # # OR input a yaml file
  # values = [
  #   file("values.yaml")
  # ]

  # depends_on = [module.eks]
}

