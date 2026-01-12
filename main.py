from black_rainbow import BlackRainbow, Page, Navigator
from black_rainbow.ui import Menu, Text, MenuItem
from black_rainbow.style import Style


app = BlackRainbow()


@app.register_page("/")
def main_page(navigator: Navigator):
    return Page(
        Text("Главное меню"),
        Menu(
            key="main_menu",
            choices=[
                MenuItem("Профиль", lambda: navigator.navigate("/profile")),
                MenuItem("Настройки", lambda: navigator.navigate("/settings")),
                MenuItem("Выход", lambda: exit()),
            ],
        )
    )

@app.register_page("/settings")
def settings_page(navigator: Navigator):
    return Page(
        Text("Настройки"),
        Menu(
            key="settings_menu",
            pointer="➤",
            unselected_prefix=" ",
            choices=[
                MenuItem("Тема: Светлая", lambda: print("Светлая тема активирована")),
                MenuItem("Язык: Русский", lambda: print("Язык изменён на Русский")),
                MenuItem("Автообновление: Вкл", lambda: print("Автообновление выключено")),
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
                MenuItem("Обратно 1", lambda: navigator.navigate("/")),
                MenuItem("Обратно 2", lambda: navigator.back()),
                MenuItem("Выход", lambda: exit()),
            ],
        ),
    )



if __name__ == "__main__":
    app.run()
