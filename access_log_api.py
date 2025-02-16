import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('logs')
    response = client.get_log_events(
        logGroupName='httpd-cloudwatch',
        logStreamName='from-fluent-bit-access_log'
    )

    logs = response['events']

    all_logs = []

    access_logs = []

    for log in logs:
        all_logs.append(log['message'])
        
    for log in all_logs:
        json_log = json.loads(log)
        real_log = json_log['log']
        access_logs.append(real_log)

    last_5_log = access_logs[-5:]
    return {"logs": last_5_log}