"""
pip install kivy

run:
python kivy_example.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class SimpleGreetingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Arrange widgets vertically
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 15

        # 1. Add a descriptive Label
        self.instruction_label = Label(
            text="Enter your name below:",
            font_size=20,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.instruction_label)

        # 2. Add a TextInput field for user input
        self.name_input = TextInput(
            multiline=False,
            font_size=18,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.name_input)

        # 3. Add a Button to submit the input
        self.submit_btn = Button(
            text="Greet Me!",
            font_size=18,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1) # Soft blue tint
        )
        # Bind the button press event to our custom function
        self.submit_btn.bind(on_press=self.on_button_click)
        self.add_widget(self.submit_btn)

        # 4. Add a larger display Label for the final message
        self.greeting_label = Label(
            text="",
            font_size=24,
            color=(0.1, 0.8, 0.1, 1) # Green text color
        )
        self.add_widget(self.greeting_label)

    def on_button_click(self, instance):
        # Extract text from the input and update the greeting label
        user_name = self.name_input.text.strip()
        if user_name:
            self.greeting_label.text = f"Hello, {user_name}! Welcome to Kivy."
        else:
            self.greeting_label.text = "Please enter a name first!"


class GreetingApp(App):
    def build(self):
        # The build method must return the root widget layout
        self.title = "Kivy Greeting App"
        return SimpleGreetingApp()


if __name__ == '__main__':
    GreetingApp().run()
