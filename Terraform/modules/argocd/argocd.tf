# https://github.com/terraform-aws-modules/terraform-aws-eks/issues/2009
data "aws_eks_cluster" "default" {
  name = var.cluster_name
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


# Deploy ArgoCD

resource "helm_release" "argocd" {
  name = "argocd"

  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  version          = "3.35.4"

  values = [templatefile("modules/argocd/argocd.yaml", {})]
}


# Deploy ArgoCD Application

module "argocd_application" {
  source = "git::https://github.com/jojand/terraform-provider-argocd.git?ref=3125bac7008fdd1a67597c3c9e9b77d965e4d413"
  # source  = "project-octal/argocd-application/kubernetes"
  # version = "~> 2.0.0"

  argocd_namespace    = "argocd"
  destination_server  = "https://kubernetes.default.svc"
  project             = "default"  # module.project.name
  name                = "hailyeah"
  namespace           = "default"
  repo_url            = "https://github.com/Gilibee-goode/Hailyeah-ArgoCD.git"
  path                = "Helm"
  chart               = ""
  target_revision     = "HEAD"
#   helm_parameters =  [  # another option to update the image that Argo uses
#     {
#         name: "weatherAppImage.tag"
#         value: var.app_image
#         force_string: true
#     }

#   ]
#   helm_values         = {
#       helm_values = "go-here"
#   }
  automated_self_heal = true
  automated_prune     = true
#   labels              = {
#       custom = "lables-to-apply"
#   }
}



# provider "argocd" {
#   server_addr = "argo.abc.com:443"
#   username    = "admin"
#   password    = ""
# }


# resource "argocd_application" "hailyeah" {
#   metadata {
#     name      = "hailyeah"
#     namespace = "argocd"
#     labels = {
#       test = "true"
#     }
#   }

#   wait = true

#   spec {
#     source {
#       repo_url        = "https://github.com/Gilibee-goode/Hailyeah-ArgoCD.git"
#       path            = "Helm"
#     #   chart           = "Helm"
#     #   target_revision = "1.2.3"
#     #   helm {
#     #     parameter {
#     #       name  = "image.tag"
#     #       value = "1.2.3"
#     #     }
#     #     parameter {
#     #       name  = "someotherparameter"
#     #       value = "true"
#     #     }
#     #     value_files = ["values-test.yml"]
#     #     values      = <<EOT
#     # someparameter:
#     # enabled: true
#     # someArray:
#     # - foo
#     # - bar    
#     # EOT
#     #     release_name = "testing"
#     #   }
#     }

#     destination {
#       server    = "https://kubernetes.default.svc"
#       namespace = "default"
#     }
#   }
# }