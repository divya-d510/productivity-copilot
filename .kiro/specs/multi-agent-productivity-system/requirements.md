# Requirements Document

## Introduction

The Multi-Agent Productivity System is an AI-powered personal assistant that helps users manage tasks, calendar events, and notes through natural language interaction. The system uses a hierarchical multi-agent architecture where a root orchestrator coordinates specialized sub-agents, each with access to specific tools via the Model Context Protocol (MCP). The system stores structured data in a PostgreSQL database with vector embeddings for semantic search, and exposes functionality through a REST API.

## Glossary

- **Root_Agent**: The primary orchestrator agent that receives user requests and delegates to specialized sub-agents
- **Calendar_Agent**: Specialized agent responsible for managing calendar events and availability
- **Task_Notes_Agent**: Specialized agent responsible for managing tasks and notes
- **Memory_Agent**: Specialized agent responsible for semantic search across historical tasks and notes
- **MCP_Toolbox**: Model Context Protocol server that provides database-backed tools to agents
- **API_Server**: FastAPI REST service that exposes chat and workflow endpoints
- **Database**: PostgreSQL database storing users, tasks, calendar events, and notes with vector embeddings
- **Session**: A conversation context maintained across multiple user interactions
- **Workflow**: A multi-step operation spanning multiple agent domains
- **Embedding**: A 768-dimensional vector representation of text for semantic similarity search
- **User_ID**: UUID identifying a specific user in the system

## Requirements

### Requirement 1: Multi-Agent Orchestration

**User Story:** As a user, I want a single interface that intelligently routes my requests to specialized agents, so that I can manage different aspects of my productivity without knowing the system architecture.

#### Acceptance Criteria

1. THE Root_Agent SHALL coordinate Calendar_Agent, Task_Notes_Agent, and Memory_Agent
2. WHEN a user request involves a single domain, THE Root_Agent SHALL delegate to exactly one sub-agent
3. WHEN a user request involves multiple domains, THE Root_Agent SHALL execute a multi-step workflow by calling multiple sub-agents in sequence
4. THE Root_Agent SHALL consolidate responses from multiple sub-agents into a single structured response
5. FOR ALL agent delegations, the Root_Agent SHALL preserve the User_ID context
6. WHEN a sub-agent completes its task, THE Root_Agent SHALL receive the sub-agent response before proceeding

### Requirement 2: Calendar Management

**User Story:** As a user, I want to schedule events and check my availability, so that I can manage my time effectively.

#### Acceptance Criteria

1. WHEN a user requests to create an event with title, start time, and end time, THE Calendar_Agent SHALL create a calendar event in the Database
2. WHEN a user requests to list upcoming events, THE Calendar_Agent SHALL retrieve events within the specified number of days ahead
3. WHEN a user requests to check availability for a time slot, THE Calendar_Agent SHALL return whether conflicts exist and list any conflicting events
4. THE Calendar_Agent SHALL convert natural language time expressions to ISO 8601 format
5. WHEN an event end time is not specified, THE Calendar_Agent SHALL assume a one-hour duration
6. WHEN creating an event, THE Database SHALL enforce that end_time is greater than start_time
7. THE Calendar_Agent SHALL confirm event creation by returning the event title and time

### Requirement 3: Task Management

**User Story:** As a user, I want to create and track tasks with priorities and due dates, so that I can organize my work effectively.

#### Acceptance Criteria

1. WHEN a user requests to create a task, THE Task_Notes_Agent SHALL store the task with title, description, priority, and due_date in the Database
2. THE Task_Notes_Agent SHALL support priority values of low, medium, and high
3. THE Task_Notes_Agent SHALL support status values of pending, in_progress, done, and cancelled
4. WHEN priority is not specified, THE Task_Notes_Agent SHALL default to medium priority
5. WHEN a user requests to list tasks, THE Task_Notes_Agent SHALL retrieve tasks ordered by priority then due_date
6. WHEN a user requests to update task status, THE Task_Notes_Agent SHALL change the status and update the updated_at timestamp
7. WHEN a user requests to retrieve a specific task, THE Task_Notes_Agent SHALL return the task by its UUID
8. THE Task_Notes_Agent SHALL filter task lists by status when requested

### Requirement 4: Note Management

**User Story:** As a user, I want to save notes with tags, so that I can capture and organize information.

#### Acceptance Criteria

1. WHEN a user requests to create a note, THE Task_Notes_Agent SHALL store the note with title, content, and tags in the Database
2. THE Task_Notes_Agent SHALL parse comma-separated tag strings into an array
3. WHEN a user requests to list notes, THE Task_Notes_Agent SHALL retrieve the 10 most recent notes ordered by creation date
4. THE Database SHALL store note content as full text without length restrictions
5. THE Task_Notes_Agent SHALL confirm note creation by returning the note ID and title

### Requirement 5: Semantic Search

**User Story:** As a user, I want to search my past tasks and notes using natural language, so that I can find relevant information even when I don't remember exact keywords.

#### Acceptance Criteria

1. WHEN a user requests to search notes, THE Memory_Agent SHALL perform semantic search using vector similarity
2. WHEN a user requests to search tasks, THE Memory_Agent SHALL perform semantic search using vector similarity
3. THE Memory_Agent SHALL return results ordered by relevance score
4. THE Memory_Agent SHALL limit search results to the specified number or default to 5 results
5. WHEN no results match the query, THE Memory_Agent SHALL report that no results were found without inventing data
6. THE Database SHALL generate embeddings using the text-embedding-005 model for all tasks and notes
7. THE Database SHALL compute similarity using cosine distance between query embedding and stored embeddings

### Requirement 6: Vector Embedding Generation

**User Story:** As a system administrator, I want automatic embedding generation for searchable content, so that semantic search works without manual intervention.

#### Acceptance Criteria

1. WHEN a task is created, THE Database SHALL generate an embedding from the concatenation of title and description
2. WHEN a note is created, THE Database SHALL generate an embedding from the concatenation of title and content
3. THE Database SHALL store embeddings as 768-dimensional vectors
4. THE Database SHALL use the text-embedding-005 model for all embedding generation
5. THE Database SHALL create vector indexes for efficient similarity search

### Requirement 7: REST API Interface

**User Story:** As a client application, I want to interact with the system via HTTP endpoints, so that I can integrate the productivity system into various platforms.

#### Acceptance Criteria

1. THE API_Server SHALL expose a /health endpoint that returns service status
2. THE API_Server SHALL expose a /chat endpoint that accepts user messages and returns agent responses
3. THE API_Server SHALL expose a /workflow/run endpoint that executes multi-step workflows
4. WHEN a chat request includes a session_id, THE API_Server SHALL use the existing session
5. WHEN a chat request omits session_id, THE API_Server SHALL create a new session with a generated UUID
6. THE API_Server SHALL maintain conversation context within a session across multiple requests
7. THE API_Server SHALL return responses in JSON format with response text, session_id, and user_id
8. THE API_Server SHALL enable CORS for cross-origin requests

### Requirement 8: Session Management

**User Story:** As a user, I want my conversation context preserved across multiple interactions, so that I can have natural multi-turn conversations.

#### Acceptance Criteria

1. THE API_Server SHALL create a unique session for each new conversation
2. THE API_Server SHALL store session state in memory during the session lifecycle
3. WHEN a request includes an existing session_id, THE API_Server SHALL retrieve the session context
4. THE API_Server SHALL pass session context to the Root_Agent for all interactions
5. THE API_Server SHALL generate session_id values as UUIDs
6. WHEN session creation fails due to duplicate session_id, THE API_Server SHALL continue with the existing session

### Requirement 9: Multi-Step Workflow Execution

**User Story:** As a user, I want to issue complex requests that span multiple domains in a single command, so that I can accomplish related tasks efficiently.

#### Acceptance Criteria

1. WHEN a workflow request spans multiple domains, THE Root_Agent SHALL identify all required sub-agents
2. THE Root_Agent SHALL execute sub-agent calls in logical order based on dependencies
3. THE Root_Agent SHALL collect all sub-agent responses before generating the final response
4. THE API_Server SHALL return workflow results including the list of agents involved and the consolidated response
5. THE Root_Agent SHALL acknowledge multi-step workflows in its response
6. THE Root_Agent SHALL provide a summary of all actions taken across agents

### Requirement 10: Tool Access Control

**User Story:** As a system architect, I want agents to access only the tools they need, so that the system follows the principle of least privilege.

#### Acceptance Criteria

1. THE Calendar_Agent SHALL have access only to calendar-tools toolset
2. THE Task_Notes_Agent SHALL have access only to task-tools and notes-tools toolsets
3. THE Memory_Agent SHALL have access only to semantic-search toolset
4. THE Root_Agent SHALL NOT have direct access to MCP tools
5. THE MCP_Toolbox SHALL filter tools by toolset name when agents connect
6. WHEN an agent requests a tool outside its assigned toolsets, THE MCP_Toolbox SHALL deny access

### Requirement 11: Database Schema and Constraints

**User Story:** As a system administrator, I want data integrity enforced at the database level, so that invalid data cannot be stored.

#### Acceptance Criteria

1. THE Database SHALL enforce that task status values are one of: pending, in_progress, done, cancelled
2. THE Database SHALL enforce that task priority values are one of: low, medium, high
3. THE Database SHALL enforce that calendar event end_time is greater than start_time
4. THE Database SHALL generate UUIDs for all primary keys
5. THE Database SHALL set created_at and updated_at timestamps automatically
6. THE Database SHALL create indexes on user_id, status, due_date, start_time, and tags columns
7. THE Database SHALL support multi-user isolation by user_id

### Requirement 12: MCP Tool Integration

**User Story:** As a developer, I want tools defined declaratively in YAML, so that I can add new capabilities without modifying agent code.

#### Acceptance Criteria

1. THE MCP_Toolbox SHALL load tool definitions from a YAML configuration file
2. THE MCP_Toolbox SHALL expose tools via HTTP at the /mcp endpoint
3. WHEN an agent calls a tool, THE MCP_Toolbox SHALL execute the corresponding SQL statement with provided parameters
4. THE MCP_Toolbox SHALL return tool results as structured JSON
5. THE MCP_Toolbox SHALL support postgres-sql tool kind for database operations
6. THE MCP_Toolbox SHALL validate tool parameters against the schema before execution
7. THE MCP_Toolbox SHALL organize tools into named toolsets for access control

### Requirement 13: Natural Language Time Parsing

**User Story:** As a user, I want to specify times in natural language, so that I don't need to format dates manually.

#### Acceptance Criteria

1. WHEN a user specifies "tomorrow at 3 PM", THE Calendar_Agent SHALL convert it to the next day at 15:00:00 in ISO 8601 format
2. WHEN a user specifies "today", THE Calendar_Agent SHALL use the current date
3. WHEN a user specifies a relative time like "in 2 days", THE Calendar_Agent SHALL calculate the absolute datetime
4. THE Calendar_Agent SHALL preserve timezone information in ISO 8601 format
5. WHEN time parsing is ambiguous, THE Calendar_Agent SHALL make reasonable assumptions and confirm with the user

### Requirement 14: Error Handling and Validation

**User Story:** As a user, I want clear error messages when something goes wrong, so that I can correct my requests.

#### Acceptance Criteria

1. WHEN a required parameter is missing, THE agent SHALL return an error message indicating which parameter is required
2. WHEN a database operation fails, THE API_Server SHALL return an HTTP error status with a descriptive message
3. WHEN an invalid status or priority value is provided, THE Database SHALL reject the operation
4. WHEN a time range is invalid, THE Database SHALL reject the calendar event creation
5. WHEN a tool call fails, THE agent SHALL report the failure to the Root_Agent
6. THE API_Server SHALL log all errors for debugging purposes

### Requirement 15: Data Serialization and Parsing

**User Story:** As a developer, I want consistent data formats between API requests and database storage, so that data integrity is maintained.

#### Acceptance Criteria

1. THE API_Server SHALL parse JSON request bodies into structured objects
2. THE API_Server SHALL serialize agent responses into JSON format
3. THE MCP_Toolbox SHALL convert SQL query results into JSON arrays
4. THE Database SHALL store timestamps in UTC timezone
5. THE Database SHALL store UUIDs in standard format
6. WHEN converting between formats, THE system SHALL preserve data precision and type information
7. FOR ALL valid API requests, parsing the request then serializing the response then parsing again SHALL produce equivalent data (round-trip property)

### Requirement 16: Deployment and Configuration

**User Story:** As a DevOps engineer, I want the system deployable via containers, so that I can run it consistently across environments.

#### Acceptance Criteria

1. THE API_Server SHALL read configuration from environment variables
2. THE API_Server SHALL support deployment as a Docker container
3. THE MCP_Toolbox SHALL support deployment as a Docker container
4. THE system SHALL provide a docker-compose configuration for local development
5. THE API_Server SHALL expose health check endpoint for container orchestration
6. THE system SHALL support configuration of database connection parameters via environment variables
7. THE system SHALL support configuration of Google Cloud project and location via environment variables

### Requirement 17: Multi-User Support

**User Story:** As a system administrator, I want the system to support multiple users with data isolation, so that users cannot access each other's data.

#### Acceptance Criteria

1. THE Database SHALL store a user_id with every task, event, and note
2. WHEN listing or searching data, THE agents SHALL filter by the requesting user's user_id
3. THE API_Server SHALL accept user_id in all requests
4. THE Database SHALL create a users table with unique email addresses
5. THE agents SHALL pass user_id to all tool calls
6. WHEN user_id is not provided, THE API_Server SHALL use a configured default demo user

### Requirement 18: Response Formatting

**User Story:** As a user, I want responses formatted clearly with appropriate structure, so that I can easily understand the results.

#### Acceptance Criteria

1. WHEN listing multiple items, THE agents SHALL use bullet points or numbered lists
2. WHEN returning multi-step workflow results, THE Root_Agent SHALL use section headers for each domain
3. THE agents SHALL confirm actions taken by summarizing what was created or retrieved
4. THE agents SHALL keep responses concise and avoid unnecessary verbosity
5. WHEN no results are found, THE agents SHALL clearly state that nothing was found
6. THE agents SHALL present task lists grouped by priority

### Requirement 19: Conflict Detection

**User Story:** As a user, I want to know if a time slot has scheduling conflicts, so that I can avoid double-booking.

#### Acceptance Criteria

1. WHEN checking availability, THE Calendar_Agent SHALL query for overlapping events using time range intersection
2. THE Calendar_Agent SHALL return the count of conflicting events
3. WHEN conflicts exist, THE Calendar_Agent SHALL return the titles of conflicting events
4. THE Database SHALL use range types for efficient time overlap queries
5. THE Calendar_Agent SHALL clearly state whether a time slot is free or has conflicts

### Requirement 20: Semantic Search Relevance

**User Story:** As a user, I want search results ranked by relevance, so that the most pertinent information appears first.

#### Acceptance Criteria

1. THE Memory_Agent SHALL compute relevance scores as 1 minus cosine distance
2. THE Memory_Agent SHALL order results by relevance score in descending order
3. THE Memory_Agent SHALL include relevance scores in search results
4. THE Memory_Agent SHALL explain why results match the query when presenting them
5. WHEN multiple results have similar relevance, THE Memory_Agent SHALL return all within the specified limit
