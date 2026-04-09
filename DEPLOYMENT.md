# Production Deployment Guide

This guide covers deploying the Productivity Copilot to Google Cloud Platform with AlloyDB.

## Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  Cloud Run   │─────▶│  AlloyDB    │
│             │      │  (API)       │      │  (Postgres) │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Cloud Run   │
                     │  (Toolbox)   │
                     └──────────────┘
```

## Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed locally
- AlloyDB cluster created

## Step 1: Set Up AlloyDB

```bash
# Create AlloyDB cluster (if not exists)
gcloud alloydb clusters create productivity-cluster \
  --region=us-central1 \
  --password=YOUR_SECURE_PASSWORD

# Create primary instance
gcloud alloydb instances create productivity-primary \
  --cluster=productivity-cluster \
  --region=us-central1 \
  --instance-type=PRIMARY \
  --cpu-count=2

# Get the instance IP
gcloud alloydb instances describe productivity-primary \
  --cluster=productivity-cluster \
  --region=us-central1 \
  --format="value(ipAddress)"
```

## Step 2: Initialize Database

```bash
# Connect via Cloud SQL Proxy or private IP
psql -h <ALLOYDB_IP> -U postgres -d postgres

# Create database and user
CREATE DATABASE productivity_db;
CREATE USER productivity_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE productivity_db TO productivity_user;

# Connect to the new database
\c productivity_db

# Run schema
\i sql/schema.sql
```

## Step 3: Update Configuration

Update `toolbox/tools.yaml` with your AlloyDB connection:

```yaml
sources:
  alloydb-pg:
    kind: postgres
    host: <ALLOYDB_IP>
    port: 5432
    database: productivity_db
    user: productivity_user
    password: <YOUR_PASSWORD>
```

## Step 4: Build and Push Container Images

```bash
# Set your project ID
export PROJECT_ID=your-project-id
export REGION=us-central1

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com

# Create Artifact Registry repository
gcloud artifacts repositories create productivity-copilot \
  --repository-format=docker \
  --location=$REGION

# Build and push API image
docker build -f Dockerfile.txt -t $REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:latest .
docker push $REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:latest

# Build and push Toolbox image
docker build -f toolbox-image/Dockerfile -t $REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/toolbox:latest ./toolbox-image
docker push $REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/toolbox:latest
```

## Step 5: Deploy to Cloud Run

### Deploy Toolbox Service

```bash
gcloud run deploy productivity-toolbox \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/toolbox:latest \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --cpu=1 \
  --max-instances=10

# Get the toolbox URL
export TOOLBOX_URL=$(gcloud run services describe productivity-toolbox \
  --region=$REGION \
  --format="value(status.url)")
```

### Deploy API Service

```bash
gcloud run deploy productivity-api \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:latest \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=20 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,TOOLBOX_URL=$TOOLBOX_URL,APP_NAME=productivity-copilot,DEMO_USER_ID=00000000-0000-0000-0000-000000000001"

# Get the API URL
export API_URL=$(gcloud run services describe productivity-api \
  --region=$REGION \
  --format="value(status.url)")

echo "API deployed at: $API_URL"
```

## Step 6: Configure VPC Connector (for AlloyDB Access)

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create productivity-connector \
  --region=$REGION \
  --network=default \
  --range=10.8.0.0/28

# Update Cloud Run services to use VPC connector
gcloud run services update productivity-toolbox \
  --region=$REGION \
  --vpc-connector=productivity-connector \
  --vpc-egress=private-ranges-only

gcloud run services update productivity-api \
  --region=$REGION \
  --vpc-connector=productivity-connector \
  --vpc-egress=private-ranges-only
```

## Step 7: Set Up Authentication (Optional)

For production, enable authentication:

```bash
# Remove unauthenticated access
gcloud run services remove-iam-policy-binding productivity-api \
  --region=$REGION \
  --member="allUsers" \
  --role="roles/run.invoker"

# Add authenticated users
gcloud run services add-iam-policy-binding productivity-api \
  --region=$REGION \
  --member="user:your-email@example.com" \
  --role="roles/run.invoker"
```

## Step 8: Test Production Deployment

```bash
# Test health endpoint
curl $API_URL/health

# Test with authentication (if enabled)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  $API_URL/health

# Run full test suite against production
API_BASE=$API_URL python test_api.py
```

## Monitoring and Logging

### View Logs

```bash
# API logs
gcloud run services logs read productivity-api --region=$REGION

# Toolbox logs
gcloud run services logs read productivity-toolbox --region=$REGION
```

### Set Up Alerts

```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=YOUR_CHANNEL_ID \
  --display-name="High Error Rate - Productivity API" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

## Scaling Configuration

### Auto-scaling Settings

```bash
# Update API service with custom scaling
gcloud run services update productivity-api \
  --region=$REGION \
  --min-instances=1 \
  --max-instances=50 \
  --concurrency=80 \
  --cpu-throttling \
  --memory=4Gi \
  --cpu=4
```

### Cost Optimization

- Set `--min-instances=0` for dev/staging environments
- Use `--cpu-throttling` to reduce costs when idle
- Monitor usage with Cloud Monitoring
- Set budget alerts in Cloud Billing

## Security Best Practices

1. **Use Secret Manager for sensitive data:**
```bash
# Store database password
echo -n "YOUR_PASSWORD" | gcloud secrets create db-password --data-file=-

# Update Cloud Run to use secret
gcloud run services update productivity-toolbox \
  --region=$REGION \
  --update-secrets=DB_PASSWORD=db-password:latest
```

2. **Enable VPC Service Controls**
3. **Use Workload Identity for service authentication**
4. **Implement rate limiting at the API level**
5. **Enable Cloud Armor for DDoS protection**

## Continuous Deployment

### Set Up Cloud Build

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build API
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-f', 'Dockerfile.txt', '-t', '$_REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:$SHORT_SHA', '.']
  
  # Push API
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', '$_REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:$SHORT_SHA']
  
  # Deploy API
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args:
      - 'run'
      - 'deploy'
      - 'productivity-api'
      - '--image=$_REGION-docker.pkg.dev/$PROJECT_ID/productivity-copilot/api:$SHORT_SHA'
      - '--region=$_REGION'

substitutions:
  _REGION: us-central1

options:
  logging: CLOUD_LOGGING_ONLY
```

### Create Build Trigger

```bash
gcloud builds triggers create github \
  --repo-name=productivity-copilot \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

## Backup and Disaster Recovery

```bash
# Set up automated AlloyDB backups
gcloud alloydb backups create productivity-backup-$(date +%Y%m%d) \
  --cluster=productivity-cluster \
  --region=us-central1

# Schedule daily backups via Cloud Scheduler
gcloud scheduler jobs create http daily-backup \
  --schedule="0 2 * * *" \
  --uri="https://alloydb.googleapis.com/v1/projects/$PROJECT_ID/locations/us-central1/clusters/productivity-cluster/backups" \
  --http-method=POST
```

## Troubleshooting

### Service won't start
- Check logs: `gcloud run services logs read productivity-api`
- Verify environment variables are set correctly
- Ensure VPC connector is properly configured

### Database connection issues
- Verify AlloyDB IP is accessible from VPC connector
- Check firewall rules
- Confirm credentials in Secret Manager

### High latency
- Check AlloyDB query performance
- Review Cloud Run instance metrics
- Consider increasing CPU/memory allocation
- Enable connection pooling

## Cost Estimation

Approximate monthly costs (us-central1):

- AlloyDB (2 vCPU): ~$300
- Cloud Run API (moderate traffic): ~$50
- Cloud Run Toolbox: ~$20
- Vertex AI API calls: ~$30
- Networking: ~$10

Total: ~$410/month

Optimize by:
- Using smaller AlloyDB instance for dev
- Setting min-instances=0 for non-prod
- Implementing caching
- Using Cloud CDN for static content
