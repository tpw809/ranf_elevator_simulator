# shiny run --reload --host 127.0.0.1 --port 8000 app.py
# http://127.0.0.1:8000
import asyncio
import paho.mqtt.client as mqtt
from shiny import App, reactive, render, ui


# Define MQTT Broker Settings
BROKER = "localhost"
PORT = 1883
TOPIC = "test/telemetry"

app_ui = ui.page_fluid(
    ui.h2("Shiny for Python + MQTT Subscriber"),
    ui.hr(),
    ui.p("Latest received MQTT message (Updates Live):"),
    ui.output_text_verbatim("mqtt_output"),
)

def server(input, output, session):
    # Move reactive state inside the session to keep it fresh
    latest_message = reactive.Value("Waiting for MQTT messages...")
    
# 1. Setup traditional Paho callbacks
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            client.subscribe(TOPIC)

    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        # Direct set is now 100% safe because we are on the same thread!
        latest_message.set(f"[{msg.topic}] {payload}")

    # 2. Configure Client without spinning up background threads
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)

    # 3. Create a continuous async loop co-existing with Shiny
    async def mqtt_loop():
        try:
            while True:
                # Let Paho handle its network socket events non-blockingly
                client.loop(timeout=0.01)
                # Yield control to Shiny's web server loop immediately
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            client.disconnect()

    # Launch the loop task inside Shiny's native async engine
    mqtt_task = asyncio.create_task(mqtt_loop())

    # 4. Clean up cleanly when the user disconnects or closes the tab
    @session.on_ended
    def _():
        mqtt_task.cancel()
    
    @render.text
    def mqtt_output():
        return latest_message.get()
        

app = App(app_ui, server)
