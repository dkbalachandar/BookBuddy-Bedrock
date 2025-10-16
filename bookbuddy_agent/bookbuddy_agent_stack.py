from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_bedrock as bedrock,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct


class BookBuddyAgentStack(Stack):
    """CDK Stack for deploying BookBuddy Bedrock Agent infrastructure."""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Configuration
        agent_name = "BookBuddy"
        foundation_model = "anthropic.claude-3-haiku-20240307-v1:0"
        alias_name = "BookBuddy"
        
        # Create IAM role for Bedrock agent
        agent_role = iam.Role(
            self, "BookBuddyAgentRole",
            role_name=f"{agent_name}-BedrockRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            description=f"IAM role for {agent_name} Bedrock agent",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
            ],
            inline_policies={
                "BedrockModelAccess": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeModel",
                                "bedrock:InvokeModelWithResponseStream",
                                "bedrock:GetFoundationModel",
                                "bedrock:ListFoundationModels"
                            ],
                            resources=["*"]
                        )
                    ]
                )
            }
        )
        
        # Create Bedrock Agent
        agent = bedrock.CfnAgent(
            self, "BookBuddyAgent",
            agent_name=agent_name,
            foundation_model=foundation_model,
            agent_resource_role_arn=agent_role.role_arn,
            instruction="""You are BookBuddy — a friendly AI reading companion.
Recommend books based on user preferences, genre, or mood.
Provide title, author, genre, and a short reason.
Only suggest well-known or highly-rated books.""",
            description="AI reading companion that recommends books",
            idle_session_ttl_in_seconds=1800,  # 30 minutes
            auto_prepare=True
        )
        
        # Create Agent Alias
        agent_alias = bedrock.CfnAgentAlias(
            self, "BookBuddyAgentAlias",
            agent_alias_name=alias_name,
            agent_id=agent.attr_agent_id,
            description=f"Production alias for {agent_name}"
        )
        
        # Outputs
        CfnOutput(
            self, "AgentId",
            value=agent.attr_agent_id,
            description="BookBuddy Agent ID"
        )
        
        CfnOutput(
            self, "AgentAliasId", 
            value=agent_alias.attr_agent_alias_id,
            description="BookBuddy Agent Alias ID"
        )
        
        CfnOutput(
            self, "AgentAliasArn",
            value=agent_alias.attr_agent_alias_arn,
            description="BookBuddy Agent Alias ARN"
        )
        
        CfnOutput(
            self, "RoleArn",
            value=agent_role.role_arn,
            description="BookBuddy Agent IAM Role ARN"
        )

