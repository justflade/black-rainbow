import sys
import os


def wait_for_key():
    """
    Ждет нажатия одной клавиши и возвращает её в унифицированном виде.
    Поддерживает стрелки, w/s/a/d и Ctrl+C.
    Кроссплатформенно: Windows, macOS, Linux, Termux.
    """
    if os.name == "nt":  # Windows
        return _wait_for_key_windows()
    else:  # Unix-like: Linux, macOS, Termux
        return _wait_for_key_unix()


# === Windows ===
def _wait_for_key_windows():
    import msvcrt

    try:
        ch = msvcrt.getch()
        if ch == b"\x03":
            raise KeyboardInterrupt()
        if ch == b"\xe0":
            ch2 = msvcrt.getch()
            return _map_special_key_windows(ch2)
        return ch.decode("utf-8").lower()
    except UnicodeDecodeError:
        return None


def _map_special_key_windows(code):
    mapping = {
        b"H": "up",
        b"P": "down",
        b"K": "left",
        b"M": "right",
    }
    return mapping.get(code, "unknown")


def _wait_for_key_unix():
    import tty
    import termios
    import select

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        if select.select([sys.stdin], [], [], None)[0]:
            ch = sys.stdin.read(1)
            if ord(ch) == 3:  # Ctrl+C
                raise KeyboardInterrupt()

            if ch == "\x1b":
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    next_ch = sys.stdin.read(1)
                    if next_ch == "[":
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            last_ch = sys.stdin.read(1)
                            return _map_arrow_key(last_ch)

                return "esc"
            return ch.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None


def _map_arrow_key(ch):
    mapping = {
        "A": "up",
        "B": "down",
        "C": "right",
        "D": "left",
    }
    return mapping.get(ch, "unknown")
