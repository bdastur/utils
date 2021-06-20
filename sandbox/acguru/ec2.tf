#---------------------------------------------------------------
# Data
#data "aws_ami" "amazon_linux" {
#    owners = ["aws-marketplace"]
#    filter {
#        name = "name"
#        values = ["amzn2-ami-hvm-2*"]
#    }
#    filter {
#        name   = "virtualization-type"
#        values = ["hvm"]
#    }
#    filter {
#        name = "architecture"
#        values = ["x86_64"]
#    }
#}

#--------------------
# Access key.
resource "aws_key_pair" "sample_keypair" {                                                                                              
    key_name = "testkey"
    public_key = "${file("/Users/behzaddastur/.ssh/ec2key.pub")}"
}

resource "aws_instance" "web" {
    ami = "ami-0cf6f5c8a62fa5da6"
    instance_type = "t2.micro"
    availability_zone = var.subnet_az2["az"] 
    subnet_id = aws_subnet.az2.id 

    tags = {
        Name = "testec2"
    }
}
