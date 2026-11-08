# shiny run --reload --host 127.0.0.1 --port 8000 app.py
# http://127.0.0.1:8000
from pathlib import Path
from shiny import App, ui, reactive, render
import asyncio

# ---------------------------------------------------------
# LCARS COLOR PALETTE
# ---------------------------------------------------------
LCARS_BG = "#000000"  # black
LCARS_PANEL = "#332244"
LCARS_ORANGE = "#FF9C41"
LCARS_BLUE = "#6699CC"
LCARS_GOLD = "#CC9966"

# ---------------------------------------------------------
# LCARS STYLES
# ---------------------------------------------------------
lcars_css = """
body {
    background-color: black;
    font-family: 'Eurostile', 'Antonio', sans-serif;
    color: #FFCC66;
    font-weight: bold;
}

.lcars-button {
    padding: 20px;
    margin: 10px;
    width: 300px;
    border-radius: 40px 40px 40px 40px;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    cursor: pointer;
    border: none;
    color: black;
}

.lcars-up {
    background-color: #FF9C41;
}

.lcars-down {
    background-color: #6699CC;
}

.lcars-display {
    background-color: #332244;
    padding: 20px;
    margin: 10px;
    border-radius: 40px;
    width: 300px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #FFCC66;
    border: 3px solid #CC9966;
}
"""

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
app_ui = ui.page_fluid(
    ui.tags.style(lcars_css),

    ui.h2("Elevator Floor Select Panel", 
        style="color:#FF9C41;"),

    ui.div(
        ui.output_text("floor_display"),
        class_="lcars-display",
        #style="display: flex;justify-content: center;align-items: center;"
    ),
    
    ui.div(
        ui.output_text("target_floor_display"),
        class_="lcars-display",
        #style="display: flex;justify-content: center;align-items: center;"
    ),
    
    ui.div(
        ui.output_text("direction_display"),
        class_="lcars-display"
    ),
    
    ui.div(
        ui.input_action_button("select_floor_2", "2", class_="lcars-button lcars-up"),
    ),
    ui.div(    
        ui.input_action_button("select_floor_1", "1", class_="lcars-button lcars-down"),
    ),
    
    ui.h2("For Priorty Calls Tap Card Here", 
        style="color:#FF9C41;"),
        
    # tap icon image:
    ui.img(src="tap_icon.png", height="100px", alt="Tap Here"),
    
    # Audio outputs
    ui.output_ui("chirp_up"),
    ui.output_ui("chirp_down")
)

# ---------------------------------------------------------
# SERVER LOGIC
# ---------------------------------------------------------
def server(input, output, session):

    current_floor = reactive.Value(1)
    target_floor = reactive.Value(None)
    direction = reactive.Value("idle")  # idle
    # timer = reactive.Timer(0.8)
    
    # Sound triggers
    play_up_chirp = reactive.Value(False)
    play_down_chirp = reactive.Value(False)

    # async def move_elevator(target):
    #     """Simulate elevator movement."""
    #     while current_floor() != target:
    #         if current_floor() < target:
    #             direction.set("▲")
    #             await asyncio.sleep(0.8)
    #             current_floor.set(current_floor() + 1)
    #         else:
    #             direction.set("▼")
    #             await asyncio.sleep(0.8)
    #             current_floor.set(current_floor() - 1)
    # 
    #     direction.set("idle")  # idle


    def reset_displays():
        pass

    # Button handlers
    @reactive.effect
    @reactive.event(input.select_floor_1)
    def _():
        target_floor.set(1)
        #direction.set("▲")
        play_up_chirp.set(True)
        play_up_chirp.set(False)
        
        # do something to call state machine

    @reactive.effect
    @reactive.event(input.select_floor_2)
    def _():
        target_floor.set(2)
        #direction.set("▼")
        play_down_chirp.set(True)
        play_down_chirp.set(False)
        
        # do something to call state machine
        

    # @reactive.effect
    # @reactive.event(timer)
    # def _():
    #     tgt = target_floor()
    #     if tgt is None:
    #         return
    # 
    #     cf = current_floor()
    # 
    #     if cf < tgt:
    #         direction.set("↑")
    #         current_floor.set(cf + 1)
    #     elif cf > tgt:
    #         direction.set("↓")
    #         current_floor.set(cf - 1)
    #     else:
    #         direction.set("•")
    #         target_floor.set(None)

    @output
    @render.text
    def floor_display():
        return f"CURRENT FLOOR: {current_floor()}"

    @output
    @render.text
    def target_floor_display():
        return f"Target FLOOR: {target_floor()}"

    @output
    @render.text
    def direction_display():
        return f"MOVE DIRECTION: {direction()}"

    # Chirp audio outputs
    @output
    @render.ui
    def chirp_up():
        if play_up_chirp():
            return ui.tags.audio(
                autoplay=True, 
                src="padd_3.mp3")
        return ""

    @output
    @render.ui
    def chirp_down():
        if play_down_chirp():
            return ui.tags.audio(
                autoplay=True, 
                src="padd_3.mp3")
        return ""


www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)

# host="127.0.0.1", port=8000
