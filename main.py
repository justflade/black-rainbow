"""Sample application that demonstrates the BlackRainbow TUI framework."""

from black_rainbow import BlackRainbow, Navigator, Page
from black_rainbow.ui import Menu, MenuItem, Text


app = BlackRainbow(initial_storage={"theme": "dark", "autoupdate": True})


@app.register_page("/")
def main_page(navigator: Navigator) -> Page:
    return Page(
        Text("Main menu"),
        Menu(
            key="main_menu",
            choices=[
                MenuItem("Profile", lambda: navigator.go("/profile")),
                MenuItem("Settings", lambda: navigator.go("/settings")),
                MenuItem("Exit", lambda: exit()),
            ],
        ),
    )


@app.register_page("/settings")
def settings_page(navigator: Navigator, storage: dict) -> Page:
    def toggle_theme() -> None:
        storage["theme"] = "light" if storage["theme"] == "dark" else "dark"

    def toggle_autoupdate() -> None:
        storage["autoupdate"] = not storage["autoupdate"]

    theme = "Dark" if storage["theme"] == "dark" else "Light"
    autoupdate = "On" if storage["autoupdate"] else "Off"

    return Page(
        Text("Settings"),
        Menu(
            key="settings_menu",
            pointer="➤  ",
            unselected_prefix="   ",
            choices=[
                MenuItem(f"Theme: {theme}", toggle_theme),
                MenuItem("Language: English", lambda: print("Language set to English")),
                MenuItem(f"Auto-update: {autoupdate}", toggle_autoupdate),
                MenuItem("Logging: Verbose", lambda: print("Log level changed")),
                MenuItem("Back", navigator.back),
            ],
        ),
    )


@app.register_page("/profile")
def profile_page(navigator: Navigator) -> Page:
    return Page(
        Text("Profile"),
        Menu(
            key="profile_menu",
            choices=[
                MenuItem("Home", lambda: navigator.go("/")),
                MenuItem("Back", navigator.back),
                MenuItem("Exit", lambda: exit()),
            ],
        ),
    )


if __name__ == "__main__":
    app.run()
