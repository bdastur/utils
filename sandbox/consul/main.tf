provider "aws" {
  region                  = var.region
  shared_credentials_file = var.credentials_file
  profile                 = var.profile
}


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

module "sandbox_sg_https_access" {
    source = "../tfmodules/sandbox_security_groups/https_access"
    sgrules_depends_on = [module.test_sandbox.sandbox_vpc_id]

    sandbox_name = var.sandbox_name
    aws_vpc_cidr_block = var.cidr_block
    sandbox_vpc_id = module.test_sandbox.sandbox_vpc_id
    https_port_open = var.https_port_open
    https_cidrs = var.https_cidrs
}

module "sandbox_sg_consul_access" {
    source = "../tfmodules/sandbox_security_groups/consul_access"
    sgrules_depends_on = [module.test_sandbox.sandbox_vpc_id]

    sandbox_name = var.sandbox_name
    aws_vpc_cidr_block = var.cidr_block
    sandbox_vpc_id = module.test_sandbox.sandbox_vpc_id
    consul_cidrs = var.consul_cidrs
}


module "sandbox_asg1" {
    source = "../tfmodules/sandbox_asg"
    asg_depends_on = [module.test_sandbox.sandbox_vpc_id, 
                      module.sandbox_sg_ssh_access.sandbox_sgrules,
                      module.sandbox_sg_https_access.sandbox_sgrules,
                      module.sandbox_sg_consul_access.sandbox_sgrules]

    sandbox_name  = var.sandbox_name
    instance_type = var.asg_1["instance_type"]
    ami_id        = var.asg_1["ami_id"]
    volume_size   = var.asg_1["volume_size"]
    volume_type   = var.asg_1["volume_type"]
    key_name      = var.asg_1["key_name"]
    min_size      = var.asg_1["min_size"]
    max_size      = var.asg_1["max_size"]
    desired_capacity = var.asg_1["desired_capacity"]
    health_check = var.asg_1_health_check

    subnet_az1_id = module.test_sandbox.sandbox_subnet_az1_id
    subnet_az2_id = module.test_sandbox.sandbox_subnet_az2_id
    sandbox_sgrule_ids = flatten([module.sandbox_sg_ssh_access.sandbox_sgrules, module.sandbox_sg_https_access.sandbox_sgrules])

    user_tags = var.asg_1_tags
}



