from typing import List, Literal, Callable, Optional, Any
from .style import Style


class _Component:
    def __init__(self, key: str = None):
        self._key = key

    def render(self, state_registry: dict) -> str:
        raise NotImplementedError

    def handle_input(
        self, user_input: str, state_registry
    ) -> Optional[Callable[..., Any]]:
        return None

    def _get_state(self, state_registry: dict) -> dict:
        key = self._key
        if key not in state_registry:
            state_registry[key] = {}
        return state_registry[key]


class Text(_Component):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def render(self, state_registry) -> str:
        return self.text


class MenuItem:
    def __init__(self, text: str, action: Callable):
        self.text = text
        self.action = action


class Menu(_Component):
    def __init__(
        self,
        key,
        choices,
        selected_style: Style = Style(bg="blue"),
        unselected_style: Style = Style(),
        pointer: str = "-> ",
        unselected_prefix: str = "   ",
    ):
        if not choices:
            raise ValueError(
                "Menu 'choices' must not be empty. Provide at least one MenuItem"
            )

        super().__init__(key)
        self.choices = choices
        self.selected_style = selected_style
        self.unselected_style = unselected_style
        self.pointer = pointer
        self.unselected_prefix = unselected_prefix

    def render(self, state_registry: dict) -> str:
        state = self._get_state(state_registry)
        selected = state.get("selected", 0)

        lines = []
        for i, choice in enumerate(self.choices):
            prefix = self.pointer if i == selected else self.unselected_prefix
            full_text = prefix + choice.text
            styled_text = (
                self.selected_style(full_text)
                if i == selected
                else self.unselected_style(full_text)
            )
            lines.append(styled_text)
        return "\n".join(lines)

    def handle_input(self, user_input: str, state_registry: dict) -> Optional[Callable]:
        state = self._get_state(state_registry)
        selected = state.get("selected", 0)
        user_input = user_input.strip().lower()

        if user_input == "w":
            state["selected"] = (selected - 1) % len(self.choices)
            return None
        elif user_input == "s":
            state["selected"] = (selected + 1) % len(self.choices)
            return None
        elif user_input in ["space", "enter"]:
            return self.choices[selected].action
