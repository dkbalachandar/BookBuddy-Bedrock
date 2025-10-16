# BookBuddy - AI Reading Companion
## AWS Agent Hackathon Submission

### 🎯 Project Overview
BookBuddy is an AI-powered reading companion built on AWS Bedrock Agents that provides personalized book recommendations with direct Amazon purchase links. Users can get tailored book suggestions based on their preferences, mood, or specific interests.

### 🚀 Key Features
- **Personalized Recommendations** - AI-powered book suggestions based on user input
- **Direct Purchase Integration** - Amazon links for immediate book purchasing
- **Multiple Interfaces** - Both console and web-based interactions
- **Summary Options** - Detailed book summaries when requested
- **Smart Response Processing** - Clean, formatted recommendations
- **Automatic Setup** - Handles AWS infrastructure automatically

### 🏗️ AWS Services Used
- **Amazon Bedrock Agents** - Core AI agent functionality
- **Claude 3 Haiku** - Foundation model for natural language processing
- **AWS IAM** - Automatic role and policy management
- **Amazon Bedrock Runtime** - Agent invocation and response handling

### 💡 Innovation Highlights
1. **Dual Interface Design** - Seamless experience across console and web
2. **Smart URL Generation** - Automatic Amazon search link creation
3. **Response Enhancement** - Intelligent parsing and formatting of AI responses
4. **Error Recovery** - Robust handling of AWS service interactions
5. **User-Centric Design** - Focus on practical book discovery and purchasing

### 🛠️ Technical Architecture
```
User Input → Bedrock Agent → Claude 3 Haiku → Response Processing → Formatted Output
     ↓
AWS IAM Role Management ← Automatic Setup ← BookBuddy Class
```

### 📱 Interfaces
1. **Console Interface** (`bookbuddy.py`) - Interactive command-line experience
2. **Web Interface** (`bookbuddy_agent/ui.py`) - Streamlit-based web application
3. **CDK Deployment** (`bookbuddy_agent_stack.py`) - Infrastructure as Code

### 🎯 Target Users
- **Book enthusiasts** seeking personalized recommendations
- **Busy professionals** needing quick book suggestions
- **Students** looking for educational material
- **Anyone** wanting to discover new books based on mood or interest

### 🚀 Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run console version
python3 bookbuddy.py

# Run web interface
streamlit run bookbuddy_agent/ui.py
```

### 🏆 Why BookBuddy Stands Out
- **Practical Application** - Solves real user problems
- **AWS Integration** - Showcases Bedrock Agents capabilities
- **User Experience** - Clean, intuitive interfaces
- **Commercial Viability** - Direct integration with e-commerce
- **Technical Excellence** - Robust error handling and response processing

### 📊 Demo Results
- **Fast Response Times** - Sub-2 second recommendations
- **High Accuracy** - Relevant, well-known book suggestions
- **User-Friendly** - Intuitive interface design
- **Reliable** - Handles edge cases and errors gracefully

### 🔮 Future Enhancements
- Book cover image integration
- User preference learning
- Reading goal tracking
- Social sharing features
- Multi-language support

---

**Built with ❤️ using AWS Bedrock Agents**