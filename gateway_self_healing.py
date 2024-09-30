import gzip
import json
import base64
import boto3 

def lambda_handler(event, context):
    igw_trigger = 0
    nat_trigger_1 = 0
    nat_trigger_2 = 0

    client = boto3.client('ec2')

    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    
    payload = json.loads(uncompressed_payload)
    log_events = payload['logEvents']
    for i in range(len(log_events)):
        log_message = log_events[i]["message"]
        route_id = json.loads(log_message)["requestParameters"]["routeTableId"]
        response = client.describe_route_tables(
            RouteTableIds=[
                route_id,
            ],
        )

        route_routetable = response["RouteTables"]

        for j in range(len(route_routetable)):
            route_association = route_routetable[j]["Associations"]
            
            for k in range(len(route_association)):
                route_subnets = route_association[k]["SubnetId"]
                
                response = client.describe_subnets(
                    SubnetIds=[
                        route_subnets,
                    ]
                )

                subnets_tags = response["Subnets"]
                for p in range(len(subnets_tags)):
                    Tags = subnets_tags[p]["Tags"]
                    
                    for l in Tags:
                        if l["Key"] == "Name":
                            if "pub" in l["Value"]:
                                igw_trigger = 1
                                nat_trigger_1 = 0
                                nat_trigger_2 = 0 

                            elif "pri" in l["Value"] and "-a" in l["Value"]:
                                igw_trigger = 0
                                nat_trigger_1 = 1
                                nat_trigger_2 = 0

                            elif "pri" in l["Value"] and "-b" in l["Value"]:
                                igw_trigger = 0
                                nat_trigger_1 = 0         
                                nat_trigger_2 = 1       

    if igw_trigger == 1 and nat_trigger_1 == 0 and nat_trigger_2 == 0:
        response = client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId='igw-0d78ccd5b7c7ed8f4',
            RouteTableId=route_id,
        )
        return "Finish"
    
    elif igw_trigger == 0 and nat_trigger_1 == 1 and nat_trigger_2  == 0:
        response = client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId='	nat-05989d97e81a73f48',
            RouteTableId=route_id,
        )
        return "nat_1 Finish"

    elif igw_trigger == 0 and nat_trigger_1 == 0 and nat_trigger_2  == 1:
        response = client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId='nat-05cd05be7d0a7b4d2',
            RouteTableId=route_id,
        )
        return "nat_2 Finish"
                
event = {"awslogs": {"data": "H4sIAAAAAAAA/5VUXW/bOBD8KwafWsBySEqUZPVJ56SOkaTNRcIF13Nh0NTaIUKJOpKKmwb+7wdRykcD3AEHP8kczu7OzvAJ1WAt30P52ALK0Gle5purs6LIl2doivShAYMyNGeYJlEcRQkO0RQpvV8a3bUoQ/xgA6F0VznDpQqU3tvgLToIk0Rs6RyGa4UzwOt3jJtFT1D2BBveBo027g64dQHdRGiKbLe1wsjWSd18lsqBsSj7CxndOQh2/g/03bOfPUDj+sMnJCuUoTClUUgTRiMchuE8wjSJE0ySkKTpPMUMhzGmhGGGKSHzNE4xmTNCMJoiJ2uwjtctykhCojRNkoTEKZk+C4Yy9LRG0Ff8A4yVulmjbI3IDM/XaLpGnQWzqqBx0j2uUfa0Ru6xBY+50dp5TGtkI2TL1aryB29F8QBuBlZumowfbCZ5nWVvUZl55uJC6K5x/8okBFh7AY8jIC9WOaO/L1eXl9ffFkW5uFn++dL3F14PnSoAHBHsDyzYfsqFbhz8cMNI3Dkjt50DO3wLA7xf0yl3AwHFNAowC3BU0jBjYcboN89W73jeubteH8EdDE3tuLKwRsfjcTpKW8r6HRErMcsimmEyEHlYoTsjBiAIOuM1/6kbfrAzoetX1MtYp6DAwU1voEGcg72B/fMKf7XgMLvnX13nVWXA2mHTJJ5FZEZZNCMxftEu30PjPOBK/5RK8RM2w5MPt7Kp9MFOvpQTgmf40+RWNnH0afIjjj5O8rZVcAvbC+lOWJjMwnjy4eK8vLqcTpS8h8kSxL3+OFncGV3DCaHRDPe/ScF33Mjxiu/AwN8dWHfNDa+hT8qwF5+Vkm8VjOs3bhvg3Xy3E1zEFHaQhvPBKBVYJxu/xYWszG9Ki3t/BQ9FT/AaHX0l2+rGwpmCuk/dWGioP1ZJQoFxuk0DIsJtEEHKgi2nPIh4yMgOh4JT4YtuDLjOe92ZDo6vg6xO/x+R3/N4qdrSMK5YEkR0FwVRJVgwJykLME/mOOIsZSEeRePV10b1MfUOfDHfc2Dzg81bueBKDd7lDd/7qf2DM3btiYRsJTQu/+8wevYFd7DX5nHwygulBzhlT8FxqUZZnbJvH5nysnggs4FLyPYOTNHJMXHlZbHJz4oNoelmubjaFOc5ZYM5hOp7uzb6QVZQnWvrzoFXYF5z84vz38fo+OYRMOCfNq4+G10vdGO1Gsr3SqzRER2/H/8BJElmNVwGAAA="}}

lambda_handler(event, "test")