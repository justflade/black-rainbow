"""UI components for BlackRainbow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from .style import Style

Action = Callable[[], None]


class _Component:
    def __init__(self, key: Optional[str] = None) -> None:
        self._key = key

    def render(self, state_registry: dict[str, dict[str, Any]]) -> str:
        raise NotImplementedError

    def handle_input(
        self, user_input: str, state_registry: dict[str, dict[str, Any]]
    ) -> Optional[Action]:
        return None

    def _get_state(self, state_registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
        if self._key is None:
            return {}
        if self._key not in state_registry:
            state_registry[self._key] = {}
        return state_registry[self._key]


@dataclass()
class Text(_Component):
    text: str

    def __init__(self, text: str) -> None:
        super().__init__(key=None)
        object.__setattr__(self, "text", text)

    def render(self, state_registry: dict[str, dict[str, Any]]) -> str:
        _ = state_registry
        return self.text


@dataclass()
class MenuItem:
    text: str
    action: Action


class Menu(_Component):
    def __init__(
        self,
        key: str,
        choices: list[MenuItem],
        selected_style: Style = Style(bg="blue"),
        unselected_style: Style = Style(),
        pointer: str = "-> ",
        unselected_prefix: str = "   ",
    ) -> None:
        if not choices:
            raise ValueError("Menu 'choices' must contain at least one MenuItem.")

        super().__init__(key)
        self.choices = choices
        self.selected_style = selected_style
        self.unselected_style = unselected_style
        self.pointer = pointer
        self.unselected_prefix = unselected_prefix

    def render(self, state_registry: dict[str, dict[str, Any]]) -> str:
        state = self._get_state(state_registry)
        selected = state.get("selected", 0)

        lines = []
        for i, choice in enumerate(self.choices):
            prefix = self.pointer if i == selected else self.unselected_prefix
            full_text = f"{prefix}{choice.text}"
            style = self.selected_style if i == selected else self.unselected_style
            lines.append(style(full_text))
        return "\n".join(lines)

    def handle_input(
        self, user_input: str, state_registry: dict[str, dict[str, Any]]
    ) -> Optional[Action]:
        state = self._get_state(state_registry)
        selected = state.get("selected", 0)
        normalized = user_input.strip().lower()

        if normalized == "w":
            state["selected"] = (selected - 1) % len(self.choices)
            return None
        if normalized == "s":
            state["selected"] = (selected + 1) % len(self.choices)
            return None
        if normalized in {"space", "enter"}:
            return self.choices[selected].action
        return None
