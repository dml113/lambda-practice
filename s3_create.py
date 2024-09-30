import json
import boto3
import datetime

def lambda_handler(event, context):
    # S3 버킷 이름과 파일 이름 설정
    bucket = 'ap-northeast-2-uijin-bucket'  # 사용할 S3 버킷의 이름
    file_name = str(datetime.datetime.now())[:-7]  # 현재 시간을 이용하여 고유한 파일 이름 생성
    file = dict()
    # 업로드할 JSON 파일의 내용 설정
    file['customerID'] = 'jinyes'
    file['age'] = '25'
    file['product'] = 'aws_solution'
    # S3에 파일 업로드 시도
    result = upload_file_s3(bucket, file_name + '.json', file)

    if result:
        return {
            'statusCode': 200,
            'body': json.dumps("업로드 성공")  # 성공 시 응답
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("업로드 실패")  # 실패 시 응답
        }

def upload_file_s3(bucket, file_name, file):
    # 파일을 UTF-8로 인코딩하여 바이트로 변환
    encode_file = bytes(json.dumps(file).encode('UTF-8'))
    # AWS SDK인 Boto3를 사용하여 S3 클라이언트 생성
    s3 = boto3.client('s3')
    try:
        # S3에 파일 업로드
        s3.put_object(Bucket=bucket, Key=file_name, Body=encode_file)
        return True  # 업로드 성공 시 True 반환
    except:
        return False  # 업로드 실패 시 False 반환
