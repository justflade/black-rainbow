from typing import Dict, Callable, Optional
import inspect, os

from .utils import wait_for_key


class BlackRainbow:
    def __init__(self, initial_storage: Optional[dict] = None):
        self._page_functions: Dict[str, Callable] = {}
        self._current_path = "/"
        self._history = ["/"]

        self._storage = initial_storage or {}
        self._state_registry = {}
        self._navigator = Navigator(self)

    def register_page(self, path: str):
        def decorator(func):
            self._page_functions[path] = func

        return decorator

    def render_page(self, page_function) -> "Page":
        sig = inspect.signature(page_function)
        kwargs = {}

        if "storage" in sig.parameters:
            kwargs["storage"] = self._storage

        if "navigator" in sig.parameters:
            kwargs["navigator"] = self._navigator

        page = page_function(**kwargs)
        page.render(self._state_registry)

        return page

    def run(self):
        while True:
            page_function = self._page_functions[self._current_path]
            rendered_page = self.render_page(page_function)

            try:
                user_input = wait_for_key()
            except (KeyboardInterrupt, EOFError):
                print("\nВыход...")
                break

            if user_input is None:
                continue

            actions = []
            for component in rendered_page._components:
                result = component.handle_input(user_input, self._state_registry)
                if result:
                    actions.append(result)

            for action in actions:
                action()


class Page:
    def __init__(self, *components):
        self._components = components

    def render(self, state_registry: dict):
        os.system("cls" if os.name == "nt" else "clear")

        print("----------------")
        for component in self._components:
            output = component.render(state_registry)
            if output:
                print(output)
        print("----------------")


class Navigator:
    def __init__(self, app):
        self._app = app

    def go(self, path):
        if path != self._app._current_path:
            self._app._history.append(path)
            self._app._current_path = path

    def back(self):
        if len(self._app._history) > 1:
            self._app._history.pop()
            self._app._current_path = self._app._history[-1]
