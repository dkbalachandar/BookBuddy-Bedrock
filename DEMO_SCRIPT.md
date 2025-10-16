# BookBuddy Demo Script for AWS Hackathon

## Demo Flow (3-4 minutes max)

### Opening (30 seconds)
"Hi! I'm presenting BookBuddy, an AI reading companion built on AWS Bedrock Agents that provides personalized book recommendations with direct Amazon purchase links."

### Problem Statement (30 seconds)
"Finding the right book to read can be overwhelming with millions of options. People need personalized recommendations based on their mood, interests, or specific needs, along with easy access to purchase."

### Solution Demo (2-3 minutes)

#### Console Version (1 minute)
1. Run `python3 bookbuddy.py`
2. Show agent initialization
3. Ask: "motivational books"
4. Show recommendations with Amazon links
5. Ask: "sci-fi books with summary" 
6. Show detailed summaries

#### Web Interface (1-2 minutes)
1. Run `streamlit run bookbuddy_agent/ui.py`
2. Show clean web interface
3. Demonstrate summary checkbox
4. Ask for "business books"
5. Show formatted recommendations
6. Click Amazon link to show it works

### Technical Highlights (30 seconds)
- "Built on AWS Bedrock Agents with Claude 3 Haiku"
- "Automatic agent setup with IAM roles"
- "Both programmatic and web interfaces"
- "Smart URL generation and response parsing"

### Closing (30 seconds)
"BookBuddy demonstrates the power of AWS Bedrock Agents for creating practical, user-friendly AI applications that solve real problems."

## Key Points to Emphasize:
- ✅ Uses AWS Bedrock Agents (core requirement)
- ✅ Practical real-world application
- ✅ Multiple interfaces (console + web)
- ✅ Smart response processing
- ✅ Direct e-commerce integration