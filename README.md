# Gestión de Torneo de Fútbol

Aplicación de escritorio para la gestión completa de torneos de fútbol con sistema de eliminatorias.

## Características

- Gestión de equipos con escudos personalizados
- Registro de participantes (jugadores y árbitros)
- Programación de partidos con calendario interactivo
- Actualización de resultados con goles y tarjetas
- Visualización de bracket de eliminatorias
- Sistema de notificaciones
- Exportación a CSV
- Interfaz moderna y responsive

## Requisitos

- Python 3.8 o superior
- PySide6

## Instalación

### 1. Instalar dependencias

```bash
pip install PySide6
```

### 2. Clonar o descargar el proyecto

Asegúrate de que la estructura de carpetas sea la siguiente:

```
GestionTorneoFutbol/
├── main.py
├── Models/
│   ├── __init__.py
│   ├── database.py
│   ├── equipo.py
│   ├── participante.py
│   ├── partido.py
│   ├── jugador_equipo.py
│   ├── gol.py
│   └── tarjeta.py
├── Views/
│   ├── __init__.py
│   └── mainwindow.py
├── Controllers/
│   └── __init__.py
├── Resources/
│   ├── img/
│   │   ├── fondo.jpg
│   │   ├── equipo.jpg
│   │   ├── participante.jpg
│   │   ├── calendario.jpg
│   │   ├── resultados.jpg
│   │   ├── clasificacion.jpg
│   │   └── escudos/
│   ├── iconos/
│   └── qss/
│       └── style.qss
└── README.md
```

## Ejecución en modo desarrollo

```bash
python main.py
```

## Base de datos

La aplicación utiliza SQLite. La base de datos se creará automáticamente al ejecutar la aplicación por primera vez en:

```
Models/torneoFutbol_sqlite.db
```

### Estructura de la base de datos

- **equipos**: Información de los equipos
- **participantes**: Jugadores y árbitros
- **jugadores_equipos**: Relación entre jugadores y equipos
- **partidos**: Información de los partidos programados
- **goles**: Registro de goles por partido
- **tarjetas**: Registro de tarjetas amarillas y rojas
- **configuracion**: Parámetros de configuración

## Normativa implementada

- **Máximo 18 jugadores por equipo** (normativa española de torneos escolares)
- **Categorías por edad**:
  - Sub-12: Menores de 12 años
  - Sub-14: Menores de 14 años
  - Sub-16: Menores de 16 años
  - Sub-18: Menores de 18 años
  - Senior: 18 años o más
- **Sistema de desempates**: Prórroga y penales
- **41 escudos disponibles** en formato SVG

## Funcionalidades

### 1. Gestión de Equipos

- Crear, editar y eliminar equipos
- Asignar escudo único de la biblioteca disponible
- Seleccionar color de camiseta
- Ver lista de jugadores del equipo
- Exportar equipos a CSV

### 2. Gestión de Participantes

- Registrar jugadores y/o árbitros
- Asignar jugadores a equipos (máximo 18)
- Registrar posición de jugadores
- Ver estadísticas de goles y tarjetas
- Exportar participantes a CSV

### 3. Gestión del Calendario

- Programar partidos con calendario interactivo
- Asignar equipos, fecha, hora y árbitro
- Especificar eliminatoria del partido
- Editar y eliminar partidos programados
- Exportar calendario a CSV

### 4. Actualización de Resultados

- Registrar goles por jugador
- Registrar tarjetas amarillas y rojas
- Registrar prórroga y resultado de penales
- Actualización automática de estadísticas
- Exportar resultados a CSV

### 5. Clasificación

- Visualización de bracket de eliminatorias
- Actualización automática según resultados
- Indicadores visuales de prórroga/penales
- Exportar clasificación a CSV

### 6. Sistema de Notificaciones

- Partidos sin árbitro asignado
- Equipos con menos de 11 jugadores
- Resultados pendientes
- Límite de jugadores alcanzado

## Distribución (Ejecutable)

Para crear el ejecutable de Windows:

```bash
pyinstaller --add-data "Models/torneoFutbol_sqlite.db;Models" --add-data "Resources;Resources" --onefile --windowed --name="GestionTorneoFutbol" main.py
```

El ejecutable se generará en la carpeta `dist/`.

## Desarrollo

### Estado actual

- ✅ Base de datos y modelos completados
- ✅ Ventana principal con navegación por tarjetas
- ✅ Estilos QSS aplicados con fondos translúcidos y colores legibles
- ✅ Interfaz de gestión de equipos implementada
- ✅ Interfaz de gestión de participantes implementada
- ✅ Interfaz de calendario con programación de partidos implementada
- ✅ Interfaz de resultados con registro de goles y tarjetas implementada
- ✅ Interfaz de clasificación con bracket visual implementada
- ✅ Diálogos de selección y edición implementados
- ✅ Sistema de créditos y ayuda implementados
- ✅ Funcionalidad de exportación a CSV implementada
- ✅ Todas las vistas con fondos translúcidos y colores de texto legibles

### Próximas fases (opcional)

1. Añadir sistema de notificaciones automáticas
2. Mejorar exportación a CSV con más opciones
3. Pruebas exhaustivas y correcciones finales
4. Documentación completa en PDF (manual e informe)
5. Empaquetado final con PyInstaller

## Autor

Daniel Gómez
Desarrollo de aplicaciones multiplataforma
Versión 1.0 - Enero 2026

## Licencia

Proyecto académico - Instituto

## Notas técnicas

- La aplicación utiliza arquitectura MVC (Modelo-Vista-Controlador)
- Los escudos se renderizan en formato SVG nativo
- Las foreign keys están activadas en SQLite para integridad referencial
- Los triggers mantienen actualizados automáticamente los contadores de goles y tarjetas
- La aplicación es completamente responsive con tamaño mínimo de 1200x800px

## Soporte

Para más información, consultar:

- Manual de Usuario (PDF)
- Informe Técnico (PDF)
- Código fuente documentado con docstrings
