provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "seyoawe_engine" {
  ami           = "ami-0d76b909de1a0595d"
  instance_type = "t2.micro"
  key_name      = "oz-seyoawe-key"

  vpc_security_group_ids = [aws_security_group.seyoawe_sg.id]

  tags = {
    Name = "seyoawe-engine"
  }

  provisioner "remote-exec" {
    inline = ["echo 'Instance is ready'"]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("/var/lib/jenkins/.ssh/oz-seyoawe-key.pem")
      host        = self.public_ip
    }
  }
}

resource "aws_security_group" "seyoawe_sg" {
  name        = "seyoawe-sg"
  description = "Security group for seyoawe engine"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080  
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}