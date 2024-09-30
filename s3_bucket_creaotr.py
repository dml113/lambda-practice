import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str)
args = parser.parse_args()

client = boto3.client('s3')
response = client.create_bucket(
    Bucket=args.name,
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-northeast-2',
    },
)