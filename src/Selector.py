import sys
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QRect, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen

class RegionSelector(QWidget):
    # Sygnał, który wyślemy po zakończeniu zaznaczania
    region_selected = Signal(QRect)

    def __init__(self):
        super().__init__()
        # Ustawienia okna: brak ramki, zawsze na wierzchu, przezroczystość
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setWindowOpacity(0.3)  # Lekkie przyciemnienie ekranu
        self.setCursor(Qt.CrossCursor)
        self.showFullScreen() # Rozciągnij na cały ekran

        self.begin = QPoint()
        self.end = QPoint()
        self.is_selecting = False

    def paintEvent(self, event):
        if self.is_selecting:
            painter = QPainter(self)
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            # Rysowanie ramki zaznaczenia
            rect = QRect(self.begin, self.end)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.is_selecting = True
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_selecting = False
        final_rect = QRect(self.begin, self.end).normalized()
        
        # Wyślij sygnał z koordynatami i zamknij selektor
        self.region_selected.emit(final_rect)
        self.close()