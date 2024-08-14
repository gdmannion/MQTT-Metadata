from flask import Flask, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = '#'

messages = []

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    messages.append(msg.payload.decode())
    
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(mqtt_topic)
    print(f"Subscribed to topic {mqtt_topic}")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    messages.append(msg.payload.decode())


# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
