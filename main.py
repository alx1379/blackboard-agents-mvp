#!/usr/bin/env python3
"""
Blackboard-Based LLM Agents MVP
A multi-agent system where agents collaborate through a shared blackboard.
"""

import time
import threading
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout

from config import Config
from blackboard import Blackboard
from router import Router
from agents import WriterAgent, EditorAgent, GrammarAgent

console = Console()

class BlackboardSystem:
    """Main system orchestrating the blackboard and agents."""
    
    def __init__(self, context_window: int = None):
        if context_window is None:
            context_window = Config.CONTEXT_WINDOW
        self.blackboard = Blackboard()
        self.router = Router(self.blackboard, context_window)
        
        # Initialize agents
        self.agents = [
            WriterAgent(self.blackboard),
            EditorAgent(self.blackboard),
            GrammarAgent(self.blackboard)
        ]
        
        self.running = False
        self.last_displayed_id = 0
    
    def display_new_messages(self):
        """Display new messages from the blackboard."""
        new_messages = self.blackboard.get_messages_since(self.last_displayed_id)
        
        for msg in new_messages:
            timestamp = time.strftime("%H:%M:%S", time.localtime(msg["timestamp"]))
            
            # Color code different senders
            if msg["from"] == "user":
                style = "bold blue"
            elif "agent" in msg["from"]:
                style = "bold green"
            else:
                style = "white"
            
            console.print(f"[{timestamp}] ", end="")
            console.print(f"{msg['from']}: ", style=style, end="")
            console.print(msg["text"])
            console.print()
        
        if new_messages:
            self.last_displayed_id = new_messages[-1]["id"]
    
    def agent_processing_loop(self):
        """Background loop for agent processing."""
        while self.running:
            if self.router.has_new_messages():
                # Let each agent try to act
                for agent in self.agents:
                    if self.running:  # Check if still running
                        agent.try_act()
                
                self.router.mark_processed()
                
                # Display any new messages
                self.display_new_messages()
            
            time.sleep(0.5)  # Small delay to prevent excessive polling
    
    def start(self):
        """Start the blackboard system."""
        self.running = True
        
        # Start agent processing in background thread
        agent_thread = threading.Thread(target=self.agent_processing_loop, daemon=True)
        agent_thread.start()
        
        console.print(Panel.fit(
            Text("🤖 Blackboard-Based LLM Agents MVP", style="bold cyan"),
            title="System Started"
        ))
        console.print("Type your requests below. Agents will collaborate to help you.")
        console.print("Type 'quit' or 'exit' to stop.\n")
        
        try:
            while self.running:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if user_input:
                    # Post user message to blackboard
                    self.blackboard.post("user", user_input)
                    self.display_new_messages()
        
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def stop(self):
        """Stop the blackboard system."""
        self.running = False
        console.print()
        console.print(Panel.fit("System stopped. Goodbye! 👋", style="bold red"))


def main():
    """Main entry point."""
    # Check for required configuration
    if not Config.validate():
        missing_vars = Config.get_missing_vars()
        console.print(Panel.fit(
            f"⚠️  Missing required environment variables: {', '.join(missing_vars)}",
            style="bold red"
        ))
        console.print("Copy .env.example to .env and set your values:")
        console.print("cp .env.example .env")
        return
    
    # Create and start the system
    system = BlackboardSystem()
    system.start()


if __name__ == "__main__":
    main()
