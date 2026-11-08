# shiny run --reload --host 127.0.0.1 --port 8000 app.py
# http://127.0.0.1:8000
import asyncio
import uuid
from gmqtt import Client as MQTTClient
from shiny import App, reactive, render, ui

# use asyncio-mqtt...

BROKER = "localhost"
PORT = 1883
TOPIC = "test/telemetry"


# Updated to use ui.output_code() instead of ui.output_text_verbatim()
app_ui = ui.page_fluid(
    ui.h2("Shiny for Python + Async MQTT Subscriber"),
    ui.hr(),
    ui.p("Latest received MQTT message (True Real-Time Updates):"),
    ui.output_code("mqtt_output"), 
)


def server(input, output, session):
    latest_message = reactive.Value("Waiting for MQTT messages...")


    # Updated decorator from @render.text to @render.code 
    # to perfectly pair with ui.output_code()
    @render.code
    def mqtt_output():
        return latest_message.get()


app = App(app_ui, server)
