import time
from Globals import Globals
from Display import get_screenshot, _resizing, _thresholding
import cv2
import numpy as np

def detect_image(template_path, step_name=None, find_img_only=False, threshold=0.9, click_position='center'):
    if not Globals.scan_running:
        return False
    processed_screenshot = get_screenshot()
    if isinstance(template_path, str):
        template_gray = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    else:
        template_gray = np.array(template_path)
        template_gray = cv2.cvtColor(template_gray, cv2.COLOR_BGR2GRAY)
        processed_screenshot = np.array(processed_screenshot)
        processed_screenshot = _thresholding(processed_screenshot)
        processed_screenshot = cv2.bitwise_not(processed_screenshot)
        processed_screenshot = _resizing(processed_screenshot) # Increases accuracy but needs to / factor the x,y coordinates again

    result = cv2.matchTemplate(processed_screenshot, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    msg_searching = f"[INFO] Looking for '{template_path}...'"
    if step_name is not None:
        msg_searching = f"[INFO] {step_name}..."

    print(f"[DEBUG] Best threshold found: {max_val}")

    if max_val >= threshold:
        print(f"Found {template_path} with confidence {max_val}")
        return True
    else:
        print(msg_searching)

    return False