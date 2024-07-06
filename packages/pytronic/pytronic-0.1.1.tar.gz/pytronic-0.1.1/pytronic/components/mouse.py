import pyautogui


class Mouse:
    @staticmethod
    def move_to(x, y):
        """Move the mouse to (x, y)."""
        pyautogui.moveTo(x, y)
        return Mouse

    @staticmethod
    def click_position(x=None, y=None, clicks=1, button='left'):
        """Click at (x, y)."""
        pyautogui.click(x=x, y=y, clicks=clicks, button=button)
        return Mouse

    @staticmethod
    def drag_to(x, y, button='left'):
        """Drag the mouse to (x, y)."""
        pyautogui.dragTo(x, y, button=button)
        return Mouse

    @staticmethod
    def click_in_window_close_button():
        """Click the window close button."""
        close_button_720p = (1270, 10)
        close_button_1080p = (1870, 10)

        screen_width, screen_height = pyautogui.size()

        if screen_height <= 720:
            close_button_position = close_button_720p
        elif screen_height <= 1080:
            close_button_position = close_button_1080p
        else:
            close_button_position = (screen_width - 50, 10)

        pyautogui.moveTo(*close_button_position)
        pyautogui.click(*close_button_position)
        return Mouse

    @staticmethod
    def click_image(image_path, clicks=1, button='left'):
        """Click on the image found on the screen."""
        location = pyautogui.locateOnScreen(image_path)
        if location:
            x, y = pyautogui.center(location)
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            return Mouse
        raise ValueError(f'Image not found on screen: {image_path}')

    @staticmethod
    def move_to_image(image_path):
        """Move the mouse to the image found on the screen."""
        location = pyautogui.locateOnScreen(image_path)
        if location:
            x, y = pyautogui.center(location)
            pyautogui.moveTo(x, y)
            return Mouse
        raise ValueError(f'Image not found on screen: {image_path}')

    @staticmethod
    def drag_and_drop(start, end):
        """Drag from start to end position."""
        pyautogui.moveTo(*start)
        pyautogui.dragTo(*end)
        return Mouse

    @staticmethod
    def scroll(amount):
        """Scroll the screen."""
        pyautogui.scroll(amount)
        return Mouse
