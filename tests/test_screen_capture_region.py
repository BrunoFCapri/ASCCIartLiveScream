import unittest
import os
import sys
THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from PIL import Image
import numpy as np


class TestScreenCaptureRegion(unittest.TestCase):
    def setUp(self):
        # Import here to allow monkeypatching pyautogui inside module namespace
        from src.core.screen_capture import ScreenCapture, pyautogui  # type: ignore
        self.ScreenCapture = ScreenCapture
        self.pyautogui = pyautogui

        # Stub screenshot to capture args and return a dummy image
        self.called = {'region': None}

        def fake_screenshot(region=None):
            self.called['region'] = region
            # Return a small colored image
            img = Image.new('RGB', (64, 32), color=(123, 45, 67))
            return img

        self._orig_screenshot = self.pyautogui.screenshot
        self.pyautogui.screenshot = fake_screenshot

    def tearDown(self):
        # Restore monkeypatch
        self.pyautogui.screenshot = self._orig_screenshot

    def test_capture_and_resize_with_region(self):
        sc = self.ScreenCapture()
        region = (10, 10, 100, 50)
        arr = sc.capture_and_resize(region=region)

        # Assert our stub was called with the same region
        self.assertEqual(self.called['region'], region)

        # Result should be a numpy array with 3 channels
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.ndim, 3)
        self.assertEqual(arr.shape[2], 3)


if __name__ == '__main__':
    unittest.main()
