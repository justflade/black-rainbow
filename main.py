from black_rainbow import BlackRainbow, Page, Navigator
from black_rainbow.ui import Menu, Text, MenuItem


app = BlackRainbow()


@app.register_page("/")
def main_page(navigator):
    return Page(
        Text("Главное меню"),
        Menu(
            choices=[
                MenuItem("Профиль", lambda: navigator.navigate("/profile")),
                MenuItem("Настройки", lambda: navigator.navigate("/settings")),
                MenuItem("Выход", lambda: exit()),
            ],
            key="main_menu",
        ),
    )


@app.register_page("/profile")
def profile_page(navigator: Navigator):
    return Page(
        Text("Профиль"),
        Menu(
            choices=[
                MenuItem("Обратно 1", lambda: navigator.navigate("/")),
                MenuItem("Обратно 2", lambda: navigator.back()),
                MenuItem("Выход", lambda: exit()),
            ],
            key="profile_menu",
        ),
    )


@app.register_page("/settings")
def settings_page():
    return Page(Text("Настройки"))


if __name__ == "__main__":
    app.run()
