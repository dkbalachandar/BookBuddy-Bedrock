import boto3
import json

# Check what models are available and accessible
bedrock = boto3.client("bedrock", region_name="us-east-1")
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

print("🔍 Checking available foundation models...")

try:
    models = bedrock.list_foundation_models()
    print(f"Found {len(models['modelSummaries'])} models:")
    
    # Group by provider
    providers = {}
    for model in models['modelSummaries']:
        provider = model['providerName']
        if provider not in providers:
            providers[provider] = []
        providers[provider].append(model['modelId'])
    
    for provider, model_list in providers.items():
        print(f"\n{provider}:")
        for model_id in model_list:
            print(f"  - {model_id}")
    
    # Test a few common models to see which ones are accessible
    test_models = [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0", 
        "amazon.titan-text-express-v1",
        "amazon.titan-text-lite-v1"
    ]
    
    print(f"\n🧪 Testing model access...")
    accessible_models = []
    
    for model_id in test_models:
        try:
            if "anthropic" in model_id:
                body = json.dumps({
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "anthropic_version": "bedrock-2023-05-31"
                })
            else:  # Titan
                body = json.dumps({
                    "inputText": "Hi",
                    "textGenerationConfig": {
                        "maxTokenCount": 10,
                        "temperature": 0.7
                    }
                })
            
            response = bedrock_runtime.invoke_model(
                modelId=model_id,
                body=body
            )
            accessible_models.append(model_id)
            print(f"  ✅ {model_id} - ACCESSIBLE")
            
        except Exception as e:
            print(f"  ❌ {model_id} - {str(e)[:50]}...")
    
    if accessible_models:
        print(f"\n🎉 You can use these models: {accessible_models}")
        print(f"\nRecommended model to use: {accessible_models[0]}")
    else:
        print(f"\n❌ No models are accessible. You need to enable model access in Bedrock console.")
        
except Exception as e:
    print(f"Error checking models: {e}")