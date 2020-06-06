provider "aws" {
  region                  = var.region
  shared_credentials_file = var.credentials_file
  profile                 = var.profile
}


module "test_sandbox" {
    source = "../tfmodules/sandbox"

    # Vpc.
    cidr_block = var.cidr_block
    instance_tenancy     = var.instance_tenancy
    enable_dns_support   = var.enable_dns_support 
    enable_dns_hostnames = var.enable_dns_hostnames 
    vpc_tags             = var.tags

    # Subnet.

    subnet_cidr_blocks       = var.subnet_cidr_blocks
    subnet_azs               = var.subnet_azs
    map_public_ip_on_launch  = var.map_public_ip_on_launch

}






