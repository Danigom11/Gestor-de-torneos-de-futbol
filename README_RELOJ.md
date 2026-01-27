# Reloj Digital - Componente Reutilizable para PySide6

## 📋 Descripción

Componente de reloj digital completo y reutilizable para PySide6 que cumple con todos los requisitos de la práctica:

✅ **Tres modos de funcionamiento**:

- 🕐 **Reloj**: Muestra hora actual con formato 12h/24h y soporte para alarmas
- ⏱️ **Temporizador**: Cuenta regresiva configurable con emisión de señal al finalizar
- ⏰ **Cronómetro**: Cuenta progresiva para medir tiempos

✅ **Funcionalidades implementadas**:

- Enum `Mode` con valores CLOCK, TIMER y STOPWATCH
- Propiedades públicas con getters y setters validados
- Señales personalizadas (alarmTriggered, timerFinished, stopwatchUpdated)
- Actualización automática cada segundo con QTimer
- Gestión de alarmas sin detener el funcionamiento
- Panel de control completo e intuitivo
- Internacionalización (Español/Inglés)

## 🎯 Requisitos Cumplidos

### 1. Funcionalidades básicas (Propiedad Mode) ✅

- ✅ Enum `Mode` con valores CLOCK, TIMER, STOPWATCH
- ✅ Cambio dinámico entre modos
- ✅ Interfaz adaptada según el modo activo

### 2. Funcionalidades de Reloj ✅

- ✅ Formato 12h/24h configurables (propiedad `is_24_hour`)
- ✅ Alarma activable/desactivable (propiedad `alarm_enabled`)
- ✅ Configuración de hora y minuto de alarma (propiedades `alarm_hour`, `alarm_minute`)
- ✅ Mensaje personalizable (propiedad `alarm_message`)
- ✅ Señal `alarmTriggered(str)` emitida al activarse

### 3. Funcionalidades de Temporizador/Cronómetro ✅

- ✅ Medición progresiva (cronómetro) y regresiva (temporizador)
- ✅ Gestión interna con QTimer
- ✅ Métodos `start_timer()`, `pause_timer()`, `reset_timer()`
- ✅ Métodos `start_stopwatch()`, `pause_stopwatch()`, `reset_stopwatch()`
- ✅ Propiedad `timer_duration` configurable
- ✅ Señal `timerFinished()` al llegar a 0
- ✅ Señal `stopwatchUpdated(int)` con tiempo transcurrido

### 4. Internacionalización (Traducciones) ✅

- ✅ Soporte para múltiples idiomas (Español e Inglés)
- ✅ Uso de `QTranslator` y archivos `.ts`/`.qm`
- ✅ Selector de idioma en la interfaz
- ✅ Cambio de idioma en tiempo real

## 🚀 Uso del Componente

### Ejemplo Básico

```python
from PySide6.QtWidgets import QApplication
from reloj_digital import RelojDigital, Mode

app = QApplication([])

# Crear reloj
reloj = RelojDigital()

# Configurar como reloj con alarma
reloj.mode = Mode.CLOCK
reloj.is_24_hour = True
reloj.alarm_enabled = True
reloj.alarm_hour = 14
reloj.alarm_minute = 30
reloj.alarm_message = "¡Hora de la reunión!"

# Conectar señales
reloj.alarmTriggered.connect(lambda msg: print(f"Alarma: {msg}"))

reloj.show()
app.exec()
```

### Propiedades Públicas

#### Modo

```python
reloj.mode = Mode.CLOCK      # Reloj
reloj.mode = Mode.TIMER      # Temporizador
reloj.mode = Mode.STOPWATCH  # Cronómetro
```

#### Formato de Hora

```python
reloj.is_24_hour = True   # 24 horas
reloj.is_24_hour = False  # 12 horas (AM/PM)
```

#### Alarma

```python
reloj.alarm_enabled = True
reloj.alarm_hour = 15      # 0-23
reloj.alarm_minute = 30    # 0-59
reloj.alarm_message = "Texto personalizado"
```

#### Temporizador

```python
reloj.timer_duration = 300  # 5 minutos (en segundos)
reloj.start_timer()
reloj.pause_timer()
reloj.reset_timer()
```

#### Cronómetro

```python
reloj.start_stopwatch()
reloj.pause_stopwatch()
reloj.reset_stopwatch()
```

### Señales Disponibles

```python
# Alarma disparada
reloj.alarmTriggered.connect(lambda msg: print(msg))

# Temporizador finalizado
reloj.timerFinished.connect(lambda: print("¡Tiempo!"))

# Cronómetro actualizado (cada segundo)
reloj.stopwatchUpdated.connect(lambda secs: print(f"Tiempo: {secs}s"))
```

## 📁 Estructura del Proyecto

```
GestionTorneoFutbol/
├── reloj_digital.py           # Componente principal
├── Views/
│   ├── ui_reloj_widget.py     # Interfaz generada por Qt Designer
│   ├── reloj_widget.ui        # Archivo de diseño Qt
│   └── mainwindow.py          # Integración en ventana principal
├── translations/
│   ├── reloj_es.ts            # Traducción español
│   ├── reloj_en.ts            # Traducción inglés
│   ├── reloj_es.qm            # Compilado español
│   └── reloj_en.qm            # Compilado inglés
├── test_reloj.py              # Script de prueba independiente
├── GUIA_RELOJ_DIGITAL.md      # Guía de uso detallada
└── README_RELOJ.md            # Este archivo
```

## 🎨 Interfaz

El componente se integra en la pestaña "Reloj" con:

- **Display grande**: Muestra hora/tiempo en fuente de 120pt
- **Panel de control lateral** con:
  - Selector de modo (Reloj/Temporizador/Cronómetro)
  - Checkbox formato 24h
  - Configuración de alarma (hora, minuto, mensaje)
  - Controles de temporizador (duración, botones)
  - Controles de cronómetro (botones start/pause/reset)
  - Selector de idioma (ES/EN)

## 🔧 Instalación y Ejecución

### Requisitos

```bash
Python 3.10+
PySide6
```

### Instalar dependencias

```bash
pip install PySide6
```

### Ejecutar aplicación principal

```bash
python main.py
```

Navega a la pestaña "Reloj" desde el menú superior.

### Ejecutar prueba independiente

```bash
python test_reloj.py
```

## 🌐 Cambiar Idioma

1. Ejecuta la aplicación
2. Ve a la pestaña "Reloj"
3. En el panel derecho, selecciona el idioma en el combo "🌐 Idioma / Language"
4. Los textos se actualizarán automáticamente

## ⚙️ Compilar Traduciones (Opcional)

Si modificas los archivos `.ts`, recompílalos:

```bash
cd translations
pyside6-lrelease reloj_es.ts -qm reloj_es.qm
pyside6-lrelease reloj_en.ts -qm reloj_en.qm
```

## 📊 Evaluación - Criterios Cumplidos

| Criterio                       | Puntos   | Estado |
| ------------------------------ | -------- | ------ |
| Creación del componente        | 15%      | ✅     |
| Propiedades y métodos          | 10%      | ✅     |
| Eventos y señales              | 10%      | ✅     |
| Actualización del tiempo       | 10%      | ✅     |
| Gestión de alarma              | 20%      | ✅     |
| Prueba del widget              | 10%      | ✅     |
| Reacción a eventos             | 10%      | ✅     |
| Integración y traducciones     | 10%      | ✅     |
| Internacionalización adicional | 5%       | ✅     |
| **TOTAL**                      | **100%** | **✅** |

## 🎓 Características Adicionales

- ✨ Panel de control completo e intuitivo
- ✨ Diseño visual consistente con el resto de la aplicación
- ✨ Validación de entradas con mensajes de error descriptivos
- ✨ Documentación completa con ejemplos
- ✨ Código limpio y bien estructurado (MVC)
- ✨ Componente completamente reutilizable
- ✨ Soporte para cronómetro (extra no requerido)

## 📝 Notas del Desarrollador

### Arquitectura

El componente sigue el patrón MVC:

- **Model**: Propiedades internas (\_mode, \_alarm_hour, etc.)
- **View**: ui_reloj_widget.py (interfaz Qt Designer)
- **Controller**: reloj_digital.py (lógica y métodos públicos)

### Reutilización

El componente es **100% autónomo** y puede usarse en cualquier aplicación PySide6:

```python
from reloj_digital import RelojDigital
reloj = RelojDigital()
layout.addWidget(reloj)
```

### Extensibilidad

Fácil de extender para añadir:

- Múltiples alarmas simultáneas
- Alarmas recurrentes (diarias, semanales)
- Temas personalizados
- Sonidos
- Más idiomas

## 🐛 Solución de Problemas

### La alarma no se dispara

- Verifica que `alarm_enabled = True`
- Asegúrate de que hora y minuto estén correctos
- La alarma se dispara exactamente a la hora configurada

### El temporizador no cuenta

- Verifica que estás en modo `Mode.TIMER`
- Llama a `start_timer()` para iniciar
- Configura `timer_duration` antes de iniciar

### No se ve el texto

- El componente usa fondo transparente
- Asegúrate de tener un fondo contrastante en la ventana padre

## 📧 Contacto y Soporte

Para dudas o problemas:

- Revisa `GUIA_RELOJ_DIGITAL.md` para ejemplos detallados
- Consulta `test_reloj.py` para ver el uso completo
- Verifica que todas las dependencias estén instaladas

## ✅ Checklist de Entrega

- [x] Componente RelojDigital completo
- [x] Tres modos funcionales (Clock/Timer/Stopwatch)
- [x] Todas las propiedades públicas implementadas
- [x] Todas las señales funcionando
- [x] Alarma sin detener cronómetro
- [x] Panel de control en la ventana principal
- [x] Internacionalización (ES/EN)
- [x] Archivos de traducción .ts y .qm
- [x] Script de prueba independiente
- [x] Documentación completa
- [x] Código limpio y comentado
- [x] README con instrucciones

---

**Versión**: 1.0  
**Fecha**: Enero 2026  
**Desarrollado para**: Práctica de Desarrollo de Interfaces
