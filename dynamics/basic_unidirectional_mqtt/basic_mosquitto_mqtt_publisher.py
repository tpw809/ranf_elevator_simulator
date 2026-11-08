"""MQTT (Message Queuing Telemetry Transport)

pip install paho-mqtt
"""
import json
import time
import numpy as np
import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


# setup mqtt client:
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)


# initial conditions:
t = 0.0


while True:
    # heartbeat:
    print(f"t = {t}")
    
    # run dynamics:
    speed = 5 + 2*np.sin(20.0*t)
    
    # create data packet:
    packet = {
        "time": t,
        "speed": speed,
    }

    # publish data packet to MQTT server:
    client.publish(
        "test/telemetry",  # MQTT Topic
        json.dumps(packet)  # json data
    )

    t += 0.1
    
    # 1 Hz:
    time.sleep(1.0)


"""
windows install:
https://mosquitto.org/download/

linux install mqtt mosquitto:
$ sudo apt update
$ sudo apt install mosquitto mosquitto-clients
$ sudo systemctl start mosquitto
$ sudo systemctl enable mosquitto

start broker in windows:
cd "C:\Program Files\mosquitto"
mosquitto -v


test mosquitto:
first terminal:
$ mosquitto_sub -h localhost -t "test/topic"
second terminal:
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"

tested: it worked!
"""
