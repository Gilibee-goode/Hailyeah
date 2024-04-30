# Set up the network module
module "vpc" {
  source = "./modules/vpc"
  region = var.region
}

# # Set up the EKS module
module "eks" {
  source = "./modules/eks"
  # region = var.region

  private_subnet_ids = module.vpc.private_subnets
  vpc_id = module.vpc.vpc_id
}

# # Set up the IAM OIDC module
# module "iam" {
#   source               = "../modules/iam-oidc"
#   eks_oidc_issuer_url = module.eks.eks_oidc_issuer_url
# }
