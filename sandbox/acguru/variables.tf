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

variable "vpc" {
    type = map
}

###########################################################
# Subnet Variables.
###########################################################
variable "subnet_az1" {
    type = map
}

variable "subnet_az2" {
    type = map
}

