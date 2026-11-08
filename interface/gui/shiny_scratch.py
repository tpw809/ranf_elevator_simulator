# shiny run --reload app.py
import numpy as np
import matplotlib.pyplot as plt

from shiny import App, Inputs, Outputs, Session, render, ui


# this defines the gui itself:
app_ui = ui.page_fluid(
    
    ui.input_switch(
        id="switchvalue", 
        label="Some value", 
        value=False,
        width=None,
    ),
    # display the render of switch_value
    ui.output_text("switch_value"),
    
    # creates input checkbox widget:
    ui.input_checkbox(
        id="checkboxvalue", 
        label="Some value", 
        value=False,
    ),
    # displays checkbox value in the gui by calling render function
    ui.output_ui("checkbox_value"),
    
    # creates input slide widget in gui:
    ui.input_slider(
        id="obs", 
        label="Number of bins:", 
        min=10, 
        max=100, 
        value=30,
    ),
    # displays plot in the gui:
    ui.output_plot("distPlot"),
    
)


def server(input: Inputs, output: Outputs, session: Session):
    
    @render.ui
    def checkbox_value():
        return input.checkboxvalue()

    @render.text
    def switch_value():
        return input.switchvalue()

    @render.plot
    def distPlot():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)

        fig, ax = plt.subplots()
        ax.hist(x, input.obs(), density=True)
        return fig



app = App(app_ui, server)




"""
https://shiny.posit.co/py/api/core/ui.input_slider.html

ui.input_slider(
    id,
    label,
    min,
    max,
    value,
    *,
    step=None,
    ticks=False,
    animate=False,
    width=None,
    sep=',',
    pre=None,
    post=None,
    time_format=None,
    timezone=None,
    drag_range=True,
)

https://shiny.posit.co/py/api/core/ui.input_checkbox.html

ui.input_checkbox(
    id, 
    label, 
    value=False, 
    *, 
    width=None,
)


https://shiny.posit.co/py/api/core/ui.input_switch.html

ui.input_switch(
    id, 
    label, 
    value=False, 
    *, 
    width=None,
)


"""