# BookBuddy - AI Reading Companion

## 🚀 **LIVE DEMO**
**Try BookBuddy now:** https://bookbuddy-bedrock-[your-app-id].streamlit.app

BookBuddy is an AI-powered reading companion built on AWS Bedrock Agents that provides personalized book recommendations with direct Amazon purchase links.

## ✨ Features

- 🤖 **AI-Powered Recommendations** using AWS Bedrock Agents with Claude 3 Haiku
- 🛒 **Direct Amazon Purchase Links** for instant book buying
- 🌐 **Live Web Interface** deployed on Streamlit Cloud
- ⚡ **Real-time Processing** with professional UI
- 📱 **Mobile-Friendly** responsive design
- 🎯 **Quick Genre Buttons** for instant recommendations

## 🎮 How to Use

### Web Interface (Recommended)
1. Visit the live app: https://bookbuddy-bedrock-[your-app-id].streamlit.app
2. Ask for book recommendations:
   - "motivational books"
   - "sci-fi novels"
   - "business books"
   - "books about productivity"
3. Use quick buttons: 🚀 Motivation, 🧠 Psychology, 💼 Business
4. Click Amazon links to purchase books

### Console Interface (Local Development)
```bash
pip install -r requirements.txt
python3 bookbuddy.py
```

## 🏗️ AWS Services Used

- **AWS Bedrock Agents** - Core AI agent functionality
- **Amazon Bedrock** - Claude 3 Haiku foundation model
- **AWS IAM** - Automatic role and policy management

## 📋 Prerequisites

- AWS Account with Bedrock access
- Python 3.8+
- AWS CLI configured
- **Enable Claude 3 Haiku model access** in Bedrock console:
  1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
  2. Click "Model access" → "Manage model access"
  3. Enable "Anthropic Claude 3 Haiku"

## 💬 Example Interactions

```
You: "motivational books"
BookBuddy: 
📚 **Atomic Habits** by James Clear
Build good habits and break bad ones with this practical guide
🛒 Buy: https://amazon.com/s?k=Atomic+Habits+James+Clear

📚 **The 7 Habits of Highly Effective People** by Stephen Covey
Timeless principles for personal and professional effectiveness
🛒 Buy: https://amazon.com/s?k=The+7+Habits+of+Highly+Effective+People+Stephen+Covey
```

## 📁 Project Structure

```
BookBuddy-Bedrock/
├── ui.py                 # Streamlit web interface (main app)
├── bookbuddy.py          # Core Bedrock Agent implementation
├── requirements.txt      # Python dependencies
├── .streamlit/config.toml # Streamlit configuration
├── bookbuddy_agent/      # CDK infrastructure code
├── DEMO_SCRIPT.md        # Live demo instructions
└── HACKATHON_SUBMISSION.md # Competition submission
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run console version
python3 bookbuddy.py

# Run web interface locally
streamlit run ui.py
```

## 🎯 Built For

- **Book enthusiasts** seeking personalized recommendations
- **Busy professionals** needing quick book suggestions
- **Students** looking for educational material
- **Anyone** wanting to discover books based on mood or interest

## 🏆 Why BookBuddy?

- ✅ **Live & Accessible** - No setup required, works immediately
- ✅ **AWS Bedrock Agents** - Showcases latest AI technology
- ✅ **Production Ready** - Deployed and scalable
- ✅ **Real-World Impact** - Solves actual book discovery problems
- ✅ **Commercial Viability** - Direct e-commerce integration

---

**Built with ❤️ using AWS Bedrock Agents | Ready for Testing**

