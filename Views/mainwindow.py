"""
Ventana principal de la aplicación de Gestión de Torneo de Fútbol.

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

Esta es la ventana raíz que contiene el menú principal y las tarjetas
de navegación a las diferentes secciones de la aplicación.
"""

import sys
import os
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QMenuBar,
    QMenu,
    QMessageBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QAction, QBrush, QColor, QPainter, QPainterPath, QPixmap


def obtener_ruta_recurso(ruta_relativa):
    """
    Obtiene la ruta absoluta de un recurso.
    Compatible con PyInstaller.
    """
    if getattr(sys, "frozen", False):
        ruta_base = sys._MEIPASS
    else:
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(ruta_base, ruta_relativa)


class FondoStackedWidget(QStackedWidget):
    """QStackedWidget con imagen de fondo y overlay para aclararla."""

    def __init__(self, imagen_fondo: str, overlay_alpha: int = 90, parent=None):
        super().__init__(parent)
        self._imagen_fondo = imagen_fondo
        self._overlay_alpha = max(0, min(255, int(overlay_alpha)))
        self.setAutoFillBackground(False)

    def set_overlay_alpha(self, overlay_alpha: int):
        self._overlay_alpha = max(0, min(255, int(overlay_alpha)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        pixmap = QPixmap(self._imagen_fondo)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                rect.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            x = (rect.width() - scaled.width()) // 2
            y = (rect.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)

        # Overlay blanco para aclarar el fondo
        if self._overlay_alpha > 0:
            painter.fillRect(rect, QColor(255, 255, 255, self._overlay_alpha))

        super().paintEvent(event)


class TarjetaNavegacion(QFrame):
    """
    Tarjeta clickeable para navegar a una sección específica.
    """

    clicked = Signal(str)

    def __init__(self, titulo, imagen_fondo, seccion, parent=None):
        super().__init__(parent)
        self.seccion = seccion
        self.imagen_fondo = imagen_fondo
        self.setObjectName("tarjeta_principal")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(250, 150)
        # Permitir que la tarjeta se expanda
        from PySide6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAutoFillBackground(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Estilo base sin imagen de fondo (la imagen se pinta en paintEvent)
        self.setStyleSheet(
            """
            QFrame#tarjeta_principal {
                border-radius: 20px;
                padding: 20px;
            }
        """
        )

        # Título de la tarjeta
        label_titulo = QLabel(titulo)
        label_titulo.setObjectName("tarjeta_titulo")
        label_titulo.setStyleSheet(
            """
            font-size: 22pt;
            font-weight: 800;
            color: white;
            background-color: rgba(0, 0, 0, 120);
            padding: 10px 12px;
            border-radius: 10px;
        """
        )
        label_titulo.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(label_titulo)
        layout.addStretch()

    def paintEvent(self, event):
        """Pinta la imagen de fondo escalada (encajada) sin taparla con overlays."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Recortar para respetar el borde redondeado
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)
        painter.setClipPath(path)

        pixmap = QPixmap(self.imagen_fondo)
        if pixmap.isNull():
            return

        # Escalar para cubrir toda la tarjeta manteniendo proporción
        scaled_pixmap = pixmap.scaled(
            rect.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        # Centrar la imagen dentro de la tarjeta
        x = (rect.width() - scaled_pixmap.width()) // 2
        y = (rect.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)

    def mousePressEvent(self, event):
        """Emite señal cuando se hace click en la tarjeta."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.seccion)
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Torneo de Fútbol")
        # Ajustar a pantallas más pequeñas (portátil)
        self.setMinimumSize(900, 600)
        self.resize(1200, 800)  # Tamaño inicial recomendado

        # Widget central con stack para cambiar entre pantallas (con fondo)
        ruta_fondo = obtener_ruta_recurso("Resources/img/fondo.jpg")
        self.stacked_widget = FondoStackedWidget(ruta_fondo, overlay_alpha=90)
        self.setCentralWidget(self.stacked_widget)

        # Crear página principal
        self.pagina_principal = self.crear_pagina_principal()
        self.stacked_widget.addWidget(self.pagina_principal)

        # Crear páginas de secciones
        from Views.equipos_view import EquiposPage
        from Views.participantes_view import ParticipantesPage
        from Views.calendario_view import CalendarioPage
        from Views.resultados_view import ResultadosPage
        from Views.clasificacion_view import ClasificacionPage

        self.paginas = {
            "equipos": EquiposPage(),
            "participantes": ParticipantesPage(),
            "calendario": CalendarioPage(),
            "resultados": ResultadosPage(),
            "clasificacion": ClasificacionPage(),
        }

        for pagina in self.paginas.values():
            pagina.volver_a_principal.connect(self.volver_a_principal)
            self.stacked_widget.addWidget(pagina)

        # Crear menú
        self.crear_menu()

    def crear_pagina_principal(self):
        """
        Crea la página principal con las tarjetas de navegación.
        """
        widget = QWidget()
        # Transparente para que se vea el fondo del stack
        widget.setAttribute(Qt.WA_TranslucentBackground, True)
        widget.setStyleSheet("background: transparent;")
        layout_principal = QVBoxLayout(widget)
        layout_principal.setContentsMargins(20, 15, 20, 15)
        layout_principal.setSpacing(15)

        # Título principal
        titulo = QLabel("Gestión Torneo de Fútbol")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignCenter)
        # Mismo estilo que las tarjetas: texto blanco y banda oscura translúcida
        titulo.setStyleSheet(
            """
            font-size: 30pt;
            font-weight: 800;
            color: white;
            background-color: rgba(0, 0, 0, 120);
            padding: 12px 18px;
            border-radius: 14px;
            """
        )
        layout_principal.addWidget(titulo)

        # Contenedor de tarjetas con grid layout
        grid_tarjetas = QGridLayout()
        grid_tarjetas.setSpacing(15)

        # Primera fila: Equipos + Participantes | Calendario
        # Crear contenedor para Equipos y Participantes
        contenedor_izq_1 = QWidget()
        contenedor_izq_1.setAttribute(Qt.WA_TranslucentBackground, True)
        contenedor_izq_1.setStyleSheet("background: transparent;")
        layout_izq_1 = QHBoxLayout(contenedor_izq_1)
        layout_izq_1.setSpacing(10)

        # Tarjeta Equipos
        ruta_equipo = obtener_ruta_recurso("Resources/img/equipo.jpg")
        tarjeta_equipos = TarjetaNavegacion("Equipos", ruta_equipo, "equipos")
        tarjeta_equipos.clicked.connect(self.navegar_a_seccion)
        layout_izq_1.addWidget(tarjeta_equipos)

        # Tarjeta Participantes
        ruta_participante = obtener_ruta_recurso("Resources/img/participante.jpg")
        tarjeta_participantes = TarjetaNavegacion(
            "Participantes", ruta_participante, "participantes"
        )
        tarjeta_participantes.clicked.connect(self.navegar_a_seccion)
        layout_izq_1.addWidget(tarjeta_participantes)

        grid_tarjetas.addWidget(contenedor_izq_1, 0, 0)

        # Tarjeta Calendario
        ruta_calendario = obtener_ruta_recurso("Resources/img/calendario.jpg")
        tarjeta_calendario = TarjetaNavegacion(
            "Calendario", ruta_calendario, "calendario"
        )
        tarjeta_calendario.clicked.connect(self.navegar_a_seccion)
        grid_tarjetas.addWidget(tarjeta_calendario, 0, 1)

        # Segunda fila: Resultados | Clasificación
        ruta_resultados = obtener_ruta_recurso("Resources/img/resultados.jpg")
        tarjeta_resultados = TarjetaNavegacion(
            "Resultados", ruta_resultados, "resultados"
        )
        tarjeta_resultados.clicked.connect(self.navegar_a_seccion)
        grid_tarjetas.addWidget(tarjeta_resultados, 1, 0)

        ruta_clasificacion = obtener_ruta_recurso("Resources/img/clasificacion.jpg")
        tarjeta_clasificacion = TarjetaNavegacion(
            "Clasificación", ruta_clasificacion, "clasificacion"
        )
        tarjeta_clasificacion.clicked.connect(self.navegar_a_seccion)
        grid_tarjetas.addWidget(tarjeta_clasificacion, 1, 1)

        # Configurar proporciones de columnas para que sean iguales
        grid_tarjetas.setColumnStretch(0, 1)
        grid_tarjetas.setColumnStretch(1, 1)

        # Configurar proporciones de filas para que sean iguales
        grid_tarjetas.setRowStretch(0, 1)
        grid_tarjetas.setRowStretch(1, 1)

        layout_principal.addLayout(grid_tarjetas, 1)  # stretch = 1
        layout_principal.addStretch(0)  # stretch mínimo al final

        return widget

    def crear_menu(self):
        """
        Crea el menú superior de la aplicación con botones de navegación.
        """
        menubar = self.menuBar()

        # Menú Opciones
        menu_opciones = menubar.addMenu("Opciones")

        # Acción Créditos
        accion_creditos = QAction("Créditos", self)
        accion_creditos.triggered.connect(self.mostrar_creditos)
        menu_opciones.addAction(accion_creditos)

        # Acción Ayuda
        accion_ayuda = QAction("Ayuda", self)
        accion_ayuda.triggered.connect(self.mostrar_ayuda)
        menu_opciones.addAction(accion_ayuda)

        menu_opciones.addSeparator()

        # Acción Salir
        accion_salir = QAction("Salir", self)
        accion_salir.triggered.connect(self.close)
        menu_opciones.addAction(accion_salir)

        # Separador visual
        menubar.addSeparator()

        # Botones de navegación directa
        accion_principal = QAction("Principal", self)
        accion_principal.triggered.connect(self.volver_a_principal)
        menubar.addAction(accion_principal)

        accion_equipos = QAction("Equipos", self)
        accion_equipos.triggered.connect(lambda: self.navegar_a_seccion("equipos"))
        menubar.addAction(accion_equipos)

        accion_participantes = QAction("Participantes", self)
        accion_participantes.triggered.connect(
            lambda: self.navegar_a_seccion("participantes")
        )
        menubar.addAction(accion_participantes)

        accion_calendario = QAction("Calendario", self)
        accion_calendario.triggered.connect(
            lambda: self.navegar_a_seccion("calendario")
        )
        menubar.addAction(accion_calendario)

        accion_resultados = QAction("Resultados", self)
        accion_resultados.triggered.connect(
            lambda: self.navegar_a_seccion("resultados")
        )
        menubar.addAction(accion_resultados)

        accion_clasificacion = QAction("Clasificación", self)
        accion_clasificacion.triggered.connect(
            lambda: self.navegar_a_seccion("clasificacion")
        )
        menubar.addAction(accion_clasificacion)

    def navegar_a_seccion(self, seccion):
        """
        Navega a una sección específica de la aplicación.

        Args:
            seccion (str): Nombre de la sección a mostrar
        """
        try:
            pagina = self.paginas.get(seccion)
            if pagina is None:
                QMessageBox.warning(
                    self, "Navegación", f"Sección no encontrada: {seccion}"
                )
                return

            # Verificar alertas antes de mostrar Calendario o Resultados
            if seccion in ["calendario", "resultados"]:
                self._verificar_alertas()

            self.stacked_widget.setCurrentWidget(pagina)
        except Exception as e:
            print(f"Error al navegar a la sección {seccion}: {e}")
            QMessageBox.critical(
                self,
                "Error de Navegación",
                f"No se pudo cargar la sección '{seccion}'.\nError: {str(e)}",
            )
        if hasattr(pagina, "on_show"):
            try:
                pagina.on_show()
            except Exception:
                pass

    def _verificar_alertas(self):
        """
        Verifica y muestra alertas sobre partidos sin árbitro o pendientes de resultado.
        """
        try:
            from Models.partido import Partido

            # Obtener partidos con problemas
            partidos_sin_arbitro = Partido.obtener_partidos_sin_arbitro()
            partidos_pendientes = Partido.obtener_partidos_pendientes()

            # Construir mensaje de alerta
            mensajes = []

            if partidos_sin_arbitro:
                mensajes.append(
                    f"⚠️ {len(partidos_sin_arbitro)} partido(s) sin árbitro asignado"
                )

            if partidos_pendientes:
                mensajes.append(
                    f"⚠️ {len(partidos_pendientes)} partido(s) pendiente(s) de resultado"
                )

            # Mostrar alerta si hay problemas
            if mensajes:
                QMessageBox.warning(
                    self,
                    "Alertas del Sistema",
                    "\n".join(mensajes)
                    + "\n\nPor favor, complete la información faltante.",
                )
        except Exception as e:
            # Si hay algún error al verificar alertas, lo registramos pero no bloqueamos la navegación
            print(f"Error al verificar alertas: {e}")

    def volver_a_principal(self):
        """
        Vuelve a la pantalla principal.
        """
        self.stacked_widget.setCurrentIndex(0)

    def mostrar_creditos(self):
        """
        Muestra la ventana de créditos.
        """
        from Views.dialogs import CreditosDialog

        dialog = CreditosDialog(self)
        dialog.exec()

    def mostrar_ayuda(self):
        """
        Muestra la ventana de ayuda.
        """
        from Views.dialogs import AyudaDialog

        dialog = AyudaDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la ventana.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar salida")
        msg.setText("¿Está seguro de que desea salir de la aplicación?")
        btn_si = msg.addButton("Sí", QMessageBox.YesRole)
        btn_no = msg.addButton("No", QMessageBox.NoRole)
        msg.setDefaultButton(btn_no)
        msg.exec()

        if msg.clickedButton() == btn_si:
            event.accept()
        else:
            event.ignore()
