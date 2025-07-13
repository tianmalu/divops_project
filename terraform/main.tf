provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "deployer" {
  key_name   = "client-app"
  public_key = file(var.public_key_path)
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