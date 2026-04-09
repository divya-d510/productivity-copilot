.PHONY: help setup start stop test clean logs build deploy

help:
	@echo "Productivity Copilot - Available Commands:"
	@echo ""
	@echo "  make setup      - Initial setup (copy .env, install deps)"
	@echo "  make start      - Start all services with Docker Compose"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make test       - Run API tests"
	@echo "  make logs       - View logs from all services"
	@echo "  make logs-api   - View API logs only"
	@echo "  make logs-db    - View database logs only"
	@echo "  make clean      - Stop and remove all containers and volumes"
	@echo "  make build      - Rebuild all Docker images"
	@echo "  make shell-api  - Open shell in API container"
	@echo "  make shell-db   - Open psql shell in database"
	@echo "  make deploy     - Deploy to Google Cloud (requires gcloud setup)"
	@echo ""

setup:
	@echo "Setting up Productivity Copilot..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file - please edit with your settings"; fi
	@pip install -r requirements.txt
	@echo "Setup complete! Edit .env and run 'make start'"

start:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services starting... Wait 30 seconds for initialization"
	@echo "API will be available at http://localhost:8080"
	@echo "Run 'make logs' to view logs"

stop:
	@echo "Stopping all services..."
	docker-compose down

restart: stop start

test:
	@echo "Running API tests..."
	@sleep 2
	python test_api.py

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-toolbox:
	docker-compose logs -f toolbox

logs-db:
	docker-compose logs -f postgres

clean:
	@echo "Cleaning up all containers and volumes..."
	docker-compose down -v
	@echo "Cleanup complete"

build:
	@echo "Building Docker images..."
	docker-compose build --no-cache

shell-api:
	docker-compose exec api /bin/bash

shell-db:
	docker-compose exec postgres psql -U productivity_user -d productivity_db

health:
	@echo "Checking service health..."
	@curl -s http://localhost:8080/health | python -m json.tool || echo "API not responding"

dev:
	@echo "Starting in development mode..."
	python -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload

deploy:
	@echo "Deploying to Google Cloud..."
	@echo "See DEPLOYMENT.md for full instructions"
	@bash -c 'read -p "Have you configured gcloud and updated toolbox/tools.yaml? (y/n) " -n 1 -r; echo; [[ $$REPLY =~ ^[Yy]$$ ]]'
	@./scripts/deploy.sh

format:
	@echo "Formatting Python code..."
	black agents/ api/ tools/
	@echo "Code formatted"

lint:
	@echo "Linting Python code..."
	flake8 agents/ api/ tools/ --max-line-length=100
	@echo "Linting complete"
