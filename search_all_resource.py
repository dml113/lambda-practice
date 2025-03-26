from flask import Flask, render_template, jsonify
import boto3

app = Flask(__name__)

def get_all_regions():
    """AWS에서 사용 가능한 모든 리전 가져오기"""
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    response = ec2_client.describe_regions()
    return [region["RegionName"] for region in response["Regions"]]

def list_ec2_instances(region):
    """해당 리전의 EC2 인스턴스 조회"""
    ec2_client = boto3.client("ec2", region_name=region)
    instances = ec2_client.describe_instances()
    return [instance["InstanceId"] for reservation in instances["Reservations"] for instance in reservation["Instances"]]

def list_rds_instances(region):
    """해당 리전의 RDS 인스턴스 조회"""
    rds_client = boto3.client("rds", region_name=region)
    response = rds_client.describe_db_instances()
    return [db["DBInstanceIdentifier"] for db in response["DBInstances"]]

def list_lambda_functions(region):
    """해당 리전의 Lambda 함수 조회"""
    lambda_client = boto3.client("lambda", region_name=region)
    response = lambda_client.list_functions()
    return [function["FunctionName"] for function in response["Functions"]]

def list_vpcs(region):
    """해당 리전의 VPC 조회"""
    ec2_client = boto3.client("ec2", region_name=region)
    response = ec2_client.describe_vpcs()
    return [vpc["VpcId"] for vpc in response["Vpcs"]]

def list_elastic_ips(region):
    """해당 리전의 Elastic IP (EIP) 조회"""
    ec2_client = boto3.client("ec2", region_name=region)
    response = ec2_client.describe_addresses()
    return [eip["PublicIp"] for eip in response["Addresses"]]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan")
def scan_resources():
    all_regions = get_all_regions()
    
    all_resources = {
        "S3": list_s3_buckets(),
        "EC2": {},
        "RDS": {},
        "Lambda": {},
        "VPC": {},
        "EIP": {}
    }
    
    for region in all_regions:
        print(f"🔎 Scanning region: {region} ...")
        all_resources["EC2"][region] = list_ec2_instances(region)
        all_resources["RDS"][region] = list_rds_instances(region)
        all_resources["Lambda"][region] = list_lambda_functions(region)
        all_resources["VPC"][region] = list_vpcs(region)
        all_resources["EIP"][region] = list_elastic_ips(region)
    
    return jsonify(all_resources)  # JSON 응답 반환

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6974, debug=True)