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
  cidr_blocks        = slice(var.https_cidrs, 0, min(50, length(var.https_cidrs)))
}






