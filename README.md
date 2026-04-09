# Productivity Copilot

A multi-agent AI system built with Google ADK that helps users manage tasks, calendar events, and notes with semantic search capabilities.

## Architecture

- **Root Agent**: Orchestrates workflow across specialized sub-agents
- **Calendar Agent**: Manages events, scheduling, and availability
- **Task & Notes Agent**: Handles to-dos and note-taking
- **Memory Agent**: Provides semantic search across tasks and notes
- **MCP Toolbox**: Database-backed tools via Model Context Protocol
- **FastAPI**: REST API for client integration

## Prerequisites

- Python 3.12+
- PostgreSQL with AlloyDB AI extensions (or compatible vector database)
- Google Cloud Project with Vertex AI enabled
- Docker (optional, for containerized deployment)

## Setup

1. Clone and install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Google Cloud project details
```

3. Set up the database:
```bash
# Connect to your PostgreSQL instance
psql -h <DB_HOST> -U <DB_USER> -d <DB_NAME> -f sql/schema.sql
```

4. Start the MCP Toolbox server:
```bash
# Option 1: Using Docker
cd toolbox-image
docker build -t productivity-toolbox .
docker run -p 5000:8080 productivity-toolbox

# Option 2: Using toolbox binary directly
toolbox --config toolbox/tools.yaml --address 0.0.0.0 --port 5000
```

5. Start the API server:
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Chat Interface
```bash
POST /chat
{
  "message": "Schedule a meeting tomorrow at 3 PM",
  "session_id": "optional-session-id",
  "user_id": "00000000-0000-0000-0000-000000000001"
}
```

### Workflow Execution
```bash
POST /workflow/run
{
  "instruction": "Create a task to review budget, schedule time for it tomorrow, and save notes about Q1 spending",
  "user_id": "00000000-0000-0000-0000-000000000001"
}
```

## Example Usage

```bash
# Create a task
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Remind me to prepare slides for the presentation"}'

# Multi-step workflow
curl -X POST http://localhost:8080/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"instruction": "I have a meeting at 3 PM tomorrow, create a task to prepare the agenda, and search my notes for previous meeting outcomes"}'

# Semantic search
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What did we discuss about the budget last week?"}'
```

## Docker Deployment

Build and run the complete system:

```bash
# Build API container
docker build -f Dockerfile.txt -t productivity-api .

# Run with docker-compose (create docker-compose.yml for full stack)
docker run -p 8080:8080 --env-file .env productivity-api
```

## Project Structure

```
.
├── agents/              # Agent definitions
│   ├── root_agent.py    # Main orchestrator
│   ├── calendar_agent.py
│   ├── task_notes_agent.py
│   └── memory_agent.py
├── api/                 # FastAPI application
│   └── main.py
├── tools/               # MCP toolset configurations
│   └── mcp_toolsets.py
├── toolbox/             # MCP server configuration
│   └── tools.yaml       # Tool definitions and DB queries
├── sql/                 # Database schema
│   └── schema.sql
└── requirements.txt
```

## Features

- Multi-agent coordination with automatic workflow decomposition
- Semantic search using vector embeddings (text-embedding-005)
- Calendar management with conflict detection
- Task tracking with priority and status management
- Note-taking with automatic tagging and search
- RESTful API with session management
- Streaming responses for real-time interaction

## Development

Run tests (when implemented):
```bash
pytest tests/
```

Format code:
```bash
black agents/ api/ tools/
```

## License

MIT
