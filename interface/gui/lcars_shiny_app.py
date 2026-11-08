from shiny import App, render, ui, reactive
import random

# Authentic LCARS color palette variables
LCARS_CSS = """
body {
    background-color: #000000;
    color: #FF9933;
    font-family: 'Antonio', 'Arial Narrow', sans-serif;
    text-transform: uppercase;
    padding: 20px;
}

/* LCARS Sidebar Frame Bracket */
.lcars-sidebar {
    background-color: #000;
    border-left: 25px solid #CC99CC;
    border-top: 25px solid #CC99CC;
    border-bottom: 25px solid #CC99CC;
    border-top-left-radius: 40px;
    border-bottom-left-radius: 40px;
    padding: 20px 15px;
    min-height: 80vh;
}

/* LCARS Content Bracket Frame */
.lcars-content-frame {
    border-top: 25px solid #FF9933;
    border-right: 15px solid #FF9933;
    border-top-right-radius: 40px;
    padding: 20px;
    margin-left: -10px;
    min-height: 80vh;
}

/* LCARS Buttons styled like console panels */
.btn-lcars {
    background-color: #FFCC66 !important;
    color: #000000 !important;
    font-weight: bold;
    border: none !important;
    border-radius: 0px 15px 15px 0px !important;
    margin-bottom: 10px;
    text-align: right;
    padding-right: 15px;
    width: 100%;
    font-size: 1.1rem;
}
.btn-lcars:hover {
    background-color: #FF9933 !important;
}

.btn-lcars-blue {
    background-color: #99CCFF !important;
}
.btn-lcars-blue:hover {
    background-color: #3399FF !important;
}

/* Data Readout boxes */
.lcars-readout {
    background-color: #111122;
    border: 2px solid #CC99CC;
    padding: 15px;
    border-radius: 5px;
    font-family: monospace;
    color: #00FF00;
    font-size: 1.2rem;
}

.lcars-header {
    color: #99CCFF;
    font-size: 2rem;
    letter-spacing: 2px;
    margin-bottom: 20px;
    border-bottom: 4px solid #99CCFF;
}

.lcars-text-orange { color: #FF9933; }
.lcars-text-purple { color: #CC99CC; }
"""

app_ui = ui.page_fluid(
    # Injecting the custom LCARS styling sheet
    ui.tags.head(ui.tags.style(LCARS_CSS)),
    
    # Header Banner
    ui.row(
        ui.column(4, ui.h2("LCARS INDEX 402", class_="lcars-text-purple")),
        ui.column(8, ui.h1("USS ENTERPRISE • SYSTEM DIAGNOSTICS", class_="text-end lcars-text-orange")),
    ),
    ui.hr(style="border-top: 5px solid #FFCC66;"),
    
    # Main Interface Layout
    ui.row(
        # Control Panel Sidebar
        ui.column(3, 
            ui.div(
                ui.p("SYS CONTROL", class_="fw-bold lcars-text-purple"),
                ui.input_action_button("btn_warp", "ENGAGE WARP", class_="btn-lcars"),
                ui.input_action_button("btn_shields", "SHIELDS TOGGLE", class_="btn-lcars btn-lcars-blue"),
                ui.input_action_button("btn_scan", "SENSOR SCAN", class_="btn-lcars"),
                ui.div(style="height: 100px; background-color: #CC99CC; margin-top: 20px; border-radius: 0 0 10px 0;"),
                class_="lcars-sidebar"
            )
        ),
        
        # Main Display Screen
        ui.column(9,
            ui.div(
                ui.div("PRIMARY READOUT SYSTEM", class_="lcars-header"),
                
                ui.row(
                    ui.column(6, 
                        ui.h4("Sector Status", class_="lcars-text-orange"),
                        ui.output_ui("txt_status")
                    ),
                    ui.column(6, 
                        ui.h4("Shield Matrix Efficiency", class_="lcars-text-purple"),
                        ui.output_text_verbatim("txt_shields")
                    )
                ),
                ui.br(),
                ui.row(
                    ui.column(12,
                        ui.h4("Tactical Sensor Feed", class_="lcars-text-orange"),
                        ui.output_text_verbatim("txt_console", placeholder=True)
                    )
                ),
                class_="lcars-content-frame"
            )
        )
    )
)

def server(input, output, session):
    # Reactive states for simulator values
    shield_efficiency = reactive.Value(100)
    
    @reactive.Effect
    @reactive.event(input.btn_shields)
    def _():
        # Randomly toggle shield levels when pressed
        shield_efficiency.set(random.randint(12, 100))

    @output
    @render.ui
    def txt_status():
        # Dynamically updates sector readouts based on Warp or Sensor actions
        if input.btn_warp() > 0:
            status_text = "STATUS: EN ROUTE // WARP FACTOR 8.4"
            color = "#99CCFF"
        elif input.btn_scan() > 0:
            status_text = "STATUS: SCANNING SECTOR // ANOMALIES DETECTED"
            color = "#FFCC66"
        else:
            status_text = "STATUS: ORBITAL ANCHOR // SYSTEM IDLE"
            color = "#00FF00"
            
        return ui.div(status_text, class_="lcars-readout", style=f"color: {color};")

    @output
    @render.text
    def txt_shields():
        return f"{shield_efficiency.get()}% — STABLE" if shield_efficiency.get() > 30 else f"{shield_efficiency.get()}% — WARNING: CRITICAL"

    @output
    @render.text
    def txt_console():
        # Logs continuous output to simulate telemetry
        logs = [
            f"LCARS: Core temperature stable.",
            f"Warp Drive Button Hits: {input.btn_warp()}",
            f"Sensor Scan Logs Sequence: {input.btn_scan() * 142}"
        ]
        return "\n".join(logs)

app = App(app_ui, server)
