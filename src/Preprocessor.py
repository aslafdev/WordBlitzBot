import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap

class BoardProcessor:
    @staticmethod
    def extract_board(img_bgr):
        if img_bgr is None: return None
        
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tile_rects = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.7 < (w/h) < 1.3 and w > 20:
                tile_rects.append((x, y, x + w, y + h))
        
        if len(tile_rects) < 4:
            return None

        x_min = min(r[0] for r in tile_rects)
        y_min = min(r[1] for r in tile_rects)
        x_max = max(r[2] for r in tile_rects)
        y_max = max(r[3] for r in tile_rects)
        
        # WYCIĘCIE: Robimy .copy(), aby uzyskać ciągły blok pamięci dla wyciętego fragmentu
        cropped = img_bgr[y_min:y_max, x_min:x_max].copy()
        return cropped

    @staticmethod
    def to_pixmap(img_bgr):
        """Konwertuje obraz OpenCV na QPixmap bez błędów bufora"""
        if img_bgr is None: return QPixmap()

        # Konwersja na RGB (PySide preferuje ten format)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # KLUCZOWA POPRAWKA: Wymuszenie ciągłości danych w pamięci (C-style)
        img_rgb = np.ascontiguousarray(img_rgb)
        
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        
        # Tworzymy QImage i od razu kopiujemy (copy()), aby PySide posiadał własne dane
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
        return QPixmap.fromImage(q_img)