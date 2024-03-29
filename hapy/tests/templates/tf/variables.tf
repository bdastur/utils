###########################################################
# Common Variables
###########################################################
variable "sandbox_name" {
    description = "Identifier for the sandbox. Adds tag Sandbox with this value"
    type = string
}

variable "credentials_file" {
  type    = string
  default = "$HOME/.aws/credentials"
}

variable "profile" {
  type    = string
}

variable "region" {
  type    = string
}

###########################################################
# VPC Variables.
###########################################################
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

variable "tags" {
    type = map
}

###########################################################
# Subnet Variables.
###########################################################
variable "subnet_cidr_blocks" {
    type = list
}

variable "subnet_azs" {
    type = list
}

variable "map_public_ip_on_launch" {
    type = bool
}


