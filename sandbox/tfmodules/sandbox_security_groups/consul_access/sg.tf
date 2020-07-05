variable "sgrules_depends_on" {
    description = "Variable to force module to wait for VPC"
}

#########################################################
# Consul INGRESS Security group (https access)
#########################################################
resource "aws_security_group" "sandbox_sgrule_consul_access" {
  name        = "${var.sandbox_name}-consul-secgroup"
  description = "Sandbox Allow Consul services access"
  vpc_id      = var.sandbox_vpc_id

  tags = {
    Sandbox  = "${var.sandbox_name}"
    Type     = "ConsulAccess"
  }
}

#########################################################
# INGRESS Security group rules
#########################################################
resource "aws_security_group_rule" "secgroup_consul_dns_tcp_access" {
  description = "Allow Consul DNS Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8600
  to_port     = 8600
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_dns_udp_access" {
  description = "Allow Consul DNS Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8600
  to_port     = 8600
  protocol    = "udp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_8500_access" {
  description = "Allow Consul http Port 8500 ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8500
  to_port     = 8500
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_8501_access" {
  description = "Allow Consul https Port 8501 ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8501
  to_port     = 8501
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_grpc_access" {
  description = "Allow Consul Port grpc ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8502
  to_port     = 8502
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_lan_access" {
  description = "Allow Consul lan Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8301
  to_port     = 8301
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_lan_udp_access" {
  description = "Allow Consul lan Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8301
  to_port     = 8301
  protocol    = "udp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_wan_access" {
  description = "Allow Consul wan Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8302
  to_port     = 8302
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_wan_udp_access" {
  description = "Allow Consul wan Port ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8302
  to_port     = 8302
  protocol    = "udp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_server_rpc_access" {
  description = "Allow Consul Server RPC ingress access from allowed subnets"
  type        = "ingress"
  from_port   = 8300
  to_port     = 8300
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
}

resource "aws_security_group_rule" "secgroup_consul_sidecar_proxy_access" {
  description = "Allow Consul Sidecar proxy access from allowed subnets"
  type        = "ingress"
  from_port   = 21000
  to_port     = 21255
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks        = var.consul_cidrs
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

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks       = ["${var.aws_vpc_cidr_block}"]
}

resource "aws_security_group_rule" "secgroup_egress_external" {
  description = "Allow TCP egress"
  type        = "egress"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"

  security_group_id = aws_security_group.sandbox_sgrule_consul_access.id
  cidr_blocks       = ["0.0.0.0/0"]
}

