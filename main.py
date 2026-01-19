from black_rainbow import BlackRainbow, Page, Navigator
from black_rainbow.ui import Menu, Text, MenuItem
from black_rainbow.style import Style


app = BlackRainbow(
    initial_storage={
        "theme": "dark",
        "autoupdate": True
    }
)


@app.register_page("/")
def main_page(navigator: Navigator):
    return Page(
        Text("Главное меню"),
        Menu(
            key="main_menu",
            choices=[
                MenuItem("Профиль", lambda: navigator.go("/profile")),
                MenuItem("Настройки", lambda: navigator.go("/settings")),
                MenuItem("Выход", lambda: exit()),
            ],
        )
    )

@app.register_page("/settings")
def settings_page(navigator: Navigator, storage: dict):

    def toggle_theme():
        if storage["theme"] == "dark":
            storage["theme"] = "light"
        else:
            storage["theme"] = "dark"

    def toggle_autoupdate():
        storage["autoupdate"] = not storage["autoupdate"] 

    theme = "Тёмная" if storage["theme"] == "dark" else "Светлая"
    autoupdate = "Вкл" if storage["autoupdate"] else "Выкл"
 
    return Page(
        Text("Настройки"),
        Menu(
            key="settings_menu",
            pointer="➤  ",
            unselected_prefix="   ",
            choices=[
                MenuItem(f"Тема: {theme}", toggle_theme),
                MenuItem("Язык: Русский", lambda: print("Язык изменён на Русский")),
                MenuItem(f"Автообновление: {autoupdate}", toggle_autoupdate),
                MenuItem("Логирование: Подробное", lambda: print("Уровень логов изменён")),
                MenuItem("Назад", lambda: navigator.back()),
            ],
        )
    )


@app.register_page("/profile")
def profile_page(navigator: Navigator):
    return Page(
        Text("Профиль"),
        Menu(
            key="profile_menu",
            choices=[
                MenuItem("Обратно 1", lambda: navigator.go("/")),
                MenuItem("Обратно 2", lambda: navigator.back()),
                MenuItem("Выход", lambda: exit()),
            ],
        ),
    )


if __name__ == "__main__":
    app.run()
