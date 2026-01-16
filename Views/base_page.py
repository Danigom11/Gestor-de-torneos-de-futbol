"""Componentes base para pantallas.

Cada pantalla de sección comparte:
- Título
- Botón volver a principal
- Contenedor de contenido

"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


class BasePage(QWidget):
    volver_a_principal = Signal()

    def __init__(self, titulo: str, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        # Título centrado sin botón volver
        self.label_titulo = QLabel(titulo)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet(
            """
            font-size: 22pt;
            font-weight: 800;
            color: white;
            background-color: rgba(0, 0, 0, 120);
            padding: 10px 14px;
            border-radius: 14px;
            """
        )

        layout.addWidget(self.label_titulo)

        self.contenido = QWidget()
        self.contenido.setAttribute(Qt.WA_TranslucentBackground, True)
        self.contenido.setStyleSheet("background: transparent;")
        layout.addWidget(self.contenido, 1)

        self._contenido_layout = QVBoxLayout(self.contenido)
        # Margen para que se vea el fondo global alrededor de los paneles.
        self._contenido_layout.setContentsMargins(14, 14, 14, 14)
        self._contenido_layout.setSpacing(14)

    @property
    def contenido_layout(self) -> QVBoxLayout:
        return self._contenido_layout
