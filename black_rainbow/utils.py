import sys
import os


def wait_for_key():
    """
    Waits for a keypress and returns a normalized key name:
    - "w", "s", "a", "d" — for arrow keys (up/down/left/right)
    - "enter" — for Enter
    - "space" — for Space
    - regular ASCII characters (str) — for normal printable characters (e.g., 'q', '1', ' ')
    - raises KeyboardInterrupt on Ctrl+C

    Supports: Windows, Linux, macOS, Termux.
    """
    if os.name == "nt":
        return _wait_for_key_windows()
    else:
        return _wait_for_key_unix()


def _wait_for_key_windows():
    import msvcrt

    try:
        ch = msvcrt.getch()
        if ch == b"\x03":  # Ctrl+C
            raise KeyboardInterrupt()
        if ch == b"\x1b":  # Escape
            return "esc"
        if ch == b"\r":  # Enter
            return "enter"
        if ch == b" ":  # Space
            return "space"
        if ch == b"\xe0":  # Arrows
            ch2 = msvcrt.getch()
            return _map_special_key_windows(ch2)
        # Other symbol
        decoded = ch.decode("utf-8", errors="ignore").lower()
        return decoded if decoded else None
    except Exception:
        return None


def _map_special_key_windows(code):
    return {
        b"H": "w",
        b"P": "s",
        b"K": "a",
        b"M": "d",
    }.get(code, "unknown")


def _wait_for_key_unix():
    import tty
    import termios
    import sys

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        ch = sys.stdin.read(1)

        if ch == "\x03":
            raise KeyboardInterrupt()
        if ch == "\x1b":

            next_ch = sys.stdin.read(1)
            if next_ch == "[":

                while True:
                    code = sys.stdin.read(1)
                    if (
                        code
                        in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~"
                    ):
                        if code == "A":
                            return "w"
                        elif code == "B":
                            return "s"
                        elif code == "C":
                            return "d"
                        elif code == "D":
                            return "a"
                        else:
                            return None
            else:
                return None

        if ch in ("\r", "\n"):
            return "enter"
        if ch == " ":
            return "space"
        if ord(ch) < 128:
            return ch.lower()
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
