import sys
import cv2 # Dodane do importów
from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                             QLabel, QApplication, QScrollArea)
from PySide6.QtCore import Qt, Slot, QRect
from Selector import RegionSelector
from BoardCapture import BoardCapturer
from Preprocessor import BoardProcessor # Nowy import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Blitz Bot v2")
        self.setGeometry(100, 100, 500, 600)

        self.capturer = BoardCapturer()
        self.processor = BoardProcessor() # Inicjalizacja procesora
        self.game_area = None

        # --- UI ---
        self.label_info = QLabel("Status: Najpierw zaznacz obszar gry")
        
        self.btn_select = QPushButton("1. Zaznacz obszar planszy (Raz)")
        self.btn_select.clicked.connect(self.start_selection)

        self.btn_capture = QPushButton("2. Pobierz planszę (Nowa runda)")
        self.btn_capture.setEnabled(False)
        self.btn_capture.clicked.connect(self.capture_current_round)

        self.image_label = QLabel("Tu pojawi się wycięta plansza")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_capture)
        layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_selection(self):
        self.hide()
        self.selector = RegionSelector()
        self.selector.region_selected.connect(self.on_region_picked)

    @Slot(QRect)
    def on_region_picked(self, rect):
        self.show()
        if rect.width() < 10 or rect.height() < 10: return

        self.game_area = {"left": rect.x(), "top": rect.y(), "width": rect.width(), "height": rect.height()}
        self.image_label.clear() # Czyścimy stary widok
        self.label_info.setText("Obszar zapisany. Kliknij 'Pobierz planszę'")
        self.btn_capture.setEnabled(True)

    def capture_current_round(self):
        if not self.game_area: return
            
        # 1. Pobierz surowy obraz (NumPy BGR)
        raw_img = self.capturer.get_raw_image(self.game_area)
        
        # 2. Przetwórz (Wytnij planszę)
        board_img = self.processor.extract_board(raw_img)
        
        if board_img is not None:
            # 3. Konwertuj tylko wycięty fragment do QPixmap i pokaż
            pixmap = self.processor.to_pixmap(board_img)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.size())
            self.label_info.setText("Status: Wycięto planszę")
        else:
            self.label_info.setText("Status: Nie znaleziono planszy na zrzucie!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())