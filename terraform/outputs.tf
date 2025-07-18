output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.react_app.public_ip
}

output "genai_public_ip" {
  description = "Public IP of the GenAI EC2 instance"
  value       = aws_instance.genai_app.public_ip
}