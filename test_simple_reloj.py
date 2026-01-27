"""Test simple del reloj"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from reloj_digital import RelojDigital

app = QApplication(sys.argv)
window = QMainWindow()
reloj = RelojDigital()
window.setCentralWidget(reloj)
window.resize(800, 600)
window.show()
print(f"Reloj creado: {reloj}")
print(f"Label del reloj: {reloj.ui.label}")
print(f"Texto del label: {reloj.ui.label.text()}")
sys.exit(app.exec())
