provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "deployer" {
  key_name   = "ec2"
  public_key = var.public_key
}

resource "aws_instance" "react_app" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  tags = {
    Name = "Client App"
  }
}

output "ec2_public_ip" {
  value = aws_instance.react_app.public_ip
}