provider "aws" {
  region = "us-east-1"
}
resource "aws_instance" "react_app" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  associate_public_ip_address = true

  tags = {
    Name = "Client App"
  }
}

resource "aws_instance" "genai_app" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.genai_key_name
  associate_public_ip_address = true

  tags = {
    Name = "GenAI App"
  }
}

output "ec2_public_ip" {
  value = aws_instance.react_app.public_ip
}