
# terraform {
#   required_version = ">= 1.0"

#   required_providers {
#   #   kubectl = {
#   #     source  = "gavinbunney/kubectl"
#   #     version = ">= 1.14.0"
#   #   }
#     helm = {
#       source  = "hashicorp/helm"
#       version = "~> 2.6.0"
#     }
#     argocd = {
#       source  = "jojand/argocd"
#       version = ">= 2.3.2"
#     }
#   }
# }



# Deploy ArgoCD

resource "helm_release" "argocd" {
  name = "argocd"

  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  version          = "3.35.4"

  values = [templatefile("./argocd.yaml", {})]
}


# -----------------------------------------------------------------------





