import ssl
import stomp
import boto3

# ActiveMQ 브로커 정보
BROKER_URL = "b-9d03ada6-fdbb-4489-882a-d5a537e76f63-1.mq.ap-northeast-2.amazonaws.com"
BROKER_PORT = 61614  # STOMP over SSL 포트
QUEUE_NAME = "/queue/gmstbank"
USERNAME = "admin"
PASSWORD = "Skills2025**"
client = boto3.client('dynamodb')

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print(f'Error: {frame}')
    
    def on_message(self, frame):
        message = frame.body
        split_message = message.split(',')
        table_name = split_message[0]
        money = split_message[1]

        if table_name == 'withdrawal':
            response = client.put_item( TableName = 'withdrawal',Item={ 'money' : { 'S':  money} } )

        elif table_name == 'deposit':
            response = client.put_item( TableName = 'deposit',Item={ 'money' : { 'S':  money} } )


conn = stomp.Connection([(BROKER_URL, BROKER_PORT)])
conn.set_listener('', MyListener())
conn.set_ssl(for_hosts=[(BROKER_URL, BROKER_PORT)], ssl_version=ssl.PROTOCOL_TLS)
conn.connect(USERNAME, PASSWORD, wait=True)

print(conn.subscribe(destination=QUEUE_NAME, id=1, ack='auto'))



import time
try:
    while conn.is_connected():
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    conn.disconnect()
