from mss.windows import MSS as mss
import numpy as np
import cv2

class BoardCapturer:
    def __init__(self):
        self.sct = mss()

    def get_raw_image(self, region):
        sct_img = self.sct.grab(region)
        # mss zwraca BGRA, konwertujemy na BGR dla OpenCV
        img_np = np.array(sct_img)
        return cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)