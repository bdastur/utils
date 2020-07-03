variable "sgrules_depends_on" {
    description = "Variable to force module to wait for VPC"
}

resource "aws_security_group" "sandbox_sgrule" {
  name        = "${var.sandbox_name}-secgroup"
  description = "Sandbox Ingress security group"
  vpc_id      = var.sandbox_vpc_id

  tags = {
    Sandbox  = "${var.sandbox_name}"
  }
}


#########################################################
# INGRESS Security group rules (ssh access)
#########################################################
resource "aws_security_group_rule" "secgroup_ssh_access" {
  count       = var.ssh_port_open ? 1 : 0
  description = "Allow SSH ingress from allowed subnets"
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule.id
  cidr_blocks       = var.ssh_cidrs
}


#########################################################
# EGRESS Security group rules
#########################################################
resource "aws_security_group_rule" "secgroup_egress_allow_all" {
  description = "Allow egress "
  type        = "egress"
  from_port   = -1
  to_port     = -1
  protocol    = "all"

  security_group_id = aws_security_group.sandbox_sgrule.id
  cidr_blocks       = ["${var.aws_vpc_cidr_block}"]
}

resource "aws_security_group_rule" "secgroup_egress_external" {
  description = "Allow TCP egress"
  type        = "egress"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule.id
  cidr_blocks       = ["0.0.0.0/0"]
}

