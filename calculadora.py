from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation='vertical')
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        main_layout.add_widget(self.solution)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    font_size=32,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    background_normal='',
                    background_color=(0.3, 0.3, 0.3, 1)
                )
                button.bind(on_press=self.on_button_press)
                button.bind(on_release=self.on_button_release)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", font_size=32, pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        Window.bind(on_key_down=self.on_key_down)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        instance.background_color = (0.1, 0.6, 0.1, 1)

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_button_release(self, instance):
        instance.background_color = (0.3, 0.3, 0.3, 1)

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(self.solution.text))
                self.solution.text = solution
            except Exception as e:
                self.solution.text = "Erro!" 

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        key_map = {
            48: "0", 49: "1", 50: "2", 51: "3", 52: "4",
            53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
            46: ".", 47: "/", 42: "*", 45: "-", 43: "+", 61: "=",
            13: "="
        }

        if key in key_map:
            key_text = key_map[key]
            if key_text == "=":
                self.on_solution(None)
            else:
                self.on_button_press(Button(text=key_text))
        elif key == 8: 
            current_text = self.solution.text
            self.solution.text = current_text[:-1]

if __name__ == '__main__':
    MainApp().run()
