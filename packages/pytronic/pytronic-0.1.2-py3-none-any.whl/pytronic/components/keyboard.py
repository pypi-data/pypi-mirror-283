import pyautogui
from contextlib import contextmanager


class Keyboard:
    @staticmethod
    def type_text(text, interval=None):
        """Type the given text."""
        pyautogui.typewrite(text, interval=interval)
        return Keyboard

    @staticmethod
    def press_key(key):
        """Press a specific key."""
        pyautogui.press(key)
        return Keyboard

    @staticmethod
    def hotkey(*keys):
        """Press a combination of keys."""
        pyautogui.hotkey(*keys)
        return Keyboard

    @staticmethod
    def press_left():
        """Press the left arrow key."""
        pyautogui.press('left')
        return Keyboard

    @staticmethod
    def press_right():
        """Press the right arrow key."""
        pyautogui.press('right')
        return Keyboard

    @staticmethod
    def press_up():
        """Press the up arrow key."""
        pyautogui.press('up')
        return Keyboard

    @staticmethod
    def press_down():
        """Press the down arrow key."""
        pyautogui.press('down')
        return Keyboard

    @staticmethod
    @contextmanager
    def hold_key(key):
        """Hold a specific key."""
        pyautogui.keyDown(key)
        try:
            yield
        finally:
            pyautogui.keyUp(key)

    @staticmethod
    @contextmanager
    def hold_ctrl():
        """Hold the Ctrl key."""
        pyautogui.keyDown('ctrl')
        try:
            yield
        finally:
            pyautogui.keyUp('ctrl')

    @staticmethod
    @contextmanager
    def hold_alt():
        """Hold the Alt key."""
        pyautogui.keyDown('alt')
        try:
            yield
        finally:
            pyautogui.keyUp('alt')

    @staticmethod
    @contextmanager
    def hold_shift():
        """Hold the Shift key."""
        pyautogui.keyDown('shift')
        try:
            yield
        finally:
            pyautogui.keyUp('shift')

    @staticmethod
    def copy():
        """Copy selected text."""
        Keyboard.hotkey('ctrl', 'c')
        return Keyboard

    @staticmethod
    def paste():
        """Paste copied text."""
        Keyboard.hotkey('ctrl', 'v')
        return Keyboard

    @staticmethod
    def select_all():
        """Select all text."""
        Keyboard.hotkey('ctrl', 'a')
        return Keyboard
