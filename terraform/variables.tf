variable "ami_id" {
  description = "AMI ID for EC2 (Ubuntu)"
  default     = "ami-0150ccaf51ab55a51"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "key_name" {
  description = "Key pair name in AWS"
  default = "ec2"
  
}