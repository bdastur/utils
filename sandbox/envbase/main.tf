provider "aws" {
  region                  = var.region
  shared_credentials_file = var.credentials_file
  profile                 = var.profile
}

/*
 Backend in custom_backend.tff
terraform {
  backend "s3" {
    bucket = "us-west-2-xxxx"
    key    = "sbox/envbase/sbox.tfstate"
    region = "us-west-2"
    profile = "dev1"
  }
}
*/


module "test_sandbox" {
    #source = "git@github.com:bdastur/utils.git//sandbox/tfmodules/sandbox_vpc"
    source = "../tfmodules/sandbox_vpc"

    # Vpc.
    cidr_block           = var.cidr_block
    instance_tenancy     = var.instance_tenancy
    enable_dns_support   = var.enable_dns_support
    enable_dns_hostnames = var.enable_dns_hostnames
    vpc_tags             = var.tags

    # Subnet.
    subnet_cidr_blocks       = var.subnet_cidr_blocks
    subnet_azs               = var.subnet_azs
    map_public_ip_on_launch  = var.map_public_ip_on_launch
}

module "sandbox_sg_ssh_access" {
    source = "../tfmodules/sandbox_security_groups/ssh_access"
    sgrules_depends_on = [module.test_sandbox.sandbox_vpc_id]

    sandbox_name = var.sandbox_name
    aws_vpc_cidr_block = var.cidr_block
    sandbox_vpc_id = module.test_sandbox.sandbox_vpc_id
    ssh_port_open = var.ssh_port_open
    ssh_cidrs = var.ssh_cidrs
}



