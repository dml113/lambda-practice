import boto3
import time

while True:
    client = boto3.client('ec2')
    describe = client.describe_route_tables(
        RouteTableIds=[
            'rtb-00bcd14fbfe0753dd',
        ],
    )

    route_describe = describe['RouteTables'][0]['Routes']

    for i in route_describe:
        if i['GatewayId'] != 'local' and i['DestinationCidrBlock'] == '0.0.0.0/0':
            print("RouteTable in IGW")
        
        else:
            replace_route = client.create_route(
                RouteTableId='rtb-00bcd14fbfe0753dd',
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId='igw-08dcd085cb896ccca'
            )
    time.sleep(10)