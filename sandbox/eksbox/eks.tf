resource "aws_eks_cluster" "sandbox_eks" {
    name = var.eks_cluster_name
    role_arn = aws_iam_role.sandbox_eks_role.arn

    vpc_config {
        subnet_ids = [aws_subnet.az1.id, aws_subnet.az2.id]
    }

    depends_on = [
        aws_iam_role_policy_attachment.eks-clusterpolicy
    ]
}

output "endpoint" {
    value = aws_eks_cluster.sandbox_eks.endpoint
}

resource "aws_eks_node_group" "sanbox_eks_ng_1" {
    cluster_name = aws_eks_cluster.sandbox_eks.name
    node_group_name = "general-1"
    node_role_arn = aws_iam_role.sandbox_eks_nodepool_role.arn
    subnet_ids = [aws_subnet.az1.id, aws_subnet.az2.id]
    
    scaling_config {
        min_size = 1
        desired_size = 1
        max_size = 3
    }
    instance_types = ["m4.large"]

    depends_on = [
        aws_iam_role_policy_attachment.eks-nodepool-nodepolicy,
        aws_iam_role_policy_attachment.eks-nodepool-registryro-policy,
        aws_iam_role_policy_attachment.eks-nodepool-cni-policy
    ]

    # Optional: Allow external changes without Terraform plan difference
    lifecycle {
        ignore_changes = [scaling_config[0].desired_size]
    }
}

