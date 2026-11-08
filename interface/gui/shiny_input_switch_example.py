# shiny run --reload app.py
from shiny import App, Inputs, Outputs, Session, render, ui


# this defines the gui itself:
app_ui = ui.page_fluid(
    # this creates the input switch:
    ui.input_switch("somevalue", "Some value", False),
    
    # this displays the switches value by calling the render function
    ui.output_text("value"),
)


# this defines the functionality:
def server(input: Inputs, output: Outputs, session: Session):
    @render.text
    def value():
        return input.somevalue()


app = App(app_ui, server)
