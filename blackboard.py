import time
from typing import List, Dict, Any, Optional

class Blackboard:
    """Shared in-memory message board for agent collaboration."""
    
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self._message_id = 0
    
    def post(self, sender: str, content: str) -> int:
        """Post a message to the blackboard."""
        self._message_id += 1
        message = {
            "id": self._message_id,
            "from": sender,
            "text": content,
            "timestamp": time.time()
        }
        self.messages.append(message)
        return self._message_id
    
    def get_last_messages(self, count: int = 1) -> List[Dict[str, Any]]:
        """Get the last N messages from the blackboard."""
        return self.messages[-count:] if self.messages else []
    
    def get_messages_since(self, message_id: int) -> List[Dict[str, Any]]:
        """Get all messages posted after the given message ID."""
        return [msg for msg in self.messages if msg["id"] > message_id]
    
    def get_all_messages(self) -> List[Dict[str, Any]]:
        """Get all messages from the blackboard."""
        return self.messages.copy()
