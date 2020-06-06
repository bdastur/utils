# VPC Variables.
variable "cidr_block" {
    type = string
}

variable "instance_tenancy" {
    type = string
}

variable "enable_dns_support" {
    type = bool
}

variable "enable_dns_hostnames" {
    type = bool
}

variable "vpc_tags" {
    type = map
}

# Subnet variables
variable "subnet_cidr_blocks" {
    type = list
}

variable "subnet_azs" {
    type = list
}

variable "map_public_ip_on_launch" {
    type = bool
}


