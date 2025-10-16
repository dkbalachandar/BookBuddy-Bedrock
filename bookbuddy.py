#!/usr/bin/env python3
"""
BookBuddy - AI Reading Companion
A Bedrock Agent that recommends books based on user preferences.
"""

import boto3
import json
import time
import re
from typing import Optional, Dict, Any


class BookBuddyAgent:
    """Manages the BookBuddy Bedrock Agent lifecycle and interactions."""
    
    def __init__(self, 
                 agent_name: str = "BookBuddy",
                 foundation_model: str = "anthropic.claude-3-haiku-20240307-v1:0",
                 alias_name: str = "BookBuddy",
                 region: str = "us-east-1"):
        
        self.agent_name = agent_name
        self.foundation_model = foundation_model
        self.alias_name = alias_name
        self.region = region
        
        # Initialize AWS clients
        self.bedrock = boto3.client("bedrock-agent", region_name=region)
        self.runtime = boto3.client("bedrock-agent-runtime", region_name=region)
        self.iam = boto3.client("iam")
        
        # Agent properties
        self.agent_id: Optional[str] = None
        self.alias_id: Optional[str] = None
        self.role_arn: Optional[str] = None
        
        self.instruction = """You are BookBuddy. Your ONLY job is to recommend specific books with purchase links.

CRITICAL RULES:
1. When someone asks for books, immediately recommend 2-3 specific books
2. ALWAYS include: Book Title, Author, brief description, and Amazon purchase link
3. If user requests summaries, include a brief plot/content summary for each book
4. Do NOT ask questions back - just give book recommendations
5. IMPORTANT: Amazon links must ONLY contain book title and author
   Format: https://amazon.com/s?k=TITLE+AUTHOR (replace spaces with +)
   Example: https://amazon.com/s?k=Atomic+Habits+James+Clear
   Do NOT include any other text in the URL

EXAMPLE FORMAT:
User: "motivational books"
You: "Here are great motivational books:

📚 **Think and Grow Rich** by Napoleon Hill
Classic success mindset book with timeless principles
🛒 Buy: https://amazon.com/s?k=Think+and+Grow+Rich+Napoleon+Hill

📚 **The Power of Now** by Eckhart Tolle  
Mindfulness and present-moment awareness guide
🛒 Buy: https://amazon.com/s?k=The+Power+of+Now+Eckhart+Tolle"

SUMMARY FORMAT (when requested):
When user asks for summaries, format each book like this:

� **[TITLE]** by [AUTHOR]
[Brief description]

� *i*What it's about:**
[2-3 sentences about the book's plot, main themes, or key content]

🛒 Buy: https://amazon.com/s?k=[TITLE]+[AUTHOR]

EXAMPLE WITH SUMMARY:
📚 **The Alchemist** by Paulo Coelho
Inspirational novel about following your dreams

📖 **What it's about:**
A young shepherd boy travels from Spain to Egypt in search of treasure, learning that the real treasure lies in following one's personal legend and listening to one's heart. The story explores themes of destiny, courage, and the importance of pursuing your dreams.

🛒 Buy: https://amazon.com/s?k=The+Alchemist+Paulo+Coelho

You are BookBuddy, not Amazon Titan. Just recommend books with purchase links."""

    def verify_model_access(self) -> bool:
        """Verify that the foundation model is available and accessible."""
        print(f"🔍 Checking model access for {self.foundation_model}...")
        
        try:
            # Check if model is listed
            bedrock_client = boto3.client("bedrock", region_name=self.region)
            models = bedrock_client.list_foundation_models()
            available_models = [model['modelId'] for model in models['modelSummaries']]
            
            if self.foundation_model not in available_models:
                print(f"❌ Model {self.foundation_model} is not available")
                return False
            
            # Test model access
            bedrock_runtime = boto3.client("bedrock-runtime", region_name=self.region)
            
            if "anthropic" in self.foundation_model:
                body = json.dumps({
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "anthropic_version": "bedrock-2023-05-31"
                })
            else:  # Titan or other models
                body = json.dumps({
                    "inputText": "Hi",
                    "textGenerationConfig": {"maxTokenCount": 10, "temperature": 0.1}
                })
            
            bedrock_runtime.invoke_model(modelId=self.foundation_model, body=body)
            print(f"✅ Model {self.foundation_model} is accessible")
            return True
            
        except Exception as e:
            print(f"❌ Model access failed: {e}")
            print("\n💡 Enable model access in Bedrock console:")
            print("1. Go to https://console.aws.amazon.com/bedrock/")
            print("2. Click 'Model access' → 'Manage model access'")
            print(f"3. Enable '{self.foundation_model}'")
            return False

    def ensure_iam_role(self) -> str:
        """Create or get the IAM role for the Bedrock agent."""
        role_name = f"{self.agent_name}-Role"
        
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "bedrock.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        
        try:
            # Try to create the role
            role_response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=f"IAM role for Bedrock agent {self.agent_name}"
            )
            role_arn = role_response['Role']['Arn']
            print(f"✅ Created IAM role: {role_arn}")
            
            # Attach necessary policies
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
            )
            time.sleep(5)  # Wait for propagation
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            # Role already exists
            role_response = self.iam.get_role(RoleName=role_name)
            role_arn = role_response['Role']['Arn']
            print(f"✅ Using existing IAM role: {role_arn}")
        
        return role_arn

    def setup_agent(self) -> tuple[str, bool]:
        """Create or update the Bedrock agent."""
        # Check for existing agent
        agents_response = self.bedrock.list_agents()
        agents = agents_response.get("agentSummaries", [])
        existing_agent = next((a for a in agents if a['agentName'] == self.agent_name), None)
        
        if existing_agent:
            agent_id = existing_agent['agentId']
            print(f"✅ Found existing agent: {self.agent_name} (ID: {agent_id})")
            
            # Check if update is needed
            agent_details = self.bedrock.get_agent(agentId=agent_id)
            current_model = agent_details['agent'].get('foundationModel')
            current_role = agent_details['agent'].get('agentResourceRoleArn')
            current_instruction = agent_details['agent'].get('instruction', '')
            
            needs_update = False
            changes = []
            
            if current_model != self.foundation_model:
                needs_update = True
                changes.append(f"Model: {current_model} → {self.foundation_model}")
            
            if not current_role:
                needs_update = True
                changes.append("Missing IAM role")
            
            if current_instruction.strip() != self.instruction.strip():
                needs_update = True
                changes.append("Instruction updated")
            
            if needs_update:
                print(f"🔧 Updating agent - Changes: {', '.join(changes)}")
                
                if not current_role:
                    self.role_arn = self.ensure_iam_role()
                else:
                    self.role_arn = current_role
                
                print("📝 Applying new instruction...")
                self.bedrock.update_agent(
                    agentId=agent_id,
                    agentName=self.agent_name,
                    foundationModel=self.foundation_model,
                    agentResourceRoleArn=self.role_arn,
                    instruction=self.instruction
                )
                print("✅ Agent updated with new configuration")
                
                # Wait for update to propagate
                print("⏳ Waiting for update to propagate...")
                time.sleep(3)
                
                return agent_id, True  # Return that update happened
            else:
                self.role_arn = current_role
                print("✅ Agent is up to date")
                return agent_id, False  # No update needed
        else:
            # Create new agent
            print(f"🔧 Creating new agent: {self.agent_name}")
            self.role_arn = self.ensure_iam_role()
            
            agent = self.bedrock.create_agent(
                agentName=self.agent_name,
                foundationModel=self.foundation_model,
                agentResourceRoleArn=self.role_arn,
                instruction=self.instruction
            )
            agent_id = agent["agent"]["agentId"]
            print(f"✅ Agent created: {agent_id}")
        
        return agent_id, True  # New agent created

    def prepare_agent(self, agent_id: str) -> None:
        """Prepare the agent for use."""
        print("🔧 Preparing agent...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.bedrock.prepare_agent(agentId=agent_id)
                print("✅ Agent prepared successfully")
                time.sleep(3)
                
                # Verify agent status
                agent_details = self.bedrock.get_agent(agentId=agent_id)
                status = agent_details['agent'].get('agentStatus')
                
                if status == 'PREPARED':
                    print("✅ Agent is ready")
                    break
                elif status == 'PREPARING':
                    print("⏳ Agent still preparing...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ Preparation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    raise

    def setup_alias(self, agent_id: str) -> str:
        """Create or find the agent alias."""
        print(f"🔧 Setting up alias: {self.alias_name}")
        
        # Check existing aliases first
        try:
            aliases_response = self.bedrock.list_agent_aliases(agentId=agent_id)
            aliases = aliases_response.get("agentAliases", [])
            
            print(f"📋 Found {len(aliases)} existing aliases for this agent")
            
            # Look for existing alias
            for alias in aliases:
                if alias.get('agentAliasName') == self.alias_name:
                    alias_id = alias['agentAliasId']
                    print(f"✅ Using existing alias: {self.alias_name} (ID: {alias_id})")
                    return alias_id
            
            # No existing alias found, try to create new one
            print(f"🆕 Creating new alias: {self.alias_name}")
            alias = self.bedrock.create_agent_alias(
                agentId=agent_id,
                agentAliasName=self.alias_name
            )
            alias_id = alias["agentAlias"]["agentAliasId"]
            print(f"✅ Created new alias: {self.alias_name} (ID: {alias_id})")
            return alias_id
            
        except Exception as e:
            if "ConflictException" in str(e) and "already exists" in str(e):
                # Extract alias ID from error message
                alias_id_match = re.search(r'id:\s*([A-Z0-9]+)', str(e))
                if alias_id_match:
                    alias_id = alias_id_match.group(1)
                    print(f"✅ Found existing alias: {self.alias_name} (ID: {alias_id})")
                    return alias_id
            raise

    def initialize(self) -> bool:
        """Initialize the complete BookBuddy agent setup."""
        try:
            print(f"🚀 Initializing BookBuddy Agent...")
            print(f"Region: {self.region}")
            print(f"Model: {self.foundation_model}")
            
            # Step 1: Verify model access
            if not self.verify_model_access():
                return False
            
            # Step 2: Setup agent
            self.agent_id, agent_updated = self.setup_agent()
            
            # Step 3: Prepare agent (always prepare if updated)
            if agent_updated:
                print("🔄 Agent was updated, forcing re-preparation...")
                time.sleep(5)  # Wait longer for update to propagate
                
                # Force re-preparation by checking status first
                try:
                    agent_details = self.bedrock.get_agent(agentId=self.agent_id)
                    current_status = agent_details['agent'].get('agentStatus')
                    print(f"Current agent status: {current_status}")
                except Exception as e:
                    print(f"Could not check agent status: {e}")
                    
            self.prepare_agent(self.agent_id)
            
            # Step 4: Setup alias
            self.alias_id = self.setup_alias(self.agent_id)
            
            print("🎉 BookBuddy is ready!")
            
            # Quick test to verify the agent is working properly
            print("🧪 Testing agent response...")
            try:
                test_response = self.chat("Test: recommend one motivational book", "test-session")
                if test_response and not test_response.startswith("❌") and ("book" in test_response.lower() or "recommend" in test_response.lower()):
                    print("✅ Agent test passed - responding appropriately")
                else:
                    print(f"⚠️ Agent test response: {test_response[:200]}...")
            except Exception as test_error:
                print(f"⚠️ Agent test failed: {test_error}")
            
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False

    def generate_amazon_url(self, title: str, author: str) -> str:
        """Generate Amazon search URL for a book."""
        import re
        
        # Clean title and author
        title = title.strip().strip('"').strip("'").strip()
        author = author.strip().strip('"').strip("'").strip()
        
        # Remove unwanted characters and format for URL
        search_query = f"{title} {author}"
        # Remove special characters that might cause issues
        search_query = re.sub(r'[^\w\s]', '', search_query)
        # Replace spaces with +
        search_query = search_query.replace(" ", "+")
        # Remove multiple + signs
        search_query = re.sub(r'\++', '+', search_query)
        # Remove leading/trailing +
        search_query = search_query.strip('+')
        
        return f"https://amazon.com/s?k={search_query}"

    def enhance_response_with_links(self, response: str) -> str:
        """Enhance response by ensuring Amazon links are properly formatted."""
        import re
        
        # Look for book patterns and ensure they have proper Amazon links
        # This is a backup in case the AI doesn't include links
        book_pattern = r'([*]{0,2})([^*\n]+?)([*]{0,2})\s+by\s+([^-–\n]+?)(?:\s*[-–]\s*([^\n]+?))?(?:\n|$)'
        
        def add_amazon_link(match):
            title = match.group(2).strip()
            author = match.group(4).strip().rstrip('-–').strip()  # Remove trailing dashes
            description = match.group(5) if match.group(5) else ""
            
            # Clean title and author of any unwanted characters
            title = title.strip().strip('-–').strip()
            author = author.strip().strip('-–').strip()
            
            amazon_url = self.generate_amazon_url(title, author)
            
            result = f"📚 **{title}** by {author}"
            if description:
                result += f"\n{description}"
            result += f"\n🛒 Buy: {amazon_url}\n"
            
            return result
        
        # Only enhance if no Amazon links are already present
        if "amazon.com" not in response.lower():
            enhanced = re.sub(book_pattern, add_amazon_link, response, flags=re.MULTILINE)
            return enhanced
        
        return response

    def chat(self, user_input: str, session_id: str = "demo-session", include_summary: bool = False) -> str:
        """Send a message to BookBuddy and get response."""
        try:
            # Modify the input to request summary if needed
            if include_summary:
                modified_input = f"{user_input}. IMPORTANT: For each book, after the description, add a section that starts with '📖 What it's about:' followed by 2-3 sentences explaining the book's main content, plot, or key themes."
            else:
                modified_input = user_input
                
            print(f"🔍 Sending to agent: {modified_input[:100]}..." if len(modified_input) > 100 else f"🔍 Sending to agent: {modified_input}")
                
            response = self.runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.alias_id,
                sessionId=session_id,
                inputText=modified_input
            )
            
            # Collect and clean response
            output_text = ""
            for event in response.get("completion", []):
                if "chunk" in event:
                    output_text += event["chunk"]["bytes"].decode("utf-8")
            
            # Clean up the response - remove unwanted prefixes and duplicates
            cleaned_output = output_text.strip()
            
            # Remove prefixes from the beginning
            prefixes_to_remove = ["Bot:", "Assistant:", "AI:", "BookBuddy:", "Human:", "User:"]
            for prefix in prefixes_to_remove:
                if cleaned_output.startswith(prefix):
                    cleaned_output = cleaned_output[len(prefix):].strip()
                    break
            
            # Remove "Bot:" that appears in the middle of responses
            import re
            cleaned_output = re.sub(r'\n\s*Bot:\s*', '\n', cleaned_output)
            cleaned_output = re.sub(r'\s+Bot:\s*', ' ', cleaned_output)
            
            # Clean up extra whitespace
            cleaned_output = re.sub(r'\n\s*\n', '\n\n', cleaned_output)
            cleaned_output = cleaned_output.strip()
            
            # Enhance with Amazon links if needed
            enhanced_output = self.enhance_response_with_links(cleaned_output)
            
            return enhanced_output
            
        except Exception as e:
            return f"❌ Error: {e}"

    def start_interactive_chat(self) -> None:
        """Start an interactive chat session with BookBuddy."""
        print("\n💡 Ask BookBuddy for book recommendations! Type 'exit' to quit.\n")
        
        session_id = f"session-{int(time.time())}"
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Goodbye! Happy reading!")
                    break
                
                if not user_input:
                    continue
                
                # Check if user wants summary
                include_summary = user_input.lower().endswith(" with summary") or user_input.lower().endswith(" summary")
                if include_summary:
                    user_input = user_input.replace(" with summary", "").replace(" summary", "")
                
                response = self.chat(user_input, session_id, include_summary=include_summary)
                print(f"BookBuddy: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Happy reading!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break


def main():
    """Main function to run BookBuddy."""
    import sys
    
    # Check for verbose flag
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    if verbose:
        print("🔍 Verbose mode enabled")
    
    # Configuration
    config = {
        "agent_name": "BookBuddy",  # Clean name
        "foundation_model": "anthropic.claude-3-haiku-20240307-v1:0",  # Fast, cost-effective
        "alias_name": "BookBuddy",
        "region": "us-east-1"
    }
    
    # Initialize BookBuddy
    bookbuddy = BookBuddyAgent(**config)
    
    if bookbuddy.initialize():
        bookbuddy.start_interactive_chat()
    else:
        print("❌ Failed to initialize BookBuddy. Please check the error messages above.")


if __name__ == "__main__":
    main()