"""Core application runtime for the BlackRainbow TUI framework."""

from __future__ import annotations

from dataclasses import dataclass
from inspect import signature
import os
from typing import Any, Callable, Dict, Iterable, Optional

from .utils import wait_for_key


PageFactory = Callable[..., "Page"]
Action = Callable[[], None]


class BlackRainbow:
    """Main application container and event loop."""

    def __init__(self, initial_storage: Optional[dict[str, Any]] = None) -> None:
        self._page_functions: Dict[str, PageFactory] = {}
        self._current_path = "/"
        self._history = ["/"]

        self._storage: dict[str, Any] = dict(initial_storage or {})
        self._state_registry: dict[str, dict[str, Any]] = {}
        self._navigator = Navigator(self)

    def register_page(self, path: str) -> Callable[[PageFactory], PageFactory]:
        """Register a page factory for a route-like path."""

        def decorator(func: PageFactory) -> PageFactory:
            self._page_functions[path] = func
            return func

        return decorator

    def _build_page(self, page_factory: PageFactory) -> "Page":
        kwargs: dict[str, Any] = {}
        params = signature(page_factory).parameters

        if "storage" in params:
            kwargs["storage"] = self._storage
        if "navigator" in params:
            kwargs["navigator"] = self._navigator

        page = page_factory(**kwargs)
        page.render(self._state_registry)
        return page

    def run(self) -> None:
        """Start the interactive event loop."""
        if self._current_path not in self._page_functions:
            raise ValueError(f"No page registered for initial path: {self._current_path}")

        while True:
            page_factory = self._page_functions.get(self._current_path)
            if page_factory is None:
                raise ValueError(f"No page registered for path: {self._current_path}")

            rendered_page = self._build_page(page_factory)

            try:
                user_input = wait_for_key()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

            if user_input is None:
                continue

            actions = [
                action
                for component in rendered_page.components
                if (action := component.handle_input(user_input, self._state_registry))
            ]
            for action in actions:
                action()


@dataclass(frozen=True)
class Page:
    """A collection of UI components rendered together."""

    components: Iterable[Any]

    def __init__(self, *components: Any) -> None:
        object.__setattr__(self, "components", components)

    def render(self, state_registry: dict[str, dict[str, Any]]) -> None:
        os.system("cls" if os.name == "nt" else "clear")

        print("----------------")
        for component in self.components:
            output = component.render(state_registry)
            if output:
                print(output)
        print("----------------")


class Navigator:
    """Navigation helper used by page handlers."""

    def __init__(self, app: BlackRainbow) -> None:
        self._app = app

    def go(self, path: str) -> None:
        if path not in self._app._page_functions:
            raise ValueError(f"Cannot navigate to unregistered path: {path}")
        if path != self._app._current_path:
            self._app._history.append(path)
            self._app._current_path = path

    def back(self) -> None:
        if len(self._app._history) > 1:
            self._app._history.pop()
            self._app._current_path = self._app._history[-1]
