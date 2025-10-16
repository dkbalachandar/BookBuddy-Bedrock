#!/usr/bin/env python3
"""
Reset BookBuddy Agent - Delete and recreate completely
"""

import boto3
import time

def reset_bookbuddy():
    """Delete and recreate BookBuddy agent from scratch."""
    
    bedrock = boto3.client("bedrock-agent", region_name="us-east-1")
    agent_name = "BookBuddy"
    
    print("🔍 Looking for existing BookBuddy agent...")
    
    # Find existing agent
    agents_response = bedrock.list_agents()
    agents = agents_response.get("agentSummaries", [])
    existing_agent = next((a for a in agents if a['agentName'] == agent_name), None)
    
    if existing_agent:
        agent_id = existing_agent['agentId']
        print(f"🗑️ Found agent {agent_name} (ID: {agent_id}), deleting...")
        
        # Delete all aliases first
        try:
            aliases_response = bedrock.list_agent_aliases(agentId=agent_id)
            aliases = aliases_response.get("agentAliases", [])
            
            for alias in aliases:
                alias_id = alias['agentAliasId']
                alias_name = alias.get('agentAliasName', 'unknown')
                print(f"🗑️ Deleting alias: {alias_name}")
                try:
                    bedrock.delete_agent_alias(agentId=agent_id, agentAliasId=alias_id)
                    print(f"✅ Deleted alias: {alias_name}")
                except Exception as e:
                    print(f"⚠️ Error deleting alias {alias_name}: {e}")
            
            if aliases:
                print("⏳ Waiting for aliases to be deleted...")
                time.sleep(15)
                
        except Exception as e:
            print(f"⚠️ Error with aliases: {e}")
        
        # Now delete the agent
        try:
            bedrock.delete_agent(agentId=agent_id)
            print(f"✅ Agent {agent_name} deleted")
            print("⏳ Waiting for deletion to complete...")
            time.sleep(10)
        except Exception as e:
            print(f"❌ Error deleting agent: {e}")
            return False
    else:
        print("ℹ️ No existing agent found")
    
    print("✅ Agent reset complete. Now run: python3 bookbuddy.py")
    return True

if __name__ == "__main__":
    reset_bookbuddy()