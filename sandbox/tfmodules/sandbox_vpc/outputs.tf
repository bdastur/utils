output "sandbox_vpc_id" {
    value = "${aws_vpc.sandbox_vpc.id}"
}

output "sandbox_subnet_az1_id" {
    value = "${aws_subnet.az1.id}"
}

output "sandbox_subnet_az2_id" {
    value = "${aws_subnet.az2.id}"
}


