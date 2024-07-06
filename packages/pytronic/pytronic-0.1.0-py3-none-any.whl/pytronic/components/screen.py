import pyautogui
import pytesseract
import time
from PIL import Image, ImageDraw
from datetime import datetime
from bots.settings import (
    SCREENSHOTS_PATH,
    IMAGES_PATH,
    OCR_LANGUAGE,
    PYTESSERACT_PATH,
)


class Screen:
    def __init__(self):
        self.screenshots_path = SCREENSHOTS_PATH
        self.images_path = IMAGES_PATH
        self.ocr_language = OCR_LANGUAGE
        pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH

    def take_screenshot(self, path, region=None):
        """Takes a screenshot and saves it to the specified path.
        If region is specified, it should be a tuple: (x, y, width, height).
        """
        pyautogui.screenshot(path, region=region)

    def take_screenshot_auto_name(self, region=None):
        """Takes a screenshot and saves it with an automatically generated name based on the current date and time.
        If region is specified, it should be a tuple: (x, y, width, height).
        """
        if not self.screenshots_path.exists():
            self.screenshots_path.mkdir(parents=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = self.screenshots_path / f'screenshot_{timestamp}.png'
        self.take_screenshot(str(path), region=region)
        return path

    def take_screenshot_with_highlight(self, path, region):
        """Takes a full-screen screenshot and highlights a specified region.
        Region should be a tuple: (x, y, width, height).
        """
        screenshot = pyautogui.screenshot()
        img = Image.fromarray(screenshot)
        draw = ImageDraw.Draw(img)
        draw.rectangle(region, outline='red', width=5)
        img.save(path)

    def locate_image(self, image_name):
        """Locate an image on the screen and return its position."""
        image_path = self.images_path / image_name
        location = pyautogui.locateOnScreen(str(image_path))
        if location:
            return pyautogui.center(location)
        raise ValueError(f'Image not found on screen: {image_path}')

    def locate_all_images(self, image_name):
        """Locate all occurrences of an image on the screen and return their positions."""
        image_path = self.images_path / image_name
        locations = pyautogui.locateAllOnScreen(str(image_path))
        centers = [pyautogui.center(loc) for loc in locations]
        return centers

    def ocr_image(self, image_name):
        """Perform OCR on a given image and return the extracted text."""
        image_path = self.images_path / image_name
        text = pytesseract.image_to_string(
            Image.open(image_path), lang=self.ocr_language
        )
        return text

    def ocr_screen_region(self, region):
        """Perform OCR on a specific region of the screen.
        Region should be a tuple: (x, y, width, height).
        """
        screenshot = pyautogui.screenshot(region=region)
        text = pytesseract.image_to_string(screenshot, lang=self.ocr_language)
        return text

    def capture_screen_region(self, region, path):
        """Capture a specific region of the screen and save it to the specified path.
        Region should be a tuple: (x, y, width, height).
        """
        self.take_screenshot(path, region=region)

    def get_pixel_color(self, x, y):
        """Get the color of a specific pixel on the screen."""
        pixel_color = pyautogui.pixel(x, y)
        return pixel_color

    def find_and_click_text(self, text):
        """Find and click on text on the screen using OCR."""
        screenshot = pyautogui.screenshot()
        img = Image.fromarray(screenshot)
        boxes = pytesseract.image_to_boxes(img, lang=self.ocr_language)
        for box in boxes.splitlines():
            b = box.split(' ')
            if b[0] == text:
                x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                pyautogui.click(x + w // 2, y + h // 2)
                return
        raise ValueError(f"Text '{text}' not found on screen")

    def record_screen(self, path, duration):
        """Record the screen for a specified duration and save it to the specified path."""
        try:
            import cv2
            import numpy as np

            screen_size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(
                str(path),
                fourcc,
                20.0,
                (screen_size.width, screen_size.height),
            )

            start_time = time.time()
            while time.time() - start_time < duration:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)

            out.release()
        except Exception:
            print('Screen recording is not supported on this OS.')

    def monitor_screen_region(
        self, region, action_on_change, timeout=None, max_iterations=None
    ):
        """Monitor a region of the screen and execute an action when changes are detected.
        Region should be a tuple: (x, y, width, height).
        The function will stop monitoring after the specified timeout (in seconds) or
        after the specified number of iterations.
        """
        start_time = time.time()
        iterations = 0
        initial_screenshot = pyautogui.screenshot(region=region)

        while (timeout is None or (time.time() - start_time) <= timeout) and (
            max_iterations is None or iterations < max_iterations
        ):
            current_screenshot = pyautogui.screenshot(region=region)
            if initial_screenshot != current_screenshot:
                action_on_change()
                initial_screenshot = current_screenshot

            iterations += 1
            time.sleep(1)
