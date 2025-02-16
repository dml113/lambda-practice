import boto3, time

while True:
    client = boto3.client('s3')
    s3 = boto3.resource('s3')
    response = client.list_buckets(BucketRegion='ap-northeast-2')
    
    bucket_list = response['Buckets']

    for bucket in bucket_list:
        bucket_name = bucket['Name']
        if 'wsc2024' not in bucket_name:
            bucket = s3.Bucket(bucket_name)
            bucket.objects.all().delete()
            response = client.delete_bucket(Bucket=bucket_name)