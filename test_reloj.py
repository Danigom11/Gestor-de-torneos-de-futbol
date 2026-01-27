"""
Script de prueba para el componente RelojDigital.
Prueba todas las funcionalidades del reloj.
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtCore import Qt
from reloj_digital import RelojDigital, Mode


class TestRelojWindow(QWidget):
    """Ventana de prueba para el RelojDigital."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba del Reloj Digital")
        self.setMinimumSize(900, 600)

        # Layout principal
        layout = QVBoxLayout(self)

        # Reloj centrado
        layout_reloj = QHBoxLayout()
        layout_reloj.addStretch()
        self.reloj = RelojDigital()
        layout_reloj.addWidget(self.reloj)
        layout_reloj.addStretch()
        layout.addLayout(layout_reloj)

        # Conectar señales
        self.reloj.alarmTriggered.connect(self.on_alarm)
        self.reloj.timerFinished.connect(self.on_timer_finished)

        # Panel de control
        layout.addWidget(self.crear_panel_control())

    def crear_panel_control(self):
        """Crea el panel de control con botones de prueba."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Título
        titulo = QLabel("Panel de Control")
        titulo.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(titulo)

        # Modo
        layout_modo = QHBoxLayout()
        layout_modo.addWidget(QLabel("Modo:"))
        btn_clock = QPushButton("Reloj")
        btn_clock.clicked.connect(lambda: setattr(self.reloj, "mode", Mode.CLOCK))
        btn_timer = QPushButton("Temporizador")
        btn_timer.clicked.connect(lambda: setattr(self.reloj, "mode", Mode.TIMER))
        layout_modo.addWidget(btn_clock)
        layout_modo.addWidget(btn_timer)
        layout_modo.addStretch()
        layout.addLayout(layout_modo)

        # Formato 12h/24h
        layout_formato = QHBoxLayout()
        self.check_24h = QCheckBox("Formato 24 horas")
        self.check_24h.setChecked(True)
        self.check_24h.stateChanged.connect(
            lambda: setattr(self.reloj, "is_24_hour", self.check_24h.isChecked())
        )
        layout_formato.addWidget(self.check_24h)
        layout_formato.addStretch()
        layout.addLayout(layout_formato)

        # Alarma
        layout.addWidget(QLabel("--- Alarma ---"))
        layout_alarma = QHBoxLayout()
        self.check_alarma = QCheckBox("Activar alarma")
        self.check_alarma.stateChanged.connect(
            lambda: setattr(self.reloj, "alarm_enabled", self.check_alarma.isChecked())
        )
        layout_alarma.addWidget(self.check_alarma)

        layout_alarma.addWidget(QLabel("Hora:"))
        self.spin_hora = QSpinBox()
        self.spin_hora.setRange(0, 23)
        self.spin_hora.valueChanged.connect(
            lambda v: setattr(self.reloj, "alarm_hour", v)
        )
        layout_alarma.addWidget(self.spin_hora)

        layout_alarma.addWidget(QLabel("Minuto:"))
        self.spin_minuto = QSpinBox()
        self.spin_minuto.setRange(0, 59)
        self.spin_minuto.valueChanged.connect(
            lambda v: setattr(self.reloj, "alarm_minute", v)
        )
        layout_alarma.addWidget(self.spin_minuto)

        layout_alarma.addWidget(QLabel("Mensaje:"))
        self.txt_mensaje = QLineEdit()
        self.txt_mensaje.setText("¡Alarma activada!")
        self.txt_mensaje.textChanged.connect(
            lambda t: setattr(self.reloj, "alarm_message", t)
        )
        layout_alarma.addWidget(self.txt_mensaje)
        layout_alarma.addStretch()
        layout.addLayout(layout_alarma)

        # Temporizador
        layout.addWidget(QLabel("--- Temporizador ---"))
        layout_timer = QHBoxLayout()

        layout_timer.addWidget(QLabel("Duración (segundos):"))
        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(0, 3600)
        self.spin_duracion.setValue(10)
        self.spin_duracion.valueChanged.connect(
            lambda v: setattr(self.reloj, "timer_duration", v)
        )
        layout_timer.addWidget(self.spin_duracion)

        btn_start = QPushButton("Iniciar")
        btn_start.clicked.connect(self.reloj.start_timer)
        layout_timer.addWidget(btn_start)

        btn_pause = QPushButton("Pausar")
        btn_pause.clicked.connect(self.reloj.pause_timer)
        layout_timer.addWidget(btn_pause)

        btn_reset = QPushButton("Reiniciar")
        btn_reset.clicked.connect(self.reloj.reset_timer)
        layout_timer.addWidget(btn_reset)

        layout_timer.addStretch()
        layout.addLayout(layout_timer)

        return panel

    def on_alarm(self, mensaje):
        """Maneja la alarma."""
        print(f"¡ALARMA! {mensaje}")
        self.setWindowTitle(f"⏰ {mensaje}")

    def on_timer_finished(self):
        """Maneja el fin del temporizador."""
        print("¡TEMPORIZADOR FINALIZADO!")
        self.setWindowTitle("⏱️ Temporizador finalizado")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestRelojWindow()
    window.show()
    sys.exit(app.exec())
