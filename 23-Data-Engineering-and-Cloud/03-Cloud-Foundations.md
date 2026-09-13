# Cloud Foundations: Compute, Storage, Networking, Serverless, and IAM

## Prerequisites
- Basic understanding of computer hardware (CPU, RAM, Hard Drives).
- Familiarity with the concept of the Internet and IP addresses.

## Objectives
- Understand the core pillars of Cloud Computing: Compute, Storage, and Networking.
- Differentiate between Server-based and Serverless architectures.
- Learn the principles of Identity and Access Management (IAM).
- Map these concepts to the two major cloud providers: AWS and GCP.

## Intuition
Historically, companies had to buy physical servers, put them in a refrigerated room (on-premise data center), and wire them up. 
**Cloud Computing** is simply renting someone else's computers, hard drives, and network cables over the internet, paying only for exactly what you use, down to the millisecond.

## Core Concepts

### 1. Compute (The Brains)
Compute resources provide the processing power (CPU/RAM) required to run applications.
- **Virtual Machines (VMs):** You rent an entire operating system instance. You manage the OS, patches, and scaling.
    - *AWS:* Amazon EC2 (Elastic Compute Cloud)
    - *GCP:* Google Compute Engine (GCE)
- **Containers:** Lightweight, standalone, executable packages of software (Docker). Orchestrated at scale using Kubernetes.
    - *AWS:* EKS (Elastic Kubernetes Service), ECS
    - *GCP:* GKE (Google Kubernetes Engine)

### 2. Storage (The Memory)
Where data is persistently saved.
- **Object Storage:** Stores data as objects (files) with metadata and a unique ID. Infinite scaling, accessed via APIs over HTTP. Perfect for backups, images, data lakes.
    - *AWS:* Amazon S3 (Simple Storage Service)
    - *GCP:* Google Cloud Storage (GCS)
- **Block Storage:** Functions like a physical hard drive attached to a VM. High performance, used for OS drives and databases.
    - *AWS:* Amazon EBS (Elastic Block Store)
    - *GCP:* Persistent Disk
- **File Storage:** Shared file systems (like a network drive) that multiple VMs can access simultaneously.
    - *AWS:* Amazon EFS (Elastic File System)
    - *GCP:* Filestore

### 3. Networking (The Veins)
The infrastructure that connects compute and storage resources securely to each other and the internet.
- **VPC (Virtual Private Cloud):** A logically isolated section of the cloud network dedicated to your account.
- **Subnets:** Subdivisions of a VPC. Public subnets have internet access; private subnets do not (used for databases).
- **Load Balancers:** Distribute incoming network traffic across multiple servers to ensure high availability and reliability.

### 4. Serverless (No-Ops)
"Serverless" doesn't mean there are no servers. It means the cloud provider dynamically manages the allocation and provisioning of servers. You only write code and pay strictly for the execution time.
- **Functions as a Service (FaaS):** Run code in response to events (e.g., an image is uploaded to S3).
    - *AWS:* AWS Lambda
    - *GCP:* Google Cloud Functions
- **Serverless Containers:** Run containers without managing the underlying VMs.
    - *AWS:* AWS Fargate
    - *GCP:* Google Cloud Run

### 5. IAM (Identity and Access Management) (The Security Guard)
The framework of policies and technologies for ensuring that proper people (or machines) have the appropriate access to technology resources.
- **Users:** Human operators or service accounts.
- **Roles:** A set of permissions that can be assumed by a user or an application.
- **Policies:** JSON documents that explicitly define what actions are allowed or denied on which resources.
- **Principle of Least Privilege:** A core security concept stating that an entity should only be granted the minimum permissions necessary to perform its job.

## Code / Examples

### AWS IAM Policy Example (JSON)
This policy grants read-only access to a specific S3 bucket.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-company-data-lake",
        "arn:aws:s3:::my-company-data-lake/*"
      ]
    }
  ]
}
```

## Summary
Cloud foundations revolve around renting Compute, Storage, and Networking. Moving towards Serverless allows developers to focus purely on business logic rather than infrastructure management. Everything must be securely locked down using strictly scoped IAM policies.

## Interview Questions
1. **What is the difference between Object Storage and Block Storage?**
   *Answer:* Object storage (S3) stores files flatly with metadata over HTTP and scales infinitely. Block storage (EBS) attaches directly to a VM like a physical hard drive, offering high performance for OS/databases.
2. **Explain the concept of "Serverless" computing.**
   *Answer:* Serverless allows developers to build and run applications without managing underlying infrastructure. The cloud provider provisions servers dynamically, and billing is based purely on execution time (pay-per-invocation).
3. **What is the Principle of Least Privilege in IAM?**
   *Answer:* It is a security principle where a user, program, or system is granted only the bare minimum permissions required to perform its designated task, reducing the attack surface.
