"""Diálogos reutilizables (selector de escudo, alta/edición de partido)."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from Models.equipo import Equipo
from Models.participante import Participante
from Models.partido import Partido
from Views.utils import obtener_ruta_recurso


class EscudoSelectorDialog(QDialog):
    """Muestra únicamente escudos disponibles y permite seleccionar uno."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar escudo")
        self.setModal(True)
        # Hacemos el diálogo un poco más ancho para que quepan bien los 5 escudos
        self.setMinimumSize(900, 600)

        # Fondo blanco para el diálogo
        self.setStyleSheet("QDialog { background-color: white; }")

        self._seleccion: str | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        titulo = QLabel("Escudos disponibles")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            """
            font-size: 18pt;
            font-weight: 800;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #3498db, stop:1 #2980b9);
            padding: 14px 20px;
            border-radius: 14px;
            """
        )
        layout.addWidget(titulo)

        # Usamos QListWidget en modo IconMode para mejor visualización y gestión
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setResizeMode(QListWidget.Adjust)  # Se ajusta al ancho
        self.list_widget.setMovement(QListWidget.Static)  # No se pueden mover
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.setSpacing(15)
        self.list_widget.setIconSize(QSize(120, 120))

        # Estilos para que se vea limpio y la selección sea clara
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: white;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: #fdfdfd;
                border: 2px solid #ecf0f1;
                border-radius: 12px;
                padding: 10px;
                color: #2c3e50;
                font-weight: 600;
            }
            QListWidget::item:selected {
                background-color: rgba(52, 152, 219, 0.15);
                border: 3px solid #3498db;
                color: #3498db;
            }
            QListWidget::item:hover:!selected {
                background-color: #f4f6f7;
                border: 2px solid #bdc3c7;
            }
        """
        )

        layout.addWidget(self.list_widget, 1)

        # Botones en español
        botones = QDialogButtonBox()
        btn_ok = QPushButton("Aceptar")
        btn_cancel = QPushButton("Cancelar")
        btn_ok.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )
        btn_cancel.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            """
        )
        btn_ok.clicked.connect(self._aceptar)
        btn_cancel.clicked.connect(self.reject)
        botones.addButton(btn_ok, QDialogButtonBox.AcceptRole)
        botones.addButton(btn_cancel, QDialogButtonBox.RejectRole)
        layout.addWidget(botones)

        self._cargar_escudos()

    def seleccion(self) -> str | None:
        return self._seleccion

    def _cargar_escudos(self):
        ruta_escudos = obtener_ruta_recurso("Resources/img/escudos")
        escudos = Equipo.obtener_escudos_disponibles(ruta_escudos)

        self.list_widget.clear()

        if not escudos:
            # Si no hay escudos, podriamos poner un item deshabilitado avisando
            item = QListWidgetItem("No hay escudos disponibles")
            item.setFlags(Qt.NoItemFlags)
            self.list_widget.addItem(item)
            return

        for nombre_svg in escudos:
            # Crear item
            # Mostramos el nombre debajo si se quiere, o lo dejamos en blanco si solo se quiere icono
            # El usuario no especificó si quiere texto, pero ayuda a identificar.
            # Ponemos el nombre limpio (sin .svg si se prefiere, pero aqui pongo nombre completo para debug)
            clean_name = nombre_svg.replace(".svg", "").replace(".png", "")
            item = QListWidgetItem(clean_name)

            # Icono
            ruta_completa = obtener_ruta_recurso(f"Resources/img/escudos/{nombre_svg}")
            item.setIcon(QIcon(ruta_completa))

            # Guardamos el nombre real del archivo en data
            item.setData(Qt.UserRole, nombre_svg)

            # Alineamos texto
            item.setTextAlignment(Qt.AlignCenter)

            self.list_widget.addItem(item)

    def _aceptar(self):
        items = self.list_widget.selectedItems()
        if not items:
            QMessageBox.warning(self, "Selección", "Debes seleccionar un escudo.")
            return

        self._seleccion = items[0].data(Qt.UserRole)
        self.accept()


class PartidoDialog(QDialog):
    """Diálogo para crear o editar un partido."""

    def __init__(self, parent=None, partido: Partido | None = None):
        super().__init__(parent)
        self.setWindowTitle("Partido")
        self.setModal(True)
        self.setMinimumSize(520, 360)

        # Fondo blanco para el diálogo y estilos para combos
        self.setStyleSheet(
            """
            QDialog { 
                background-color: white; 
            }
            QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
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
            QDateTimeEdit {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 10pt;
                min-height: 24px;
            }
            QDateTimeEdit:hover {
                border-color: #95a5a6;
            }
            QDateTimeEdit:focus {
                border-color: #3498db;
            }
            QDateTimeEdit::up-button, QDateTimeEdit::down-button {
                background-color: transparent;
                border: none;
                width: 16px;
            }
            QDateTimeEdit::up-arrow, QDateTimeEdit::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
            }
            QDateTimeEdit::up-arrow {
                border-bottom: 5px solid #2c3e50;
            }
            QDateTimeEdit::down-arrow {
                border-top: 5px solid #2c3e50;
            }
            
            /* Estilos para el calendario popup */
            QCalendarWidget QWidget {
                background-color: white;
                color: #2c3e50;
            }
            QCalendarWidget QToolButton {
                background-color: white;
                color: #2c3e50;
                border: none;
                border-radius: 4px;
                padding: 4px;
                font-weight: 600;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #ecf0f1;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #bdc3c7;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton {
                color: #2c3e50;
                font-weight: 700;
                font-size: 11pt;
                padding: 6px 12px;
            }
            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                color: #2c3e50;
                font-weight: 700;
                font-size: 11pt;
                padding: 6px 12px;
            }
            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }
            QCalendarWidget QMenu {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
            }
            QCalendarWidget QSpinBox {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
                alternate-background-color: #f8f9fa;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: 700;
                border: 1px solid #bdc3c7;
                padding: 4px;
            }
            QCalendarWidget QAbstractItemView::item {
                border: 1px solid #ecf0f1;
                padding: 4px;
            }
            QCalendarWidget QAbstractItemView::item:selected {
                background-color: #3498db;
                color: white;
            }
            QCalendarWidget QAbstractItemView::item:hover {
                background-color: #e8f4f8;
            }
            """
        )

        self.partido = partido

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(10)

        self.combo_local = QComboBox()
        self.combo_visitante = QComboBox()
        self.combo_arbitro = QComboBox()
        self.combo_eliminatoria = QComboBox()
        self.combo_eliminatoria.addItems(Partido.ELIMINATORIAS)

        self.dt = QDateTimeEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("yyyy-MM-dd HH:mm")

        form.addWidget(QLabel("Equipo local"), 0, 0)
        form.addWidget(self.combo_local, 0, 1)
        form.addWidget(QLabel("Equipo visitante"), 1, 0)
        form.addWidget(self.combo_visitante, 1, 1)
        form.addWidget(QLabel("Fecha y hora"), 2, 0)
        form.addWidget(self.dt, 2, 1)
        form.addWidget(QLabel("Árbitro"), 3, 0)
        form.addWidget(self.combo_arbitro, 3, 1)
        form.addWidget(QLabel("Eliminatoria"), 4, 0)
        form.addWidget(self.combo_eliminatoria, 4, 1)

        layout.addLayout(form)

        # Botones personalizados en español
        botones = QDialogButtonBox()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        btn_guardar.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """
        )
        btn_cancelar.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            """
        )
        btn_guardar.clicked.connect(self._guardar)
        btn_cancelar.clicked.connect(self.reject)
        botones.addButton(btn_guardar, QDialogButtonBox.AcceptRole)
        botones.addButton(btn_cancelar, QDialogButtonBox.RejectRole)
        layout.addWidget(botones)

        self._equipos = Equipo.obtener_todos()
        self._arbitros = Participante.obtener_arbitros()

        self.combo_local.addItem("— Selecciona —", None)
        self.combo_visitante.addItem("— Selecciona —", None)
        for e in self._equipos:
            self.combo_local.addItem(f"{e.nombre} ({e.curso})", e.id)
            self.combo_visitante.addItem(f"{e.nombre} ({e.curso})", e.id)

        self.combo_arbitro.addItem("Sin árbitro", None)
        for a in self._arbitros:
            self.combo_arbitro.addItem(a.nombre, a.id)

        if partido is None:
            self.dt.setDateTime(datetime.now())
        else:
            self._cargar_partido(partido)

    def _cargar_partido(self, partido: Partido):
        self._set_combo_data(self.combo_local, partido.equipo_local_id)
        self._set_combo_data(self.combo_visitante, partido.equipo_visitante_id)
        self._set_combo_data(self.combo_arbitro, partido.arbitro_id)
        if partido.fecha_hora:
            # formato guardado: "YYYY-MM-DD HH:MM:SS" (según modelos)
            try:
                dt = datetime.strptime(partido.fecha_hora, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    dt = datetime.strptime(partido.fecha_hora, "%Y-%m-%d %H:%M")
                except ValueError:
                    dt = datetime.now()
            self.dt.setDateTime(dt)
        if partido.eliminatoria:
            idx = self.combo_eliminatoria.findText(partido.eliminatoria)
            if idx >= 0:
                self.combo_eliminatoria.setCurrentIndex(idx)

    @staticmethod
    def _set_combo_data(combo: QComboBox, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return

    def _guardar(self):
        local_id = self.combo_local.currentData()
        visitante_id = self.combo_visitante.currentData()
        if not local_id or not visitante_id:
            QMessageBox.warning(self, "Datos", "Selecciona ambos equipos.")
            return
        if local_id == visitante_id:
            QMessageBox.warning(
                self, "Datos", "Local y visitante no pueden ser iguales."
            )
            return

        fecha_hora = self.dt.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        arbitro_id = self.combo_arbitro.currentData()
        eliminatoria = self.combo_eliminatoria.currentText()

        if self.partido is None:
            self.partido = Partido(
                equipo_local_id=local_id,
                equipo_visitante_id=visitante_id,
                fecha_hora=fecha_hora,
                arbitro_id=arbitro_id,
                eliminatoria=eliminatoria,
            )
        else:
            self.partido.equipo_local_id = local_id
            self.partido.equipo_visitante_id = visitante_id
            self.partido.fecha_hora = fecha_hora
            self.partido.arbitro_id = arbitro_id
            self.partido.eliminatoria = eliminatoria

        if not self.partido.guardar():
            QMessageBox.critical(self, "Error", "No se pudo guardar el partido.")
            return

        self.accept()


class CreditosDialog(QDialog):
    """Diálogo scrollable para mostrar los créditos del programa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créditos")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMaximumHeight(500)

        # Fondo blanco para el diálogo
        self.setStyleSheet("QDialog { background-color: white; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Área scrollable para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background-color: white; border: none; }")

        # Widget contenedor del contenido
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Crear el label con el contenido HTML
        label = QLabel()
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setStyleSheet("color: black; background-color: white;")
        label.setText(
            "<h2 style='color: #1a5490;'>Gestión Torneo de Fútbol</h2>"
            "<hr>"
            "<p><b>Autor:</b> Daniel Gómez Delgado</p>"
            "<p><b>Versión:</b> 1.0</p>"
            "<p><b>Fecha de actualización:</b> 11/01/2025</p>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>Contexto del Proyecto</h3>"
            "<p>Programa propuesto en la asignatura de <b>Diseño de Interfaces</b> de 2º de "
            "<b>Desarrollo de Aplicaciones Multiplataforma</b> de Formación Profesional Superior "
            "en el <b>Brianda de Mendoza</b> de Guadalajara.</p>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>Tecnologías Utilizadas</h3>"
            "<ul>"
            "<li><b>Python 3.x</b> - Lenguaje de programación</li>"
            "<li><b>PySide6 (Qt6)</b> - Framework para interfaz gráfica</li>"
            "<li><b>Qt Designer</b> - Diseño visual de interfaces</li>"
            "<li><b>SQLite</b> - Base de datos relacional embebida</li>"
            "<li><b>PyInstaller</b> - Empaquetado de la aplicación</li>"
            "<li><b>QSS (Qt Style Sheets)</b> - Hojas de estilo personalizadas</li>"
            "</ul>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>Arquitectura del Proyecto</h3>"
            "<p>El proyecto sigue el patrón de diseño <b>Modelo-Vista-Controlador (MVC)</b>:</p>"
            "<ul>"
            "<li><b>Models/</b> - Gestión de base de datos y entidades (Equipos, Participantes, Partidos, etc.)</li>"
            "<li><b>Views/</b> - Interfaces gráficas diseñadas en Qt Designer y código Python</li>"
            "<li><b>Controllers/</b> - Lógica de control y coordinación entre modelo y vista</li>"
            "<li><b>Resources/</b> - Recursos gráficos (iconos, imágenes, estilos QSS)</li>"
            "</ul>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>Características Principales</h3>"
            "<ul>"
            "<li>Gestión completa de equipos y participantes (jugadores y árbitros)</li>"
            "<li>Sistema de calendario para programación de partidos eliminatorios</li>"
            "<li>Registro detallado de resultados, goles y tarjetas</li>"
            "<li>Visualización de bracket de eliminatorias con actualización automática</li>"
            "<li>Base de datos SQLite con relaciones y restricciones de integridad</li>"
            "<li>Interfaz moderna y responsiva con estilos personalizados</li>"
            "<li>Aplicación empaquetada como ejecutable independiente</li>"
            "</ul>"
            "<br>"
            "<p style='text-align: center; font-style: italic; color: #7f8c8d;'>"
            "Desarrollado con dedicación para facilitar la gestión de torneos de fútbol"
            "</p>"
        )

        content_layout.addWidget(label)
        content_layout.addStretch()
        scroll.setWidget(content_widget)

        layout.addWidget(scroll)

        # Botón de cerrar fijo en la parte inferior y centrado
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.setCenterButtons(True)
        layout.addWidget(button_box)


class AyudaDialog(QDialog):
    """Diálogo scrollable para mostrar la ayuda del programa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda")
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setMaximumHeight(500)

        # Fondo blanco para el diálogo
        self.setStyleSheet("QDialog { background-color: white; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Área scrollable para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background-color: white; border: none; }")

        # Widget contenedor del contenido
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Crear el label con el contenido HTML
        label = QLabel()
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setStyleSheet("color: black; background-color: white;")
        label.setText(
            "<h2 style='color: #1a5490;'>Manual de Ayuda - Gestión Torneo de Fútbol</h2>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>📋 Descripción General</h3>"
            "<p>Esta aplicación permite gestionar un torneo de fútbol por eliminatorias, "
            "desde la inscripción de equipos hasta la final del torneo.</p>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>🚀 Primeros Pasos</h3>"
            "<p><b>Orden recomendado para comenzar:</b></p>"
            "<ol>"
            "<li>Registrar los <b>equipos</b> participantes con sus datos y escudos</li>"
            "<li>Registrar los <b>participantes</b> (jugadores y árbitros)</li>"
            "<li>Asignar jugadores a sus respectivos equipos</li>"
            "<li>Crear el <b>calendario</b> de partidos para octavos de final</li>"
            "<li>Registrar <b>resultados</b> conforme se juegan los partidos</li>"
            "<li>Consultar la <b>clasificación</b> y el bracket actualizado</li>"
            "</ol>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>⚽ Secciones de la Aplicación</h3>"
            "<p><b>1. Equipos:</b></p>"
            "<ul>"
            "<li>Crear nuevos equipos con nombre, curso, color de camiseta y escudo</li>"
            "<li>Ver listado completo de equipos registrados</li>"
            "<li>Editar información de equipos existentes</li>"
            "<li>Eliminar equipos (solo si no tienen partidos asociados)</li>"
            "<li>Ver jugadores asignados a cada equipo al seleccionarlo</li>"
            "</ul>"
            "<p><b>2. Participantes:</b></p>"
            "<ul>"
            "<li>Registrar jugadores con datos personales y posición</li>"
            "<li>Registrar árbitros para los partidos</li>"
            "<li>Un participante puede ser jugador, árbitro o ambos</li>"
            "<li>Asignar jugadores a equipos desde esta sección</li>"
            "<li>Editar o eliminar participantes</li>"
            "<li>Ver estadísticas de goles y tarjetas de cada jugador</li>"
            "</ul>"
            "<p><b>3. Calendario:</b></p>"
            "<ul>"
            "<li>Programar partidos indicando equipos, fecha, hora y árbitro</li>"
            "<li>Especificar la fase del torneo (octavos, cuartos, semifinales, final)</li>"
            "<li>Ver todos los partidos programados ordenados por fecha</li>"
            "<li>Editar o eliminar partidos antes de que se jueguen</li>"
            "<li>Visualización en formato de lista o árbol de eliminatorias</li>"
            "</ul>"
            "<p><b>4. Resultados:</b></p>"
            "<ul>"
            "<li>Registrar goles de cada equipo en los partidos jugados</li>"
            "<li>Asignar goles específicos a jugadores</li>"
            "<li>Registrar tarjetas amarillas y rojas</li>"
            "<li>Ver historial completo de partidos jugados</li>"
            "<li>Filtrar y clasificar por diferentes criterios</li>"
            "<li>Los resultados actualizan automáticamente la clasificación</li>"
            "</ul>"
            "<p><b>5. Clasificación:</b></p>"
            "<ul>"
            "<li>Visualizar el bracket completo de eliminatorias</li>"
            "<li>Ver emparejamientos de todas las fases del torneo</li>"
            "<li>Seguir el progreso de los equipos a través de las rondas</li>"
            "<li>La clasificación se genera automáticamente según los resultados</li>"
            "<li>Identificar fácilmente al campeón del torneo</li>"
            "</ul>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>💡 Consejos Útiles</h3>"
            "<ul>"
            "<li>✓ Utiliza el menú superior para navegar rápidamente entre secciones</li>"
            "<li>✓ Asegúrate de tener al menos 16 equipos para un torneo completo</li>"
            "<li>✓ Verifica que cada equipo tenga suficientes jugadores asignados</li>"
            "<li>✓ Asigna árbitros diferentes a cada partido cuando sea posible</li>"
            "<li>✓ Registra los resultados inmediatamente después de cada partido</li>"
            "<li>✓ Las eliminatorias siguientes se generan automáticamente</li>"
            "<li>✓ No puedes eliminar equipos o participantes con partidos asociados</li>"
            "<li>✓ Usa el botón 'Volver' para regresar a la pantalla principal</li>"
            "</ul>"
            "<hr>"
            "<h3 style='color: #2c3e50;'>❓ Solución de Problemas</h3>"
            "<p><b>¿No puedes crear un partido?</b> Verifica que ambos equipos estén registrados "
            "y que haya al menos un árbitro disponible.</p>"
            "<p><b>¿No se actualiza la clasificación?</b> Asegúrate de haber guardado "
            "correctamente los resultados del partido.</p>"
            "<p><b>¿No puedes eliminar un equipo?</b> El equipo debe no tener partidos "
            "programados ni jugadores asignados.</p>"
            "<hr>"
            "<p style='text-align: center;'><i>Para más información, consulta el manual completo "
            "de usuario en formato PDF incluido con la aplicación.</i></p>"
        )

        content_layout.addWidget(label)
        content_layout.addStretch()
        scroll.setWidget(content_widget)

        layout.addWidget(scroll)

        # Botón de cerrar fijo en la parte inferior y centrado
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.setCenterButtons(True)
        layout.addWidget(button_box)
