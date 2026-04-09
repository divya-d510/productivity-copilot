# Quick Start Guide

Get your Productivity Copilot running in 5 minutes!

## Option 1: Docker Compose (Recommended for Local Development)

This starts everything you need: PostgreSQL, MCP Toolbox, and the API.

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your GOOGLE_CLOUD_PROJECT

# 2. Start all services
docker-compose up --build

# 3. Wait for services to be ready (about 30 seconds)
# You'll see: "Application startup complete" when ready

# 4. Test the API
python test_api.py
```

Access the API at: http://localhost:8080

## Option 2: Manual Setup (For Production or Custom Deployment)

### Step 1: Database Setup

```bash
# Using PostgreSQL with pgvector
psql -h localhost -U postgres -c "CREATE DATABASE productivity_db;"
psql -h localhost -U postgres -d productivity_db -f sql/schema.sql
```

### Step 2: Start MCP Toolbox Server

```bash
# Download toolbox binary (if not already installed)
# See: https://github.com/google/genai-toolbox

# Start the server
toolbox --config toolbox/tools.yaml --address 0.0.0.0 --port 5000
```

### Step 3: Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings:
# - GOOGLE_CLOUD_PROJECT
# - TOOLBOX_URL (default: http://localhost:5000)
```

### Step 4: Start the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
```

## Testing Your Setup

### Health Check
```bash
curl http://localhost:8080/health
```

### Create a Task
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a task to review the budget report"}'
```

### Schedule an Event
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Schedule a team meeting tomorrow at 2 PM"}'
```

### Multi-Step Workflow
```bash
curl -X POST http://localhost:8080/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Schedule a budget review meeting for tomorrow at 3 PM, create a task to prepare the slides, and search my notes for previous budget discussions"
  }'
```

### Run Full Test Suite
```bash
python test_api.py
```

## Troubleshooting

### "Connection refused" error
- Make sure all services are running
- Check `docker-compose ps` to see service status
- Wait a bit longer for services to start

### "Database connection failed"
- Verify PostgreSQL is running: `docker-compose ps postgres`
- Check database credentials in .env match docker-compose.yml

### "Google Cloud authentication error"
- Set GOOGLE_CLOUD_PROJECT in .env
- Authenticate: `gcloud auth application-default login`
- Ensure Vertex AI API is enabled in your project

### Toolbox server not responding
- Check logs: `docker-compose logs toolbox`
- Verify tools.yaml syntax is correct
- Ensure database is accessible from toolbox container

## Next Steps

1. Explore the API endpoints in README.md
2. Customize agent instructions in `agents/` directory
3. Add more tools in `toolbox/tools.yaml`
4. Deploy to production (see deployment guide)

## Production Deployment Notes

For production with AlloyDB:

1. Update `toolbox/tools.yaml` with AlloyDB connection details
2. Uncomment AlloyDB-specific features in `sql/schema.sql`:
   - `google_ml_integration` extension
   - Vector index creation
   - `embedding()` function calls
3. Use the full semantic search queries with vector similarity
4. Deploy to Cloud Run or GKE for scalability

## Support

- Check README.md for detailed documentation
- Review agent code in `agents/` for customization
- Inspect `toolbox/tools.yaml` for tool definitions
