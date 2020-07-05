output "sandbox_sgrules" {
    value = ["${aws_security_group.sandbox_sgrule_consul_access.id}"]
}

