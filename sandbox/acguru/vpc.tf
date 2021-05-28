###########################################################
# Sandbox VPC
###########################################################
resource "aws_vpc" "sandbox_vpc" {
  cidr_block           = var.vpc["cidr_block"]
  instance_tenancy     = var.instance_tenancy
  enable_dns_support   = var.enable_dns_support
  enable_dns_hostnames = var.enable_dns_hostnames

  tags = {
    Name    = var.tags["sandbox_name"]
    Sandbox = var.tags["sandbox_name"]
  }
}


###########################################################
# Sandbox Subnets
###########################################################
resource "aws_subnet" "az1" {
  vpc_id                  = aws_vpc.sandbox_vpc.id
  cidr_block              = var.subnet_az1["cidr_block"]
  availability_zone       = var.subnet_az1["az"]
  map_public_ip_on_launch = var.subnet_az1["map_public_ip_on_launch"]

  tags = {
    Name  = join("-", [var.tags["sandbox_name"], "az-1"])
    Stack = "dev"
    join("", ["kubernetes.io/cluster/", var.tags["sandbox_name"]]) = "shared"
  }
}

resource "aws_subnet" "az2" {
  vpc_id                  = aws_vpc.sandbox_vpc.id
  cidr_block              = var.subnet_az2["cidr_block"]
  availability_zone       = var.subnet_az2["az"]
  map_public_ip_on_launch = var.subnet_az2["map_public_ip_on_launch"]

  tags = {
    Name  = join("-", [var.tags["sandbox_name"], "az-2"])
    Stack = "dev"
    join("", ["kubernetes.io/cluster/", var.tags["sandbox_name"]]) = "shared"
  }
}

###########################################################
# Sandbox IGW
###########################################################
resource "aws_internet_gateway" "internet_gw" {
  vpc_id = aws_vpc.sandbox_vpc.id

  tags = {
    Name  = join("-", [var.tags["sandbox_name"], "igw"])
    Stack = "envbase"
  }
}

###########################################################
# Sandbox route table public
###########################################################
resource "aws_route_table" "rtable_public" {
  vpc_id = aws_vpc.sandbox_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gw.id
  }

  tags = {
    Name  = join("-", [var.tags["sandbox_name"], "public-rtable"])
    Stack = "envbase"
  }
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.az2.id
  route_table_id = aws_route_table.rtable_public.id
}

###########################################################
# Sandbox route table private
###########################################################
resource "aws_route_table" "rtable_private" {
  vpc_id = aws_vpc.sandbox_vpc.id

  tags = {
    Name  = join("-", [var.tags["sandbox_name"], "private-rtable"])
    Stack = "envbase"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.az1.id
  route_table_id = aws_route_table.rtable_private.id
}


