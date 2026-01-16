# Manual de Usuario

## Gestión de Torneo de Fútbol

**Versión:** 1.0  
**Fecha:** 11 de enero de 2025  
**Autor:** Daniel Gómez Delgado  
**Asignatura:** Desarrollo de Interfaces - DAM 2º  
**Centro:** IES Brianda de Mendoza

---

## 1. Introducción

### 1.1 Descripción de la aplicación

Gestión de Torneo de Fútbol es una aplicación de escritorio desarrollada para facilitar la organización y seguimiento de torneos de fútbol con sistema de eliminatorias. Permite gestionar equipos, jugadores, árbitros, programar partidos y mantener un registro completo de resultados.

### 1.2 Requisitos del sistema

- **Sistema operativo:** Windows 10 o superior
- **Memoria RAM:** Mínimo 2 GB
- **Espacio en disco:** 100 MB libres
- **Resolución de pantalla:** Mínimo 1024x768

### 1.3 Instalación

#### Versión ejecutable (.exe)

1. Descargar el archivo `GestionTorneoFutbol.exe`
2. Hacer doble clic en el archivo
3. La aplicación se ejecutará automáticamente sin necesidad de instalación adicional

#### Versión de desarrollo

```bash
# Instalar Python 3.8 o superior
# Instalar dependencias
pip install PySide6

# Ejecutar la aplicación
python main.py
```

---

## 2. Primeros pasos

### 2.1 Inicio de la aplicación

Al iniciar la aplicación, se mostrará la ventana principal con un menú lateral que contiene las siguientes secciones:

- **⚽ Equipos**: Gestión de equipos participantes
- **👥 Participantes**: Registro de jugadores y árbitros
- **📅 Calendario**: Programación de partidos
- **📊 Resultados**: Actualización de resultados de partidos
- **🏆 Clasificación**: Visualización del bracket de eliminatorias

_[INSERTAR CAPTURA: Pantalla principal de la aplicación]_

### 2.2 Orden recomendado de uso

Para comenzar a usar la aplicación correctamente, siga este orden:

1. **Crear equipos** (sección Equipos)
2. **Registrar participantes** (sección Participantes)
3. **Asignar jugadores a equipos** (desde Participantes o Equipos)
4. **Programar partidos** (sección Calendario)
5. **Actualizar resultados** (sección Resultados)
6. **Visualizar bracket** (sección Clasificación)

---

## 3. Gestión de Equipos

### 3.1 Crear un nuevo equipo

Para crear un equipo:

1. Clic en **⚽ Equipos** en el menú lateral
2. Clic en el botón **"Añadir Equipo"** (botón verde con símbolo +)
3. Rellenar los campos del formulario:
   - **Nombre del equipo**: Nombre identificativo (obligatorio)
   - **Curso**: Curso al que pertenece el equipo
   - **Color**: Seleccionar color de camiseta usando el selector de color
   - **Escudo**: Seleccionar un escudo de la lista desplegable (57 escudos disponibles)
4. Clic en **"Guardar"**

_[INSERTAR CAPTURA: Formulario de creación de equipo]_

**Nota:** Cada escudo solo puede ser usado por un equipo.

### 3.2 Ver jugadores de un equipo

1. En la lista de equipos, hacer clic sobre un equipo
2. Se mostrarán automáticamente los jugadores asignados a ese equipo en el panel inferior

_[INSERTAR CAPTURA: Lista de equipos con jugadores]_

### 3.3 Editar un equipo

1. Clic en el botón del lápiz (✎) junto al equipo que desea editar
2. Modificar los campos deseados
3. Clic en **"Guardar"**

### 3.4 Eliminar un equipo

1. Clic en el botón rojo con "×" junto al equipo
2. Confirmar la eliminación en el diálogo que aparece

**Advertencia:** No se puede eliminar un equipo que tenga partidos programados.

### 3.5 Buscar equipos

Utilice la barra de búsqueda en la parte superior para filtrar equipos por nombre.

### 3.6 Exportar datos

Clic en el botón **"Exportar a CSV"** para guardar la lista de equipos en formato CSV.

---

## 4. Gestión de Participantes

### 4.1 Registrar un nuevo participante

Para registrar un participante (jugador y/o árbitro):

1. Clic en **👥 Participantes** en el menú lateral
2. Clic en el botón **"Añadir Participante"**
3. Rellenar el formulario:
   - **Nombre completo**: Nombre y apellidos
   - **Fecha de nacimiento**: Usar el selector de fecha
   - **Curso**: Curso al que pertenece
   - **Es jugador**: Marcar si es jugador
   - **Es árbitro**: Marcar si es árbitro (puede ser ambos)
   - **Posición** (solo si es jugador): Portero, Defensa, Centrocampista o Delantero
   - **Equipo** (opcional): Asignar directamente a un equipo
4. Clic en **"Guardar"**

_[INSERTAR CAPTURA: Formulario de registro de participante]_

**Nota:** La categoría (Sub-12, Sub-14, etc.) se calcula automáticamente según la edad.

### 4.2 Ver estadísticas de participantes

En la lista de participantes se muestran:

- Nombre y curso
- Categoría por edad
- Tipo (Jugador/Árbitro)
- Equipo asignado
- **Goles** marcados (⚽)
- **Tarjetas amarillas** (🟨)
- **Tarjetas rojas** (🟥)

_[INSERTAR CAPTURA: Lista de participantes con estadísticas]_

### 4.3 Editar un participante

1. Clic en el botón del lápiz (✎) junto al participante
2. Modificar los datos necesarios
3. Clic en **"Guardar"**

### 4.4 Eliminar un participante

1. Clic en el botón rojo con "×" junto al participante
2. Confirmar la eliminación

**Advertencia:** No se puede eliminar un participante que tenga goles o tarjetas registradas.

### 4.5 Filtrar participantes

Use los filtros disponibles para mostrar:

- Todos los participantes
- Solo jugadores
- Solo árbitros

### 4.6 Límite de jugadores por equipo

La aplicación respeta la normativa española: **máximo 18 jugadores por equipo**.

---

## 5. Gestión del Calendario

### 5.1 Programar un partido

Para programar un nuevo partido:

1. Clic en **📅 Calendario** en el menú lateral
2. Clic en el botón **"Añadir Partido"**
3. Rellenar el formulario:
   - **Equipo local**: Seleccionar del desplegable
   - **Equipo visitante**: Seleccionar del desplegable (debe ser diferente al local)
   - **Fecha**: Seleccionar en el calendario
   - **Hora**: Indicar hora del partido
   - **Árbitro**: Seleccionar árbitro disponible
   - **Eliminatoria**: Octavos, Cuartos, Semifinales o Final
4. Clic en **"Guardar"**

_[INSERTAR CAPTURA: Formulario de programación de partido]_

### 5.2 Ver partidos programados

Los partidos se muestran en orden cronológico con:

- Fecha y hora
- Equipos participantes (con escudos)
- Árbitro asignado
- Fase de la eliminatoria

_[INSERTAR CAPTURA: Lista de partidos en el calendario]_

### 5.3 Editar un partido

1. Hacer doble clic sobre el partido en la lista
2. O clic en el botón de edición
3. Modificar los campos necesarios
4. Clic en **"Guardar"**

### 5.4 Eliminar un partido

1. Clic en el botón rojo "×" junto al partido
2. Confirmar la eliminación

**Nota:** No se puede eliminar un partido que ya tenga resultados registrados.

### 5.5 Notificaciones

La aplicación mostrará alertas automáticas si:

- Hay partidos sin árbitro asignado
- Hay partidos pendientes de registrar resultados

---

## 6. Actualización de Resultados

### 6.1 Registrar resultado de un partido

Para actualizar el resultado de un partido:

1. Clic en **📊 Resultados** en el menú lateral
2. Seleccionar el partido de la lista
3. Clic en **"Actualizar Resultado"**
4. Introducir:
   - **Goles equipo local**
   - **Goles equipo visitante**
5. En caso de empate en eliminatorias:
   - Activar **"¿Hubo prórroga?"**
   - Si persiste el empate: introducir **goles de penales**
6. Clic en **"Continuar"**

_[INSERTAR CAPTURA: Formulario de actualización de resultado]_

### 6.2 Registrar goles de jugadores

Después de introducir el marcador:

1. Para cada gol, seleccionar el jugador que lo marcó
2. Introducir el minuto del gol
3. Clic en **"Añadir Gol"**
4. Repetir para todos los goles

_[INSERTAR CAPTURA: Diálogo de registro de goles por jugador]_

### 6.3 Registrar tarjetas

Para registrar tarjetas amarillas o rojas:

1. Seleccionar el jugador sancionado
2. Seleccionar tipo de tarjeta (Amarilla/Roja)
3. Introducir el minuto
4. Clic en **"Añadir Tarjeta"**

_[INSERTAR CAPTURA: Diálogo de registro de tarjetas]_

### 6.4 Ver partidos jugados

La lista muestra:

- Fecha del partido
- Equipos y resultado final
- Indicadores de prórroga (si hubo)
- Indicadores de penales (si hubo)

_[INSERTAR CAPTURA: Lista de partidos con resultados]_

### 6.5 Actualización automática

Los contadores de goles y tarjetas de cada participante se actualizan automáticamente al registrar los datos.

---

## 7. Visualización de Clasificación

### 7.1 Ver bracket de eliminatorias

1. Clic en **🏆 Clasificación** en el menú lateral
2. Se mostrará el bracket completo con:
   - **Octavos de final** (8 partidos)
   - **Cuartos de final** (4 partidos)
   - **Semifinales** (2 partidos)
   - **Final** (1 partido)

_[INSERTAR CAPTURA: Bracket completo de eliminatorias]_

### 7.2 Interpretación del bracket

- **Equipos en verde**: Ganadores que avanzan a la siguiente ronda
- **Equipos en rojo**: Equipos eliminados
- **Líneas de conexión**: Muestran el camino de cada equipo
- **Escudos**: Identifican visualmente cada equipo
- **Marcadores**: Resultado de cada partido
- **Indicadores**: Muestran si hubo prórroga (P) o penales (Pen)

_[INSERTAR CAPTURA: Detalle del bracket con indicadores]_

### 7.3 Exportar bracket

Clic en **"Exportar a CSV"** para guardar el bracket completo en formato CSV.

---

## 8. Base de Datos

### 8.1 Ubicación

La base de datos se crea automáticamente en:

```
Models/torneoFutbol_sqlite.db
```

### 8.2 Estructura

La aplicación utiliza SQLite con las siguientes tablas:

- **equipos**: Almacena información de los equipos
- **participantes**: Jugadores y árbitros registrados
- **jugadores_equipos**: Relación entre jugadores y equipos (N:M)
- **partidos**: Información de partidos programados y jugados
- **goles**: Registro detallado de goles por partido y jugador
- **tarjetas**: Registro de tarjetas amarillas y rojas
- **configuracion**: Parámetros de configuración del sistema

### 8.3 Respaldo de datos

**Importante:** Para hacer una copia de seguridad, simplemente copie el archivo `torneoFutbol_sqlite.db` a una ubicación segura.

---

## 9. Funciones Adicionales

### 9.1 Exportación a CSV

Todas las secciones principales permiten exportar datos a formato CSV:

- Lista de equipos
- Lista de participantes
- Calendario de partidos
- Resultados
- Bracket de clasificación

### 9.2 Sistema de notificaciones

La aplicación muestra automáticamente notificaciones cuando:

- Hay partidos sin árbitro asignado
- Hay partidos pendientes de registrar resultados

### 9.3 Búsqueda y filtros

Cada sección incluye herramientas de búsqueda y filtrado para encontrar rápidamente la información deseada.

---

## 10. Solución de Problemas

### 10.1 La aplicación no inicia

- Verifique que tiene los permisos necesarios para ejecutar el archivo
- En versión de desarrollo: asegúrese de tener Python 3.8+ y PySide6 instalados

### 10.2 No se guardan los datos

- Verifique que la aplicación tiene permisos de escritura en la carpeta Models/
- Asegúrese de hacer clic en "Guardar" después de realizar cambios

### 10.3 No aparecen los escudos

- Verifique que la carpeta Resources/img/escudos/ contiene los archivos de escudos
- Los escudos deben estar en formato PNG o SVG

### 10.4 Error al exportar a CSV

- Asegúrese de tener permisos de escritura en la ubicación de destino
- Cierre el archivo CSV si está abierto en otra aplicación

### 10.5 No se puede eliminar un equipo/participante

- Los equipos con partidos programados no pueden eliminarse
- Los participantes con goles o tarjetas registradas no pueden eliminarse
- Primero elimine los registros dependientes

---

## 11. Normativa Implementada

La aplicación respeta las siguientes normativas:

- **Máximo 18 jugadores por equipo** (normativa española de torneos escolares)
- **Categorías por edad**:
  - Sub-12: Menores de 12 años
  - Sub-14: Menores de 14 años
  - Sub-16: Menores de 16 años
  - Sub-18: Menores de 18 años
  - Senior: 18 años o más
- **Sistema de desempate**: Prórroga y penales en eliminatorias
- **Integridad de datos**: Validaciones para mantener la coherencia de la información

---

## 12. Contacto y Soporte

**Desarrollador:** Daniel Gómez Delgado  
**Institución:** IES Brianda de Mendoza  
**Asignatura:** Desarrollo de Interfaces - DAM 2º  
**Versión:** 1.0  
**Fecha:** 11 de enero de 2025

---

## 13. Créditos

**Tecnologías utilizadas:**

- Python 3.12+
- PySide6 (Qt for Python)
- SQLite
- Qt Designer

**Recursos:**

- 57 escudos de equipos en formato SVG y PNG
- Hojas de estilo QSS personalizadas
- Imágenes de fondo y decorativas

---

_Fin del Manual de Usuario_
