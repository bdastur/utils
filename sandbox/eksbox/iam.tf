##############################################
# EKS Cluster role
##############################################
resource "aws_iam_role" "sandbox_eks_role" {
    name = "eks-sandbox-role"
    assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY

}

resource "aws_iam_role_policy_attachment" "eks-clusterpolicy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
    role       = aws_iam_role.sandbox_eks_role.name
}

##############################################
# EKS Nodegroup role
##############################################
resource "aws_iam_role" "sandbox_eks_nodepool_role" {
    name = "eks-sandbox-nodepool-role"
    assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "eks-nodepool-nodepolicy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
    role       = aws_iam_role.sandbox_eks_nodepool_role.name
}

resource "aws_iam_role_policy_attachment" "eks-nodepool-registryro-policy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
    role       = aws_iam_role.sandbox_eks_nodepool_role.name
}

resource "aws_iam_role_policy_attachment" "eks-nodepool-cni-policy" {
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
    role       = aws_iam_role.sandbox_eks_nodepool_role.name
}


resource "aws_iam_role_policy" "eks_autoscaling_policy" {
  name = "eks_autoscaling_policy"
  role = aws_iam_role.sandbox_eks_nodepool_role.name

  policy = <<-EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeTags",
                "autoscaling:SetDesiredCapacity",
                "autoscaling:TerminateInstanceInAutoScalingGroup",
                "ec2:DescribeLaunchTemplateVersions"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
EOF
}
