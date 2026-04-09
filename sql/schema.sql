-- Productivity Copilot Database Schema
-- For production: Use AlloyDB with AI extensions for vector embeddings
-- For local dev: Uses pgvector extension

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- For AlloyDB (production):
-- CREATE EXTENSION IF NOT EXISTS "google_ml_integration";

-- For local development with pgvector:
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table (optional - for multi-user support)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks table with vector embeddings for semantic search
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT DEFAULT '',
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'done', 'cancelled')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMPTZ,
    embedding vector(768),  -- Optional: for semantic search with AlloyDB or pgvector
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
-- Uncomment for vector search:
-- CREATE INDEX idx_tasks_embedding ON tasks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Calendar events table
CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT DEFAULT '',
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    location VARCHAR(500) DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_time_range CHECK (end_time > start_time)
);

CREATE INDEX idx_calendar_user_id ON calendar_events(user_id);
CREATE INDEX idx_calendar_start_time ON calendar_events(start_time);
CREATE INDEX idx_calendar_time_range ON calendar_events USING gist (tstzrange(start_time, end_time));

-- Notes table with vector embeddings for semantic search
CREATE TABLE IF NOT EXISTS notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    embedding vector(768),  -- Optional: for semantic search with AlloyDB or pgvector
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_tags ON notes USING gin(tags);
CREATE INDEX idx_notes_created_at ON notes(created_at DESC);
-- Uncomment for vector search:
-- CREATE INDEX idx_notes_embedding ON notes USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Insert demo user
INSERT INTO users (id, email, name) 
VALUES ('00000000-0000-0000-0000-000000000001', 'demo@example.com', 'Demo User')
ON CONFLICT (id) DO NOTHING;

-- Sample data for testing
INSERT INTO tasks (user_id, title, description, priority, due_date)
VALUES 
    ('00000000-0000-0000-0000-000000000001', 
     'Review Q1 budget report', 
     'Analyze spending patterns and prepare summary for leadership team',
     'high',
     NOW() + INTERVAL '2 days')
ON CONFLICT DO NOTHING;

INSERT INTO notes (user_id, title, content, tags)
VALUES 
    ('00000000-0000-0000-0000-000000000001',
     'Team standup notes - April 5',
     'Discussed sprint progress. Backend API is 80% complete. Frontend team blocked on design assets. Need to follow up with design team by EOD.',
     ARRAY['meeting', 'standup', 'team'])
ON CONFLICT DO NOTHING;

INSERT INTO calendar_events (user_id, title, description, start_time, end_time, location)
VALUES 
    ('00000000-0000-0000-0000-000000000001',
     'Weekly team sync',
     'Regular team synchronization meeting',
     NOW() + INTERVAL '1 day',
     NOW() + INTERVAL '1 day' + INTERVAL '1 hour',
     'Conference Room A')
ON CONFLICT DO NOTHING;
