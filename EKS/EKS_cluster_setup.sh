#!/bin/bash

###
# This script creates an EKS cluster with an ALB controller 
###


aws_account_id=058264276766
cluster_name=hailyeah-cluster
region=eu-north-1
node_type=t3.small
node_count=2
nodegroup_name=hailyeah-nodes

#set up cluster 
eksctl create cluster --name $cluster_name --region $region --nodegroup-name $nodegroup_name --node-type $node_type --nodes $node_count

#configure OIDC provider for the cluster. Documented at: https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html

#oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
#echo $oidc_id

eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve


#Install the AWS Load Balancer Controller using Helm. Documented in: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
#Step 1: Create IAM Role using eksctl

curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json


eksctl create iamserviceaccount \
  --cluster=$cluster_name \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::$aws_account_id:policy/AWSLoadBalancerControllerIAMPolicy \
  --region $region \
  --approve


rm iam_policy.json  #remove file downloaded via curl


#Step 2: Install AWS Load Balancer Controller

helm repo add eks https://aws.github.io/eks-charts

helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=$cluster_name \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller 










