# **🏗️ Infrastructure as Code (IaC)**

## 🌟 Introduction

This repository is at the heart of the application's automated deployment. It uses Terraform to define, provision and manage the entire cloud stack on AWS.

The goal of this configuration is to provide an immutable and scalable infrastructure, allowing you to move from local code to a secure production application with a single command.

## Intial Configuration
To protect our secrets, the file containing sensitive values is not tracked by Git. A template is provided to facilitate configuration.

**🔑 Variable Management**

* Locate the terraform.tfvars.txt file at the root of the terraform folder.

* Rename it to terraform.tfvars

* Open it and replace the values with your own settings

**⚙️ Environment and Authentication**

Before launching Terraform, ensure that your local environment is ready:

* **AWS configuration:** Authenticate your terminal with your IAM credentials.

```bash
AWS configure
```

Check your connection with: `aws sts get-caller-identity`

* **Docker Engine:** Docker Desktop must be active to enable the initial build and push of the image.

```bash
Docker info
```

## 🏛️ Architecture de l'Infrastructure

The deployed infrastructure follows AWS best practices for containerised applications:

* **Network Layer:** A custom VPC with traffic isolation.

* **Storage Layer:** Amazon ECR for Docker image versioning.

* **Compute Layer:** Amazon ECS Fargate (serverless) for container execution.

* **CI/CD Layer:** AWS CodeBuild with Webhooks for continuous deployment.

* **Security Layer:** Least Privilege IAM roles and Secrets Manager for token management.

## 🚀 Deployment Guide

```bash
# Initialise modules
terraform init

# Check plan
terraform plan

# Deploy (Docker must be running)
terraform apply
```

## 🛠️ Maintenance & Cleaning

* **Update:** To modify the infrastructure (e.g. change the size of the ECS memory), modify the .tf files and restart an apply.

* **Destruction:** To delete all resources and stop AWS billing:

```bash
terraform destroy
```