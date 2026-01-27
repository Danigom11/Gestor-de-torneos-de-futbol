"""
Componente RelojDigital reutilizable para PySide6.
Soporta modo reloj con alarma y modo temporizador.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QTime, QDateTime, Signal, Slot, QCoreApplication, Qt
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
    """

    # Señales
    alarmTriggered = Signal(str)  # Emite el mensaje de alarma
    timerFinished = Signal()  # Emite cuando el temporizador llega a 0
    stopwatchUpdated = Signal(int)  # Emite el tiempo transcurrido en segundos

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar interfaz
        self.ui = Ui_lbl_tiempo()
        self.ui.setupUi(self)

        # Establecer fondo transparente como el resto de pestañas
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        # Reconfigurar el label para que use layout y ocupe todo el espacio
        from PySide6.QtWidgets import QVBoxLayout, QSizePolicy

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Remover el label del parent anterior si tiene geometría absoluta
        if self.ui.label.parent():
            self.ui.label.setParent(None)

        # Añadir el label al layout
        layout.addWidget(self.ui.label)

        # Configurar el label para que sea grande y visible
        self.ui.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label.setStyleSheet(
            """
            QLabel {
                background-color: rgba(0, 0, 0, 120);
                color: white;
                font-size: 120pt;
                font-weight: 800;
                padding: 40px;
                border-radius: 20px;
            }
        """
        )

        # Propiedades internas
        self._mode = Mode.CLOCK
        self._is_24_hour = True

        # Alarma
        self._alarm_enabled = False
        self._alarm_hour = 0
        self._alarm_minute = 0
        self._alarm_message = self.tr("¡Alarma activada!")
        self._alarm_triggered_today = False

        # Temporizador
        self._timer_duration = 0

        # Cronómetro
        self._stopwatch_elapsed = 0
        self._stopwatch_active = False
        self._timer_remaining = 0
        self._timer_active = False

        # QTimer principal
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_display)
        self.timer.start(1000)  # Actualizar cada segundo

        # Primera actualización
        self._update_display()

    # ========== PROPIEDADES: MODE ==========
    @property
    def mode(self):
        """Obtiene el modo actual (CLOCK, TIMER o STOPWATCH)."""
        return self._mode

    @mode.setter
    def mode(self, value):
        """Establece el modo del reloj."""
        if not isinstance(value, Mode):
            raise ValueError(
                self.tr("El modo debe ser de tipo Mode (CLOCK, TIMER o STOPWATCH)")
            )
        self._mode = value
        self._update_display()

    # ========== PROPIEDADES: FORMATO 12H/24H ==========
    @property
    def is_24_hour(self):
        """Obtiene si está en formato 24h."""
        return self._is_24_hour

    @is_24_hour.setter
    def is_24_hour(self, value):
        """Establece el formato de hora (True=24h, False=12h)."""
        self._is_24_hour = bool(value)
        self._update_display()

    # ========== PROPIEDADES: ALARMA ==========
    @property
    def alarm_enabled(self):
        """Obtiene si la alarma está habilitada."""
        return self._alarm_enabled

    @alarm_enabled.setter
    def alarm_enabled(self, value):
        """Habilita o deshabilita la alarma."""
        self._alarm_enabled = bool(value)
        if self._alarm_enabled:
            self._alarm_triggered_today = False

    @property
    def alarm_hour(self):
        """Obtiene la hora de la alarma."""
        return self._alarm_hour

    @alarm_hour.setter
    def alarm_hour(self, value):
        """Establece la hora de la alarma (0-23)."""
        if not 0 <= value <= 23:
            raise ValueError(self.tr("La hora debe estar entre 0 y 23"))
        self._alarm_hour = int(value)
        self._alarm_triggered_today = False

    @property
    def alarm_minute(self):
        """Obtiene los minutos de la alarma."""
        return self._alarm_minute

    @alarm_minute.setter
    def alarm_minute(self, value):
        """Establece los minutos de la alarma (0-59)."""
        if not 0 <= value <= 59:
            raise ValueError(self.tr("Los minutos deben estar entre 0 y 59"))
        self._alarm_minute = int(value)
        self._alarm_triggered_today = False

    @property
    def alarm_message(self):
        """Obtiene el mensaje de alarma."""
        return self._alarm_message

    @alarm_message.setter
    def alarm_message(self, value):
        """Establece el mensaje que se emitirá con la alarma."""
        self._alarm_message = str(value)

    # ========== PROPIEDADES: TEMPORIZADOR ==========
    @property
    def timer_duration(self):
        """Obtiene la duración del temporizador en segundos."""
        return self._timer_duration

    @timer_duration.setter
    def timer_duration(self, value):
        """Establece la duración del temporizador en segundos."""
        if value < 0:
            raise ValueError(self.tr("La duración debe ser mayor o igual a 0"))
        self._timer_duration = int(value)
        self._timer_remaining = self._timer_duration
        self._timer_active = False
        self._update_display()

    # ========== MÉTODOS PÚBLICOS: TEMPORIZADOR ==========
    @Slot()
    def start_timer(self):
        """Inicia o reanuda el temporizador."""
        if self._mode != Mode.TIMER:
            return

        if self._timer_remaining > 0:
            self._timer_active = True

    @Slot()
    def pause_timer(self):
        """Pausa el temporizador."""
        if self._mode != Mode.TIMER:
            return

        self._timer_active = False

    @Slot()
    def reset_timer(self):
        """Reinicia el temporizador a su duración inicial."""
        if self._mode != Mode.TIMER:
            return

        self._timer_remaining = self._timer_duration
        self._timer_active = False
        self._update_display()

    # ========== MÉTODOS PÚBLICOS: CRONÓMETRO ==========
    @Slot()
    def start_stopwatch(self):
        """Inicia o reanuda el cronómetro."""
        if self._mode != Mode.STOPWATCH:
            return

        self._stopwatch_active = True

    @Slot()
    def pause_stopwatch(self):
        """Pausa el cronómetro."""
        if self._mode != Mode.STOPWATCH:
            return

        self._stopwatch_active = False

    @Slot()
    def reset_stopwatch(self):
        """Reinicia el cronómetro a 0."""
        if self._mode != Mode.STOPWATCH:
            return

        self._stopwatch_elapsed = 0
        self._stopwatch_active = False
        self._update_display()

    # ========== LÓGICA INTERNA ==========
    def _update_display(self):
        """Actualiza el display según el modo actual."""
        if self._mode == Mode.CLOCK:
            self._update_clock()
        elif self._mode == Mode.TIMER:
            self._update_timer()
        elif self._mode == Mode.STOPWATCH:
            self._update_stopwatch()

    def _update_clock(self):
        """Actualiza el reloj y verifica alarma."""
        current_time = QDateTime.currentDateTime().time()

        # Formatear tiempo
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
            self.alarmTriggered.emit(self._alarm_message)

        # Reset de la bandera de alarma a medianoche
        if (
            current_time.hour() == 0
            and current_time.minute() == 0
            and current_time.second() == 0
        ):
            self._alarm_triggered_today = False

    def _update_timer(self):
        """Actualiza el temporizador con cuenta regresiva."""
        # Decrementar si está activo
        if self._timer_active and self._timer_remaining > 0:
            self._timer_remaining -= 1

            # Verificar si terminó
            if self._timer_remaining == 0:
                self._timer_active = False
                self.timerFinished.emit()

        # Formatear tiempo restante
        hours = self._timer_remaining // 3600
        minutes = (self._timer_remaining % 3600) // 60
        seconds = self._timer_remaining % 60

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.ui.label.setText(time_str)

    def _update_stopwatch(self):
        """Actualiza el cronómetro con cuenta progresiva."""
        # Incrementar si está activo
        if self._stopwatch_active:
            self._stopwatch_elapsed += 1
            self.stopwatchUpdated.emit(self._stopwatch_elapsed)

        # Formatear tiempo transcurrido
        hours = self._stopwatch_elapsed // 3600
        minutes = (self._stopwatch_elapsed % 3600) // 60
        seconds = self._stopwatch_elapsed % 60

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.ui.label.setText(time_str)
