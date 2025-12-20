from black_rainbow import BlackRainbow, Page

import time

app = BlackRainbow()


@app.register_page("/")
def main_page():



    return Page(
        header="Header for main",
        caption=f"Caaaaaption"
    )


if __name__ == "__main__":
    app.run()