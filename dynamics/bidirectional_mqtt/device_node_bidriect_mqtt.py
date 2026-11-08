# node.py
# pip install paho-mqtt
import json
import random
import threading
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
CMD_TOPIC = "demo/node1/cmd"
TLM_TOPIC = "demo/node1/tlm"

node_state = {
    "enabled": False,
    "setpoint": 50
}


def on_connect(client, userdata, flags, rc, properties=None):
    print("Node connected")
    client.subscribe(CMD_TOPIC)


def on_message(client, userdata, msg):
    global node_state

    try:
        command = json.loads(msg.payload.decode())

        print(f"CMD RECEIVED: {command}")

        cmd = command.get("command")

        if cmd == "ENABLE":
            node_state["enabled"] = True

        elif cmd == "DISABLE":
            node_state["enabled"] = False

        elif cmd == "SETPOINT":
            node_state["setpoint"] = command["value"]

    except Exception as e:
        print("Command error:", e)


def telemetry_task(client):
    while True:

        if node_state["enabled"]:
            process_value = (
                node_state["setpoint"]
                + random.uniform(-2, 2)
            )
        else:
            process_value = 0

        telemetry = {
            "enabled": node_state["enabled"],
            "setpoint": node_state["setpoint"],
            "process_value": round(process_value, 2),
            "temperature": round(
                25 + random.uniform(-5, 5), 2
            ),
            "timestamp": time.time()
        }

        client.publish(
            TLM_TOPIC,
            json.dumps(telemetry)
        )

        time.sleep(1)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883)

threading.Thread(
    target=telemetry_task,
    args=(client,),
    daemon=True
).start()

client.loop_forever()
