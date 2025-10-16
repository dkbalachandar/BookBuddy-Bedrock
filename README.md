# BookBuddy - AI Reading Companion

BookBuddy is an AI-powered reading companion built on Amazon Bedrock that provides personalized book recommendations based on your preferences, genre, or mood.

## 🚀 Two Deployment Options

### Option 1: Python Script (Quick Start)
Perfect for development, testing, and learning.

### Option 2: AWS CDK (Production Ready)
Infrastructure as Code for production deployments.

---

## 📋 Prerequisites

- AWS Account with Bedrock access
- Python 3.8+
- AWS CLI configured
- Bedrock model access enabled (see setup below)

---

## 🔧 Setup

### 1. Install Dependencies

```bash
# For Python script approach
pip install -r requirements.txt

# For CDK approach (additional)
pip install -r cdk_requirements.txt
npm install -g aws-cdk
```

### 2. Configure AWS Credentials

```bash
aws configure
```

### 3. Enable Bedrock Model Access

**Important**: You must enable model access in the Bedrock console:

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click **"Model access"** → **"Manage model access"**
3. Enable **"Anthropic Claude 3 Haiku"** (recommended)
4. Submit request (usually approved instantly)

---

## 🐍 Option 1: Python Script Approach

### Quick Start

```bash
python3 bookbuddy_clean.py
```

### Features

- ✅ **Automatic setup** - Creates agent, IAM roles, aliases
- ✅ **Model switching** - Easy to change foundation models
- ✅ **Interactive chat** - Real-time conversation
- ✅ **Error handling** - Helpful error messages and recovery
- ✅ **Clean architecture** - Well-organized, maintainable code

### Configuration

Edit the config in `bookbuddy_clean.py`:

```python
config = {
    "agent_name": "BookBuddy",
    "foundation_model": "anthropic.claude-3-haiku-20240307-v1:0",
    "alias_name": "BookBuddy",
    "region": "us-east-1"
}
```

### Available Models

```python
# Fast and cost-effective (recommended)
"anthropic.claude-3-haiku-20240307-v1:0"

# More capable but slower
"anthropic.claude-3-sonnet-20240229-v1:0"

# Amazon's newest model
"amazon.nova-micro-v1:0"

# Basic text generation
"amazon.titan-text-express-v1"
```

---

## 🏗️ Option 2: AWS CDK Approach

### Deploy Infrastructure

```bash
# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy the stack
cdk deploy
```

### Features

- ✅ **Infrastructure as Code** - Version controlled infrastructure
- ✅ **Production ready** - Proper IAM roles and policies
- ✅ **Repeatable deployments** - Consistent across environments
- ✅ **CloudFormation integration** - Full AWS integration
- ✅ **Outputs** - Agent IDs and ARNs for integration

### CDK Outputs

After deployment, you'll get:
- **Agent ID** - For direct API calls
- **Agent Alias ID** - For production usage
- **Agent Alias ARN** - For cross-service integration
- **IAM Role ARN** - For reference

### Use the Deployed Agent

```python
import boto3

runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

response = runtime.invoke_agent(
    agentId="YOUR_AGENT_ID",
    agentAliasId="YOUR_ALIAS_ID", 
    sessionId="session-123",
    inputText="Recommend a good sci-fi book"
)
```

### Clean Up

```bash
cdk destroy
```

---

## 💬 Usage Examples

### Book Recommendations

```
You: motivational books
BookBuddy: I'd recommend "Atomic Habits" by James Clear - it's a practical guide to building good habits and breaking bad ones. The book provides actionable strategies backed by scientific research.

You: sci-fi for beginners  
BookBuddy: "The Martian" by Andy Weir is perfect for sci-fi newcomers! It's accessible, humorous, and focuses on problem-solving rather than complex technology. Great storytelling with realistic science.

You: classic literature
BookBuddy: "To Kill a Mockingbird" by Harper Lee is an excellent choice. This timeless novel explores themes of justice, morality, and growing up in the American South. It's both engaging and thought-provoking.
```

---

## 🔍 Troubleshooting

### Model Access Issues

```
❌ Model access failed: AccessDeniedException
```

**Solution**: Enable model access in Bedrock console (see setup above)

### IAM Permission Issues

```
❌ User: arn:aws:iam::123:user/myuser is not authorized
```

**Solution**: Add `AmazonBedrockFullAccess` policy to your AWS user

### Agent Not Prepared

```
❌ Agent is in Not Prepared state
```

**Solution**: The script handles this automatically with retries

---

## 📁 Project Structure

```
bookbuddy/
├── bookbuddy_clean.py          # Clean Python script (recommended)
├── bookbuddy_demo_fixed.py     # Working demo script  
├── bookbuddy_agent/
│   └── bookbuddy_agent_stack.py # CDK stack definition
├── app.py                      # CDK app entry point
├── cdk.json                    # CDK configuration
├── requirements.txt            # Python dependencies
├── cdk_requirements.txt        # CDK dependencies
└── README.md                   # This file
```

---

## 🎯 Which Approach to Choose?

### Use Python Script When:
- 🧪 **Learning and experimenting**
- 🚀 **Quick prototyping**
- 🔧 **Development and testing**
- 👤 **Personal projects**

### Use CDK When:
- 🏢 **Production deployments**
- 👥 **Team environments**
- 🔄 **CI/CD pipelines**
- 📋 **Compliance requirements**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both Python and CDK approaches
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure model access is enabled in Bedrock console
3. Verify your AWS credentials and permissions
4. Check the AWS region (us-east-1 recommended)

Happy reading! 📚

