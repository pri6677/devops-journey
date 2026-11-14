# AWS Infrastructure Implementation Guide

This document describes the step-by-step implementation of the AWS high-availability and scalable web infrastructure project.

**AWS Region:** US East (N. Virginia) — `us-east-1`

## 1. Create a Custom VPC

Created a custom VPC named `devops-project-vpc`.

Configuration:

- IPv4 CIDR: `10.0.0.0/16`
- Tenancy: Default

This VPC provides an isolated network for the project infrastructure.

## 2. Create Subnets

Created four subnets across two Availability Zones.

| Subnet | CIDR | Availability Zone |
|---|---|---|
| public-subnet-1a | `10.0.1.0/24` | `us-east-1a` |
| public-subnet-1b | `10.0.2.0/24` | `us-east-1b` |
| private-subnet-1a | `10.0.11.0/24` | `us-east-1a` |
| private-subnet-1b | `10.0.12.0/24` | `us-east-1b` |

Public subnets are used for internet-facing infrastructure, while private subnets host application instances.

## 3. Configure Internet Gateway

Created an Internet Gateway named `devops-project-igw` and attached it to the custom VPC.

The Internet Gateway provides internet connectivity for resources in public subnets when their routing and security configurations permit it.

## 4. Configure Route Tables

### Public Route Table

Created `public-route-table` and associated it with both public subnets.

Routes:

| Destination | Target |
|---|---|
| `10.0.0.0/16` | Local |
| `0.0.0.0/0` | Internet Gateway |

This allows public subnet resources to communicate with the internet.

### Private Route Table

Created `private-route-table` and associated it with both private subnets.

Routes:

| Destination | Target |
|---|---|
| `10.0.0.0/16` | Local |
| `0.0.0.0/0` | NAT Gateway |

This allows private instances to initiate outbound internet connections without requiring public IP addresses.

## 5. Create NAT Gateway

Created a NAT Gateway in a public subnet and associated it with an Elastic IP address.

The private route table uses this NAT Gateway as its default route.

This allows private EC2 instances to access external services, such as Ubuntu package repositories, while keeping them inaccessible through direct internet-initiated connections.

**Cost and availability consideration:** One NAT Gateway was used for both private subnets to reduce project costs. A production design requiring stronger Availability Zone independence would normally deploy a NAT Gateway in each AZ.

## 6. Launch an EC2 Web Server

Initially launched an Ubuntu EC2 instance in a public subnet to test web server deployment.

Installed Nginx:

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl enable --now nginx
```

Created a custom webpage at:

```bash
sudo nano /var/www/html/index.html
```

Verified the website by accessing the instance's public IP address.

Also inspected Nginx logs:

```bash
sudo tail /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

This initial instance was used for testing and was later terminated after the Auto Scaling infrastructure was verified.

## 7. Configure Security Groups

Created separate security groups for the Application Load Balancer and web servers.

### ALB Security Group

- HTTP — TCP port 80 — `0.0.0.0/0`
- HTTPS — TCP port 443 — `0.0.0.0/0`

The configured ALB listener forwards HTTP traffic on port 80. An HTTPS listener and certificate were not configured.

### Web Server Security Group

- HTTP — TCP port 80 — Source: ALB security group
- Outbound traffic — Allowed

This ensures application HTTP traffic is accepted from the load balancer rather than directly from arbitrary internet sources.

## 8. Create an Application Load Balancer

Created an internet-facing Application Load Balancer named:

`devops-web-alb`

Configuration:

- Scheme: Internet-facing
- IP address type: IPv4
- VPC: `devops-project-vpc`
- Subnets: Both public subnets
- Security group: `alb-security-group`
- Listener: HTTP port 80

Created a target group:

`web-server-target-group`

Configuration:

- Target type: Instances
- Protocol: HTTP
- Port: 80
- Health check path: `/`
- Health check protocol: HTTP

The ALB forwards incoming requests to healthy registered application instances.

## 9. Create a Launch Template

Created a Launch Template named:

`devops-web-launch-template`

Configuration:

- AMI: Ubuntu Server 24.04 LTS
- Instance type: `t3.micro`
- Key pair: `devops-project-key`
- Security group: `devops-web-server-sg`
- Storage: 8 GiB gp3

Configured User Data to automatically install and start Nginx when an instance launches.

```bash
#!/bin/bash

apt-get update -y
apt-get install nginx -y

systemctl enable nginx
systemctl start nginx

cat > /var/www/html/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head>
<title>DevOps Auto Scaling</title>
</head>
<body>
<h1>DevOps Cloud Infrastructure</h1>
<h2>Running on Auto Scaling EC2</h2>
<p>Deployed automatically using AWS Launch Template.</p>
</body>
</html>
EOF
```

This allows newly launched instances to configure themselves automatically without manually installing Nginx.

## 10. Create an Auto Scaling Group

Created an Auto Scaling Group named:

`devops-web-asg`

Configuration:

| Setting | Value |
|---|---|
| Launch Template | `devops-web-launch-template` |
| VPC | `devops-project-vpc` |
| Subnets | Both private subnets |
| Minimum capacity | 2 |
| Desired capacity | 2 |
| Maximum capacity | 3 |
| Health checks | EC2 and ELB |

Attached the Auto Scaling Group to `web-server-target-group`.

Configured a Target Tracking scaling policy:

- Policy name: `cpu-target-tracking`
- Average CPU utilization target: 50%
- Instance warmup: 180 seconds

The group automatically maintains the desired number of instances and adjusts capacity according to CPU utilization.

## 11. Configure AWS Systems Manager

The application instances run in private subnets without public IP addresses.

Created an IAM role:

`devops-ec2-ssm-role`

Attached the AWS-managed policy:

`AmazonSSMManagedInstanceCore`

Assigned the IAM role to the EC2 instances.

Verified that both instances appeared online in Systems Manager Fleet Manager and used Session Manager to connect to them.

This provided administrative access without requiring publicly exposed SSH access.

## 12. Test Auto Scaling

Used `stress-ng` to generate CPU load on an application instance through Session Manager.

Installed the utility and ran:

```bash
cd /tmp
stress-ng --cpu 2 --timeout 600s
```

Monitored CPU utilization through Amazon CloudWatch.

Observed the following:

1. CPU utilization increased.
2. The Target Tracking scaling policy triggered.
3. Auto Scaling launched a third EC2 instance.
4. The new instance registered with the target group.
5. The target group reported three healthy instances.

After stopping the CPU stress test, the Auto Scaling Group scaled back down to two instances.

Both scale-out and scale-in operations were successfully demonstrated.

## 13. Configure CloudWatch and SNS Alerts

Created an SNS topic:

`devops-infrastructure-alerts`

Configured an email subscription and confirmed it.

Created a CloudWatch alarm:

`devops-asg-low-capacity-alarm`

Configuration:

- Metric: `GroupInServiceInstances`
- Auto Scaling Group: `devops-web-asg`
- Statistic: Minimum
- Period: 5 minutes
- Threshold: Fewer than 2 instances
- Evaluation: 1 datapoint out of 1
- Notification: SNS email notification

Temporarily changed the threshold to fewer than 3 instances while two instances were running to test the notification.

Successfully received the email alert.

## 14. Final Architecture Verification

Verified the main infrastructure components:

- Custom VPC and subnet configuration
- Public and private route tables
- Internet Gateway and NAT Gateway
- Application Load Balancer
- Healthy target group instances
- Auto Scaling Group
- Systems Manager connectivity
- CloudWatch monitoring
- SNS email notifications

The original manually launched public EC2 instance was terminated after testing. The application infrastructure was tested using private EC2 instances managed by the Auto Scaling Group.

## 15. Implementation Outcome

Successfully demonstrated an AWS web infrastructure with:

- Network isolation using public and private subnets
- Internet-facing load balancing
- Private application instances
- Automatic EC2 provisioning
- CPU-based scaling
- Health checks
- Secure administrative access through Systems Manager
- Monitoring and email alerts

The project provides a practical foundation for future improvements using Terraform, Docker, AWS CLI, and CI/CD automation.