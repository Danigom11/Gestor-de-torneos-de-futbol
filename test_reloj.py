"""
Script de prueba para el componente RelojDigital.
Prueba el componente autocontenido.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from reloj_digital import RelojDigital


def main():
    app = QApplication(sys.argv)
    
    # Ventana principal para la prueba
    window = QMainWindow()
    window.setWindowTitle("Prueba Componente RelojDigital")
    window.resize(1000, 600)
    
    # Instanciar el componente
    reloj = RelojDigital()
    
    # Añadir a la ventana
    window.setCentralWidget(reloj)
    
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
