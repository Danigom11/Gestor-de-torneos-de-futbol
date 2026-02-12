"""
Controlador de Informes del Torneo de Fútbol.

Gestiona la generación de informes PDF mediante JasperReports.
Los informes (.jrxml) se diseñan en JasperSoft Studio y se compilan /
exportan a PDF desde Python usando la librería pyreportjasper.
"""

import os
import sys
import shutil
import tempfile
import gc
from datetime import datetime

from PySide6.QtSql import QSqlQuery

# ── Motor Jasper ────────────────────────────────────────────────────────────
try:
    from pyreportjasper import PyReportJasper

    JASPER_DISPONIBLE = True
except ImportError:
    JASPER_DISPONIBLE = False
    print("⚠ pyreportjasper no instalado. Instalar con: pip install pyreportjasper")


# ═══════════════════════════════════════════════════════════════════════════════
# RUTAS DEL PROYECTO
# ═══════════════════════════════════════════════════════════════════════════════


def _ruta_proyecto():
    """Devuelve la raíz del proyecto."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ruta_reports():
    """Devuelve la ruta de la carpeta reports, creándola si no existe."""
    if getattr(sys, "frozen", False):
        # En modo empaquetado, los reports están en _MEIPASS (bundled)
        ruta = os.path.join(sys._MEIPASS, "reports")
        if os.path.exists(ruta):
            return ruta
    ruta = os.path.join(_ruta_proyecto(), "reports")
    os.makedirs(ruta, exist_ok=True)
    return ruta


def _ruta_db():
    """Devuelve la ruta absoluta de la base de datos SQLite."""
    if getattr(sys, "frozen", False):
        # En modo empaquetado, la BD de trabajo está junto al .exe
        directorio_exe = os.path.dirname(sys.executable)
        bd = os.path.join(directorio_exe, "torneoFutbol_sqlite.db")
        if os.path.exists(bd):
            return bd
    return os.path.join(_ruta_proyecto(), "Models", "torneoFutbol_sqlite.db")


def _ruta_jdbc():
    """Devuelve la carpeta que contiene el driver JDBC de SQLite."""
    ruta = os.path.join(_ruta_reports(), "lib")
    os.makedirs(ruta, exist_ok=True)
    return ruta


# ═══════════════════════════════════════════════════════════════════════════════
# CONSULTAS AUXILIARES PARA LA INTERFAZ (filtros de la Vista)
# ═══════════════════════════════════════════════════════════════════════════════


def obtener_lista_equipos():
    """Devuelve [(id, nombre), ...] de todos los equipos."""
    equipos = []
    q = QSqlQuery("SELECT id, nombre FROM equipos ORDER BY nombre")
    while q.next():
        equipos.append((q.value(0), q.value(1)))
    return equipos


def obtener_lista_eliminatorias():
    """Devuelve las eliminatorias disponibles."""
    return ["Octavos", "Cuartos", "Semifinales", "Final"]


# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE GENERACIÓN CON JASPERREPORTS
# ═══════════════════════════════════════════════════════════════════════════════


def _generar_informe_jasper(jrxml_nombre, ruta_salida, parametros=None):
    """
    Compila un .jrxml y genera un PDF usando pyreportjasper.

    Args:
        jrxml_nombre (str): Nombre del archivo .jrxml dentro de reports/.
        ruta_salida  (str): Ruta completa del PDF de salida (con .pdf).
        parametros  (dict): Parámetros opcionales para el informe Jasper.

    Returns:
        str: Ruta del PDF generado.

    Raises:
        RuntimeError: Si pyreportjasper no está disponible o falla la generación.
        FileNotFoundError: Si el archivo .jrxml no existe.
    """
    if not JASPER_DISPONIBLE:
        raise RuntimeError(
            "pyreportjasper no está instalado.\n"
            "Instálalo con:  pip install pyreportjasper"
        )

    input_file = os.path.join(_ruta_reports(), jrxml_nombre)
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"No se encuentra el archivo de informe:\n{input_file}\n\n"
            "Asegúrate de que los archivos .jrxml están en la carpeta 'reports/'."
        )

    # pyreportjasper espera la ruta de salida SIN extensión .pdf
    # Generamos a un archivo temporal para evitar que la JVM bloquee el PDF final
    temp_dir = tempfile.mkdtemp(prefix="jasper_")
    temp_base = os.path.join(temp_dir, "informe_tmp")

    db_path = _ruta_db()
    jdbc_dir = _ruta_jdbc()

    jasper = PyReportJasper()
    jasper.config(
        input_file=input_file,
        output_file=temp_base,
        output_formats=["pdf"],
        db_connection={
            "driver": "generic",
            "jdbc_driver": "org.sqlite.JDBC",
            "jdbc_url": f"jdbc:sqlite:{db_path}",
            "jdbc_dir": jdbc_dir,
        },
        parameters=parametros or {},
    )
    jasper.process_report()

    temp_pdf = temp_base + ".pdf"
    if not os.path.exists(temp_pdf):
        raise RuntimeError(f"No se generó el PDF temporal en:\n{temp_pdf}")

    # Copiar los bytes del PDF temporal al destino final (desbloqueado)
    pdf_path = ruta_salida
    if not pdf_path.lower().endswith(".pdf"):
        pdf_path = pdf_path + ".pdf"

    with open(temp_pdf, "rb") as src:
        datos = src.read()
    with open(pdf_path, "wb") as dst:
        dst.write(datos)

    # Liberar referencia a Jasper y limpiar
    del jasper
    gc.collect()

    # Intentar limpiar el temporal (puede fallar si la JVM lo tiene bloqueado)
    try:
        os.remove(temp_pdf)
        os.rmdir(temp_dir)
    except OSError:
        pass  # Se limpiará cuando termine el proceso

    if not os.path.exists(pdf_path):
        raise RuntimeError(f"No se generó el PDF en:\n{pdf_path}")

    return pdf_path


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES PÚBLICAS DE GENERACIÓN DE INFORMES
# ═══════════════════════════════════════════════════════════════════════════════


def generar_informe_equipos_jugadores(ruta_destino=None, equipo_id=None):
    """
    Genera el Informe 1 – Equipos y Jugadores.

    Args:
        ruta_destino (str | None): Ruta completa del PDF (.pdf).
        equipo_id (int | None): Filtrar por un equipo concreto.

    Returns:
        str: Ruta del PDF generado.
    """
    if ruta_destino is None:
        ruta_destino = os.path.join(
            _ruta_reports(),
            f"Informe_Equipos_Jugadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )

    parametros = {}
    if equipo_id is not None:
        parametros["EQUIPO_ID"] = equipo_id

    return _generar_informe_jasper(
        "Informe_Equipos_Jugadores.jrxml", ruta_destino, parametros
    )


def generar_informe_partidos_resultados(ruta_destino=None, eliminatoria=None):
    """
    Genera el Informe 2 – Partidos y Resultados.

    Args:
        ruta_destino (str | None): Ruta completa del PDF (.pdf).
        eliminatoria (str | None): Filtrar por eliminatoria.

    Returns:
        str: Ruta del PDF generado.
    """
    if ruta_destino is None:
        ruta_destino = os.path.join(
            _ruta_reports(),
            f"Informe_Partidos_Resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )

    parametros = {}
    if eliminatoria is not None:
        parametros["ELIMINATORIA"] = eliminatoria

    return _generar_informe_jasper(
        "Informe_Partidos_Resultados.jrxml", ruta_destino, parametros
    )


def generar_informe_clasificacion(ruta_destino=None, eliminatoria=None):
    """
    Genera el Informe 3 – Clasificación y Eliminatorias.

    Args:
        ruta_destino (str | None): Ruta completa del PDF (.pdf).
        eliminatoria (str | None): Filtrar por eliminatoria.

    Returns:
        str: Ruta del PDF generado.
    """
    if ruta_destino is None:
        ruta_destino = os.path.join(
            _ruta_reports(),
            f"Informe_Clasificacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )

    parametros = {}
    if eliminatoria is not None:
        parametros["ELIMINATORIA"] = eliminatoria

    return _generar_informe_jasper(
        "Informe_Clasificacion.jrxml", ruta_destino, parametros
    )
