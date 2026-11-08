# client.py

import json
import threading
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
CMD_TOPIC = "demo/node1/cmd"
TLM_TOPIC = "demo/node1/tlm"


def on_connect(client, userdata, flags, rc, properties=None):
    print("Client connected")
    client.subscribe(TLM_TOPIC)


def on_message(client, userdata, msg):

    telemetry = json.loads(msg.payload.decode())

    print(
        "\nTelemetry:"
    )

    print(
        json.dumps(
            telemetry,
            indent=2
        )
    )


def command_task(client):

    time.sleep(3)

    client.publish(
        CMD_TOPIC,
        json.dumps({
            "command": "ENABLE"
        })
    )

    print("Sent ENABLE")

    time.sleep(5)

    client.publish(
        CMD_TOPIC,
        json.dumps({
            "command": "SETPOINT",
            "value": 75
        })
    )

    print("Sent SETPOINT=75")

    time.sleep(10)

    client.publish(
        CMD_TOPIC,
        json.dumps({
            "command": "DISABLE"
        })
    )

    print("Sent DISABLE")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883)

threading.Thread(
    target=command_task,
    args=(client,),
    daemon=True
).start()

client.loop_forever()
