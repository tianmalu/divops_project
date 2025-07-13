variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "public_key_path" {
  description = "Path to your public SSH key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "ami_id" {
  description = "AMI ID for EC2 (Ubuntu)"
  default     = "ami-020cba7c55df1f615"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.nano"
}