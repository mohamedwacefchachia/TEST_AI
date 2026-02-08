# logs group
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.stack_name}-app"
  retention_in_days = var.logs_retention
  tags              = merge(var.common_tags, var.environment)
}

# 5XX errors alarms
resource "aws_cloudwatch_metric_alarm" "api_errors" {
  alarm_name        = "${var.stack_name}-high-api-error-rate"
  alarm_description = "This alarm is triggered if the API returns too many 5XX errors"

  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = var.api_error_threshold

  dimensions = {
    LoadBalancer = aws_lb.main.arn_suffix
  }
  tags = merge(var.common_tags, var.environment)
}