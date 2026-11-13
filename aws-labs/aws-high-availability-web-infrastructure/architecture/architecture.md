# AWS Infrastructure Architecture

## 1. High-Level Architecture

The infrastructure uses a custom Amazon VPC across two Availability Zones.

```text
                         INTERNET
                            |
                            v
                    INTERNET GATEWAY
                            |
             +--------------+--------------+
             |                             |
       PUBLIC SUBNET A               PUBLIC SUBNET B
         10.0.1.0/24                  10.0.2.0/24
             |                             |
             +-------------+---------------+
                           |
                           v
                APPLICATION LOAD BALANCER
                           |
             +-------------+-------------+
             |                           |
       PRIVATE SUBNET A            PRIVATE SUBNET B
        10.0.11.0/24                10.0.12.0/24
             |                           |
             v                           v
          EC2 A                         EC2 B
          NGINX                         NGINX
             |                           |
             +-------------+-------------+
                           |
                    AUTO SCALING GROUP
                      Min: 2, Max: 3
                           |
                           v
                     CLOUDWATCH
                           |
                           v
                         SNS
                           |
                           v
                    EMAIL NOTIFICATION
```

## 2. Network Traffic Flow

### Incoming Traffic

1. A user accesses the website through the internet.
2. Traffic reaches the Internet Gateway.
3. The Application Load Balancer receives HTTP traffic on port 80.
4. The ALB forwards requests to healthy EC2 instances.
5. Nginx serves the website from the private EC2 instances.

### Outgoing Traffic

1. Private EC2 instances require outbound internet access for package installation and updates.
2. Their default route sends traffic to the NAT Gateway.
3. The NAT Gateway forwards outbound traffic through the Internet Gateway.

## 3. Auto Scaling Flow

1. CloudWatch monitors average CPU utilization.
2. CPU utilization exceeds the configured target.
3. The Target Tracking scaling policy triggers scale-out.
4. The Auto Scaling Group launches another EC2 instance.
5. The instance registers with the ALB target group.
6. After passing health checks, it receives traffic.
7. When demand decreases, the group can scale back in.

## 4. Security Architecture

- Public subnets contain the internet-facing ALB.
- Private subnets contain application EC2 instances.
- Security groups restrict application traffic to the ALB.
- Systems Manager provides administrative access without exposing SSH to the internet.
- An EC2 IAM role provides the required Systems Manager permissions.

## 5. Availability and Scaling

Two Availability Zones are used to distribute application instances.

The Auto Scaling Group maintains a minimum of two instances and can increase capacity to three instances when required.

**Note:** This project uses one NAT Gateway shared by both private subnets as a cost-saving configuration. A production architecture requiring stronger Availability Zone independence would typically use a NAT Gateway in each AZ.