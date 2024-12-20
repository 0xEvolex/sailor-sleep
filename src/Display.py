import numpy as np, cv2

def get_screenshot(numpy=True, grayscale=True, resize=None, gaussian_blur=None, threshold=None, dilate=None, erode=None, invert=None):
    import pyautogui
    screenshot = pyautogui.screenshot()

    if numpy:
        screenshot = np.array(screenshot)
    if grayscale:
        screenshot = _grayscaling(screenshot)
    if resize:
        screenshot = _resizing(screenshot)
    if gaussian_blur:
        screenshot = _gaussianbluring(screenshot)
    if threshold:
        screenshot = _thresholding(screenshot)
    if dilate:
        screenshot = _dilating(screenshot)
    if erode:
        screenshot = _eroding(screenshot)
    if invert:
        screenshot = _inverting(screenshot)

    return screenshot

def _resizing(img):
    img = cv2.resize(img, (img.shape[1]*5, img.shape[0]*5), interpolation=cv2.INTER_CUBIC)
    return img

def _grayscaling(img): 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def _gaussianbluring(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img

def _thresholding(img):
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img

def _dilating(img):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    return img

def _eroding(img):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    return img

def _inverting(img):
    img = cv2.bitwise_not(img)
    return img