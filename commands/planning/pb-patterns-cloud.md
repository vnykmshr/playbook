---
name: "pb-patterns-cloud"
title: "Cloud Deployment Patterns (AWS, GCP, Azure)"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-deployment', 'pb-patterns-core', 'pb-observability', 'pb-patterns-distributed']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Cloud Deployment Patterns (AWS, GCP, Azure)

## Overview

Cloud platforms (AWS, GCP, Azure) offer multiple ways to deploy the same architecture. Choosing patterns based on your constraints—cost, latency, skill, scale—is crucial. This guide covers proven deployment patterns across the three major cloud platforms, with real-world trade-offs.

**Caveat:** Each platform has competing patterns. Use `/pb-preamble` thinking (challenge assumptions, surface trade-offs) and `/pb-design-rules` thinking (especially Simplicity and Parsimony—choose what you actually need, not what's available).

Question your actual constraints before choosing. Challenge vendor recommendations. The cheapest or most featured pattern isn't always the right one. Choose based on your requirements, not vendor features.

**Resource Hint:** sonnet — Cloud deployment pattern reference; platform-specific implementation guidance.

---

## AWS Patterns

### Pattern 1: API on EC2 with RDS

**When to use**: Small-to-medium services, full control needed, existing infrastructure knowledge

**How it works**:
1. Application runs on EC2 instances (managed servers)
2. PostgreSQL/MySQL in RDS (managed database)
3. Auto Scaling Group scales instances based on CPU/memory
4. Application Load Balancer (ALB) distributes traffic

**Go/Python Example (Deployment)**:
```bash
# AWS CloudFormation template (simplified)
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # Security group
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP/HTTPS
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

  # RDS Database
  Database:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.t3.micro
      Engine: postgres
      AllocatedStorage: 20
      MasterUsername: admin
      MasterUserPassword: !Sub '{{resolve:secretsmanager:db-password::password}}'
      VPCSecurityGroups:
        - !GetAtt WebSecurityGroup.GroupId

  # Launch Configuration
  LaunchConfig:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      ImageId: ami-0c55b159cbfafe1f0  # Amazon Linux 2
      InstanceType: t3.micro
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          yum install -y golang
          git clone https://github.com/yourorg/app.git /app
          cd /app
          go build -o app ./cmd/main.go
          ./app

  # Auto Scaling Group
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      LaunchConfigurationName: !Ref LaunchConfig
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      LoadBalancerNames:
        - !Ref LoadBalancer
      VPCZoneIdentifier:
        - subnet-12345678
        - subnet-87654321

  # Load Balancer
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing
      Subnets:
        - subnet-12345678
        - subnet-87654321
```

**Terraform Alternative**:
```hcl
provider "aws" {
  region = "us-east-1"
}

# RDS Database
resource "aws_db_instance" "app_db" {
  identifier     = "app-db"
  engine         = "postgres"
  engine_version = "14"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  username       = "admin"
  password       = random_password.db.result
  skip_final_snapshot = true

  lifecycle {
    ignore_changes = [password]
  }
}

# EC2 Instance
resource "aws_instance" "app_server" {
  count           = 2
  ami             = data.aws_ami.amazon_linux.id
  instance_type   = "t3.micro"
  security_groups = [aws_security_group.app.id]

  user_data = base64encode(file("${path.module}/user_data.sh"))

  tags = {
    Name = "app-server-${count.index + 1}"
  }
}

# Application Load Balancer
resource "aws_lb" "app" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}
```

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

**Dockerfile**:
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /build
COPY . .
RUN go build -o app ./cmd/main.go

FROM debian:bookworm-slim
COPY --from=builder /build/app /app
EXPOSE 8080
CMD ["/app"]
```

**AWS CloudFormation (ECS Fargate)**:
```yaml
Resources:
  ECRRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: app
      ImageScanningConfiguration:
        ScanOnPush: true

  TaskExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: app-task
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: 256
      Memory: 512
      ExecutionRoleArn: !GetAtt TaskExecutionRole.Arn
      ContainerDefinitions:
        - Name: app
          Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/app:latest'
          PortMappings:
            - ContainerPort: 8080
          Environment:
            - Name: DATABASE_URL
              Value: !Sub 'postgres://user:pass@${Database.Endpoint.Address}:5432/app'
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref LogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: ecs

  Service:
    Type: AWS::ECS::Service
    DependsOn: LoadBalancerListener
    Properties:
      Cluster: !Ref Cluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: DISABLED
          Subnets: [subnet-12345, subnet-67890]
          SecurityGroups: [sg-abc123]
      LoadBalancers:
        - ContainerName: app
          ContainerPort: 8080
          TargetGroupArn: !Ref TargetGroup

  AutoScaling:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 10
      MinCapacity: 2
      ResourceId: !Sub 'service/${Cluster}/${Service.Name}'
      RoleARN: !Sub 'arn:aws:iam::${AWS::AccountId}:role/service-role'
      ScalableDimension: ecs:service:DesiredCount
      ServiceNamespace: ecs

  ScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: cpu-scaling
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref AutoScaling
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 70.0
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageCPUUtilization
        ScaleOutCooldown: 60
        ScaleInCooldown: 300
```

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

**Go Lambda Example**:
```go
package main

import (
  "context"
  "github.com/aws/aws-lambda-go/events"
  "github.com/aws/aws-lambda-go/lambda"
)

func HandleRequest(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
  // Get user ID from path
  userID := request.PathParameters["id"]

  // Query DynamoDB
  item, err := getUser(userID)
  if err != nil {
    return events.APIGatewayProxyResponse{
      StatusCode: 500,
      Body:       "Error retrieving user",
    }, nil
  }

  return events.APIGatewayProxyResponse{
    StatusCode: 200,
    Body:       item.String(),
  }, nil
}

func main() {
  lambda.Start(HandleRequest)
}
```

**CloudFormation**:
```yaml
Resources:
  ApiRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: dynamodb-access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                Resource: !GetAtt UsersTable.Arn

  GetUserFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: get-user
      Runtime: go1.x
      Handler: bootstrap
      Code:
        S3Bucket: deployment-bucket
        S3Key: lambda.zip
      Role: !GetAtt ApiRole.Arn
      Environment:
        Variables:
          TABLE_NAME: !Ref UsersTable

  ApiGateway:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: user-api
      ProtocolType: HTTP

  ApiRoute:
    Type: AWS::ApiGatewayV2::Route
    Properties:
      ApiId: !Ref ApiGateway
      RouteKey: 'GET /users/{id}'
      Target: !Sub 'integrations/${GetUserIntegration}'

  GetUserIntegration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      ApiId: !Ref ApiGateway
      IntegrationType: AWS_PROXY
      IntegrationUri: !Sub 'arn:aws:apigatewayv2:${AWS::Region}:lambda:path/2015-03-31/functions/${GetUserFunction}/invocations'
      PayloadFormatVersion: '2.0'

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH
```

**Trade-offs**:
- ✅ No infrastructure management
- ✅ Cost-effective for bursty load
- ✅ Automatic scaling
- ❌ Cold start latency (500ms+)
- ❌ Limited execution time (15 minutes)
- ❌ Harder to debug and test

---

## GCP Patterns

### Pattern 1: Cloud Run (Containers)

**When to use**: Containerized services, stateless workloads, simple to manage

**How it works**:
1. Push container to Container Registry
2. Cloud Run deploys and manages
3. Auto-scales based on requests
4. Traffic split for canary deployments
5. Cloud SQL for databases

**Deployment (gcloud CLI)**:
```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT/app:latest

# Deploy to Cloud Run
gcloud run deploy app \
  --image gcr.io/PROJECT/app:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 100 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=cloudsql://... \
  --clear-sql-instances

# Canary deployment (10% to new version)
gcloud run services update-traffic app \
  --to-revisions app-v1=90,app-v2=10 \
  --region us-central1
```

**Terraform**:
```hcl
resource "google_cloud_run_service" "app" {
  name     = "app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/my-project/app:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "DATABASE_URL"
          value = google_sql_database_instance.postgres.connection_name
        }
        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
      service_account_name = google_service_account.app.email
      timeout_seconds      = 3600
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "100"
        "autoscaling.knative.dev/minScale" = "1"
      }
    }
  }

  traffic {
    percent        = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

**Trade-offs**:
- ✅ Simple deployment (push container, auto-manages)
- ✅ Easy traffic splitting (canary/blue-green)
- ✅ Pay per request
- ❌ Cold start for idle services
- ❌ Limited to 1 hour execution
- ❌ Not suitable for background jobs

---

### Pattern 2: GKE (Kubernetes)

**When to use**: Complex microservice architectures, multi-region, advanced networking

**How it works**:
1. Kubernetes cluster manages containers
2. Service mesh (Istio) for networking
3. Advanced routing, load balancing, retry logic
4. StatefulSet for stateful services

**Kubernetes Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: app
        image: gcr.io/project/app:v1.2
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

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

**Azure CLI Deployment**:
```bash
# Create App Service plan
az appservice plan create \
  --name myplan \
  --resource-group mygroup \
  --sku B1 \
  --is-linux

# Create App Service
az webapp create \
  --resource-group mygroup \
  --plan myplan \
  --name myapp \
  --runtime "go|1.21"

# Deploy from GitHub
az webapp deployment github-actions add \
  --repo-url https://github.com/user/app \
  --branch main \
  --runtime-version 1.21

# Configure environment
az webapp config appsettings set \
  --resource-group mygroup \
  --name myapp \
  --settings DATABASE_URL="Server=mydb..." ENVIRONMENT="production"

# Enable auto-scaling
az monitor autoscale create \
  --resource-group mygroup \
  --resource myapp \
  --resource-type "microsoft.web/serverfarms" \
  --min-count 2 \
  --max-count 10 \
  --count 2

az monitor autoscale rule create \
  --resource-group mygroup \
  --autoscale-name myappautoscale \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

**Terraform**:
```hcl
resource "azurerm_app_service_plan" "app" {
  name                = "app-plan"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "app" {
  name                = "myapp"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name
  app_service_plan_id = azurerm_app_service_plan.app.id

  site_config {
    linux_fx_version = "DOCKER|myregistry.azurecr.io/app:latest"
  }

  app_settings = {
    DATABASE_URL = azurerm_postgresql_server.db.fqdn
    ENVIRONMENT  = "production"
  }
}

resource "azurerm_monitor_autoscale_setting" "app" {
  name                = "app-autoscale"
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  target_resource_id  = azurerm_app_service_plan.app.id

  profile {
    name = "default"

    capacity {
      default = 2
      minimum = 2
      maximum = 10
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.app.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        operator           = "GreaterThan"
        threshold          = 70
      }
      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT5M"
      }
    }
  }
}
```

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

**Python Azure Function Example**:
```python
import azure.functions as func
import json
from azure.data.tables import TableClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('id')

    try:
        # Query Azure Table Storage
        table_client = TableClient.from_connection_string(
            conn_str=os.environ['STORAGE_CONNECTION_STRING'],
            table_name='Users'
        )
        entity = table_client.get_entity(partition_key='user', row_key=user_id)

        return func.HttpResponse(json.dumps(entity), status_code=200)
    except:
        return func.HttpResponse("User not found", status_code=404)
```

**Terraform**:
```hcl
resource "azurerm_function_app" "app" {
  name                       = "myapp"
  location                   = azurerm_resource_group.app.location
  resource_group_name        = azurerm_resource_group.app.name
  app_service_plan_id        = azurerm_app_service_plan.consumption.id
  storage_account_name       = azurerm_storage_account.app.name
  storage_account_access_key = azurerm_storage_account.app.primary_access_key

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME       = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.app.instrumentation_key
  }
}
```

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

## Cost Comparison (Example: API server, 1M requests/month)

| Platform | Compute | Database | Total (monthly) |
|----------|---------|----------|-----------------|
| **AWS Lambda** | $0.20 | $8 | $8.20 |
| **AWS EC2** | $15 | $8 | $23 |
| **GCP Cloud Run** | $2.50 | $12 | $14.50 |
| **Azure Functions** | $0.16 | $15 | $15.16 |

*Costs vary by region, data transfer, and specific services. Use cloud calculators for accurate estimates.*

---

## Anti-Patterns

❌ **Lift-and-shift without optimization** — Refactor for cloud, not just migrate
❌ **Multi-cloud without strategy** — Complexity without clear benefit
❌ **Ignoring data residency** — Some data must stay in specific regions
❌ **Not monitoring costs** — Cloud spending grows silently
❌ **Manual infrastructure** — Use Infrastructure as Code (Terraform, CloudFormation)
❌ **No disaster recovery** — Plan for region failures

---

## When to Use Cloud Patterns

- **MVP**: Start simple (Lambda/Cloud Functions), add complexity as needed
- **High scale**: Multi-region architecture with data replication
- **Cost-sensitive**: Serverless for bursty workloads
- **Operations-heavy**: Kubernetes for full control
- **Simple services**: PaaS (App Service, Cloud Run)

---

## Related Commands

- See `/pb-deployment` for deployment strategy selection
- See `/pb-patterns-core` for architectural patterns
- See `/pb-observability` for cloud monitoring setup
- See `/pb-patterns-distributed` for multi-region patterns

---

**Choose cloud patterns based on your constraints: cost, skill, latency, scale. Start simple, evolve with needs.**
