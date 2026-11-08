import json
import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print(data)


# setup mqtt client:
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect("localhost", 1883)

# MQTT Topic:
client.subscribe("test/telemetry")

client.loop_forever()
