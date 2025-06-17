# Terraform — Infrastructure as Code for AI Assistant Deployment

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_ecs_cluster" "ai_assistant_cluster" {
  name = "ai-assistant-cluster"
}

resource "aws_ecs_task_definition" "assistant_task" {
  family                   = "ai-assistant-task"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  network_mode             = "awsvpc"

  container_definitions = jsonencode([{
    name  = "ai-assistant"
    image = "your-dockerhub-username/ai_personal_assistant:latest"
    portMappings = [{
      containerPort = 8080
      hostPort      = 8080
    }]
    environment = [
      {
        name  = "OPENAI_API_KEY"
        value = var.openai_api_key
      }
    ]
  }])
}

variable "openai_api_key" {
  description = "Your OpenAI API Key"
  type        = string
}
