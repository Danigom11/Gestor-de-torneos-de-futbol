"""Pantalla de Equipos.

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

- Dos paneles translúcidos (izq: formulario, der: lista + filtro).
- Selector de color y selector de escudo (solo disponibles).
- Al seleccionar un equipo de la lista, carga datos a la izquierda.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QColorDialog,
)

from Models.equipo import Equipo
from Models.jugador_equipo import JugadorEquipo
from Models.participante import Participante
from Views.base_page import BasePage
from Views.dialogs import EscudoSelectorDialog
from Views.utils import obtener_ruta_recurso


class _EquipoListItem(QWidget):
    def __init__(self, equipo: Equipo, on_delete, on_edit, parent=None):
        super().__init__(parent)
        self.equipo = equipo

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Escudo (SVG)
        svg_path = obtener_ruta_recurso(f"Resources/img/escudos/{equipo.escudo}")
        svg = QSvgWidget(svg_path)
        svg.setFixedSize(50, 50)
        layout.addWidget(svg, 0, Qt.AlignVCenter)

        info = QVBoxLayout()
        info.setSpacing(2)

        nombre = QLabel(equipo.nombre)
        nombre.setStyleSheet("font-weight: 800; color: #2c3e50; font-size: 11pt;")
        nombre.setWordWrap(False)
        curso = QLabel(f"Curso: {equipo.curso}   Color: {equipo.color}")
        curso.setStyleSheet("color: #34495e; font-size: 9pt;")
        curso.setWordWrap(False)
        info.addWidget(nombre)
        info.addWidget(curso)

        layout.addLayout(info, 1)

        # Botón de editar
        btn_edit = QPushButton("✎")
        btn_edit.setFixedSize(32, 32)
        btn_edit.setToolTip("Editar equipo")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setStyleSheet(
            """
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white; 
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                font-family: 'Segoe UI', 'Arial';
                font-weight: normal; 
                font-size: 16pt;
                padding: 0px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: #21618c;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            """
        )
        btn_edit.clicked.connect(lambda: on_edit(equipo))
        layout.addWidget(btn_edit, 0, Qt.AlignVCenter)

        # Botón de eliminar
        btn_del = QPushButton("×")
        btn_del.setFixedSize(32, 32)
        btn_del.setToolTip("Eliminar equipo")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.setStyleSheet(
            """
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #ee5a6f);
                color: white; 
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                font-family: 'Segoe UI', 'Arial';
                font-weight: normal; 
                font-size: 20pt;
                padding: 0px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff5252, stop:1 #e53935);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: #c62828;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            """
        )
        btn_del.clicked.connect(lambda: on_delete(equipo))
        layout.addWidget(btn_del, 0, Qt.AlignVCenter)

        self.setStyleSheet(
            """
            background-color: rgba(52, 152, 219, 0.15);
            border-radius: 14px;
            border: 1px solid rgba(52, 152, 219, 0.3);
            """
        )


class EquiposPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Equipos", parent)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")
        self.contenido_layout.addWidget(splitter, 1)

        # Panel izquierdo (form)
        self.panel_izq = QFrame()
        self.panel_izq.setObjectName("panel_izquierdo")
        self.panel_izq.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.panel_izq.setStyleSheet(
            """
            QFrame#panel_izquierdo {
                background-color: rgba(255, 255, 255, 210);
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }
            QFrame#panel_izquierdo QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
        """
        )
        splitter.addWidget(self.panel_izq)

        # LAYOUT PRINCIPAL DEL PANEL IZQUIERDO
        izq = QVBoxLayout(self.panel_izq)
        izq.setContentsMargins(15, 15, 15, 15)
        izq.setSpacing(10)

        self._equipo_actual: Equipo | None = None
        self._color_actual = "#3498db"
        self._escudo_actual: str | None = None

        # Inputs
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre")
        self.txt_nombre.editingFinished.connect(self._actualizar_preview)

        self.txt_curso = QComboBox()
        self.txt_curso.setEditable(True)
        self.txt_curso.addItems(
            ["1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bach", "2º Bach"]
        )
        self.txt_curso.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px 8px;
                padding-right: 30px;
                font-size: 10pt;
                min-height: 24px;
            }
            QComboBox:hover {
                border-color: #95a5a6;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #2c3e50;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )
        # No conectar evento para mejor rendimiento

        # Fila de Color
        fila_color = QHBoxLayout()
        lbl_color_titulo = QLabel("Color:")
        lbl_color_titulo.setStyleSheet("font-weight: 700; color: #2c3e50;")
        self.btn_color = QPushButton("Elegir color")
        self.btn_color.setToolTip("Seleccionar color de camiseta del equipo")
        self.btn_color.setFixedHeight(36)
        self.btn_color.setMinimumWidth(120)
        self.btn_color.setStyleSheet(
            """
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            """
        )
        self.btn_color.clicked.connect(self._elegir_color)
        fila_color.addWidget(lbl_color_titulo)
        fila_color.addWidget(self.btn_color)
        fila_color.addStretch(1)

        # Fila de Escudo
        fila_escudo = QHBoxLayout()
        lbl_escudo_titulo = QLabel("Escudo:")
        lbl_escudo_titulo.setStyleSheet("font-weight: 700; color: #2c3e50;")
        self.preview_escudo = QSvgWidget()
        self.preview_escudo.setFixedSize(36, 36)
        self.preview_escudo.setVisible(False)
        self.btn_escudo = QPushButton("Elegir escudo")
        self.btn_escudo.setToolTip(
            "Seleccionar escudo del equipo de la galería disponible"
        )
        self.btn_escudo.setFixedHeight(36)
        self.btn_escudo.setMinimumWidth(120)
        self.btn_escudo.setStyleSheet(
            """
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            """
        )
        self.btn_escudo.clicked.connect(self._elegir_escudo)
        fila_escudo.addWidget(lbl_escudo_titulo)
        fila_escudo.addWidget(self.preview_escudo)
        fila_escudo.addWidget(self.btn_escudo)
        fila_escudo.addStretch(1)

        # =====================================================================
        # TARJETA DE PREVIEW
        # =====================================================================
        self.tarjeta_preview = QFrame()
        self.tarjeta_preview.setFixedHeight(320)
        # Borde limpio, sin sombras raras que confundan
        self.tarjeta_preview.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self._color_actual};
                border-radius: 16px;
                border: 1px solid rgba(0,0,0,0.1);
            }}
            """
        )

        layout_tarjeta = QVBoxLayout(self.tarjeta_preview)
        # Margen superior generoso para separar el texto del borde
        layout_tarjeta.setContentsMargins(20, 25, 20, 20)
        layout_tarjeta.setSpacing(5)

        # 1. Nombre (Alineado ARRIBA)
        self.lbl_preview_nombre = QLabel("Nombre del equipo")
        self.lbl_preview_nombre.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.lbl_preview_nombre.setWordWrap(True)
        self.lbl_preview_nombre.setStyleSheet(
            """
            color: white;
            font-size: 18pt;
            font-weight: 800;
            background: transparent;
            """
        )
        # Importante: Fixed vertical para que no ocupe más de lo que debe
        self.lbl_preview_nombre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 2. Curso (Alineado ARRIBA, justo debajo del nombre)
        self.lbl_preview_curso = QLabel("Curso")
        self.lbl_preview_curso.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.lbl_preview_curso.setStyleSheet(
            """
            color: rgba(255, 255, 255, 0.9);
            font-size: 12pt;
            font-weight: 600;
            background: transparent;
            """
        )
        self.lbl_preview_curso.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 3. Escudo (Alineado al CENTRO del espacio restante)
        self.svg_preview_escudo = QSvgWidget()
        # Tamaño máximo controlado para que no se deforme ni se haga gigante
        self.svg_preview_escudo.setMaximumSize(160, 160)
        self.svg_preview_escudo.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.svg_preview_escudo.setVisible(False)

        # --- AÑADIR ELEMENTOS A LA TARJETA ---
        layout_tarjeta.addWidget(self.lbl_preview_nombre)
        layout_tarjeta.addWidget(self.lbl_preview_curso)

        # Espacio flexible para empujar el escudo un poco hacia abajo,
        # pero dejando que el escudo ocupe el resto
        layout_tarjeta.addSpacing(10)

        # El escudo va con aligment Center para que flote en el medio del espacio libre
        layout_tarjeta.addWidget(self.svg_preview_escudo, 1, Qt.AlignCenter)

        # =====================================================================

        # BOTÓN REGISTRAR
        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setObjectName("boton_primario")
        self.btn_registrar.setToolTip("Guardar el equipo en la base de datos")
        self.btn_registrar.setMinimumHeight(45)
        self.btn_registrar.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: 700;
                font-size: 12pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: #21618c;
            }
            """
        )
        self.btn_registrar.clicked.connect(self._guardar_equipo)

        # --- MONTAJE PANEL IZQUIERDO (ORDEN CRÍTICO) ---
        izq.addWidget(self.txt_nombre)
        izq.addWidget(self.txt_curso)
        izq.addLayout(fila_color)
        izq.addLayout(fila_escudo)

        # 1. Añadimos la tarjeta
        izq.addWidget(self.tarjeta_preview)

        # 2. Añadimos ESPACIO FIJO (30px) entre tarjeta y botón
        # Esto asegura que el botón NUNCA toque la tarjeta
        izq.addSpacing(30)

        # 3. Añadimos el botón
        izq.addWidget(self.btn_registrar)

        # 4. Añadimos un Stretch al final para que empuje todo hacia arriba
        # y rellene el vacío inferior del panel, no entre los elementos.
        izq.addStretch(1)
        # --------------------------------------------------

        # Panel derecho (lista)
        self.panel_der = QFrame()
        self.panel_der.setObjectName("panel_derecho")
        self.panel_der.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.panel_der.setStyleSheet(
            """
            QFrame#panel_derecho {
                background-color: rgba(255, 255, 255, 210);
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }
            QFrame#panel_derecho QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
        """
        )
        splitter.addWidget(self.panel_der)

        der = QVBoxLayout(self.panel_der)
        der.setContentsMargins(15, 15, 15, 15)
        der.setSpacing(10)

        titulo_lista = QLabel("Lista de equipos")
        titulo_lista.setStyleSheet("font-size: 14pt; font-weight: 800; color: #2c3e50;")
        der.addWidget(titulo_lista)

        self.txt_filtro = QLineEdit()
        self.txt_filtro.setPlaceholderText("Filtrar por nombre/curso...")
        self.txt_filtro.textChanged.connect(self._refrescar_lista)
        der.addWidget(self.txt_filtro)

        self.lista = QListWidget()
        self.lista.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lista.itemClicked.connect(self._mostrar_jugadores)
        der.addWidget(self.lista, 1)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        self._refrescar_lista()
        self._actualizar_labels()

    def on_show(self):
        self._refrescar_lista()

    def _actualizar_labels(self):
        # Actualizar el fondo del botón de color
        self.btn_color.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self._color_actual};
                color: white;
                border: 2px solid {self._color_actual};
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                opacity: 0.9;
                border-color: #2c3e50;
            }}
            """
        )

        # Actualizar el preview del escudo pequeño
        if self._escudo_actual:
            self.preview_escudo.load(
                obtener_ruta_recurso(f"Resources/img/escudos/{self._escudo_actual}")
            )
            self.preview_escudo.setVisible(True)
        else:
            self.preview_escudo.setVisible(False)

        self.btn_registrar.setText("Guardar" if self._equipo_actual else "Registrar")

        # Actualizar la tarjeta de preview
        self._actualizar_preview()

    def _actualizar_preview(self):
        """Actualiza la tarjeta de preview con los datos actuales del formulario."""
        # Actualizar color de fondo de la tarjeta
        self.tarjeta_preview.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self._color_actual};
                border-radius: 16px;
                border: 1px solid rgba(0,0,0,0.1);
            }}
            """
        )

        # Actualizar nombre (solo texto, sin cambiar estilo)
        nombre = self.txt_nombre.text().strip()
        if nombre:
            self.lbl_preview_nombre.setText(nombre)
        else:
            self.lbl_preview_nombre.setText("Nombre del equipo")

        # Actualizar curso (solo texto, sin cambiar estilo)
        curso = self.txt_curso.currentText().strip()
        if curso:
            self.lbl_preview_curso.setText(curso)
        else:
            self.lbl_preview_curso.setText("Curso")

        # Actualizar escudo
        if self._escudo_actual:
            self.svg_preview_escudo.load(
                obtener_ruta_recurso(f"Resources/img/escudos/{self._escudo_actual}")
            )
            self.svg_preview_escudo.setVisible(True)
        else:
            self.svg_preview_escudo.setVisible(False)

    def _elegir_color(self):
        dlg = QColorDialog(QColor(self._color_actual), self)
        dlg.setWindowTitle("Color de camiseta")
        # Configurar opciones para mostrar en español
        dlg.setOption(QColorDialog.DontUseNativeDialog, True)
        dlg.setStyleSheet(
            """
            QColorDialog {
                background-color: white;
            }
            QColorDialog QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
            QColorDialog QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
                min-width: 80px;
            }
            QColorDialog QPushButton:hover {
                background-color: #2980b9;
            }
            QColorDialog QLineEdit, QColorDialog QSpinBox {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )
        if dlg.exec():
            color = dlg.selectedColor()
            if color.isValid():
                self._color_actual = color.name()
                self._actualizar_labels()

    def _elegir_escudo(self):
        dlg = EscudoSelectorDialog(self)
        if dlg.exec():
            self._escudo_actual = dlg.seleccion()
            self._actualizar_labels()

    def _validar(self) -> bool:
        if not self.txt_nombre.text().strip():
            QMessageBox.warning(self, "Datos", "El nombre es obligatorio.")
            return False
        if not self.txt_curso.currentText().strip():
            QMessageBox.warning(self, "Datos", "El curso es obligatorio.")
            return False
        if not self._escudo_actual:
            QMessageBox.warning(self, "Datos", "Selecciona un escudo.")
            return False
        return True

    def _guardar_equipo(self):
        if not self._validar():
            return

        if self._equipo_actual is None:
            equipo = Equipo(
                nombre=self.txt_nombre.text().strip(),
                curso=self.txt_curso.currentText().strip(),
                color=self._color_actual,
                escudo=self._escudo_actual or "",
            )
        else:
            equipo = self._equipo_actual
            equipo.nombre = self.txt_nombre.text().strip()
            equipo.curso = self.txt_curso.currentText().strip()
            equipo.color = self._color_actual
            equipo.escudo = self._escudo_actual or equipo.escudo

        if not equipo.guardar():
            QMessageBox.critical(self, "Error", "No se pudo guardar el equipo.")
            return

        self._equipo_actual = None
        self.txt_nombre.clear()
        self.txt_curso.setCurrentIndex(0)
        self._color_actual = "#3498db"
        self._escudo_actual = None
        self._actualizar_labels()
        self._refrescar_lista()

    def _refrescar_lista(self):
        texto = self.txt_filtro.text().strip()
        equipos = Equipo.buscar(texto) if texto else Equipo.obtener_todos()

        self.lista.clear()
        for e in equipos:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, e.id)
            # Altura suficiente para mostrar todo sin cortes (escudo 50px + márgenes 20px + borde)
            item.setSizeHint(QSize(100, 90))

            widget = _EquipoListItem(e, self._eliminar_equipo, self._editar_equipo)
            self.lista.addItem(item)
            self.lista.setItemWidget(item, widget)

    def _mostrar_jugadores(self, item):
        """Muestra un diálogo con los jugadores del equipo seleccionado."""
        equipo_id = item.data(Qt.UserRole)
        equipo = Equipo.obtener_por_id(equipo_id)
        if not equipo:
            return

        # Crear y mostrar el diálogo
        dialogo = JugadoresEquipoDialog(equipo, self)
        dialogo.exec()

    def _editar_equipo(self, equipo: Equipo):
        """Carga los datos del equipo en el formulario para editarlo."""
        self._equipo_actual = equipo
        self.txt_nombre.setText(equipo.nombre)
        self.txt_curso.setCurrentText(equipo.curso)
        self._color_actual = equipo.color
        self._escudo_actual = equipo.escudo
        self._actualizar_labels()

    def _eliminar_equipo(self, equipo: Equipo):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Eliminar")
        msg.setText(f"¿Eliminar el equipo '{equipo.nombre}'?")
        msg.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 10pt;
                font-weight: 600;
            }
            QMessageBox QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QMessageBox QPushButton:pressed {
                background-color: #bdc3c7;
            }
            """
        )
        btn_si = msg.addButton("Sí", QMessageBox.YesRole)
        btn_no = msg.addButton("No", QMessageBox.NoRole)
        msg.setDefaultButton(btn_no)
        msg.exec()
        if msg.clickedButton() != btn_si:
            return

        if not equipo.eliminar():
            QMessageBox.critical(self, "Error", "No se pudo eliminar el equipo.")
            return

        self._refrescar_lista()


class JugadoresEquipoDialog(QDialog):
    """Diálogo que muestra los jugadores de un equipo."""

    def __init__(self, equipo: Equipo, parent=None):
        super().__init__(parent)
        self.equipo = equipo
        self.setWindowTitle(f"Jugadores de {equipo.nombre}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        titulo = QLabel(f"Jugadores del equipo: {equipo.nombre}")
        titulo.setStyleSheet("font-size: 14pt; font-weight: 800; color: #2c3e50;")
        layout.addWidget(titulo)

        # Obtener jugadores del equipo
        jugadores_ids = JugadorEquipo.obtener_jugadores_de_equipo(equipo.id)

        if not jugadores_ids:
            msg = QLabel("Este equipo no tiene jugadores asignados.")
            msg.setStyleSheet(
                "color: #7f8c8d; font-size: 10pt; font-style: italic; padding: 20px;"
            )
            msg.setAlignment(Qt.AlignCenter)
            layout.addWidget(msg)
        else:
            # Lista de jugadores
            lista = QListWidget()
            lista.setStyleSheet(
                """
                QListWidget {
                    background-color: white;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    padding: 5px;
                }
                QListWidget::item {
                    padding: 10px;
                    border-bottom: 1px solid #ecf0f1;
                }
                QListWidget::item:hover {
                    background-color: #ecf0f1;
                }
                """
            )

            for jugador_id in jugadores_ids:
                participante = Participante.obtener_por_id(jugador_id)
                if participante:
                    texto = f"{participante.nombre} - {participante.posicion}"
                    if participante.goles > 0:
                        texto += f" | Goles: {participante.goles}"
                    if participante.t_amarillas > 0:
                        texto += f" | T.Amarillas: {participante.t_amarillas}"
                    if participante.t_rojas > 0:
                        texto += f" | T.Rojas: {participante.t_rojas}"

                    item = QListWidgetItem(texto)
                    lista.addItem(item)

            layout.addWidget(lista)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFixedHeight(40)
        btn_cerrar.setMinimumWidth(120)
        btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cerrar.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 700;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: #21618c;
            }
            """
        )
        btn_cerrar.clicked.connect(self.accept)

        layout_btn = QHBoxLayout()
        layout_btn.addStretch(1)
        layout_btn.addWidget(btn_cerrar)
        layout.addLayout(layout_btn)

        # Estilo del diálogo
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            """
        )
