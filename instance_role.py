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
        print(log_message)
        policy_arn = json.loads(log_message)["requestParameters"]["policyArn"]
        role_name = json.loads(log_message)["requestParameters"]["roleName"]

    iam_client = boto3.client("iam")
    delete_role_policy = iam_client.detach_role_policy(
        PolicyArn=policy_arn,
        RoleName=role_name,
    )

    
event = {'awslogs': {'data': 'H4sIAAAAAAAA/31TXXPbNhD8Kx08mwoAEvzAG0d2XKVx41pyM5My4zmRJxkzJMACYFXVo//eIWDLTtLpm6hb7N7t7T2RAZ2DPW6OIxJJLutN/XBztV7X11fkgpiDRkskqQTlRZZnWUFTckF6s7+2ZhqJJHBwSdubqfMWVJ/0Zu+St+hkm6ci5W0Rn629RRi+Y3xYzgSbmeABxkQb6x8RnE/4w6zmpq1rrRq9Mvq96j1aR+QfpPYe2sdb06v2GP8mX4PG1V+o/Qx5IqojkqQlF3khqKjyrKQVFzylBUuzlFUZL3hZ8IrllLGUlVlVliUv8pIWxSzt1YDOwzASyQomsopTXoisunixjUjy1BCcFX9H65TRDZENYQtaNeSiIZNDu+pQe+WPDZFPDfHHEQNmVd/cO7QBNlqlWzVCv+pCrV5d1oL/dr36+PH2/ubDhy+fuLgLSLBRAayWcHBSwSDlWzPlLPnuahh7c0SMb9rWTNo/c78Fv5TRuV/w+CK+Xp3F+fJeLH++/nwe5lcYYvvfKDh08+xLoz3+7eOg4L1V28mji9+tRZhXeAk+MnDKs4SKhPEN5ZIyyYsvgW3YQT35x9m1FjzGrnbQO2zI6XS6eDZ8o4YfiYRMmcxoJAqwtZlsG4EKhgUM8I/RcHCL1gyvqPNcMVZ3pscYrWjRwd3h/mW7k0tCPFmcPfCvbuuus+hc3D/LFxlbcJEtWE7P5tV71D6qfF7/tNIerYY+lC3+OaHzt2BhwDni0TRrejy3dnBtGFVp50G3mMzVmJ/Qav1f2Zh/xPK7uhuUVs5b8MbWYesNOQVxNxrt8KrHYb6dhkg99f1rW6vLGJ08x6qANOmAsSSjLUugQpoURVnuBJRiu2tfLX1+tO1EiSnNk4rudknGRJps27RMtm3OOkGzQlT4bAF0n3Q/30lY9nnPLxdTH1w9qiX00bIBNOxDw+HiGyK9nTAQtWpUqH39/8EP7EvwuDf2GCA3Z8pvYm0xnDD0760Zlka74LtsyCzYkBM5fT39CyCbv+9KBQAA'}}
lambda_handler(event, "test")