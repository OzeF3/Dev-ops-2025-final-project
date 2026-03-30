output "instance_public_ip" {
  description = "Public IP of the seyoawe engine EC2 instance"
  value       = aws_instance.seyoawe_engine.public_ip
}

output "instance_id" {
  description = "ID of the seyoawe engine EC2 instance"
  value       = aws_instance.seyoawe_engine.id
}