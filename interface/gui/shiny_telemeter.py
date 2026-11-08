# shiny run --reload --host 127.0.0.1 --port 8000 app.py
# http://127.0.0.1:8000
import time
import asyncio
import numpy as np
from pathlib import Path
from shiny import App, reactive, render, ui

# Locate your CSS file safely using pathlib
css_path = Path(__file__).parent / "bootstrap_cyborg.css"

# Replaces the default Bootstrap theme entirely
app_ui = ui.page_fluid(
    #title="Custom Theme App",
    #theme=css_path, 
    #content=(
    ui.h2("Telemeter 0.1", style="color:#FF9C41;"),
    
    ui.layout_columns(
        # card:
        ui.card(
            ui.card_header(
                "Power Module",
                #class_="bg-dark"
            ),
            ui.card_body(
                ui.input_switch(
                    id="power_switch", 
                    label="Power Switch", 
                    value=False,
                ),
                #ui.markdown("Some text with a [link](https://github.com)"),
                ui.output_text(id="power_status_display", inline=True),
                #"Power:", 
                ui.output_text(id="power", inline=True),
                #"Current:", 
                ui.output_text(id="current", inline=True),
                #"voltage", 
                ui.output_text(id="voltage", inline=True),
                ui.input_action_button(id="power_off", label="Power Off"),
                ui.input_action_button(id="power_on", label="Power On"),
            )
        ),
        # card:
        ui.card(
            ui.card_header(
                "Flux Sublimator",
                #class_="bg-dark"
            ),
            ui.card_body(
                #ui.markdown("Some text with a [link](https://github.com)"),
                ui.output_text(id="text"),
                ui.output_text(id="text1"),
                ui.output_text(id="text2"),
                ui.output_text(id="text3"),
                ui.output_text(id="rotor_speed_display"),
                ui.input_action_button("open_valve", "Open Valve"),
                ui.input_action_button("close_valve", "Close Valve"),
            )
        ),
        col_widths=[6, 6],
        height="600px",
    ),
    #theme=css_path,
)

def server(input, output, session):
    
    power_status = reactive.Value("OFF")
    power_status.set("OFF")
    
    rotor_speed = reactive.Value("0.0")
    rotor_speed.set("0.0")
    
    @output
    @render.text
    def power_status_display():
        # return f"Status: {power_status()}"
        return f"Status: {input.power_switch()}"
    
    @output
    @render.text
    def power():
        return f"Power: {np.round(5.2*24.0, 4)}"

    @output
    @render.text
    def current():
        return "Current: 5.2"

    @output
    @render.text
    def voltage():
        return "Voltage: 24.0"

    @output
    @render.text
    def text():
        return "Flux Density: 0.03"

    @output
    @render.text
    def text1():
        return "Sublim. Rate: 12.3"

    @output
    @render.text
    def text2():
        return "Reyez Const: 5.6"

    @output
    @render.text
    def text3():
        return "Temp.: 1205.0"

    @output
    @render.text
    def rotor_speed_display():
        return f"Rotor Speed: {rotor_speed()}"


def dynamics(freq: float=0.2):
    """create telemetry"""
    # update period:
    dt = 1.0 / freq
    # time.sleep(dt)  # blocks entire program...
    #await asyncio.sleep(dt)
    
    
    
    



app = App(app_ui, server)
