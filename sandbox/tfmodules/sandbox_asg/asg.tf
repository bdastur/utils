###########################################################
# Sandbox Launch template
###########################################################
resource "aws_launch_template" "sandbox_lt" {
  name          = "sandbox_lt"
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
  #vpc_security_group_ids = [aws_security_group.secgroup-ssh-ingress.id]

  lifecycle {
    create_before_destroy = true
  }

}

