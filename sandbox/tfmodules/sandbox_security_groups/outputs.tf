output "sandbox_sgrules" {
    value = ["${aws_security_group.sandbox_sgrule.id}",
             "${aws_security_group.sandbox_sgrule_https_access.id}"]

}



