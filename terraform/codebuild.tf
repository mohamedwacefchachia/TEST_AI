resource "aws_codebuild_project" "app_build" {
  name          = "${var.stack_name}-codebuild"
  description   = "Build and Push the docker image to ECR"
  build_timeout = 5
  service_role  = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/amazonlinux2-x86_64-standard:5.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true

    environment_variable {
      name  = "REPOSITORY_URI"
      value = aws_ecr_repository.app.repository_url
    }

    environment_variable {
      name  = "ECS_CLUSTER"
      value = aws_ecs_cluster.main.name
    }

    environment_variable {
      name  = "ECS_SERVICE"
      value = aws_ecs_service.main.name
    }
  }

  source {
    type            = "GITHUB"
    location        = var.github_repo_url
    git_clone_depth = 1
  }

  tags = var.common_tags
}

