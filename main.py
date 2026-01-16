"""
Punto de entrada principal de la aplicación de Gestión de Torneo de Fútbol.

Este módulo inicializa la aplicación, conecta la base de datos,
carga los estilos QSS y lanza la ventana principal.

Autor: [Nombre del autor]
Versión: 1.0
Fecha: 08/01/2026
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTranslator, QLocale, QLibraryInfo
from Models import database


def obtener_ruta_recurso(ruta_relativa):
    """
    Obtiene la ruta absoluta de un recurso.
    Compatible con PyInstaller para el ejecutable.

    Args:
        ruta_relativa (str): Ruta relativa del recurso

    Returns:
        str: Ruta absoluta del recurso
    """
    if getattr(sys, "frozen", False):
        # Ejecutando como ejecutable empaquetado
        ruta_base = sys._MEIPASS
    else:
        # Ejecutando en modo desarrollo
        ruta_base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(ruta_base, ruta_relativa)


def cargar_stylesheet(ruta):
    """
    Carga el archivo QSS y lo devuelve como string.

    Args:
        ruta (str): Ruta al archivo QSS

    Returns:
        str: Contenido del archivo QSS
    """
    try:
        ruta_absoluta = obtener_ruta_recurso(ruta)
        with open(ruta_absoluta, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo QSS en {ruta}")
        return ""
    except Exception as e:
        print(f"Error al cargar stylesheet: {e}")
        return ""


def main():
    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    # Configurar High DPI antes de crear QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)

    # Configurar traductor para español
    translator = QTranslator(app)
    # Intentar cargar la traducción de Qt en español
    qt_translations_path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    if translator.load(QLocale(QLocale.Spanish), "qtbase", "_", qt_translations_path):
        app.installTranslator(translator)

    # Configurar propiedades de la aplicación
    app.setApplicationName("Gestión Torneo de Fútbol")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Instituto")

    try:
        # Conectar a la base de datos
        print("Iniciando conexión a la base de datos...")
        db = database.conectar()
        print("Base de datos inicializada correctamente\n")

        # Cargar estilos QSS
        print("Cargando estilos visuales...")
        qss = cargar_stylesheet("Resources/qss/style.qss")
        if qss:
            app.setStyleSheet(qss)
            print("Estilos aplicados correctamente\n")

        # Importar y mostrar la ventana principal
        # NOTA: Se importa aquí para que la base de datos esté conectada primero
        from Views.mainwindow import MainWindow

        ventana_principal = MainWindow()
        ventana_principal.show()

        print("Aplicación iniciada correctamente")
        print("=" * 50)

        # Ejecutar el bucle de eventos de la aplicación
        codigo_salida = app.exec()

        # Cerrar conexión a la base de datos al salir
        database.cerrar_conexion()

        sys.exit(codigo_salida)

    except Exception as e:
        # Manejar errores críticos
        import traceback

        print(f"Error crítico al iniciar la aplicación: {e}")
        print("\nTraceback completo:")
        traceback.print_exc()
        QMessageBox.critical(
            None,
            "Error de inicio",
            f"No se pudo iniciar la aplicación:\n\n{str(e)}\n\nPor favor, contacte con el soporte técnico.",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
