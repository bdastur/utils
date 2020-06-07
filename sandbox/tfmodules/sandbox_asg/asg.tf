variable "asg_depends_on" {
    description = "Variable to force module to wait for VPC"
}

###########################################################
# Sandbox Launch template
###########################################################
resource "aws_launch_template" "sandbox_lt" {
  depends_on    = [var.asg_depends_on]
  name_prefix   = "sandbox_lt"
  instance_type = var.instance_type
  image_id      = var.ami_id

  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size = var.volume_size
      volume_type = var.volume_type
    }
  }

  ebs_optimized          = true
  key_name               = var.key_name
  vpc_security_group_ids = var.sandbox_sgrule_ids

  lifecycle {
    create_before_destroy = true
  }
}

###########################################################
# Autoscaling group
###########################################################
resource "aws_autoscaling_group" "sandbox_asg" {
  depends_on = [
    aws_launch_template.sandbox_lt
  ]
  name_prefix = "sandbox-asg"

  vpc_zone_identifier       = [var.subnet_az1_id, var.subnet_az2_id]
  min_size                  = 1
  max_size                  = 1
  desired_capacity          = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  termination_policies      = ["OldestInstance", "OldestLaunchConfiguration"]
  target_group_arns         = [""]
  load_balancers            = [""]

  launch_template {
    id      = aws_launch_template.sandbox_lt.id
    version = "$Latest"
  }

  lifecycle {
    create_before_destroy = true
  }

  tag {
    key                 = "Sandbox"
    value               = var.sandbox_name
    propagate_at_launch = true
  }

}


