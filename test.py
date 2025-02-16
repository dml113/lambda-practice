import boto3
import time

client = boto3.client("ec2")
response = client.describe_volumes()

response = client.enable_ebs_encryption_by_default(
    DryRun=False
)