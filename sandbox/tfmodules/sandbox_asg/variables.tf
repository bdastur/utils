variable "sandbox_name" {
    type = string
}

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

variable "subnet_az1_id" {
    type = string
}

variable  "subnet_az2_id" {
    type = string
}

variable "sandbox_sgrule_ids" {
    type = list
}

variable "min_size" {
    type = number
}

variable "max_size" {
    type = number
}

variable "desired_capacity" {
    type = number
}

variable "health_check" {
    type = map
}

