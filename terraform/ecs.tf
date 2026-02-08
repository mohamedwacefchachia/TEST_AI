#ECS cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.stack_name}-ecs-cluster"
  tags = merge({ Name = "ECS-Cluster" }, var.common_tags, var.environment)
}

#Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.stack_name}-ecs-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name      = "${var.stack_name}-app-container"
    image     = "${aws_ecr_repository.app.repository_url}:latest"
    essential = true
    portMappings = [{
      containerPort = 8000
      hostPort      = 8000
    }]

    #Langfuse secrets injection
    secrets = [
      {
        name      = "LANGFUSE_PUBLIC_KEY"
        valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:LANGFUSE_PUBLIC_KEY::"
      },
      {
        name      = "LANGFUSE_SECRET_KEY"
        valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:LANGFUSE_SECRET_KEY::"
      },
      {
        name      = "LANGFUSE_BASE_URL"
        valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:LANGFUSE_BASE_URL::"
      }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.stack_name}-app"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
  tags = merge({ Name = "ECS-Task" }, var.common_tags, var.environment)
}

#Security Group for ECS
resource "aws_security_group" "ecs_sg" {
  name   = "${var.stack_name}-ecs-security-group"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(var.common_tags, var.environment)
}

##ECS service
resource "aws_ecs_service" "main" {
  name            = "${var.stack_name}-ecs-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.ecs_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "${var.stack_name}-app-container"
    container_port   = 8000
  }
  depends_on = [
    terraform_data.bootstrap_docker_image,
    aws_lb_listener.http
  ]

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count
    ]
  }

  tags = merge({ Name = "ECS-Service" }, var.common_tags, var.environment)
}