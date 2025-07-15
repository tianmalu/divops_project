# Logger Configuration for TarotAI
# This file contains different logging configurations for different environments

import os
from typing import Dict, Any

# Default logging configuration
DEFAULT_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format": "%(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/tarot_ai.log",
            "mode": "a"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "logs/tarot_ai_errors.log",
            "mode": "a"
        }
    },
    "loggers": {
        "tarot_ai": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "app": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "server": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console", "error_file"]
    }
}

# Development configuration - more verbose
DEV_LOG_CONFIG = {
    **DEFAULT_LOG_CONFIG,
    "handlers": {
        **DEFAULT_LOG_CONFIG["handlers"],
        "console": {
            **DEFAULT_LOG_CONFIG["handlers"]["console"],
            "level": "DEBUG",
            "formatter": "detailed"
        }
    },
    "loggers": {
        **DEFAULT_LOG_CONFIG["loggers"],
        "tarot_ai": {
            **DEFAULT_LOG_CONFIG["loggers"]["tarot_ai"],
            "level": "DEBUG"
        },
        "app": {
            **DEFAULT_LOG_CONFIG["loggers"]["app"],
            "level": "DEBUG"
        },
        "server": {
            **DEFAULT_LOG_CONFIG["loggers"]["server"],
            "level": "DEBUG"
        }
    }
}

# Production configuration - less verbose, more focus on errors
PROD_LOG_CONFIG = {
    **DEFAULT_LOG_CONFIG,
    "handlers": {
        **DEFAULT_LOG_CONFIG["handlers"],
        "console": {
            **DEFAULT_LOG_CONFIG["handlers"]["console"],
            "level": "WARNING",
            "formatter": "simple"
        }
    },
    "loggers": {
        **DEFAULT_LOG_CONFIG["loggers"],
        "tarot_ai": {
            **DEFAULT_LOG_CONFIG["loggers"]["tarot_ai"],
            "level": "INFO",
            "handlers": ["file", "error_file"]
        },
        "app": {
            **DEFAULT_LOG_CONFIG["loggers"]["app"],
            "level": "INFO",
            "handlers": ["file", "error_file"]
        },
        "server": {
            **DEFAULT_LOG_CONFIG["loggers"]["server"],
            "level": "INFO",
            "handlers": ["file", "error_file"]
        }
    }
}

# Testing configuration - minimal logging
TEST_LOG_CONFIG = {
    **DEFAULT_LOG_CONFIG,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "tarot_ai": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
        "app": {
            "level": "WARNING", 
            "handlers": ["console"],
            "propagate": False
        },
        "server": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        }
    }
}

def get_log_config() -> Dict[str, Any]:
    """
    Get logging configuration based on environment.
    
    Returns:
        Logging configuration dictionary
    """
    env = os.getenv("TAROT_ENV", "development").lower()
    
    config_map = {
        "development": DEV_LOG_CONFIG,
        "production": PROD_LOG_CONFIG,
        "testing": TEST_LOG_CONFIG
    }
    
    return config_map.get(env, DEFAULT_LOG_CONFIG)

# Environment-specific log levels
LOG_LEVELS = {
    "development": "DEBUG",
    "production": "INFO",
    "testing": "WARNING"
}

def get_log_level() -> str:
    """
    Get log level based on environment.
    
    Returns:
        Log level string
    """
    env = os.getenv("TAROT_ENV", "development").lower()
    return LOG_LEVELS.get(env, "INFO")
