#!/usr/bin/env python3
"""
BookBuddy Agent Management Script
Provides utilities to manage the BookBuddy agent
"""

import sys
from bookbuddy import BookBuddyAgent

def delete_agent():
    """Delete the BookBuddy agent."""
    config = {
        "agent_name": "BookBuddy",
        "foundation_model": "anthropic.claude-3-haiku-20240307-v1:0",
        "alias_name": "BookBuddy",
        "region": "us-east-1"
    }
    
    bookbuddy = BookBuddyAgent(**config)
    
    # Find existing agent
    agents_response = bookbuddy.bedrock.list_agents()
    agents = agents_response.get("agentSummaries", [])
    existing_agent = next((a for a in agents if a['agentName'] == config["agent_name"]), None)
    
    if existing_agent:
        agent_id = existing_agent['agentId']
        bookbuddy.delete_agent(agent_id)
        print("✅ Agent deleted successfully")
    else:
        print("❌ No agent found to delete")

def list_agents():
    """List all agents."""
    config = {"region": "us-east-1"}
    bookbuddy = BookBuddyAgent(**config)
    
    agents_response = bookbuddy.bedrock.list_agents()
    agents = agents_response.get("agentSummaries", [])
    
    print(f"Found {len(agents)} agents:")
    for agent in agents:
        print(f"  - {agent['agentName']} (ID: {agent['agentId']})")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 manage_agent.py delete    # Delete BookBuddy agent")
        print("  python3 manage_agent.py list      # List all agents")
        return
    
    command = sys.argv[1].lower()
    
    if command == "delete":
        delete_agent()
    elif command == "list":
        list_agents()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()