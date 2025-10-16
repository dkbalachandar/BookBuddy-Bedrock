import boto3
import json

# Test direct model access
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

try:
    print("🧪 Testing direct Titan model access...")
    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "max_tokens": 100,
            "messages": [{"role": "user", "content": "Recommend a good book"}],
            "anthropic_version": "bedrock-2023-05-31"
        })
    )
    
    result = json.loads(response['body'].read())
    print("✅ Direct model access successful!")
    print(f"Response: {result}")
    
except Exception as e:
    print(f"❌ Direct model access failed: {e}")
    if "accessDeniedException" in str(e):
        print("\n💡 This means the Titan model is not enabled in your account.")
        print("To fix this:")
        print("1. Go to AWS Bedrock Console")
        print("2. Click 'Model access' in the left menu")
        print("3. Click 'Manage model access'")
        print("4. Find 'Amazon Titan Text Express' and enable it")
        print("5. Submit the request (usually approved instantly)")