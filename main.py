# main.py
from black_rainbow import BlackRainbow, Page
from black_rainbow.ui import Menu, Text, MenuItem

app = BlackRainbow()

@app.register_page("/")
def main_page(navigator):
    return Page(
        Text("Главное меню"),
        Menu(choices=[
            MenuItem("Профиль", lambda: navigator.navigate("/profile")),
            MenuItem("Настройки", lambda: navigator.navigate("/settings")),
            MenuItem("Выход", lambda: exit()),
        ])
    )

@app.register_page("/profile")
def profile_page():
    return Page(Text("Профиль"))

@app.register_page("/settings")
def settings_page():
    return Page(Text("Настройки"))

if __name__ == "__main__":
    app.run()

