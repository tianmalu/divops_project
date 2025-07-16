# TarotAI Logger System

This document describes the logging system implementation for the TarotAI project.

## Overview

The TarotAI logging system provides structured logging across all modules with configurable log levels, file output, and environment-specific configurations.

## Quick Start

### Basic Usage

```python
from app.logger_config import get_tarot_logger

# Get a logger for your module
logger = get_tarot_logger(__name__)

# Log messages at different levels
logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical error")
```

### Configuration

Set environment variables to control logging behavior:

```bash
# Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export LOG_LEVEL=INFO

# Set log file path (optional)
export LOG_FILE="/path/to/logfile.log"

# Set environment (development, production, testing)
export TAROT_ENV=development
```

## Features

### 1. Automatic Log File Creation

- Logs are automatically written to `logs/tarot_ai_YYYYMMDD.log`
- Error logs are written to `logs/tarot_ai_errors.log`
- Log directory is created automatically if it doesn't exist

### 2. Environment-Specific Configuration

- **Development**: Verbose logging with detailed formatting
- **Production**: Minimal console output, comprehensive file logging
- **Testing**: Minimal logging to avoid test noise

### 3. Module-Specific Loggers

Each module gets its own logger instance:

```python
# In server.py
logger = get_tarot_logger(__name__)  # Creates "server.server" logger

# In app/rag_engine.py
logger = get_tarot_logger(__name__)  # Creates "app.rag_engine" logger
```

### 4. Structured Log Format

Default format includes:
- Timestamp
- Module name
- Log level
- Message

Example output:
```
2025-01-16 10:30:45 - app.rag_engine - INFO - Starting new discussion for user user123: Career Growth
2025-01-16 10:30:46 - app.rag_engine - DEBUG - Generated discussion ID: abc123-def456
```

## Implementation Details

### Logger Configuration Module (`app/logger_config.py`)

Main functions:
- `get_tarot_logger(name)`: Get a configured logger instance
- `setup_logger(name, level, log_file)`: Setup logger with custom configuration

### Configuration File (`config/logging_config.py`)

Provides environment-specific configurations:
- `DEFAULT_LOG_CONFIG`: Standard configuration
- `DEV_LOG_CONFIG`: Development environment
- `PROD_LOG_CONFIG`: Production environment
- `TEST_LOG_CONFIG`: Testing environment

## Usage Examples

### 1. In a Class

```python
from app.logger_config import get_tarot_logger

class TarotReader:
    def __init__(self):
        self.logger = get_tarot_logger(f"{__name__}.{self.__class__.__name__}")
    
    def read_cards(self, question):
        self.logger.info(f"Starting reading for: {question}")
        try:
            # ... reading logic ...
            self.logger.info("Reading completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Reading failed: {e}")
            raise
```

### 2. In a Function

```python
from app.logger_config import get_tarot_logger

def process_feedback(feedback_data):
    logger = get_tarot_logger(__name__)
    
    logger.info(f"Processing feedback from user {feedback_data['user_id']}")
    
    try:
        # ... processing logic ...
        logger.info("Feedback processed successfully")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Feedback processing failed: {e}")
        return {"status": "error", "message": str(e)}
```

### 3. In API Endpoints

```python
from app.logger_config import get_tarot_logger

logger = get_tarot_logger(__name__)

@app.post("genai/reading/enhanced")
async def get_enhanced_reading(reading_data: dict):
    logger.info("Enhanced reading request received")
    
    try:
        # ... processing logic ...
        logger.info("Enhanced reading generated successfully")
        return result
    except Exception as e:
        logger.error(f"Enhanced reading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| DEBUG | Detailed information for debugging |
| INFO | General information about program flow |
| WARNING | Something unexpected happened but program continues |
| ERROR | A serious problem occurred |
| CRITICAL | A very serious error occurred |

## Testing

Run the logger test script:

```bash
cd genai/tests
python test_logger.py
```

View usage examples:

```bash
cd genai/examples
python logger_usage_examples.py
```

## Best Practices

1. **Use appropriate log levels**: Don't log everything at INFO level
2. **Include context**: Log user IDs, request IDs, etc. for traceability
3. **Log exceptions**: Always log exceptions with stack traces
4. **Don't log sensitive data**: Avoid logging passwords, API keys, etc.
5. **Use structured logging**: Include relevant metadata in log messages

## Troubleshooting

### Common Issues

1. **Log files not created**: Check permissions and disk space
2. **Too verbose logging**: Adjust LOG_LEVEL environment variable
3. **Performance issues**: Use DEBUG level sparingly in production

### Log File Locations

Default log files are created in:
- `logs/tarot_ai_YYYYMMDD.log` - All logs
- `logs/tarot_ai_errors.log` - Error logs only

## Migration from Old Logging

Replace old logging patterns:

```python
# Old way
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# New way
from app.logger_config import get_tarot_logger
logger = get_tarot_logger(__name__)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level | INFO |
| `LOG_FILE` | Log file path | `logs/tarot_ai_YYYYMMDD.log` |
| `TAROT_ENV` | Environment (development/production/testing) | development |
