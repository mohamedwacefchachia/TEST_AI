output "alb_dns_name" {
  value       = "http://${aws_lb.main.dns_name}"
  description = "URL publique de ton API"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.app.repository_url
  description = "ECR registry URL for your images"
}

output "cloudwatch_log_group" {
  value       = aws_cloudwatch_log_group.ecs_logs.name
  description = "Name of the log group to view errors"
}

output "codebuild_project_name" {
  value       = aws_codebuild_project.app_build.name
  description = "CodeBuild project name to launch a build manually"
}

output "ecs_service_name" {
  value       = aws_ecs_service.main.name
  description = "ECS service name"
}