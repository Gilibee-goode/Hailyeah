#!/bin/bash

#documentation here: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
#and also: https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
#eks cluster set up with: eksctl create cluster --name hailyeah-cluster --region il-central-1 --nodegroup-name hailyeah-nodes --node-type t3.small --nodes 2

eksctl create iamserviceaccount \
  --cluster=hailyeah-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::058264276766:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve \
  --region il-central-1
