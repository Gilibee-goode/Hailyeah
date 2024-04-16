#documentation at: https://docs.aws.amazon.com/eks/latest/userguide/csi-iam-role.html
 
eksctl create iamserviceaccount \
    --name ebs-csi-controller-sa \
    --namespace kube-system \
    --cluster hailyeah-cluster \
    --role-name AmazonEKS_EBS_CSI_DriverRole \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
    --region il-central-1 \
    --approve




eksctl create addon --name aws-ebs-csi-driver --cluster hailyeah-cluster --region il-central-1 --service-account-role-arn arn:aws:iam::058264276766:role/AmazonEKS_EBS_CSI_DriverRole --force

