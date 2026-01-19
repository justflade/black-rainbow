from typing import Union, Optional, Tuple, Any

_RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
STRIKETHROUGH = "\033[9m"

_COLOR_NAMES = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

_BG_COLOR_NAMES = {name: code + 10 for name, code in _COLOR_NAMES.items()}


def _ansi(code: Union[int, str]) -> str:
    return f"\033[{code}m"


class Style:
    """
    Стиль текста с поддержкой ANSI.

    Примеры:
        red = Style(fg="red")
        bold_red = Style(fg="red", bold=True)
        custom = Style(fg=(255, 100, 50))  # RGB
        bg_yellow = Style(bg="yellow")

    Использование:
        print(red("Ошибка!"))
        menu_item = MenuItem(bold_red("Важно"), ...)
    """

    def __init__(
        self,
        fg: Optional[Union[str, int, Tuple[int, int, int]]] = None,
        bg: Optional[Union[str, int, Tuple[int, int, int]]] = None,
        bold: bool = False,
        dim: bool = False,
        italic: bool = False,
        underline: bool = False,
        blink: bool = False,
        reverse: bool = False,
        strikethrough: bool = False,
    ):
        self._parts = []

        if bold:
            self._parts.append(BOLD)
        if dim:
            self._parts.append(DIM)
        if italic:
            self._parts.append(ITALIC)
        if underline:
            self._parts.append(UNDERLINE)
        if blink:
            self._parts.append(BLINK)
        if reverse:
            self._parts.append(REVERSE)
        if strikethrough:
            self._parts.append(STRIKETHROUGH)

        if fg is not None:
            self._parts.append(self._resolve_color(fg, is_bg=False))
        if bg is not None:
            self._parts.append(self._resolve_color(bg, is_bg=True))

    def _resolve_color(
        self, color: Union[str, int, Tuple[int, int, int]], is_bg: bool = False
    ) -> str:
        if isinstance(color, tuple) and len(color) == 3:
            r, g, b = color
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError("RGB values must be in range 0–255")
            mode = 48 if is_bg else 38
            return f"\033[{mode};2;{r};{g};{b}m"
        elif isinstance(color, int):
            if not (0 <= color <= 255):
                raise ValueError("256-color index must be in range 0–255")
            mode = 48 if is_bg else 38
            return f"\033[{mode};5;{color}m"
        elif isinstance(color, str):
            color = color.lower()
            mapping = _BG_COLOR_NAMES if is_bg else _COLOR_NAMES
            if color in mapping:
                return _ansi(mapping[color])
            else:
                raise ValueError(f"Unknown color name: {color}")
        else:
            raise TypeError("Color must be str, int, or (r, g, b) tuple")

    def __call__(self, text: str) -> str:
        """Применяет стиль к тексту."""
        if not self._parts:
            return text
        start = "".join(self._parts)
        return f"{start}{text}{_RESET}"

    def __repr__(self) -> str:
        return f"<Style parts={len(self._parts)}>"
