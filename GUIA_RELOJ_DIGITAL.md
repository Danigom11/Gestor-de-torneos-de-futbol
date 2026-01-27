# Guía de Uso: RelojDigital Component

## Descripción

`RelojDigital` es un widget de PySide6 reutilizable que puede funcionar como:

- **Reloj**: Muestra la hora actual con soporte para alarmas
- **Temporizador**: Cuenta regresiva con emisión de señal al finalizar

## Características

### Modos de Operación

- `Mode.CLOCK`: Modo reloj con hora actual
- `Mode.TIMER`: Modo temporizador con cuenta regresiva

### Propiedades Públicas

#### Modo

```python
reloj.mode = Mode.CLOCK  # Cambiar a modo reloj
reloj.mode = Mode.TIMER  # Cambiar a modo temporizador
```

#### Formato de Hora

```python
reloj.is_24_hour = True   # Formato 24 horas (por defecto)
reloj.is_24_hour = False  # Formato 12 horas (AM/PM)
```

#### Alarma

```python
# Configurar alarma
reloj.alarm_enabled = True
reloj.alarm_hour = 14      # 14:00 (2 PM)
reloj.alarm_minute = 30    # 14:30
reloj.alarm_message = "¡Hora de la reunión!"

# Desactivar alarma
reloj.alarm_enabled = False
```

#### Temporizador

```python
# Configurar temporizador de 60 segundos
reloj.timer_duration = 60

# Controlar el temporizador
reloj.start_timer()   # Iniciar/reanudar
reloj.pause_timer()   # Pausar
reloj.reset_timer()   # Reiniciar a la duración inicial
```

### Señales

#### alarmTriggered(str)

Se emite cuando la hora actual coincide con la alarma configurada.

```python
def on_alarm(mensaje):
    print(f"Alarma: {mensaje}")

reloj.alarmTriggered.connect(on_alarm)
```

#### timerFinished()

Se emite cuando el temporizador llega a 0.

```python
def on_timer_finished():
    print("¡Temporizador finalizado!")

reloj.timerFinished.connect(on_timer_finished)
```

## Ejemplos de Uso

### Ejemplo 1: Reloj Simple

```python
from PySide6.QtWidgets import QApplication, QMainWindow
from reloj_digital import RelojDigital, Mode

app = QApplication([])
window = QMainWindow()

# Crear y configurar reloj
reloj = RelojDigital()
reloj.mode = Mode.CLOCK
reloj.is_24_hour = True

window.setCentralWidget(reloj)
window.show()
app.exec()
```

### Ejemplo 2: Reloj con Alarma

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from reloj_digital import RelojDigital, Mode

app = QApplication([])
window = QMainWindow()

# Crear reloj
reloj = RelojDigital()
reloj.mode = Mode.CLOCK

# Configurar alarma para dentro de 2 minutos
from PySide6.QtCore import QTime
current_time = QTime.currentTime()
alarm_time = current_time.addSecs(120)  # +2 minutos

reloj.alarm_hour = alarm_time.hour()
reloj.alarm_minute = alarm_time.minute()
reloj.alarm_message = "¡Alarma de prueba!"
reloj.alarm_enabled = True

# Conectar señal
def mostrar_alarma(mensaje):
    QMessageBox.information(window, "Alarma", mensaje)

reloj.alarmTriggered.connect(mostrar_alarma)

window.setCentralWidget(reloj)
window.show()
app.exec()
```

### Ejemplo 3: Temporizador de Cocina

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from reloj_digital import RelojDigital, Mode

app = QApplication([])
window = QMainWindow()

# Widget central con layout
central = QWidget()
layout = QVBoxLayout(central)

# Crear temporizador
reloj = RelojDigital()
reloj.mode = Mode.TIMER
reloj.timer_duration = 300  # 5 minutos

# Botones de control
btn_start = QPushButton("Iniciar")
btn_start.clicked.connect(reloj.start_timer)

btn_pause = QPushButton("Pausar")
btn_pause.clicked.connect(reloj.pause_timer)

btn_reset = QPushButton("Reiniciar")
btn_reset.clicked.connect(reloj.reset_timer)

# Añadir al layout
layout.addWidget(reloj)
layout.addWidget(btn_start)
layout.addWidget(btn_pause)
layout.addWidget(btn_reset)

# Conectar señal de finalización
def timer_done():
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.information(window, "Timer", "¡Tiempo completado!")

reloj.timerFinished.connect(timer_done)

window.setCentralWidget(central)
window.show()
app.exec()
```

### Ejemplo 4: Centrado en una Pestaña

```python
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QVBoxLayout, QHBoxLayout
)
from reloj_digital import RelojDigital

app = QApplication([])
window = QMainWindow()

# TabWidget
tabs = QTabWidget()

# Crear página con reloj centrado
pagina_reloj = QWidget()
layout_v = QVBoxLayout(pagina_reloj)

# Espaciador superior
layout_v.addStretch()

# Layout horizontal para centrar
layout_h = QHBoxLayout()
layout_h.addStretch()

# Reloj
reloj = RelojDigital()
reloj.setFixedSize(640, 480)
layout_h.addWidget(reloj)

layout_h.addStretch()
layout_v.addLayout(layout_h)

# Espaciador inferior
layout_v.addStretch()

# Añadir pestaña
tabs.addTab(pagina_reloj, "Reloj")

window.setCentralWidget(tabs)
window.show()
app.exec()
```

## Internacionalización

Todos los textos visibles utilizan `self.tr()` para soportar traducción:

```python
# Los mensajes por defecto están en español
reloj.alarm_message = "¡Alarma activada!"

# Pero puedes cambiarlos
reloj.alarm_message = "Alarm triggered!"
```

## Validación de Errores

El componente valida automáticamente los valores:

```python
# ✅ Válido
reloj.alarm_hour = 15

# ❌ Genera ValueError
reloj.alarm_hour = 25  # Error: "La hora debe estar entre 0 y 23"

# ✅ Válido
reloj.alarm_minute = 30

# ❌ Genera ValueError
reloj.alarm_minute = 60  # Error: "Los minutos deben estar entre 0 y 59"

# ✅ Válido
reloj.timer_duration = 100

# ❌ Genera ValueError
reloj.timer_duration = -10  # Error: "La duración debe ser mayor o igual a 0"
```

## Pruebas

Ejecuta el archivo de prueba incluido:

```bash
python test_reloj.py
```

Este script abre una ventana con todos los controles para probar todas las funcionalidades del componente.

## Integración en tu Aplicación

El componente ya está integrado en la aplicación principal (`Views/mainwindow.py`) como una nueva pestaña "Reloj" en el menú de navegación.

Para acceder:

1. Ejecuta la aplicación: `python main.py`
2. Haz clic en "Reloj" en el menú superior
3. O navega desde la ventana principal

---

**Autor**: Sistema de Gestión de Torneo de Fútbol  
**Versión**: 1.0  
**Fecha**: Enero 2026
