variable "sandbox_name" {
    type = string
}

variable "aws_vpc_cidr_block" {
    type = string
}

variable "sandbox_vpc_id" {
    type = string
}


variable "https_port_open" {
    type = bool
}

variable "https_cidrs" {
    type = list
}


