# AWS Infrastructure Testing Results

This document records the practical tests performed during the AWS infrastructure project.

## 1. Nginx Web Server Test

**Objective:** Verify that the web server serves the application successfully.

**Test performed:**
- Installed Nginx on Ubuntu EC2 instances.
- Deployed a custom HTML webpage.
- Accessed the website through the Application Load Balancer DNS name.

**Result:** Successful. The website displayed the expected DevOps Cloud Infrastructure page.

## 2. Application Load Balancer Test

**Objective:** Verify that the ALB forwards traffic to healthy application instances.

**Test performed:**
- Configured an HTTP listener on port 80.
- Connected the listener to `web-server-target-group`.
- Configured HTTP health checks using `/`.
- Verified that registered EC2 targets became healthy.

**Result:** Successful. The target group reported two healthy application instances after the original manually launched EC2 instance was deregistered.

## 3. Systems Manager Connectivity Test

**Objective:** Access private EC2 instances without exposing SSH publicly.

**Test performed:**
- Created an EC2 IAM role with `AmazonSSMManagedInstanceCore`.
- Attached the role to the Auto Scaling instances.
- Verified their Systems Manager Ping status.
- Started a Session Manager session.

**Result:** Successful. Both private instances appeared online and could be accessed using Session Manager.

## 4. Auto Scaling Scale-Out Test

**Objective:** Verify automatic instance scaling under increased CPU utilization.

**Test performed:**

Used `stress-ng` through Session Manager:

```bash
cd /tmp
stress-ng --cpu 2 --timeout 600s
```

Observed CloudWatch CPU metrics and Auto Scaling activity.

**Result:** Successful.

- CPU utilization increased.
- CloudWatch scaling alarm entered the ALARM state.
- Auto Scaling launched a third EC2 instance.
- The new instance registered with the target group.
- The target group reported three healthy instances.

## 5. Auto Scaling Scale-In Test

**Objective:** Verify that the group reduces capacity when demand decreases.

**Test performed:**
- Stopped the CPU stress test.
- Waited for CPU utilization to decrease.
- Monitored Auto Scaling activity.

**Result:** Successful. The Auto Scaling Group reduced its capacity from three instances to two.

## 6. CloudWatch and SNS Email Alert Test

**Objective:** Verify that infrastructure alarms can send email notifications.

**Test performed:**
- Created an SNS topic named `devops-infrastructure-alerts`.
- Confirmed the email subscription.
- Created the CloudWatch alarm `devops-asg-low-capacity-alarm`.
- Temporarily changed the threshold to trigger the alarm while two instances were running.

**Result:** Successful. The CloudWatch alarm entered the ALARM state and an email notification was received.

## 7. Overall Test Summary

| Test | Result |
|---|---|
| Nginx website | Passed |
| ALB traffic forwarding | Passed |
| Target group health checks | Passed |
| Systems Manager connectivity | Passed |
| Auto Scaling scale-out | Passed |
| Auto Scaling scale-in | Passed |
| CloudWatch alarm | Passed |
| SNS email notification | Passed |

## Conclusion

The core infrastructure was successfully deployed and tested.

The project demonstrated load balancing, private-instance access, automatic scaling, health checks, infrastructure monitoring, and email alerting using AWS services.

These tests were performed during the project implementation. Resource cleanup and final cost verification are tracked separately.