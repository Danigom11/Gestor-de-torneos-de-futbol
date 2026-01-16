"""Pantalla de Calendario.

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

- Dos paneles translúcidos.
- Izquierda: QCalendarWidget; click abre diálogo de alta/edición de partido.
- Derecha: lista scrollable con "Escudo nombre VS Escudo nombre" + papelera.
- Click en partido abre diálogo para editar.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCalendarWidget,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from Models.equipo import Equipo
from Models.participante import Participante
from Models.partido import Partido
from Views.base_page import BasePage
from Views.dialogs import PartidoDialog
from Views.utils import obtener_ruta_recurso


class _PartidoItem(QWidget):
    def __init__(self, partido: Partido, on_delete, parent=None):
        super().__init__(parent)
        self.partido = partido
        self.setFixedHeight(78)

        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 6, 8, 6)
        main_layout.setSpacing(2)

        # Layout horizontal para equipos y botón eliminar
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        e_local = Equipo.obtener_por_id(partido.equipo_local_id)
        e_vis = Equipo.obtener_por_id(partido.equipo_visitante_id)

        # Escudo local
        svg_l = QSvgWidget(
            obtener_ruta_recurso(f"Resources/img/escudos/{e_local.escudo}")
            if e_local
            else ""
        )
        svg_l.setFixedSize(36, 36)
        layout.addWidget(svg_l, 0, Qt.AlignVCenter)

        # Nombre local
        lbl_local = QLabel(e_local.nombre if e_local else "Local")
        lbl_local.setStyleSheet("font-weight: 700; color: #2c3e50; font-size: 10pt;")
        lbl_local.setWordWrap(False)
        layout.addWidget(lbl_local, 0, Qt.AlignVCenter)

        # VS
        vs = QLabel("VS")
        vs.setStyleSheet("font-weight: 900; color: #3498db; font-size: 10pt;")
        vs.setFixedWidth(28)
        vs.setAlignment(Qt.AlignCenter)
        layout.addWidget(vs, 0, Qt.AlignVCenter)

        # Escudo visitante
        svg_v = QSvgWidget(
            obtener_ruta_recurso(f"Resources/img/escudos/{e_vis.escudo}")
            if e_vis
            else ""
        )
        svg_v.setFixedSize(36, 36)
        layout.addWidget(svg_v, 0, Qt.AlignVCenter)

        # Nombre visitante
        lbl_vis = QLabel(e_vis.nombre if e_vis else "Visitante")
        lbl_vis.setStyleSheet("font-weight: 700; color: #2c3e50; font-size: 10pt;")
        lbl_vis.setWordWrap(False)
        layout.addWidget(lbl_vis, 0, Qt.AlignVCenter)

        layout.addStretch(1)

        # Botón eliminar
        btn_del = QPushButton("×")
        btn_del.setFixedSize(32, 32)
        btn_del.setToolTip("Eliminar partido")
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
        btn_del.clicked.connect(lambda: on_delete(partido))
        layout.addWidget(btn_del, 0, Qt.AlignVCenter)

        # Añadir layout horizontal al layout principal
        main_layout.addLayout(layout)

        # Línea con fecha y árbitro
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(
            44, 0, 0, 0
        )  # Margen izquierdo para alinear con los nombres
        info_layout.setSpacing(8)

        # Obtener árbitro
        arbitro = (
            Participante.obtener_por_id(partido.arbitro_id)
            if partido.arbitro_id
            else None
        )
        arbitro_nombre = arbitro.nombre if arbitro else "Sin árbitro"

        # Formatear fecha
        fecha_texto = partido.fecha_hora if partido.fecha_hora else "Fecha no definida"

        # Label con fecha y árbitro
        lbl_info = QLabel(f"📅 {fecha_texto}  |  🔔 Árbitro: {arbitro_nombre}")
        lbl_info.setStyleSheet("font-size: 8pt; color: #7f8c8d; font-weight: 500;")
        lbl_info.setWordWrap(False)
        info_layout.addWidget(lbl_info, 0, Qt.AlignLeft)
        info_layout.addStretch(1)

        main_layout.addLayout(info_layout)

        self.setStyleSheet(
            """
            QWidget { color: #2c3e50; }
            background-color: rgba(52, 152, 219, 0.15);
            border-radius: 14px;
            """
        )


class CalendarioPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Calendario", parent)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")
        self.contenido_layout.addWidget(splitter, 1)

        self.panel_izq = QFrame()
        self.panel_izq.setObjectName("panel_izquierdo")
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

        izq = QVBoxLayout(self.panel_izq)
        izq.setContentsMargins(15, 15, 15, 15)
        izq.setSpacing(10)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self._click_dia)
        izq.addWidget(self.calendar, 1)

        self.panel_der = QFrame()
        self.panel_der.setObjectName("panel_derecho")
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

        titulo = QLabel("Partidos")
        titulo.setStyleSheet("font-size: 14pt; font-weight: 800; color: #2c3e50;")
        der.addWidget(titulo)

        self.lista = QListWidget()
        self.lista.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lista.itemDoubleClicked.connect(self._editar_seleccionado)
        self.lista.setSpacing(5)
        self.lista.setStyleSheet(
            """
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: rgba(189, 195, 199, 0.3);
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(52, 152, 219, 0.6);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(52, 152, 219, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )
        der.addWidget(self.lista, 1)

        # Ajustar proporciones: 1:1 para que cada panel ocupe la mitad
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        self._refrescar_lista()

    def on_show(self):
        self._refrescar_lista()

    def _click_dia(self, qdate):
        # Crear partido (la fecha del diálogo ya es editable)
        dlg = PartidoDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self._refrescar_lista()

    def _refrescar_lista(self):
        partidos = Partido.obtener_todos()
        self.lista.clear()
        for p in partidos:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, p.id)
            item.setSizeHint(QSize(100, 80))
            self.lista.addItem(item)
            self.lista.setItemWidget(item, _PartidoItem(p, self._eliminar_partido))

    def _editar_seleccionado(self, item: QListWidgetItem):
        partido_id = item.data(Qt.UserRole)
        p = Partido.obtener_por_id(partido_id)
        if not p:
            return
        dlg = PartidoDialog(self, partido=p)
        if dlg.exec() == QDialog.Accepted:
            self._refrescar_lista()

    def _eliminar_partido(self, partido: Partido):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Eliminar")
        msg.setText("¿Eliminar este partido?")
        btn_si = msg.addButton("Sí", QMessageBox.YesRole)
        btn_no = msg.addButton("No", QMessageBox.NoRole)
        msg.setDefaultButton(btn_no)
        msg.exec()
        if msg.clickedButton() != btn_si:
            return
        if not partido.eliminar():
            QMessageBox.critical(self, "Error", "No se pudo eliminar el partido.")
            return
        self._refrescar_lista()
