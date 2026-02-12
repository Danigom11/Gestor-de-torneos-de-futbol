===============================================================================
                   README ACLARACIÓN – Gestión Torneo de Fútbol
              Tarea 5: Informes en la Aplicación de Torneo de Fútbol
===============================================================================

Autor:   Daniel Gómez
Módulo:  Desarrollo de Interfaces (DI) – DAM2
Fecha:   Febrero 2026

===============================================================================
1. DESCRIPCIÓN GENERAL
===============================================================================

Aplicación de escritorio desarrollada en Python con PySide6 (Qt) que gestiona
un torneo de fútbol con sistema de eliminatorias. Esta versión incluye la
generación de informes PDF profesionales diseñados en JasperSoft Studio y
generados desde Python mediante la librería pyreportjasper.

===============================================================================
2. REQUISITOS DEL SISTEMA
===============================================================================

  - Sistema operativo: Windows 10/11
  - Java JDK 11 o superior (OBLIGATORIO para generar informes PDF)

  ★ IMPORTANTE: La generación de informes desde el ejecutable (.exe)
    requiere Java instalado en el sistema. La librería pyreportjasper
    utiliza internamente la JVM (Java Virtual Machine) para compilar
    los archivos .jrxml y generar los PDFs con JasperReports.

    SIN Java instalado: La aplicación funciona normalmente para gestionar
    el torneo (equipos, partidos, clasificación, etc.), pero al intentar
    generar un informe PDF dará error.

    CON Java instalado: La generación de informes funciona automáticamente.

===============================================================================
3. CONFIGURACIÓN DE JAVA PARA EL EJECUTABLE (.exe)
===============================================================================

  Para que la generación de informes funcione desde el ejecutable:

  PASO 1 – Instalar Java JDK 11 o superior:
    Descargar desde: https://adoptium.net/
    Seleccionar "Windows x64" → instalar con opciones por defecto.

  PASO 2 – Verificar que Java está en el PATH:
    Abrir una consola (cmd o PowerShell) y escribir:
      java -version
    Debe mostrar la versión instalada (ej: openjdk version "17.0.x").

    Si no se reconoce el comando:
      1. Abrir "Variables de entorno del sistema"
      2. En "Variables del sistema" → editar "Path"
      3. Añadir la ruta del bin de Java, por ejemplo:
         C:\Program Files\Eclipse Adoptium\jdk-17.0.x-hotspot\bin
      4. Aceptar y reiniciar la consola.

  PASO 3 – Ejecutar la aplicación:
    El ejecutable buscará automáticamente Java en el PATH del sistema.
    No es necesario configurar nada más.

  NOTA: La carpeta "reports" con los archivos .jrxml, .jasper y la
  subcarpeta "lib" (driver JDBC) DEBE estar junto al ejecutable .exe.
  Al distribuir, copiar:
    - La carpeta dist/GestionTorneoFutbol/ completa
    - Dentro de ella ya se encuentra la carpeta reports/

===============================================================================
4. ESTRUCTURA DEL PROYECTO
===============================================================================

  GestionTorneoFutbol/
  ├── main.py                          ← Punto de entrada de la aplicación
  ├── Models/                          ← Modelos de datos (MVC)
  │   ├── database.py                  ← Conexión y creación de BD SQLite
  │   ├── equipo.py, participante.py, partido.py, etc.
  │   └── torneoFutbol_sqlite.db       ← Base de datos SQLite
  ├── Views/                           ← Vistas de la interfaz (MVC)
  │   ├── mainwindow.py                ← Ventana principal
  │   ├── informes_view.py             ← ★ Ventana de Informes (Tarea 5)
  │   ├── equipos_view.py, calendario_view.py, etc.
  │   └── ui/                          ← Archivos .ui de Qt Designer
  ├── Controllers/                     ← Controladores (MVC)
  │   └── informes_controller.py       ← Lógica de generación de PDFs
  ├── Resources/                       ← Recursos gráficos, estilos, iconos
  │   ├── img/escudos/                 ← Escudos SVG de equipos
  │   └── qss/style.qss               ← Hoja de estilos
  ├── reports/                         ← ★ INFORMES JASPER (Tarea 5)
  │   ├── Informe_Equipos_Jugadores.jrxml / .jasper
  │   ├── Informe_Partidos_Resultados.jrxml / .jasper
  │   ├── Informe_Clasificacion.jrxml / .jasper
  │   ├── Muestra_Equipos_Jugadores.pdf
  │   ├── Muestra_Partidos_Resultados.pdf
  │   ├── Muestra_Clasificacion.pdf
  │   └── lib/sqlite-jdbc-3.46.0.0.jar ← Driver JDBC para SQLite
  ├── translations/                    ← Traducciones del reloj
  ├── reloj_digital.py                 ← Componente reloj digital
  ├── GestionTorneoFutbol.spec         ← Configuración de PyInstaller
  ├── Informe_Tecnico.md               ← Informe técnico del proyecto
  ├── Manual_Usuario.md                ← Manual de usuario
  ├── README.md                        ← Documentación general
  ├── README_RELOJ.md                  ← Documentación del componente reloj
  └── README Aclaración.txt            ← ★ Este archivo

===============================================================================
5. EJECUCIÓN DE LA APLICACIÓN
===============================================================================

  5.1 Ejecutable (.exe):
      Ir a la carpeta dist/GestionTorneoFutbol/ y ejecutar
      GestionTorneoFutbol.exe con doble clic.
      La carpeta "reports" ya está incluida junto al ejecutable.

  5.2 Modo desarrollo (requiere Python 3.10+ y dependencias):
      cd GestionTorneoFutbol
      pip install PySide6 pyreportjasper
      python main.py

===============================================================================
6. USO DE LA VENTANA DE INFORMES
===============================================================================

  La ventana de informes se encuentra en la barra de navegación lateral
  de la aplicación, identificada como "Informes".

  ── Pasos para generar un informe PDF ──

  1. Abrir la aplicación y pulsar "Informes" en el menú lateral izquierdo.

  2. En el panel izquierdo, seleccionar el tipo de informe en el
     desplegable "Seleccionar Informe":
     • Equipos y Jugadores
     • Partidos y Resultados
     • Clasificación y Eliminatorias

  3. (Opcional) Configurar filtros según el tipo de informe:
     • Para "Equipos y Jugadores": seleccionar un equipo específico
       del desplegable o dejar "Todos los equipos".
     • Para "Partidos y Resultados" o "Clasificación y Eliminatorias":
       seleccionar una eliminatoria específica o dejar "Todas".

  4. (Opcional) Cambiar la ruta de guardado pulsando "Cambiar" en
     la sección "Ruta de Guardado". Por defecto se guarda en reports/.

  5. Pulsar el botón verde "Generar Informe PDF".
     — La aplicación compilará el .jrxml, conectará con la BD SQLite
       y generará el PDF. Este proceso tarda unos segundos.

  6. Al finalizar, aparecerá un mensaje de confirmación con los datos
     del PDF generado (nombre, ubicación, tamaño).

  7. Para abrir el PDF generado:
     • Pulsar "Abrir Último PDF Generado" → lo abre con el visor
       predeterminado del sistema (Adobe Reader, navegador, etc.).
     • Pulsar "Abrir Carpeta Reports" → abre el explorador de archivos
       en la carpeta donde se guardan los informes.

  ── Panel derecho: Vista Previa / Información ──

  El panel derecho muestra:
  • Antes de generar: descripción detallada del informe seleccionado,
    indicando qué datos incluirá y qué filtros están disponibles.
  • Después de generar: resumen del PDF creado (nombre, ubicación,
    tamaño en KB).

===============================================================================
7. INFORMES DISPONIBLES (DETALLE)
===============================================================================

  ─── Informe 1: Equipos y Jugadores ───
  Archivo: Informe_Equipos_Jugadores.jrxml / .jasper
  • Listado alfabético de equipos con todos sus jugadores
  • Datos por jugador: posición, goles, tarjetas amarillas y rojas
  • Estadísticas por equipo: total goles, total tarjetas, promedio
    goles/jugador
  • Destacados: jugadores con más goles y más tarjetas resaltados
  • Filtro opcional: por equipo específico (parámetro EQUIPO_ID)

  ─── Informe 2: Partidos y Resultados ───
  Archivo: Informe_Partidos_Resultados.jrxml / .jasper
  • Listado cronológico agrupado por eliminatoria
  • Información: equipos, árbitro, fecha/hora, eliminatoria, resultado
  • Historial de enfrentamientos previos entre equipos
  • Partidos pendientes resaltados con fondo naranja
  • Filtro opcional: por eliminatoria (parámetro ELIMINATORIA)

  ─── Informe 3: Clasificación y Eliminatorias ───
  Archivo: Informe_Clasificacion.jrxml / .jasper
  • Tabla de clasificación: PJ, V, E, D, GF, GC, Diferencia
  • Cuadro visual de emparejamientos (Octavos→Cuartos→Semis→Final)
  • Estadísticas globales: goles y tarjetas por eliminatoria, promedios
  • Comparativa: equipos con más victorias, más goles, menos recibidos
  • Top-3 resaltados con colores (oro, plata, bronce)
  • Filtro opcional: por eliminatoria (parámetro ELIMINATORIA)

  ─── PDFs de muestra ───
  En la carpeta reports/ se incluyen PDFs de muestra pregenerados:
  • Muestra_Equipos_Jugadores.pdf
  • Muestra_Partidos_Resultados.pdf
  • Muestra_Clasificacion.pdf
  Estos permiten ver el resultado final sin necesidad de tener Java
  instalado.

===============================================================================
8. ARCHIVOS .jrxml, .jasper Y PDFs
===============================================================================

  Los archivos de informes están en la carpeta reports/:

  • .jrxml → Archivo fuente XML del informe (editable con JasperSoft
             Studio). Contiene el diseño, consultas SQL y parámetros.
  • .jasper → Versión compilada del .jrxml (binario). Se genera
              automáticamente al compilar. Mejora el rendimiento ya que
              no necesita recompilar cada vez.
  • .pdf    → Documento PDF generado. Se crea desde la aplicación
              al pulsar "Generar Informe PDF".

  Driver JDBC: reports/lib/sqlite-jdbc-3.46.0.0.jar
    Necesario para que JasperReports conecte con la BD SQLite.
    Ya incluido en el proyecto, no necesita descarga adicional.

===============================================================================
9. EXPORTACIÓN A CSV
===============================================================================

  Cada sección de la aplicación dispone de un botón "Exportar a CSV":
  • Equipos → Exporta la lista de equipos con sus datos
  • Participantes → Exporta jugadores/árbitros
  • Calendario → Exporta partidos programados
  • Resultados → Exporta resultados con goles y tarjetas
  • Clasificación → Exporta la tabla de clasificación

===============================================================================
10. NOTAS TÉCNICAS
===============================================================================

  • Los archivos .jrxml usan java.lang.Long para campos numéricos
    enteros, ya que el driver JDBC de SQLite devuelve enteros como Long.

  • Los PDFs se generan a través de un directorio temporal para evitar
    bloqueos de archivo por parte de la JVM.

  • La conexión a la BD en los informes usa JDBC (org.sqlite.JDBC)
    con el driver incluido en reports/lib/.

  • pyreportjasper NO es un ejecutable independiente. Es una librería
    Python que invoca JasperReports internamente, por lo que necesita
    Java accesible en el PATH.

  • NO es necesario tener instalado JasperSoft Studio para generar los
    informes. JasperSoft Studio solo se usa para DISEÑAR los .jrxml.
    La generación de PDFs la hace pyreportjasper con la JVM.

===============================================================================
11. SOLUCIÓN DE PROBLEMAS
===============================================================================

  Problema: "pyreportjasper no está instalado"
  Solución: Esto solo ocurre en modo desarrollo.
            Ejecutar: pip install pyreportjasper
            En el ejecutable .exe ya está incluido.

  Problema: Error al generar informe / "No se puede iniciar la JVM"
  Solución: Verificar que Java JDK 11+ está instalado y en el PATH.
            Ejecutar "java -version" en consola para comprobar.
            Ver sección 3 de este documento para la configuración.

  Problema: "No se encuentra el driver JDBC"
  Solución: Verificar que reports/lib/sqlite-jdbc-3.46.0.0.jar existe
            junto al ejecutable.

  Problema: El PDF no se abre automáticamente
  Solución: La aplicación reintenta la apertura 3 veces automáticamente.
            Si persiste, abrir manualmente desde la carpeta reports/.

  Problema: Error de tipos (ClassCastException)
  Solución: Los .jrxml deben usar java.lang.Long, no java.lang.Integer.
            Los archivos incluidos ya están corregidos.

  Problema: La carpeta "reports" no se encuentra
  Solución: La carpeta "reports" debe estar en el mismo directorio que
            el ejecutable. Al copiar/distribuir la aplicación, asegurarse
            de incluir la carpeta reports con todo su contenido.

===============================================================================
