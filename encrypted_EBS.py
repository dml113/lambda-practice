import boto3

# search not encryption volume

client = boto3.client("ec2")
response = client.describe_volumes()
volumes = response["Volumes"]
for i in volumes:
    if i["Encrypted"] == False:
        volume_id = i["VolumeId"]

# create snapshot

snapshot = client.create_snapshot(
    VolumeId=volume_id,
)

snapshot = client.describe_snapshots()
for l in snapshot["Snapshots"]:
    if l["VolumeId"] == volume_id:
        snapshot_id = l["SnapshotId"]

# create encryption volume

create_volume = client.create_volume(
    AvailabilityZone="ap-northeast-2a",
    Encrypted=True,
    Iops=3000,
    SnapshotId=snapshot_id,
    VolumeType='gp3',
)

# Delete not encryption snapshot,volume

response = client.delete_volume(
    VolumeId=volume_id,
)

response = client.delete_snapshot(
    SnapshotId=snapshot_id,
)


# 1. 스냅샷 생성
# 2. 스냅샷으로 암호화된 볼륨 생성
# 3. 전에 생성한 볼륨 삭제