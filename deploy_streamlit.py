#!/usr/bin/env python3
"""
Deploy BookBuddy Streamlit app to AWS using CDK
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class StreamlitAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create VPC
        vpc = ec2.Vpc(self, "BookBuddyVPC", max_azs=2)
        
        # Create ECS Cluster
        cluster = ecs.Cluster(self, "BookBuddyCluster", vpc=vpc)
        
        # Create task role with Bedrock permissions
        task_role = iam.Role(
            self, "BookBuddyTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
            ]
        )
        
        # Create Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "BookBuddyService",
            cluster=cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("."),
                container_port=8501,
                task_role=task_role,
                environment={
                    "AWS_DEFAULT_REGION": self.region
                }
            ),
            public_load_balancer=True,
            desired_count=1
        )
        
        # Configure health check
        fargate_service.target_group.configure_health_check(
            path="/",
            healthy_http_codes="200"
        )

def main():
    app = cdk.App()
    StreamlitAppStack(app, "BookBuddyStreamlitStack")
    app.synth()

if __name__ == "__main__":
    main()