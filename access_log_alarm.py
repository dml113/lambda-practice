import boto3
import json
import time

def lambda_handler(event, context):
    client = boto3.client('logs')
    sqs = boto3.client('sqs')
    resouce_sqs = boto3.resource('sqs')
    queue = resouce_sqs.Queue('https://sqs.ap-northeast-2.amazonaws.com/950274644703/my-queue')    
    response = client.get_log_events(logGroupName='fluent-bit-cloudwatch', logStreamName='from-fluent-bit-access_log')

    logs = response['events']

    for log in logs:
        json_log = json.loads(log['message'])
        last_log = json_log['log']

    if '/admin' in last_log or '/administrator' in last_log or '/auth' in last_log:
        send_message = sqs.send_message( QueueUrl='https://sqs.ap-northeast-2.amazonaws.com/950274644703/my-queue', MessageBody='Alarm')
        print("success seding message")
        time.sleep(5)
        receive_message = queue.receive_messages()

    else:
        print('No Alarm')