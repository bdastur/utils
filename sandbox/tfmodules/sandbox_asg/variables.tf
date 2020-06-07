variable "instance_type" {
    type = string
    default = "t2.small"
}

variable "ami_id" {
    type = string
}

variable "volume_size" {
    type = number
}

variable "volume_type" {
    type = string
    default = "gp2"
}

variable "key_name" {
    type = string
}

