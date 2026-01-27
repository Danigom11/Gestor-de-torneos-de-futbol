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
from PySide6.QtCore import Qt, Signal, QSize, QTranslator
from PySide6.QtWidgets import QApplication
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
        from reloj_digital import RelojDigital

        self.paginas = {
            "equipos": EquiposPage(),
            "participantes": ParticipantesPage(),
            "calendario": CalendarioPage(),
            "resultados": ResultadosPage(),
            "clasificacion": ClasificacionPage(),
            "reloj": self._crear_pagina_reloj(),
        }

        for nombre, pagina in self.paginas.items():
            if (
                nombre != "reloj"
            ):  # La página del reloj no tiene señal volver_a_principal
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

    def _crear_pagina_reloj(self):
        """
        Crea la página del reloj digital con panel de control completo.

        Returns:
            QWidget: Página con el reloj y controles
        """
        from reloj_digital import RelojDigital, Mode
        from PySide6.QtWidgets import (
            QSizePolicy,
            QPushButton,
            QComboBox,
            QSpinBox,
            QLineEdit,
            QCheckBox,
            QGroupBox,
            QFormLayout,
            QGridLayout,
        )

        # Widget contenedor
        contenedor = QWidget()
        contenedor.setAttribute(Qt.WA_TranslucentBackground, True)
        contenedor.setStyleSheet("background: transparent;")

        # Layout principal horizontal (reloj + panel)
        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # === RELOJ (lado izquierdo) ===
        self.reloj_digital = RelojDigital()
        self.reloj_digital.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reloj_digital.alarmTriggered.connect(self._on_alarm_triggered)
        self.reloj_digital.timerFinished.connect(self._on_timer_finished)
        self.reloj_digital.stopwatchUpdated.connect(self._on_stopwatch_updated)
        layout_principal.addWidget(self.reloj_digital, 3)  # 75% del espacio

        # === PANEL DE CONTROL (lado derecho) ===
        panel = QWidget()
        panel.setStyleSheet(
            """
            QWidget {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 15px;
            }
            QGroupBox {
                background-color: rgba(200, 200, 200, 100);
                border: 2px solid rgba(0, 0, 0, 100);
                border-radius: 10px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        )
        layout_panel = QVBoxLayout(panel)
        layout_panel.setSpacing(15)

        # --- SELECTOR DE MODO ---
        group_modo = QGroupBox("Modo de Funcionamiento")
        layout_modo = QVBoxLayout(group_modo)

        self.combo_modo = QComboBox()
        self.combo_modo.addItem("🕐 Reloj", Mode.CLOCK)
        self.combo_modo.addItem("⏱️ Temporizador", Mode.TIMER)
        self.combo_modo.addItem("⏰ Cronómetro", Mode.STOPWATCH)
        self.combo_modo.currentIndexChanged.connect(self._on_mode_changed)
        layout_modo.addWidget(self.combo_modo)

        self.check_24h = QCheckBox("Formato 24 horas")
        self.check_24h.setChecked(True)
        self.check_24h.stateChanged.connect(
            lambda: setattr(
                self.reloj_digital, "is_24_hour", self.check_24h.isChecked()
            )
        )
        layout_modo.addWidget(self.check_24h)

        layout_panel.addWidget(group_modo)

        # --- ALARMA ---
        self.group_alarma = QGroupBox("⏰ Configuración de Alarma")
        layout_alarma = QFormLayout(self.group_alarma)

        self.check_alarma = QCheckBox("Activar alarma")
        self.check_alarma.stateChanged.connect(
            lambda: setattr(
                self.reloj_digital, "alarm_enabled", self.check_alarma.isChecked()
            )
        )
        layout_alarma.addRow(self.check_alarma)

        self.spin_hora_alarma = QSpinBox()
        self.spin_hora_alarma.setRange(0, 23)
        self.spin_hora_alarma.valueChanged.connect(
            lambda v: setattr(self.reloj_digital, "alarm_hour", v)
        )
        self.lbl_hora_alarma = QLabel("Hora:")
        layout_alarma.addRow(self.lbl_hora_alarma, self.spin_hora_alarma)

        self.spin_minuto_alarma = QSpinBox()
        self.spin_minuto_alarma.setRange(0, 59)
        self.spin_minuto_alarma.valueChanged.connect(
            lambda v: setattr(self.reloj_digital, "alarm_minute", v)
        )
        self.lbl_minuto_alarma = QLabel("Minuto:")
        layout_alarma.addRow(self.lbl_minuto_alarma, self.spin_minuto_alarma)

        self.txt_mensaje_alarma = QLineEdit()
        self.txt_mensaje_alarma.setText("¡Alarma activada!")
        self.txt_mensaje_alarma.textChanged.connect(
            lambda t: setattr(self.reloj_digital, "alarm_message", t)
        )
        self.lbl_mensaje_alarma = QLabel("Mensaje:")
        layout_alarma.addRow(self.lbl_mensaje_alarma, self.txt_mensaje_alarma)

        layout_panel.addWidget(self.group_alarma)

        # --- TEMPORIZADOR ---
        self.group_timer = QGroupBox("⏱️ Temporizador")
        layout_timer = QFormLayout(self.group_timer)

        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(1, 7200)
        self.spin_duracion.setValue(60)
        self.spin_duracion.setSuffix(" seg")
        self.spin_duracion.valueChanged.connect(
            lambda v: setattr(self.reloj_digital, "timer_duration", v)
        )
        self.lbl_duracion = QLabel("Duración:")
        layout_timer.addRow(self.lbl_duracion, self.spin_duracion)

        layout_btns_timer = QGridLayout()
        self.btn_timer_start = QPushButton("▶ Iniciar")
        self.btn_timer_start.clicked.connect(self.reloj_digital.start_timer)
        layout_btns_timer.addWidget(self.btn_timer_start, 0, 0)

        self.btn_timer_pause = QPushButton("⏸ Pausar")
        self.btn_timer_pause.clicked.connect(self.reloj_digital.pause_timer)
        layout_btns_timer.addWidget(self.btn_timer_pause, 0, 1)

        self.btn_timer_reset = QPushButton("↻ Reiniciar")
        self.btn_timer_reset.clicked.connect(self.reloj_digital.reset_timer)
        layout_btns_timer.addWidget(self.btn_timer_reset, 1, 0, 1, 2)

        layout_timer.addRow(layout_btns_timer)
        layout_panel.addWidget(self.group_timer)

        # --- CRONÓMETRO ---
        self.group_stopwatch = QGroupBox("⏰ Cronómetro")
        layout_stopwatch = QVBoxLayout(self.group_stopwatch)

        layout_btns_stopwatch = QGridLayout()
        self.btn_stopwatch_start = QPushButton("▶ Iniciar")
        self.btn_stopwatch_start.clicked.connect(self.reloj_digital.start_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_start, 0, 0)

        self.btn_stopwatch_pause = QPushButton("⏸ Pausar")
        self.btn_stopwatch_pause.clicked.connect(self.reloj_digital.pause_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_pause, 0, 1)

        self.btn_stopwatch_reset = QPushButton("↻ Reiniciar")
        self.btn_stopwatch_reset.clicked.connect(self.reloj_digital.reset_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_reset, 1, 0, 1, 2)

        layout_stopwatch.addLayout(layout_btns_stopwatch)
        layout_panel.addWidget(self.group_stopwatch)

        # --- SELECTOR DE IDIOMA ---
        group_idioma = QGroupBox("🌐 Idioma / Language")
        layout_idioma = QVBoxLayout(group_idioma)

        self.combo_idioma = QComboBox()
        self.combo_idioma.setMinimumHeight(35)
        self.combo_idioma.setStyleSheet(
            """
            QComboBox {
                padding: 5px;
                font-size: 12pt;
                background-color: white;
            }
            QComboBox::drop-down {
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #3498db;
                font-size: 12pt;
                padding: 5px;
            }
        """
        )
        self.combo_idioma.addItem("🇪🇸 Español", "es")
        self.combo_idioma.addItem("🇬🇧 English", "en")
        self.combo_idioma.currentIndexChanged.connect(self._on_language_changed)
        layout_idioma.addWidget(self.combo_idioma)

        layout_panel.addWidget(group_idioma)

        # Espaciador
        layout_panel.addStretch()

        layout_principal.addWidget(panel, 1)  # 25% del espacio

        # Guardar referencias a widgets para traducción
        self._texts = {
            "group_modo": group_modo,
            "check_24h": self.check_24h,
            "group_alarma": self.group_alarma,
            "check_alarma": self.check_alarma,
            "group_timer": self.group_timer,
            "group_stopwatch": self.group_stopwatch,
        }

        # Configurar visibilidad inicial
        self._on_mode_changed(0)

        # Guardar referencia a Mode para usar en métodos
        self._Mode = Mode

        return contenedor

    def _on_mode_changed(self, index):
        """Cambia el modo del reloj y actualiza visibilidad de controles."""
        from reloj_digital import Mode

        mode = self.combo_modo.itemData(index)
        self.reloj_digital.mode = mode

        # Mostrar/ocultar grupos según el modo
        self.group_alarma.setVisible(mode == Mode.CLOCK)
        self.group_timer.setVisible(mode == Mode.TIMER)
        self.group_stopwatch.setVisible(mode == Mode.STOPWATCH)
        self.check_24h.setVisible(mode == Mode.CLOCK)

    def _on_stopwatch_updated(self, elapsed_seconds):
        """Maneja la actualización del cronómetro."""
        # Se puede usar para mostrar información adicional si se necesita
        pass

    def _on_language_changed(self, index):
        """Cambia el idioma solo en la ventana del reloj."""
        lang_code = self.combo_idioma.itemData(index)

        # Actualizar textos según el idioma
        if lang_code == "es":
            self._apply_spanish_texts()
        else:
            self._apply_english_texts()

    def _apply_spanish_texts(self):
        """Aplica textos en español a la interfaz del reloj."""
        # Títulos de grupos
        self._texts["group_modo"].setTitle("Modo de Funcionamiento")
        self._texts["check_24h"].setText("Formato 24 horas")
        self._texts["group_alarma"].setTitle("⏰ Configuración de Alarma")
        self._texts["check_alarma"].setText("Activar alarma")
        self._texts["group_timer"].setTitle("⏱️ Temporizador")
        self._texts["group_stopwatch"].setTitle("⏰ Cronómetro")

        # Combo de modo
        self.combo_modo.setItemText(0, "🕐 Reloj")
        self.combo_modo.setItemText(1, "⏱️ Temporizador")
        self.combo_modo.setItemText(2, "⏰ Cronómetro")

        # Labels de formulario
        self.lbl_hora_alarma.setText("Hora:")
        self.lbl_minuto_alarma.setText("Minuto:")
        self.lbl_mensaje_alarma.setText("Mensaje:")
        self.lbl_duracion.setText("Duración:")

        # Botones del temporizador
        self.btn_timer_start.setText("▶ Iniciar")
        self.btn_timer_pause.setText("⏸ Pausar")
        self.btn_timer_reset.setText("↻ Reiniciar")

        # Botones del cronómetro
        self.btn_stopwatch_start.setText("▶ Iniciar")
        self.btn_stopwatch_pause.setText("⏸ Pausar")
        self.btn_stopwatch_reset.setText("↻ Reiniciar")

        # Sufijo del spinbox
        self.spin_duracion.setSuffix(" seg")

        # Actualizar mensaje de alarma si está en inglés
        if self.txt_mensaje_alarma.text() == "Alarm triggered!":
            self.txt_mensaje_alarma.setText("¡Alarma activada!")

    def _apply_english_texts(self):
        """Aplica textos en inglés a la interfaz del reloj."""
        # Títulos de grupos
        self._texts["group_modo"].setTitle("Operating Mode")
        self._texts["check_24h"].setText("24-hour format")
        self._texts["group_alarma"].setTitle("⏰ Alarm Settings")
        self._texts["check_alarma"].setText("Enable alarm")
        self._texts["group_timer"].setTitle("⏱️ Timer")
        self._texts["group_stopwatch"].setTitle("⏰ Stopwatch")

        # Combo de modo
        self.combo_modo.setItemText(0, "🕐 Clock")
        self.combo_modo.setItemText(1, "⏱️ Timer")
        self.combo_modo.setItemText(2, "⏰ Stopwatch")

        # Labels de formulario
        self.lbl_hora_alarma.setText("Hour:")
        self.lbl_minuto_alarma.setText("Minute:")
        self.lbl_mensaje_alarma.setText("Message:")
        self.lbl_duracion.setText("Duration:")

        # Botones del temporizador
        self.btn_timer_start.setText("▶ Start")
        self.btn_timer_pause.setText("⏸ Pause")
        self.btn_timer_reset.setText("↻ Reset")

        # Botones del cronómetro
        self.btn_stopwatch_start.setText("▶ Start")
        self.btn_stopwatch_pause.setText("⏸ Pause")
        self.btn_stopwatch_reset.setText("↻ Reset")

        # Sufijo del spinbox
        self.spin_duracion.setSuffix(" sec")

        # Actualizar mensaje de alarma si está en español
        if self.txt_mensaje_alarma.text() == "¡Alarma activada!":
            self.txt_mensaje_alarma.setText("Alarm triggered!")

        # Actualizar texto del reloj si tiene alarma configurada
        if self.reloj_digital.alarm_message == "¡Alarma activada!":
            self.reloj_digital.alarm_message = "Alarm triggered!"

    def _on_alarm_triggered(self, mensaje):
        """
        Maneja la señal de alarma del reloj.

        Args:
            mensaje (str): Mensaje de la alarma
        """
        QMessageBox.information(self, self.tr("Alarma"), mensaje)

    def _on_timer_finished(self):
        """
        Maneja la señal de finalización del temporizador.
        """
        QMessageBox.information(
            self, self.tr("Temporizador"), self.tr("¡El temporizador ha finalizado!")
        )

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

        accion_reloj = QAction("Reloj", self)
        accion_reloj.triggered.connect(lambda: self.navegar_a_seccion("reloj"))
        menubar.addAction(accion_reloj)

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
