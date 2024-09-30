import boto3

client = boto3.client('s3')
response = client.list_buckets()
bucket_list = response["Buckets"]

for i in range(len(bucket_list)):
    if "wsc2024-" not in bucket_list[i]["Name"]:
        response = client.delete_bucket(
            Bucket=bucket_list[i]["Name"],
        )
        print("Successfully Delete" + bucket_list[i]["Name"] + "!")