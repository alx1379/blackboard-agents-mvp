from typing import List, Dict, Any
from rich.console import Console
from blackboard import Blackboard

console = Console()

class Router:
    """Routes messages to agents based on configurable context window."""
    
    def __init__(self, blackboard: Blackboard, context_window: int = 1):
        self.blackboard = blackboard
        self.context_window = context_window
        self.last_processed_id = 0
    
    def get_context_for_agent(self) -> List[Dict[str, Any]]:
        """Get the last N messages for agent decision making."""
        return self.blackboard.get_last_messages(self.context_window)
    
    def has_new_messages(self) -> bool:
        """Check if there are new messages since last processing."""
        latest_messages = self.blackboard.get_messages_since(self.last_processed_id)
        return len(latest_messages) > 0
    
    def mark_processed(self):
        """Mark current messages as processed."""
        if self.blackboard.messages:
            self.last_processed_id = self.blackboard.messages[-1]["id"]
    
    def format_context(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for agent decision making."""
        if not messages:
            return "No messages available."
        
        formatted = []
        for msg in messages:
            formatted.append(f"{msg['from']}: {msg['text']}")
        
        return "\n".join(formatted)
