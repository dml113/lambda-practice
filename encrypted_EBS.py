import boto3
import time

client = boto3.client("ec2")
response = client.describe_volumes()

for i in response["Volumes"]:
    if i["Encrypted"] == False:
        volume_id = i["VolumeId"]

        # 스냅샷 생성
        create_snapshot = client.create_snapshot(VolumeId=volume_id)
        snapshot_id = create_snapshot["SnapshotId"]

        while True:
            describe_snapshot = client.describe_snapshots(SnapshotIds=[snapshot_id])
            snapshot_state = describe_snapshot["Snapshots"][0]["State"]

            if snapshot_state == "completed":
                print("Successfully created snapshot.")
                break
            
            else:
                print("Creating snapshot")
                time.sleep(10)

        create_volume = client.create_volume(
            AvailabilityZone="ap-northeast-1a",
            Encrypted=True,
            SnapshotId=snapshot_id,
            VolumeType="gp3",
        )