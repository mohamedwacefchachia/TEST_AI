variable "aws_region" {
  default     = "eu-west-1"
  description = "AWS region for deployment"
}

variable "stack_name" {
  description = "Stack name for resource naming"
  type        = string
  default     = "wacef-project"
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "keep_last_n_images" {
  description = "Number of images to be retained in ECR"
  type        = number
  default     = 3
}
variable "ecr_repository_name" {
  description = "ECR repository name"
  type        = string
  default     = "test-repo"
}

variable "langfuse_public_key" {
  type        = string
  sensitive   = true
  description = "Langfuse pulic key"
}

variable "langfuse_secret_key" {
  type        = string
  sensitive   = true
  description = "Langfuse secret key"
}
variable "langfuse_base_url" {
  type      = string
  sensitive = true
  default   = "https://cloud.langfuse.com"
}

variable "secrets_recovery_window" {
  description = "Number of days after creation before secrets can be deleted"
  type        = number
  default     = 0 #to delete it immediately when i run the test
}

variable "logs_retention" {
  description = "Number of days that logs will be retained in CloudWatch"
  type        = number
  default     = 30
}

variable "api_error_threshold" {
  description = "Maximum number of 5XX errors per minute"
  type        = number
  default     = 5
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "github_repo_url" {
  description = "Github URL of the project (Like 'https://github.com/repo/projet.git')"
  type        = string
}




