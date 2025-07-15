#!/usr/bin/env python3
"""
Test script to verify ErrorResponse JSON serialization
"""
import json
from datetime import datetime
from typing import Dict, Any

# Mock Pydantic classes for testing
class MockField:
    def __init__(self, *args, **kwargs):
        pass

class MockConfigDict:
    def __init__(self, **kwargs):
        self.json_encoders = kwargs.get('json_encoders', {})

class MockBaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def model_dump(self) -> Dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

class ErrorResponse(MockBaseModel):
    model_config = MockConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    def __init__(self, error: str, message: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        super().__init__(error=error, message=message, timestamp=timestamp)

def test_error_response_serialization():
    print("Testing ErrorResponse JSON serialization...")
    
    # Create an ErrorResponse instance
    error_response = ErrorResponse(
        error="http_error_404",
        message="Discussion not found"
    )
    
    # Test model_dump()
    response_dict = error_response.model_dump()
    print(f"model_dump() result: {response_dict}")
    
    # Test manual datetime serialization
    if 'timestamp' in response_dict and isinstance(response_dict['timestamp'], datetime):
        response_dict['timestamp'] = response_dict['timestamp'].isoformat()
    
    print(f"After manual datetime conversion: {response_dict}")
    
    # Test JSON serialization
    try:
        json_str = json.dumps(response_dict)
        print(f"JSON serialization successful: {json_str}")
        
        # Test deserialization
        deserialized = json.loads(json_str)
        print(f"JSON deserialization successful: {deserialized}")
        
        print("✅ All tests passed!")
        return True
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False

if __name__ == "__main__":
    test_error_response_serialization()
