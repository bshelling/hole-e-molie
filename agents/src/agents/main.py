from strands import Agent
from strands.models.anthropic import AnthropicModel
from strands.models.bedrock import BedrockModel

# Boto3 and AWS Imports
import boto3
import os

# Global var imports
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL")
AWSPROFILE = os.getenv("AWS_DEFAULT")


bedrock_session = boto3.Session(profile_name=AWSPROFILE)



def run():
    agent = Agent(model=BEDROCK_MODEL)
    agent("Hello")


run()
