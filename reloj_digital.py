"""
Componente RelojDigital reutilizable para PySide6.
Soporta modo reloj con alarma, modo temporizador y cronómetro.
Incluye panel de control integrado.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtCore import (
    QTimer,
    QTime,
    QDateTime,
    Signal,
    Slot,
    Qt,
    QCoreApplication,
    QTranslator,
    QLibraryInfo,
    QLocale,
)
from enum import Enum
from Views.ui_reloj_widget import Ui_lbl_tiempo


class Mode(Enum):
    """Enum para los modos del reloj."""

    CLOCK = "clock"
    TIMER = "timer"
    STOPWATCH = "stopwatch"


class RelojDigital(QWidget):
    """
    Widget de reloj digital que puede funcionar como:
    - Reloj con alarma
    - Temporizador con cuenta regresiva
    - Cronómetro progresivo
    
    Incluye controles integrados.
    """

    # Señales
    alarmTriggered = Signal(str)  # Emite el mensaje de alarma
    timerFinished = Signal()  # Emite cuando el temporizador llega a 0
    stopwatchUpdated = Signal(int)  # Emite el tiempo transcurrido en segundos

    def __init__(self, parent=None):
        super().__init__(parent)

        # Propiedades internas
        self._mode = Mode.CLOCK
        self._is_24_hour = True

        # Alarma
        self._alarm_enabled = False
        self._alarm_hour = 0
        self._alarm_minute = 0
        self._alarm_message = "¡Alarma activada!"
        self._alarm_triggered_today = False

        # Temporizador
        self._timer_duration = 60
        self._timer_remaining = 60
        self._timer_active = False

        # Cronómetro
        self._stopwatch_elapsed = 0
        self._stopwatch_active = False

        # QTimer principal
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_display)
        self.timer.start(1000)  # Actualizar cada segundo

        # Configurar UI
        self._setup_ui()
        
        # Primera actualización
        self._update_display()
        self._on_mode_changed(0) # Inicializar en modo reloj

    def _setup_ui(self):
        """Configura la interfaz de usuario completa."""
        # Configuración básica del widget
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        # Layout principal horizontal
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(20)

        # === 1. VISUALIZACIÓN (IZQUIERDA) ===
        # Usamos el Ui_lbl_tiempo pero adaptado
        self.container_display = QWidget()
        self.ui = Ui_lbl_tiempo()
        self.ui.setupUi(self.container_display)
        
        # Ajustes al label del display
        self.ui.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Aseguramos que el label ocupe todo el container
        if self.ui.label.parent() == self.container_display:
             # Si Qt Designer lo puso absoluto, lo metemos en un layout
            l = QVBoxLayout(self.container_display)
            l.setContentsMargins(0,0,0,0)
            l.addWidget(self.ui.label)
        
        style_display = """
            QLabel {
                background-color: rgba(0, 0, 0, 120);
                color: white;
                font-size: 100pt;
                font-weight: 800;
                padding: 20px;
                border-radius: 20px;
            }
        """
        self.ui.label.setStyleSheet(style_display)
        layout_principal.addWidget(self.container_display, 3) # 75% ancho

        # === 2. PANEL DE CONTROL (DERECHA) ===
        self.panel = QWidget()
        self.panel.setStyleSheet(
            """
            QWidget {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 15px;
                color: black;
            }
            QGroupBox {
                background-color: rgba(200, 200, 200, 100);
                border: 2px solid rgba(0, 0, 0, 100);
                border-radius: 10px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                color: black;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: black;
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
            QLabel {
                color: black;
                background-color: transparent;
            }
            QCheckBox {
                color: black;
                background-color: transparent;
            }
            """
        )
        
        layout_panel = QVBoxLayout(self.panel)
        layout_panel.setSpacing(15)

        # --- Selector de Modo ---
        self.group_modo = QGroupBox("Modo de Funcionamiento")
        layout_modo = QVBoxLayout(self.group_modo)

        self.combo_modo = QComboBox()
        self.combo_modo.addItem("🕐 Reloj", Mode.CLOCK)
        self.combo_modo.addItem("⏱️ Temporizador", Mode.TIMER)
        self.combo_modo.addItem("⏰ Cronómetro", Mode.STOPWATCH)
        self.combo_modo.currentIndexChanged.connect(self._on_mode_changed)
        layout_modo.addWidget(self.combo_modo)

        self.check_24h = QCheckBox("Formato 24 horas")
        self.check_24h.setChecked(True)
        self.check_24h.stateChanged.connect(
            lambda: setattr(self, "is_24_hour", self.check_24h.isChecked())
        )
        layout_modo.addWidget(self.check_24h)
        layout_panel.addWidget(self.group_modo)

        # --- Alarma ---
        self.group_alarma = QGroupBox("⏰ Configuración de Alarma")
        layout_alarma = QFormLayout(self.group_alarma)

        self.check_alarma = QCheckBox("Activar alarma")
        self.check_alarma.stateChanged.connect(
            lambda: setattr(self, "alarm_enabled", self.check_alarma.isChecked())
        )
        layout_alarma.addRow(self.check_alarma)

        self.spin_hora_alarma = QSpinBox()
        self.spin_hora_alarma.setRange(0, 23)
        self.spin_hora_alarma.valueChanged.connect(
            lambda v: setattr(self, "alarm_hour", v)
        )
        self.lbl_hora_alarma = QLabel("Hora:")
        layout_alarma.addRow(self.lbl_hora_alarma, self.spin_hora_alarma)

        self.spin_minuto_alarma = QSpinBox()
        self.spin_minuto_alarma.setRange(0, 59)
        self.spin_minuto_alarma.valueChanged.connect(
            lambda v: setattr(self, "alarm_minute", v)
        )
        self.lbl_minuto_alarma = QLabel("Minuto:")
        layout_alarma.addRow(self.lbl_minuto_alarma, self.spin_minuto_alarma)

        self.txt_mensaje_alarma = QLineEdit()
        self.txt_mensaje_alarma.setText("¡Alarma activada!")
        self.txt_mensaje_alarma.textChanged.connect(
            lambda t: setattr(self, "alarm_message", t)
        )
        self.lbl_mensaje_alarma = QLabel("Mensaje:")
        layout_alarma.addRow(self.lbl_mensaje_alarma, self.txt_mensaje_alarma)

        layout_panel.addWidget(self.group_alarma)

        # --- Temporizador ---
        self.group_timer = QGroupBox("⏱️ Temporizador")
        layout_timer = QFormLayout(self.group_timer)

        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(1, 7200)
        self.spin_duracion.setValue(60)
        self.spin_duracion.setSuffix(" seg")
        self.spin_duracion.valueChanged.connect(
            lambda v: setattr(self, "timer_duration", v)
        )
        self.lbl_duracion = QLabel("Duración:")
        layout_timer.addRow(self.lbl_duracion, self.spin_duracion)

        layout_btns_timer = QGridLayout()
        self.btn_timer_start = QPushButton("▶ Iniciar")
        self.btn_timer_start.clicked.connect(self.start_timer)
        layout_btns_timer.addWidget(self.btn_timer_start, 0, 0)

        self.btn_timer_pause = QPushButton("⏸ Pausar")
        self.btn_timer_pause.clicked.connect(self.pause_timer)
        layout_btns_timer.addWidget(self.btn_timer_pause, 0, 1)

        self.btn_timer_reset = QPushButton("↻ Reiniciar")
        self.btn_timer_reset.clicked.connect(self.reset_timer)
        layout_btns_timer.addWidget(self.btn_timer_reset, 1, 0, 1, 2)

        layout_timer.addRow(layout_btns_timer)
        layout_panel.addWidget(self.group_timer)

        # --- Cronómetro ---
        self.group_stopwatch = QGroupBox("⏰ Cronómetro")
        layout_stopwatch = QVBoxLayout(self.group_stopwatch)

        layout_btns_stopwatch = QGridLayout()
        self.btn_stopwatch_start = QPushButton("▶ Iniciar")
        self.btn_stopwatch_start.clicked.connect(self.start_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_start, 0, 0)

        self.btn_stopwatch_pause = QPushButton("⏸ Pausar")
        self.btn_stopwatch_pause.clicked.connect(self.pause_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_pause, 0, 1)

        self.btn_stopwatch_reset = QPushButton("↻ Reiniciar")
        self.btn_stopwatch_reset.clicked.connect(self.reset_stopwatch)
        layout_btns_stopwatch.addWidget(self.btn_stopwatch_reset, 1, 0, 1, 2)

        layout_stopwatch.addLayout(layout_btns_stopwatch)
        layout_panel.addWidget(self.group_stopwatch)

        # --- Idioma ---
        group_idioma = QGroupBox()
        self.group_idioma = group_idioma # Guardar referencia
        layout_idioma = QVBoxLayout(group_idioma)

        self.combo_idioma = QComboBox()
        self.combo_idioma.addItem("🇬🇧 English", "en")
        self.combo_idioma.addItem("🇪🇸 Español", "es")
        self.combo_idioma.currentIndexChanged.connect(self._on_language_changed)
        layout_idioma.addWidget(self.combo_idioma)

        layout_panel.addWidget(group_idioma)

        # Espaciador final
        layout_panel.addStretch()

        layout_principal.addWidget(self.panel, 1) # 25% ancho
        
        # Inicializar traductor
        self.translator = QTranslator()
        
        # Aplicar textos iniciales
        self.retranslateUi()
        
    def retranslateUi(self):
        """Actualiza todos los textos de la interfaz para el idioma actual."""
        # Grupos
        self.group_modo.setTitle(self.tr("Operating Mode"))
        self.group_alarma.setTitle(self.tr("Alarm Settings"))
        self.group_timer.setTitle(self.tr("Timer"))
        self.group_stopwatch.setTitle(self.tr("Stopwatch"))
        self.group_idioma.setTitle(self.tr("Language"))
        
        # Controles Modo
        self.check_24h.setText(self.tr("24-hour format"))
        
        # Items del combo modo - Cuidado: al cambiar texto no queremos disparar eventos indeseados si fuera el caso
        # guardamos el índice y lo restauramos si es necesario, o setItemText
        self.combo_modo.setItemText(0, self.tr("Clock"))
        self.combo_modo.setItemText(1, self.tr("Timer"))
        self.combo_modo.setItemText(2, self.tr("Stopwatch"))
        
        # Alarma
        self.check_alarma.setText(self.tr("Enable alarm"))
        self.lbl_hora_alarma.setText(self.tr("Hour:"))
        self.lbl_minuto_alarma.setText(self.tr("Minute:"))
        self.lbl_mensaje_alarma.setText(self.tr("Message:"))
        
        # Timer
        self.lbl_duracion.setText(self.tr("Duration:"))
        self.spin_duracion.setSuffix(" " + self.tr("sec"))
        self.btn_timer_start.setText(self.tr("Start"))
        self.btn_timer_pause.setText(self.tr("Pause"))
        self.btn_timer_reset.setText(self.tr("Reset"))
        
        # Stopwatch
        self.btn_stopwatch_start.setText(self.tr("Start"))
        self.btn_stopwatch_pause.setText(self.tr("Pause"))
        self.btn_stopwatch_reset.setText(self.tr("Reset"))
        
    # ========== INTERACCIÓN UI ==========
    def _on_mode_changed(self, index):
        """Cambia el modo del reloj y actualiza visibilidad."""
        mode = self.combo_modo.itemData(index)
        self.mode = mode # Llama al setter

        # Visibilidad
        self.group_alarma.setVisible(mode == Mode.CLOCK)
        self.group_timer.setVisible(mode == Mode.TIMER)
        self.group_stopwatch.setVisible(mode == Mode.STOPWATCH)
        self.check_24h.setVisible(mode == Mode.CLOCK)

    def _on_language_changed(self, index):
        """Carga y aplica el archivo de traducción seleccionado."""
        lang_code = self.combo_idioma.itemData(index)
        
        # Remover traductor previo
        QCoreApplication.removeTranslator(self.translator)
        
        if lang_code == "es":
            # Cargar español
            if self.translator.load(f"Resources/translations/reloj_es.qm"):
                QCoreApplication.installTranslator(self.translator)
        
        # Si es inglés (default), simplemente al quitar el traductor vuelven los textos originales (source)
        # o cargamos en.qm si existiera. Asumimos source=English.
        
        # Actualizar textos
        self.retranslateUi()


    # ========== PROPIEDADES ==========
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, Mode):
            raise ValueError("Modo inválido")
        self._mode = value
        self._update_display()
        
        # Sincronizar UI si el cambio no vino del combo
        idx = -1
        if value == Mode.CLOCK: idx = 0
        elif value == Mode.TIMER: idx = 1
        elif value == Mode.STOPWATCH: idx = 2
        
        if idx != -1 and self.combo_modo.currentIndex() != idx:
            self.combo_modo.setCurrentIndex(idx)

    @property
    def is_24_hour(self):
        return self._is_24_hour

    @is_24_hour.setter
    def is_24_hour(self, value):
        self._is_24_hour = bool(value)
        if self.check_24h.isChecked() != value:
            self.check_24h.setChecked(value)
        self._update_display()

    # ========== ALARMA ==========
    @property
    def alarm_enabled(self):
        return self._alarm_enabled

    @alarm_enabled.setter
    def alarm_enabled(self, value):
        self._alarm_enabled = bool(value)
        if self.check_alarma.isChecked() != value:
            self.check_alarma.setChecked(value)
        if value:
            self._alarm_triggered_today = False

    @property
    def alarm_hour(self):
        return self._alarm_hour

    @alarm_hour.setter
    def alarm_hour(self, value):
        val = int(value)
        if not 0 <= val <= 23: return
        self._alarm_hour = val
        if self.spin_hora_alarma.value() != val:
            self.spin_hora_alarma.setValue(val)
        self._alarm_triggered_today = False

    @property
    def alarm_minute(self):
        return self._alarm_minute

    @alarm_minute.setter
    def alarm_minute(self, value):
        val = int(value)
        if not 0 <= val <= 59: return
        self._alarm_minute = val
        if self.spin_minuto_alarma.value() != val:
            self.spin_minuto_alarma.setValue(val)
        self._alarm_triggered_today = False

    @property
    def alarm_message(self):
        return self._alarm_message

    @alarm_message.setter
    def alarm_message(self, value):
        self._alarm_message = str(value)
        if self.txt_mensaje_alarma.text() != value:
            self.txt_mensaje_alarma.setText(value)

    # ========== TEMPORIZADOR ==========
    @property
    def timer_duration(self):
        return self._timer_duration

    @timer_duration.setter
    def timer_duration(self, value):
        val = int(value)
        if val < 0: return
        self._timer_duration = val
        if self.spin_duracion.value() != val:
            self.spin_duracion.setValue(val)
            
        # Si cambiamos duración en UI, reseteamos el timer logic
        self._timer_remaining = val
        self._timer_active = False
        self._update_display()

    # ========== MÉTODOS PÚBLICOS TIMER/STOPWATCH ==========
    @Slot()
    def start_timer(self):
        if self._mode != Mode.TIMER: return
        if self._timer_remaining > 0:
            self._timer_active = True

    @Slot()
    def pause_timer(self):
        if self._mode != Mode.TIMER: return
        self._timer_active = False

    @Slot()
    def reset_timer(self):
        if self._mode != Mode.TIMER: return
        self._timer_remaining = self._timer_duration
        self._timer_active = False
        self._update_display()

    @Slot()
    def start_stopwatch(self):
        if self._mode != Mode.STOPWATCH: return
        self._stopwatch_active = True

    @Slot()
    def pause_stopwatch(self):
        if self._mode != Mode.STOPWATCH: return
        self._stopwatch_active = False

    @Slot()
    def reset_stopwatch(self):
        if self._mode != Mode.STOPWATCH: return
        self._stopwatch_elapsed = 0
        self._stopwatch_active = False
        self._update_display()

    # ========== LÓGICA INTERNA ==========
    def _update_display(self):
        if self._mode == Mode.CLOCK:
            self._update_clock()
        elif self._mode == Mode.TIMER:
            self._update_timer()
        elif self._mode == Mode.STOPWATCH:
            self._update_stopwatch()

    def _update_clock(self):
        current_time = QDateTime.currentDateTime().time()
        if self._is_24_hour:
            time_str = current_time.toString("HH:mm:ss")
        else:
            time_str = current_time.toString("hh:mm:ss AP")
        self.ui.label.setText(time_str)

        # Verificar alarma
        if (
            self._alarm_enabled
            and not self._alarm_triggered_today
            and current_time.hour() == self._alarm_hour
            and current_time.minute() == self._alarm_minute
            and current_time.second() == 0
        ):
            self._alarm_triggered_today = True
            # Mostrar MessageBox por defecto, además de emitir señal
            # El uso como componente puede decidir si mostrar o no, pero 
            # como ahora es standalone, deberíamos manejarlo aquí o dejar
            # que la app padre maneje.
            # Para cumplir "self-contained", podemos mostrar un diálogo si nadie conecta,
            # pero mejor emitimos y manejamos internamente si es necesario.
            # Aquí emitimos la señal.
            self.alarmTriggered.emit(self._alarm_message)
            
            # Mostramos un popup simple interno
            QMessageBox.information(self, "Alarma", self._alarm_message)

        if current_time.hour() == 0 and current_time.minute() == 0 and current_time.second() == 0:
            self._alarm_triggered_today = False

    def _update_timer(self):
        if self._timer_active and self._timer_remaining > 0:
            self._timer_remaining -= 1
            if self._timer_remaining == 0:
                self._timer_active = False
                self.timerFinished.emit()
                QMessageBox.information(self, "Timer", "¡Tiempo completado!")

        hours = self._timer_remaining // 3600
        minutes = (self._timer_remaining % 3600) // 60
        seconds = self._timer_remaining % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.ui.label.setText(time_str)

    def _update_stopwatch(self):
        if self._stopwatch_active:
            self._stopwatch_elapsed += 1
            self.stopwatchUpdated.emit(self._stopwatch_elapsed)

        hours = self._stopwatch_elapsed // 3600
        minutes = (self._stopwatch_elapsed % 3600) // 60
        seconds = self._stopwatch_elapsed % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.ui.label.setText(time_str)
