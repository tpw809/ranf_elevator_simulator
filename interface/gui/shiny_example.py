"""Basic shiny example using python

How to run:
shiny run app.py --reload
open http://127.0.0.1:8000 in browser

to run on a different port:
shiny run app.py --port 5000 --reload
open http://127.0.0.1:5000 in browser


"""
from shiny import App, render, ui

# 1. Define the User Interface (UI)
app_ui = ui.page_fluid(
    ui.h2("Hello Shiny for Python!"),
    ui.input_slider("n", "Choose a number:", 0, 100, 20),
    ui.output_code("txt"),  # Updated from ui.output_text_verbatim
)

# 2. Define the Server Logic
def server(input, output, session):
    @output
    @render.code            # Updated from @render.text
    def txt():
        return f"The doubled value is: {input.n() * 2}"

# 3. Combine into an App
app = App(app_ui, server)


#if __name__ == "__main__":
#    app.run(host="127.0.0.1", port=5000, reload=True)
