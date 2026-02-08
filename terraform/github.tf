resource "aws_codebuild_source_credential" "github" {
  auth_type   = "PERSONAL_ACCESS_TOKEN"
  server_type = "GITHUB"
  token       = aws_secretsmanager_secret_version.github_token_val.secret_string
}

# Webhook
resource "aws_codebuild_webhook" "app" {
  project_name = aws_codebuild_project.app_build.name
  build_type   = "BUILD"

  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PUSH"
    }
    filter {
      type    = "HEAD_REF"
      pattern = "refs/heads/master"
    }
  }
}