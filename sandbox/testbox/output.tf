output "sandbox_vpc_id" {
    value = module.test_sandbox.sandbox_vpc_id
}

output "sandbox_subnet_az1_id" {
    value = module.test_sandbox.sandbox_subnet_az1_id
}

output "sandbox_subnet_az2_id" {
    value = module.test_sandbox.sandbox_subnet_az2_id
}

output "sandbox_sgrules" {
    value = [module.sandbox_sg.sandbox_sgrules]
}
