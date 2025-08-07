# AWS Architecture for Skyral Transport Simulation Demo

## Overview

This document describes the AWS setup for the Skyral Transport Simulation demo.  
The infrastructure is designed for security, scalability, and easy management using standard AWS services.

---

## 1. Core AWS Services Used

### **1.1. Route 53**
- Custom DNS for the public app URL (e.g., `skyraldemo.obaidmalik.co.uk`).
- Routes traffic to CloudFront distribution.

### **1.2. CloudFront**
- CDN in front of the application.
- Serves static assets directly from S3 and proxies dynamic app traffic to EC2.
- Enforces HTTPS using AWS Certificate Manager.

### **1.3. S3**
- Stores static files: documentation, images, project assets, results, logs.
- Integrated as an origin for CloudFront.
- Versioning and access logging enabled for data integrity and traceability.

### **1.4. EC2 (used for app and chatbot backend)**
- The main application server (Streamlit, future chatbot/LLM backend) is run on an EC2 instance.
- Ollama LLM/chatbot runs locally on the same instance, not exposed to the public.
- Only HTTPS (via CloudFront) allowed for inbound web access.

### **1.5. IAM**
- Used to manage permissions for:
    - EC2
    - S3 bucket access
    - GitHub Actions deployments
- Principle of least privilege enforced.

### **1.6. Certificate Manager**
- Issues and manages SSL/TLS certificates for the app domain.
- Used with CloudFront to ensure all traffic is encrypted.

### **1.7. GitHub Actions**
- Automated deployment: pushes new app versions from GitHub to AWS (typically via SSH, S3 sync, or CI/CD user roles).

### **1.8. CloudWatch**
- Centralized logging and basic monitoring (EC2, S3, app logs if configured).
- Custom metrics or alarms set for error rates, billing, and usage.

### **1.9. Billing and Cost Management**
- Simple cost alarms/alerts set to avoid runaway AWS charges.
- Monitors monthly cost thresholds and notifies via email.

---

## 2. Architecture Diagram (ASCII)

┌──────────────┐
│ End Users │
└──────┬───────┘
│
▼
┌───────────────┐
│ Route 53 │
└──────┬────────┘
│
▼
┌───────────────┐
│ CloudFront │
└─────┬─┬───────┘
/
┌───▼─┐ ┌─▼───┐
│ S3 │ │ EC2 │ (app + chatbot/LLM)
└─────┘ └─────┘
- **Static assets** (docs, images, JS, CSS) served from S3 via CloudFront.
- **App traffic** proxied to EC2 (Streamlit backend and chatbot).
- All access is via HTTPS; SSL certs managed by AWS Certificate Manager.

---

## 3. Security

- **IAM roles**: Tight permissions for all services; deployment roles limited to only necessary actions.
- **S3 bucket policy**: Public read for static assets only (if required); all other objects private.
- **CloudFront**: Protects against direct S3 bucket access; WAF optional for extra protection.
- **No direct public EC2 access**: All traffic routed through CloudFront; admin access (if any) via VPN or SSH from trusted IPs.
- **Certificates**: TLS/SSL everywhere using AWS Certificate Manager.
- **Cost controls**: CloudWatch billing alarms to monitor and cap monthly spend.

---

## 4. CI/CD Workflow

- Code is pushed to GitHub.
- On main branch updates, **GitHub Actions** builds and deploys app updates to AWS:
    - Syncs static assets to S3.
    - Deploys new backend code to EC2.
- Deployments use IAM user/role with restricted permissions.

---

## 5. Monitoring

- **CloudWatch** collects logs from S3 and EC2 (if configured).
- Custom CloudWatch alarms for billing, error rates, or app downtime.

---

## 6. SSL/TLS Certificates

- Managed by **AWS Certificate Manager**.
- Automatically renews and attaches to CloudFront for end-to-end encryption.

---

## 7. Cost Management

- **Free tier or low-cost eligible:** S3 storage and Route 53 are very inexpensive for small demo apps.
- **CloudFront:** Small monthly fee for bandwidth.
- **Certificate Manager:** Free for SSL certs used in CloudFront.
- **Billing alerts:** Notifies you if AWS spend exceeds thresholds (e.g., £10, £20).

---

## 8. Chatbot/LLM Backend Approach

- The chatbot is deployed on the **same EC2 instance** as the main Streamlit app.
- **Ollama** (all-MiniLM-L6-v2) local LLM is run alongside the app and only exposed internally (not public).
- **No extra AWS services are required** for LLM/QA: No SageMaker, no external API costs.
- Cost is determined by the EC2 instance size and uptime; for small LLMs, t3a.medium is typically sufficient.

---

## 9. Summary Table

| Service            | Purpose                       | Typical Cost (demo)         |
|--------------------|------------------------------|-----------------------------|
| Route 53           | Custom domain                 | ~$1/month                   |
| CloudFront         | CDN + HTTPS                   | $1–5/month (demo use)       |
| S3                 | Static file storage           | < $1/month                  |
| Certificate Mgr    | SSL/TLS certs                 | Free (if used with CF/S3)   |
| IAM                | Roles/policies                | Free                        |
| GitHub Actions     | CI/CD                         | Free for small projects     |
| CloudWatch         | Logs/billing                  | Free for basic use/alarms   |
| EC2                | App/LLM backend               | $5–$20/month depending on instance size and usage |

---
