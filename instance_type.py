import gzip
import json
import base64
import boto3 

def lambda_handler(event, context):
    client = boto3.client('ec2')

    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    
    payload = json.loads(uncompressed_payload)
    log_events = payload['logEvents']

    for i in log_events:
        log_message = i["message"]
        items = json.loads(log_message)["responseElements"]["instancesSet"]["items"]
        instance_type = json.loads(log_message)["requestParameters"]["instanceType"]
        for j in items:
            if instance_type not in ["t3.nano","t3.micro","t3.small","t3.medium","t3.large","t3.xlarge","t3.2xlarge"]:
                instance_id = j["instanceId"]

    instance_describe = client.describe_instances(
    InstanceIds=[
        instance_id,
    ],
)
    print(instance_describe)


    
event = {'awslogs': {'data': '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'}}

lambda_handler(event, "test")