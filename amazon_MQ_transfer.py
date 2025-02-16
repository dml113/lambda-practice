import ssl
import stomp
from flask import Flask, request

app = Flask(__name__)

BROKER_URL = "b-9d03ada6-fdbb-4489-882a-d5a537e76f63-1.mq.ap-northeast-2.amazonaws.com"
BROKER_PORT = 61614  # STOMP over SSL 포트
QUEUE_NAME = "/queue/gmstbank"
USERNAME = "admin"
PASSWORD = "Skills2025**"

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print(f'Error: {message}')
    
    def on_message(self, headers, message):
        print(f'Received message: {message}')



@app.route('/v1/api/deposit', methods=['GET'])
def deposit_api():
    money = request.args['money']

    conn = stomp.Connection([(BROKER_URL, BROKER_PORT)])
    conn.set_listener('', MyListener())
    conn.set_ssl(for_hosts=[(BROKER_URL, BROKER_PORT)], ssl_version=ssl.PROTOCOL_TLS)
    conn.connect(USERNAME, PASSWORD, wait=True)

    message = f'deposit, {money}'
    conn.send(destination=QUEUE_NAME, body=message, persistent='false')

    conn.disconnect()
    return "Deposit API Message sent successfully!"



@app.route('/v1/api/withdrawal', methods=['GET'])
def withdrawal_api():
    money = request.args['money']

    conn = stomp.Connection([(BROKER_URL, BROKER_PORT)])
    conn.set_listener('', MyListener())
    conn.set_ssl(for_hosts=[(BROKER_URL, BROKER_PORT)], ssl_version=ssl.PROTOCOL_TLS)
    conn.connect(USERNAME, PASSWORD, wait=True)

    message = f'withdrawal, {money}'
    conn.send(destination=QUEUE_NAME, body=message, persistent='false')

    conn.disconnect()
    return "withdrawal API Message sent successfully!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)