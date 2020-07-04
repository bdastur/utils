variable "sgrules_depends_on" {
    description = "Variable to force module to wait for VPC"
}

#########################################################
# HTTPS INGRESS Security group (https access)
#########################################################
resource "aws_security_group" "sandbox_sgrule_https_access" {
  name        = "${var.sandbox_name}-https-secgroup"
  description = "Sandbox Allow Https access"
  vpc_id      = var.sandbox_vpc_id

  tags = {
    Sandbox  = "${var.sandbox_name}"
    Type     = "IngressHttps"
  }
}

#########################################################
# INGRESS Security group rules (https access)
#########################################################
resource "aws_security_group_rule" "secgroup_https_access" {
  count       = var.https_port_open ? 1 : 0
  description = "Allow HTTPS ingress from allowed subnets"
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_https_access.id
  cidr_blocks        = var.https_cidrs
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

  security_group_id = aws_security_group.sandbox_sgrule_https_access.id
  cidr_blocks       = ["${var.aws_vpc_cidr_block}"]
}

resource "aws_security_group_rule" "secgroup_egress_external" {
  description = "Allow TCP egress"
  type        = "egress"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_https_access.id
  cidr_blocks       = ["0.0.0.0/0"]
}

