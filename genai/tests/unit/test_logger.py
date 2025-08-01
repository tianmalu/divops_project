#!/usr/bin/env python3
"""
Simple test script to verify logger configuration is working.
"""

import sys
import os
import unittest

# Add the genai directory to the path (go up two levels from tests/unit/ to genai/)
genai_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, genai_root)

from app.logger_config import get_tarot_logger

def test_logger():
    """Test logger functionality"""
    logger = get_tarot_logger(__name__)
    
    print("Testing TarotAI Logger Configuration")
    print("=" * 50)
    
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    
    print("\nLogger test completed! Check the log file for messages.")
    
    # Test with different modules
    rag_logger = get_tarot_logger("app.rag_engine")
    rag_logger.info("Test message from rag_engine module")
    
    feedback_logger = get_tarot_logger("app.feedback")
    feedback_logger.info("Test message from feedback module")
    
    server_logger = get_tarot_logger("server.server")
    server_logger.info("Test message from server module")

class TestLogger(unittest.TestCase):
    def test_logger_basic(self):
        import logging
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.DEBUG)
        with self.assertLogs(logger, level="DEBUG") as cm:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
        self.assertTrue(any("Debug message" in msg for msg in cm.output))
        self.assertTrue(any("Info message" in msg for msg in cm.output))
        self.assertTrue(any("Warning message" in msg for msg in cm.output))
        self.assertTrue(any("Error message" in msg for msg in cm.output))

if __name__ == "__main__":
    test_logger()
    unittest.main()
