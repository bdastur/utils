###########################################################
# Sandbox VPC
###########################################################
resource "aws_vpc" "sandbox_vpc" {
  cidr_block           = var.cidr_block
  instance_tenancy     = var.instance_tenancy
  enable_dns_support   = var.enable_dns_support
  enable_dns_hostnames = var.enable_dns_hostnames

  tags = {
    Sandbox = var.vpc_tags["sandbox_name"]
  }

}

###########################################################
# Sandbox Subnets
###########################################################
resource "aws_subnet" "az1" {
  vpc_id                  = aws_vpc.sandbox_vpc.id
  cidr_block              = var.subnet_cidr_blocks[0]
  availability_zone       = var.subnet_azs[0]
  map_public_ip_on_launch = var.map_public_ip_on_launch

  tags = {
    Name  = "brdtest101-subnet-1"
    Stack = "teststack"
  }
}

resource "aws_subnet" "az2" {
  vpc_id                  = aws_vpc.sandbox_vpc.id
  cidr_block              = var.subnet_cidr_blocks[1]
  availability_zone       = var.subnet_azs[1]
  map_public_ip_on_launch = var.map_public_ip_on_launch

  tags = {
    Name  = "brdtest101-subnet-2"
    Stack = "teststack"
  }
}

###########################################################
# Sandbox IGW
###########################################################
resource "aws_internet_gateway" "internet_gw" {
  vpc_id = aws_vpc.sandbox_vpc.id

  tags = {
    Name  = "brdtest101-igw"
    Stack = "teststack"
  }
}

###########################################################
# Sandbox route table
###########################################################
resource "aws_route_table" "rtable" {
  vpc_id = aws_vpc.sandbox_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gw.id
  }

  tags = {
    Name  = "brdtest101-rtable"
    Stack = "teststack"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.az1.id
  route_table_id = aws_route_table.rtable.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.az2.id
  route_table_id = aws_route_table.rtable.id
}

