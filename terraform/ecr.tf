#ECR register 
resource "aws_ecr_repository" "app" {
  name                 = "${var.stack_name}-${var.ecr_repository_name}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  force_delete = true
  tags         = merge(var.common_tags, var.environment)
}

#Push the image
resource "terraform_data" "bootstrap_docker_image" {
  triggers_replace = [
    md5(file("${path.module}/../app/Dockerfile")),
    md5(file("${path.module}/../app/src/main.py"))
  ]

  provisioner "local-exec" {
    working_dir = "${path.module}/../app"
    interpreter = ["PowerShell", "-Command"]
    command     = <<EOF
      $region = "${data.aws_region.current.name}"
      $repository_url = "${aws_ecr_repository.app.repository_url}"
      aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $repository_url
      docker build -t "$($repository_url):latest" .
      docker push "$($repository_url):latest"
    EOF
  }

  depends_on = [aws_ecr_repository.app]
}


#Cleaning
resource "aws_ecr_lifecycle_policy" "cleanup" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last ${var.keep_last_n_images} images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = var.keep_last_n_images
      }
      action = {
        type = "expire"
      }
    }]
  })
}