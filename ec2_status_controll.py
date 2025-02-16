import json
import boto3

client = boto3.client('ec2')

def server_control(param):
    if param == 'on':
        return client.start_instances(InstanceIds=['i-0af30873f467f05b3']), {'statusCode': 200, 'body': json.dumps('Server is starting')}

    elif param == 'off':
        return client.stop_instances(InstanceIds=['i-0af30873f467f05b3']), {'statusCode': 200, 'body': json.dumps('Server is stopping')}

def lambda_handler(event, context):
    param = event['queryStringParameters']['status']
    status = client.describe_instances(InstanceIds=['i-0af30873f467f05b3'])['Reservations'][0]['Instances'][0]['State']['Name']

    if status == 'running' and param == 'on':
        return {'statusCode': 200, 'body': json.dumps({"msg": "this server is running"})}
    elif status == 'stopped' and param == 'off':
        return {'statusCode': 200, 'body': json.dumps({"msg": "this server is stopped"})}
    else:
        return server_control(param)[1]