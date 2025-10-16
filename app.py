#!/usr/bin/env python3
"""
BookBuddy CDK Application
Deploy BookBuddy Bedrock Agent using AWS CDK Infrastructure as Code
"""

import aws_cdk as cdk
from bookbuddy_agent.bookbuddy_agent_stack import BookBuddyAgentStack


def main():
    """Main CDK application entry point."""
    app = cdk.App()
    
    # Get configuration from context or use defaults
    env = cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    )
    
    # Create the BookBuddy stack
    BookBuddyAgentStack(
        app, 
        "BookBuddyAgentStack",
        env=env,
        description="BookBuddy AI Reading Companion - Bedrock Agent Infrastructure"
    )
    
    app.synth()


if __name__ == "__main__":
    main()

