#Langfuse secrets
resource "aws_secretsmanager_secret" "app_secrets" {
  name                    = "${var.stack_name}-app-secrets"
  description             = "Langfuse secrets"
  recovery_window_in_days = var.secrets_recovery_window
  tags                    = merge({ Name = "app-secrets" }, var.common_tags, var.environment)
}

resource "aws_secretsmanager_secret_version" "app_secrets_val" {
  secret_id = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    LANGFUSE_PUBLIC_KEY = var.langfuse_public_key
    LANGFUSE_SECRET_KEY = var.langfuse_secret_key
    LANGFUSE_BASE_URL   = var.langfuse_base_url
  })
}

#Github token
resource "aws_secretsmanager_secret" "github_token" {
  name                    = "${var.stack_name}-github-token"
  description             = "Github token for CodeBuild"
  recovery_window_in_days = var.secrets_recovery_window
  tags                    = merge({ Name = "github-token" }, var.common_tags, var.environment)
}

resource "aws_secretsmanager_secret_version" "github_token_val" {
  secret_id     = aws_secretsmanager_secret.github_token.id
  secret_string = var.github_token
}