---
name: "pb-patterns-cloud"
title: "Cloud Deployment Patterns (AWS, GCP, Azure)"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-deployment', 'pb-patterns-core', 'pb-observability', 'pb-patterns-distributed', 'pb-zero-stack']
last_reviewed: "2026-11-04"
version: "2.0.0"
version_notes: "v2.0.0: Cut from 872 to 222 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. Cloud Run deploys from Artifact Registry; the unsourced cold-start figure is gone."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Cloud Deployment Patterns (AWS, GCP, Azure)

## Overview

Cloud platforms (AWS, GCP, Azure) offer multiple ways to deploy the same architecture. Choosing patterns based on your constraints (cost, latency, skill, scale) is crucial. This guide covers proven deployment patterns across the three major cloud platforms, with real-world trade-offs.

**Caveat:** Each platform has competing patterns. Use `/pb-preamble` thinking (challenge assumptions, surface trade-offs) and `/pb-design-rules` thinking (especially Simplicity and Parsimony: choose what you actually need, not what's available).

Question your actual constraints before choosing. Challenge vendor recommendations. The cheapest or most featured pattern isn't always the right one. Choose based on your requirements, not vendor features.

**Resource Hint:** sonnet - Cloud deployment pattern reference; platform-specific implementation guidance.

---

## AWS Patterns

### Pattern 1: API on EC2 with RDS

**When to use**: Small-to-medium services, full control needed, existing infrastructure knowledge

**How it works**:
1. Application runs on EC2 instances (managed servers)
2. PostgreSQL/MySQL in RDS (managed database)
3. Auto Scaling Group scales instances based on CPU/memory
4. Application Load Balancer (ALB) distributes traffic

**Trade-offs**:
- ✅ Full control over infrastructure
- ✅ Cost-effective for steady workloads
- ✅ Familiar to traditional sysadmins
- ❌ Requires managing patches, security
- ❌ Manual scaling not as responsive
- ❌ Overkill for small/bursty workloads

---

### Pattern 2: Containerized Service on ECS

**When to use**: Consistent deployments, rolling updates, container-based workflows

**How it works**:
1. Application containerized in Docker
2. ECS Fargate runs containers (serverless container orchestration)
3. RDS for data persistence
4. ALB routes traffic
5. CloudWatch monitors logs and metrics

**Trade-offs**:
- ✅ Consistent deployments (same container everywhere)
- ✅ Easy rolling updates
- ✅ Fargate abstracts infrastructure
- ❌ Docker knowledge required
- ❌ Less control than EC2
- ❌ Startup time longer than serverless

---

### Pattern 3: API Gateway + Lambda (Serverless)

**When to use**: Event-driven, variable load, minimal operations, cost-conscious

**How it works**:
1. API Gateway exposes HTTP endpoint
2. Lambda functions execute on-demand
3. DynamoDB for ultra-high throughput data
4. Pay only for compute used

**Trade-offs**:
- ✅ No infrastructure management
- ✅ Cost-effective for bursty load
- ✅ Automatic scaling
- ❌ Cold start latency
- ❌ Limited execution time (15 minutes)
- ❌ Harder to debug and test

---

## GCP Patterns

### Pattern 1: Cloud Run (Containers)

**When to use**: Containerized services, stateless workloads, simple to manage

**How it works**:
1. Push container to Artifact Registry
2. Cloud Run deploys and manages
3. Auto-scales based on requests
4. Traffic split for canary deployments
5. Cloud SQL for databases

**Trade-offs**:
- ✅ Simple deployment (push container, auto-manages)
- ✅ Easy traffic splitting (canary/blue-green)
- ✅ Pay per request
- ❌ Cold start for idle services
- ❌ Limited to 1 hour execution

---

### Pattern 2: GKE (Kubernetes)

**When to use**: Complex microservice architectures, multi-region, advanced networking

**How it works**:
1. Kubernetes cluster manages containers
2. Service mesh (Istio) for networking
3. Advanced routing, load balancing, retry logic
4. StatefulSet for stateful services

**Trade-offs**:
- ✅ Powerful multi-region orchestration
- ✅ Advanced networking and routing
- ✅ Service mesh capabilities
- ❌ Steep learning curve
- ❌ Operational overhead
- ❌ Overkill for simple services

---

## Azure Patterns

### Pattern 1: App Service (PaaS)

**When to use**: Simple to moderately complex services, .NET/Node/Python/Go apps

**How it works**:
1. Deploy code or container directly
2. App Service handles infrastructure
3. Auto-scaling based on metrics
4. Azure Database (SQL, PostgreSQL, MySQL)
5. Traffic Manager for multi-region

**Trade-offs**:
- ✅ Simple to deploy and manage
- ✅ Good integration with .NET ecosystem
- ✅ Built-in auto-scaling
- ❌ Less control than IaaS
- ❌ Vendor lock-in to Azure
- ❌ Cold starts for idle apps

---

### Pattern 2: Azure Container Instances + Functions

**When to use**: Serverless workloads, event-driven, minimal management

**How it works**:
1. Azure Functions run code on demand
2. Timer triggers, HTTP triggers, event triggers
3. Auto-scaling per trigger
4. Pay per execution

**Trade-offs**:
- ✅ No infrastructure management
- ✅ Cheap for sporadic workloads
- ✅ Event-driven (timers, queues, HTTP)
- ❌ 10-minute execution limit
- ❌ Cold start latency
- ❌ Vendor lock-in

---

## Cloud Selection Matrix

| Pattern | AWS | GCP | Azure | Best For |
|---------|-----|-----|-------|----------|
| **Simple CRUD API** | EC2+RDS | Cloud Run | App Service | Simplicity |
| **Serverless Events** | Lambda+DynamoDB | Cloud Functions | Functions | Cost-sensitive, bursty |
| **Kubernetes Microservices** | EKS | GKE | AKS | Complex, multi-region |
| **Container Services** | ECS Fargate | Cloud Run | Container Instances | Consistency |
| **Global CDN** | CloudFront | Cloud CDN | Azure CDN | Static/media content |
| **Data Warehouse** | Redshift | BigQuery | Synapse | Analytics |
| **Message Queue** | SQS | Pub/Sub | Service Bus | Async processing |

---

## Anti-Patterns

❌ **Lift-and-shift without optimization** - Refactor for cloud, not just migrate
❌ **Multi-cloud without strategy** - Complexity without clear benefit
❌ **Ignoring data residency** - Some data must stay in specific regions
❌ **Not monitoring costs** - Cloud spending grows silently
❌ **Manual infrastructure** - Use Infrastructure as Code (Terraform, CloudFormation)
❌ **No disaster recovery** - Plan for region failures

---

## When to Use Cloud Patterns

- **MVP**: Start simple (Lambda/Cloud Functions), add complexity as needed
- **High scale**: Multi-region architecture with data replication
- **Cost-sensitive**: Serverless for bursty workloads
- **Operations-heavy**: Kubernetes for full control
- **Simple services**: PaaS (App Service, Cloud Run)

---

## Related Commands

- `/pb-deployment` - Deployment strategy selection
- `/pb-patterns-core` - Architectural patterns
- `/pb-observability` - Cloud monitoring setup
- `/pb-patterns-distributed` - Multi-region patterns
- `/pb-zero-stack` - $0/month app architecture (static + edge proxy + CI)

---

**Choose cloud patterns based on your constraints: cost, skill, latency, scale. Start simple, evolve with needs.**
