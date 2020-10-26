output "sandbox_vpc_id" {
    value = module.buildbot_vpc.sandbox_vpc_id
}

output "sandbox_subnet_az1_id" {
    value = module.buildbot_vpc.sandbox_subnet_az1_id
}

output "sandbox_subnet_az2_id" {
    value = module.buildbot_vpc.sandbox_subnet_az2_id
}

output "sandbox_sgrules" {
    value = [module.sandbox_sg_ssh_access.sandbox_sgrules]
}
