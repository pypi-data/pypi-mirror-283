import time
from pytronic.components import Keyboard, Mouse, Screen


class ComputerInteraction:
    def __init__(self):
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.screen = Screen()

    def wait_for_image_and_click(self, image_name, timeout=None):
        """Wait for an image to appear on the screen and click it."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                x, y = self.screen.locate_image(image_name)
                self.mouse.click_position(x, y)
                return
            except ValueError:
                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(
                        f'Image {image_name} not found within {timeout} seconds.'
                    )
                time.sleep(1)
        raise TimeoutError(
            f'Image {image_name} not found within {timeout} seconds.'
        )

    def wait_for_image_to_disappear(self, image_name, timeout=None):
        """Wait for an image to disappear from the screen."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                self.screen.locate_image(image_name)
                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(
                        f'Image {image_name} did not disappear within {timeout} seconds.'
                    )
                time.sleep(1)
            except ValueError:
                return
        raise TimeoutError(
            f'Image {image_name} did not disappear within {timeout} seconds.'
        )

    def type_text_when_image_appears(self, image_name, text, timeout=None):
        """Type text when a specific image appears on the screen."""
        self.wait_for_image_and_click(image_name, timeout=timeout)
        self.keyboard.type_text(text)

    def click_image_until_disappears(self, image_name, timeout=None):
        """Click on an image repeatedly until it disappears from the screen or the timeout is reached."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                x, y = self.screen.locate_image(image_name)
                self.mouse.click_position(x, y)
                time.sleep(0.5)  # Adjust sleep duration as needed
            except ValueError:
                return
        raise TimeoutError(
            f'Image {image_name} did not disappear within {timeout} seconds.'
        )

    def wait_for_text_and_type(self, text, input_text, timeout=None):
        """Wait for specific text to appear on the screen and type the given input text."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            screenshot_path = self.screen.take_screenshot_auto_name()
            detected_text = self.screen.ocr_image(screenshot_path.name)
            if text in detected_text:
                self.keyboard.type_text(input_text)
                return
            time.sleep(1)
        raise TimeoutError(f'Text {text} not found within {timeout} seconds.')

    def scroll_until_image_visible(
        self, image_name, direction='down', timeout=None
    ):
        """Scroll the screen until a specific image is visible or the timeout is reached."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                self.screen.locate_image(image_name)
                return
            except ValueError:
                if direction == 'down':
                    self.mouse.scroll(-10)  # Scroll down
                elif direction == 'up':
                    self.mouse.scroll(10)  # Scroll up
                time.sleep(0.5)  # Adjust sleep duration as needed
        raise TimeoutError(
            f'Image {image_name} not found within {timeout} seconds.'
        )

    def wait_for_image_and_double_click(self, image_name, timeout=None):
        """Wait for an image to appear on the screen and double click it."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                x, y = self.screen.locate_image(image_name)
                self.mouse.click_position(x, y, clicks=2)
                return
            except ValueError:
                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(
                        f'Image {image_name} not found within {timeout} seconds.'
                    )
                time.sleep(1)
        raise TimeoutError(
            f'Image {image_name} not found within {timeout} seconds.'
        )

    def capture_screenshot_when_image_appears(self, image_name, timeout=None):
        """Capture a screenshot when a specific image appears on the screen."""
        start_time = time.time()
        while timeout is None or (time.time() - start_time) <= timeout:
            try:
                self.screen.locate_image(image_name)
                screenshot_path = self.screen.take_screenshot_auto_name()
                return screenshot_path
            except ValueError:
                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(
                        f'Image {image_name} not found within {timeout} seconds.'
                    )
                time.sleep(1)
        raise TimeoutError(
            f'Image {image_name} not found within {timeout} seconds.'
        )
