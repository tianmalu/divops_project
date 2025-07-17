# TarotAI System Guide

## Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run the Application
```bash
# Start the server
uvicorn server.server:app --reload

# Or run with Docker
# Build the Docker image

docker build -t tarotai .
# Then run the container

docker run -p 8000:8000 tarotai
```

### 3. Basic Usage

```python
from app.logger_config import get_tarot_logger
from app.client_manager import get_weaviate_client

# Get logger
logger = get_tarot_logger(__name__)

# Get database client
client = get_weaviate_client()

# Use in your code
logger.info("Application started")
```

## System Architecture

### Server Layer

- **server/server.py**: Main FastAPI application with all API endpoints
- **server/schemas.py**: API request/response schemas and validation

### Core Application Layer

- **app/main.py**: Core business logic and standalone functions
- **app/rag_engine.py**: LLM integration and AI response generation
- **app/models.py**: Data models and Pydantic schemas
- **app/card_engine.py**: Tarot card drawing and layout algorithms
- **app/context_aware_reading.py**: Context-enhanced reading processing
- **app/feedback.py**: User feedback processing and storage
- **app/prompt_loader.py**: Template loading and prompt rendering

### Infrastructure Layer

- **app/weaviate_client.py**: Weaviate vector database connections
- **app/logger_config.py**: Centralized logging configuration

### Configuration Files

- **app/gemini_config.json**: Gemini AI model configuration
- **app/tarot_prompt_template.txt**: Base tarot reading prompt template
- **app/tarot_prompt_with_history_template.txt**: Conversation history prompt template
- **app/.env**: Environment variables and API keys

## API Endpoints

### System Endpoints

- `GET /genai/health` - Health check endpoint

### Core Endpoints

- `GET /genai/daily-reading` - Get daily tarot reading

### Discussion Management

- `POST /genai/discussion/start` - Start a new discussion
- `POST /genai/discussion/{discussion_id}/followup` - Add followup question to discussion
- `POST /genai/discussion/{discussion_id}/feedback` - Submit feedback for a discussion

### Feedback & Analytics

- `GET /genai/feedback/stats` - Get general feedback statistics
- `GET /genai/feedback/discussion/{discussion_id}` - Get feedback for specific discussion

## API Usage Examples

### Basic Tarot Reading

```bash
# Get daily reading
curl -X GET "http://localhost:8000/genai/daily-reading?user_id=user123"

```

### Discussion Flow

```bash
# Start a new discussion
curl -X POST "http://localhost:8000/genai/discussion/start" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "initial_question": "What does my future hold?",
  }'

# Add followup question
curl -X POST "http://localhost:8000/genai/discussion/{discussion_id}/followup" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can you tell me more about my career path?",
    "user_id": "user123"
  }'
```

## Configuration

### Environment Variables

```bash
# Required
WEAVIATE_URL=your_weaviate_url
WEAVIATE_API_KEY=your_weaviate_key
GEMINI_API_KEY=your_gemini_key
```

### Logging Levels

- DEBUG: Detailed debugging information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Testing

Run all tests:

```bash
python tests/test_all_systems.py
```

## Troubleshooting

### Common Issues

1. **Connection errors**: Check API keys and network
2. **Log file permissions**: Ensure logs/ directory is writable
3. **Import errors**: Verify Python path configuration

### Getting Help

- Check logs in `logs/tarot_ai_*.log`
- Run system tests to verify setup
- Review API documentation at `/docs`