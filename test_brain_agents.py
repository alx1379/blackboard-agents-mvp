#!/usr/bin/env python3
"""
Test script for brain model agents
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from blackboard import Blackboard
from brain_agents import (
    CriticAgent, OpportunistAgent, RationalizerAgent, 
    OptimistAgent, PessimistAgent, DoerAgent, 
    LazyAgent, ProcrastinatorAgent, ConsensusAgent
)

def test_brain_agents():
    """Test that all brain agents can be instantiated and have proper attributes."""
    
    print("Testing Brain Model Agents...")
    
    # Check config
    if not Config.validate():
        print("❌ Missing required environment variables")
        missing = Config.get_missing_vars()
        print(f"Missing: {', '.join(missing)}")
        print("Copy .env.example to .env and set your API key")
        return False
    
    # Create blackboard
    blackboard = Blackboard()
    
    # Test each brain agent
    agents = [
        ("Critic", CriticAgent),
        ("Opportunist", OpportunistAgent), 
        ("Rationalizer", RationalizerAgent),
        ("Optimist", OptimistAgent),
        ("Pessimist", PessimistAgent),
        ("Doer", DoerAgent),
        ("Lazy", LazyAgent),
        ("Procrastinator", ProcrastinatorAgent),
        ("Consensus", ConsensusAgent)
    ]
    
    print(f"\n✅ Config validated - using {Config.LLM_PROVIDER}")
    print("✅ Blackboard created")
    
    for name, agent_class in agents:
        try:
            agent = agent_class(blackboard)
            print(f"✅ {name}Agent: {agent.goal[:50]}...")
        except Exception as e:
            print(f"❌ {name}Agent failed: {e}")
            return False
    
    print(f"\n🧠 All {len(agents)} brain model agents initialized successfully!")
    
    # Test a simple interaction
    print("\n--- Testing Simple Interaction ---")
    blackboard.post("user", "I need to decide whether to start a new business or keep my current job.")
    
    # Let a few agents respond
    test_agents = [
        CriticAgent(blackboard),
        OptimistAgent(blackboard), 
        PessimistAgent(blackboard),
        ConsensusAgent(blackboard)
    ]
    
    for agent in test_agents:
        try:
            agent.try_act()
            print(f"✅ {agent.name} processed the scenario")
        except Exception as e:
            print(f"❌ {agent.name} failed: {e}")
    
    # Show final messages
    messages = blackboard.get_all_messages()
    print(f"\n📝 Total messages on blackboard: {len(messages)}")
    
    for msg in messages[-5:]:  # Show last 5 messages
        print(f"  {msg['from']}: {msg['text'][:80]}...")
    
    return True

if __name__ == "__main__":
    success = test_brain_agents()
    sys.exit(0 if success else 1)
