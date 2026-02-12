"""Pantalla de Informes del Torneo.

Diseño hecho en ui con QTDesigner en Resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

Permite seleccionar tipo de informe, aplicar filtros y generar PDFs.
Incluye vista previa del PDF generado y selección de ruta de guardado.
"""

from __future__ import annotations

import os
import sys
import subprocess
import time

from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QProgressBar,
    QStackedWidget,
    QScrollArea,
    QGridLayout,
    QSpacerItem,
    QAbstractItemView,
)

from Views.base_page import BasePage


def _ruta_proyecto():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ruta_reports_vista():
    """Ruta de reports para la vista (donde guardar PDFs generados)."""
    if getattr(sys, "frozen", False):
        # Guardar PDFs junto al ejecutable en carpeta reports/
        ruta = os.path.join(os.path.dirname(sys.executable), "reports")
    else:
        ruta = os.path.join(_ruta_proyecto(), "reports")
    os.makedirs(ruta, exist_ok=True)
    return ruta


class InformesPage(BasePage):
    """Página de generación de informes PDF del torneo."""

    INFORMES = [
        (
            "Equipos y Jugadores",
            "equipos_jugadores",
            "Listado completo de equipos, jugadores, estadísticas y destacados.",
        ),
        (
            "Partidos y Resultados",
            "partidos_resultados",
            "Listado cronológico de partidos, resultados e historial de enfrentamientos.",
        ),
        (
            "Clasificación y Eliminatorias",
            "clasificacion",
            "Tabla de clasificación, cuadro de emparejamientos y estadísticas globales.",
        ),
    ]

    def __init__(self, parent=None):
        super().__init__("Informes del Torneo", parent)
        self._ultimo_pdf = None
        self._construir_ui()

    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ─────────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        """Construye toda la interfaz de la página de informes."""
        # Panel principal con splitter vertical
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(6)

        # ── Panel Izquierdo: Controles ──
        panel_izq = self._crear_panel_controles()
        splitter.addWidget(panel_izq)

        # ── Panel Derecho: Vista previa / Info ──
        panel_der = self._crear_panel_preview()
        splitter.addWidget(panel_der)

        # Proporciones 40/60
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        self.contenido_layout.addWidget(splitter, 1)

    def _crear_panel_controles(self):
        """Crea el panel izquierdo con selector de informe, filtros y botones."""
        panel = QFrame()
        panel.setObjectName("panel_informes_controles")
        panel.setStyleSheet(
            """
            QFrame#panel_informes_controles {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 14px;
                padding: 10px;
            }
        """
        )
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ── Selector de informe ──
        lbl_informe = QLabel("Seleccionar Informe:")
        lbl_informe.setStyleSheet("font-weight: bold; font-size: 11pt; color: #1a5490;")
        layout.addWidget(lbl_informe)

        self.combo_informe = QComboBox()
        self.combo_informe.setMinimumHeight(36)
        self.combo_informe.setStyleSheet(
            """
            QComboBox {
                padding: 6px 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
                font-size: 10pt;
            }
            QComboBox:focus { border-color: #1a5490; }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #bdc3c7;
                selection-background-color: #1a5490;
                selection-color: white;
                color: #2c3e50;
                padding: 4px;
            }
        """
        )
        for nombre, clave, desc in self.INFORMES:
            self.combo_informe.addItem(nombre, clave)
        self.combo_informe.currentIndexChanged.connect(self._on_informe_cambiado)
        layout.addWidget(self.combo_informe)

        # Descripción del informe
        self.lbl_descripcion = QLabel()
        self.lbl_descripcion.setWordWrap(True)
        self.lbl_descripcion.setStyleSheet(
            """
            color: #7f8c8d; font-size: 9pt; padding: 4px 2px;
            background: transparent;
        """
        )
        layout.addWidget(self.lbl_descripcion)

        # ── Grupo de Filtros ──
        self.grupo_filtros = QGroupBox("Filtros")
        self.grupo_filtros.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold; font-size: 10pt; color: #2c3e50;
                border: 2px solid #dfe6e9; border-radius: 10px;
                margin-top: 8px; padding-top: 18px;
                background: rgba(245, 248, 250, 0.6);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """
        )
        filtros_layout = QVBoxLayout(self.grupo_filtros)
        filtros_layout.setContentsMargins(12, 12, 12, 12)
        filtros_layout.setSpacing(8)

        # Filtro por equipo
        self.lbl_filtro_equipo = QLabel("Equipo:")
        self.lbl_filtro_equipo.setStyleSheet(
            "font-weight: normal; font-size: 9pt; background: transparent;"
        )
        self.combo_equipo = QComboBox()
        self.combo_equipo.setMinimumHeight(32)
        self.combo_equipo.setStyleSheet(
            """
            QComboBox {
                padding: 4px 10px; border: 1px solid #bdc3c7;
                border-radius: 6px; background: white; font-size: 9pt;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #bdc3c7;
                selection-background-color: #1a5490;
                selection-color: white;
                color: #2c3e50;
                padding: 4px;
            }
        """
        )
        filtros_layout.addWidget(self.lbl_filtro_equipo)
        filtros_layout.addWidget(self.combo_equipo)

        # Filtro por eliminatoria
        self.lbl_filtro_eliminatoria = QLabel("Eliminatoria:")
        self.lbl_filtro_eliminatoria.setStyleSheet(
            "font-weight: normal; font-size: 9pt; background: transparent;"
        )
        self.combo_eliminatoria = QComboBox()
        self.combo_eliminatoria.setMinimumHeight(32)
        self.combo_eliminatoria.setStyleSheet(
            """
            QComboBox {
                padding: 4px 10px; border: 1px solid #bdc3c7;
                border-radius: 6px; background: white; font-size: 9pt;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #bdc3c7;
                selection-background-color: #1a5490;
                selection-color: white;
                color: #2c3e50;
                padding: 4px;
            }
        """
        )
        filtros_layout.addWidget(self.lbl_filtro_eliminatoria)
        filtros_layout.addWidget(self.combo_eliminatoria)

        layout.addWidget(self.grupo_filtros)

        # ── Ruta de guardado ──
        grupo_ruta = QGroupBox("Ruta de Guardado")
        grupo_ruta.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold; font-size: 10pt; color: #2c3e50;
                border: 2px solid #dfe6e9; border-radius: 10px;
                margin-top: 8px; padding-top: 18px;
                background: rgba(245, 248, 250, 0.6);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """
        )
        ruta_layout = QHBoxLayout(grupo_ruta)
        ruta_layout.setContentsMargins(12, 12, 12, 12)

        self.txt_ruta = QLineEdit()
        self.txt_ruta.setPlaceholderText("Carpeta reports (por defecto)")
        self.txt_ruta.setReadOnly(True)
        self.txt_ruta.setStyleSheet(
            """
            QLineEdit {
                padding: 6px 10px; border: 1px solid #bdc3c7;
                border-radius: 6px; background: #fafafa; font-size: 9pt;
            }
        """
        )
        ruta_layout.addWidget(self.txt_ruta, 1)

        btn_ruta = QPushButton("📁 Cambiar")
        btn_ruta.setMinimumHeight(32)
        btn_ruta.setCursor(Qt.PointingHandCursor)
        btn_ruta.setStyleSheet(
            """
            QPushButton {
                padding: 6px 14px; background: #74b9ff; color: white;
                border-radius: 6px; font-weight: bold; font-size: 9pt; border: none;
            }
            QPushButton:hover { background: #0984e3; }
        """
        )
        btn_ruta.clicked.connect(self._seleccionar_ruta)
        ruta_layout.addWidget(btn_ruta)

        layout.addWidget(grupo_ruta)

        # ── Botones de acción ──
        layout.addSpacerItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.btn_generar = QPushButton("📄  Generar Informe PDF")
        self.btn_generar.setMinimumHeight(46)
        self.btn_generar.setCursor(Qt.PointingHandCursor)
        self.btn_generar.setStyleSheet(
            """
            QPushButton {
                padding: 10px 20px; background: #00b894; color: white;
                border-radius: 10px; font-weight: bold; font-size: 12pt;
                border: none;
            }
            QPushButton:hover { background: #00a381; }
            QPushButton:pressed { background: #009070; }
        """
        )
        self.btn_generar.clicked.connect(self._generar_informe)
        layout.addWidget(self.btn_generar)

        # Botón abrir último PDF
        self.btn_abrir_pdf = QPushButton("🔍  Abrir Último PDF Generado")
        self.btn_abrir_pdf.setMinimumHeight(36)
        self.btn_abrir_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_abrir_pdf.setEnabled(False)
        self.btn_abrir_pdf.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px; background: #636e72; color: white;
                border-radius: 8px; font-weight: bold; font-size: 10pt; border: none;
            }
            QPushButton:hover { background: #2d3436; }
            QPushButton:disabled { background: #b2bec3; color: #dfe6e9; }
        """
        )
        self.btn_abrir_pdf.clicked.connect(self._abrir_ultimo_pdf)
        layout.addWidget(self.btn_abrir_pdf)

        # Botón abrir carpeta reports
        btn_carpeta = QPushButton("📂  Abrir Carpeta Reports")
        btn_carpeta.setMinimumHeight(32)
        btn_carpeta.setCursor(Qt.PointingHandCursor)
        btn_carpeta.setStyleSheet(
            """
            QPushButton {
                padding: 6px 14px; background: #a29bfe; color: white;
                border-radius: 8px; font-weight: bold; font-size: 9pt; border: none;
            }
            QPushButton:hover { background: #6c5ce7; }
        """
        )
        btn_carpeta.clicked.connect(self._abrir_carpeta_reports)
        layout.addWidget(btn_carpeta)

        return panel

    def _crear_panel_preview(self):
        """Crea el panel derecho con información y vista previa."""
        panel = QFrame()
        panel.setObjectName("panel_informes_preview")
        panel.setStyleSheet(
            """
            QFrame#panel_informes_preview {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 14px;
                padding: 10px;
            }
        """
        )
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        lbl_titulo = QLabel("Vista Previa / Información")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 11pt; color: #1a5490;")
        layout.addWidget(lbl_titulo)

        self.text_preview = QTextBrowser()
        self.text_preview.setOpenExternalLinks(True)
        self.text_preview.setStyleSheet(
            """
            QTextBrowser {
                background: #fafafa; border: 1px solid #dfe6e9;
                border-radius: 8px; padding: 10px; font-size: 9pt;
            }
        """
        )
        layout.addWidget(self.text_preview, 1)

        # Barra de estado
        self.lbl_estado = QLabel("Listo. Selecciona un informe y pulsa Generar.")
        self.lbl_estado.setStyleSheet(
            """
            color: #636e72; font-size: 9pt; padding: 4px 8px;
            background: rgba(223,230,233,0.5); border-radius: 6px;
        """
        )
        layout.addWidget(self.lbl_estado)

        return panel

    # ─────────────────────────────────────────────────────────────────────────
    # LÓGICA DE EVENTOS
    # ─────────────────────────────────────────────────────────────────────────

    def on_show(self):
        """Se llama cuando se muestra la página. Recarga filtros."""
        self._cargar_filtros()
        self._on_informe_cambiado(self.combo_informe.currentIndex())

    def _cargar_filtros(self):
        """Carga las opciones de filtro desde la base de datos."""
        from Controllers.informes_controller import (
            obtener_lista_equipos,
            obtener_lista_eliminatorias,
        )

        # Equipos
        self.combo_equipo.clear()
        self.combo_equipo.addItem("— Todos los equipos —", None)
        for eid, nombre in obtener_lista_equipos():
            self.combo_equipo.addItem(nombre, eid)

        # Eliminatorias
        self.combo_eliminatoria.clear()
        self.combo_eliminatoria.addItem("— Todas las eliminatorias —", None)
        for e in obtener_lista_eliminatorias():
            self.combo_eliminatoria.addItem(e, e)

    def _on_informe_cambiado(self, index):
        """Ajusta los controles visibles según el tipo de informe."""
        if index < 0 or index >= len(self.INFORMES):
            return

        nombre, clave, desc = self.INFORMES[index]
        self.lbl_descripcion.setText(desc)

        # Mostrar/ocultar filtros según el informe
        es_equipos = clave == "equipos_jugadores"
        es_partidos = clave == "partidos_resultados"
        es_clasificacion = clave == "clasificacion"

        self.lbl_filtro_equipo.setVisible(es_equipos)
        self.combo_equipo.setVisible(es_equipos)
        self.lbl_filtro_eliminatoria.setVisible(es_partidos or es_clasificacion)
        self.combo_eliminatoria.setVisible(es_partidos or es_clasificacion)

        # Actualizar vista previa con información del informe
        self._mostrar_info_informe(clave)

    def _mostrar_info_informe(self, clave):
        """Muestra información descriptiva del informe seleccionado en el panel."""
        info = {
            "equipos_jugadores": """
                <h3 style='color:#1a5490;'>📋 Informe Equipos y Jugadores</h3>
                <p>Este informe genera un listado completo con:</p>
                <ul>
                    <li><b>Equipos</b> en orden alfabético con todos sus jugadores</li>
                    <li><b>Datos por jugador:</b> Posición, goles, tarjetas amarillas y rojas</li>
                    <li><b>Estadísticas por equipo:</b> Total goles, tarjetas y promedio de goles/jugador</li>
                    <li><b>Destacados:</b> Jugadores con más goles y más tarjetas resaltados</li>
                </ul>
                <p><i>Filtro disponible: por equipo específico</i></p>
            """,
            "partidos_resultados": """
                <h3 style='color:#1a5490;'>⚽ Informe Partidos y Resultados</h3>
                <p>Listado cronológico y por eliminatoria con:</p>
                <ul>
                    <li><b>Información:</b> Equipos, árbitro, fecha/hora, eliminatoria</li>
                    <li><b>Resultados:</b> Marcador final (incluyendo prórroga y penales)</li>
                    <li><b>Historial:</b> Enfrentamientos previos entre equipos</li>
                    <li><b>Pendientes:</b> Partidos sin jugar resaltados en naranja</li>
                </ul>
                <p><i>Filtro disponible: por eliminatoria</i></p>
            """,
            "clasificacion": """
                <h3 style='color:#1a5490;'>🏆 Informe Clasificación y Eliminatorias</h3>
                <p>Informe completo con:</p>
                <ul>
                    <li><b>Tabla de clasificación:</b> PJ, V, E, D, GF, GC, Diferencia</li>
                    <li><b>Cuadro de eliminatorias:</b> Octavos → Cuartos → Semifinales → Final</li>
                    <li><b>Estadísticas globales:</b> Goles y tarjetas por eliminatoria</li>
                    <li><b>Comparativa:</b> Más victorias, más goles, menos goles recibidos</li>
                </ul>
                <p><i>Filtro disponible: por eliminatoria específica</i></p>
            """,
        }
        self.text_preview.setHtml(info.get(clave, ""))

    def _seleccionar_ruta(self):
        """Abre diálogo para seleccionar carpeta de guardado."""
        ruta_actual = self.txt_ruta.text() or _ruta_reports_vista()
        carpeta = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta de guardado", ruta_actual
        )
        if carpeta:
            self.txt_ruta.setText(carpeta)

    def _generar_informe(self):
        """Genera el informe PDF seleccionado."""
        from Controllers.informes_controller import (
            generar_informe_equipos_jugadores,
            generar_informe_partidos_resultados,
            generar_informe_clasificacion,
            JASPER_DISPONIBLE,
        )

        if not JASPER_DISPONIBLE:
            QMessageBox.critical(
                self,
                "Error",
                "La librería pyreportjasper no está instalada.\n\n"
                "Ejecuta en terminal:\n  pip install pyreportjasper",
            )
            return

        index = self.combo_informe.currentIndex()
        if index < 0:
            return

        clave = self.INFORMES[index][1]
        nombre_informe = self.INFORMES[index][0]

        # Determinar ruta de destino
        carpeta = self.txt_ruta.text() or _ruta_reports_vista()
        os.makedirs(carpeta, exist_ok=True)

        self.lbl_estado.setText(f"Generando informe: {nombre_informe}...")
        self.lbl_estado.setStyleSheet(
            """
            color: #0984e3; font-size: 9pt; padding: 4px 8px;
            background: rgba(116,185,255,0.2); border-radius: 6px;
        """
        )
        self.btn_generar.setEnabled(False)

        # Importar QApplication para procesar eventos durante la generación
        from PySide6.QtWidgets import QApplication

        QApplication.processEvents()

        try:
            ruta_pdf = None

            if clave == "equipos_jugadores":
                equipo_id = self.combo_equipo.currentData()
                # Convertir a int si no es None (puede venir como Long de Qt)
                if equipo_id is not None:
                    equipo_id = int(equipo_id)
                from datetime import datetime

                nombre_archivo = os.path.join(
                    carpeta,
                    f"Informe_Equipos_Jugadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                )
                ruta_pdf = generar_informe_equipos_jugadores(nombre_archivo, equipo_id)

            elif clave == "partidos_resultados":
                eliminatoria = self.combo_eliminatoria.currentData()
                from datetime import datetime

                nombre_archivo = os.path.join(
                    carpeta,
                    f"Informe_Partidos_Resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                )
                ruta_pdf = generar_informe_partidos_resultados(
                    nombre_archivo, eliminatoria
                )

            elif clave == "clasificacion":
                eliminatoria = self.combo_eliminatoria.currentData()
                from datetime import datetime

                nombre_archivo = os.path.join(
                    carpeta,
                    f"Informe_Clasificacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                )
                ruta_pdf = generar_informe_clasificacion(nombre_archivo, eliminatoria)

            if ruta_pdf and os.path.exists(ruta_pdf):
                ruta_normalizada = os.path.normpath(os.path.abspath(ruta_pdf))
                self._ultimo_pdf = ruta_normalizada
                self.btn_abrir_pdf.setEnabled(True)
                self.lbl_estado.setText(
                    f"✅ Informe generado: {os.path.basename(ruta_pdf)}"
                )
                self.lbl_estado.setStyleSheet(
                    """
                    color: #00b894; font-size: 9pt; padding: 4px 8px;
                    background: rgba(0,184,148,0.15); border-radius: 6px;
                """
                )

                # Mostrar resumen en vista previa
                self.text_preview.setHtml(
                    f"""
                    <h3 style='color:#00b894;'>✅ Informe Generado Correctamente</h3>
                    <p><b>Informe:</b> {nombre_informe}</p>
                    <p><b>Archivo:</b> {os.path.basename(ruta_pdf)}</p>
                    <p><b>Ubicación:</b> {os.path.dirname(ruta_pdf)}</p>
                    <p><b>Tamaño:</b> {os.path.getsize(ruta_pdf) / 1024:.1f} KB</p>
                    <hr>
                    <p>Puedes abrir el PDF con el botón <b>"Abrir Último PDF"</b>
                    o acceder a la carpeta con <b>"Abrir Carpeta Reports"</b>.</p>
                """
                )
            else:
                error_msg = ruta_pdf if ruta_pdf else "Error desconocido"
                self.lbl_estado.setText(f"❌ Error: {error_msg}")
                self.lbl_estado.setStyleSheet(
                    """
                    color: #e74c3c; font-size: 9pt; padding: 4px 8px;
                    background: rgba(231,76,60,0.15); border-radius: 6px;
                """
                )

        except Exception as e:
            QMessageBox.critical(self, "Error al generar informe", str(e))
            self.lbl_estado.setText(f"❌ Error: {str(e)}")
            self.lbl_estado.setStyleSheet(
                """
                color: #e74c3c; font-size: 9pt; padding: 4px 8px;
                background: rgba(231,76,60,0.15); border-radius: 6px;
            """
            )
        finally:
            self.btn_generar.setEnabled(True)

    def _abrir_ultimo_pdf(self):
        """Abre el último PDF generado con el visor predeterminado del sistema."""
        if self._ultimo_pdf and os.path.exists(self._ultimo_pdf):
            # Reintentar si el archivo está bloqueado
            max_intentos = 3
            for intento in range(max_intentos):
                try:
                    # Intentar abrir con ruta absoluta normalizada
                    ruta_normalizada = os.path.normpath(
                        os.path.abspath(self._ultimo_pdf)
                    )
                    if sys.platform == "win32":
                        os.startfile(ruta_normalizada)
                    else:
                        QDesktopServices.openUrl(QUrl.fromLocalFile(ruta_normalizada))
                    break
                except Exception as e:
                    if intento < max_intentos - 1:
                        time.sleep(1)  # Esperar 1 segundo antes de reintentar
                    else:
                        QMessageBox.warning(
                            self,
                            "Error al abrir PDF",
                            f"No se pudo abrir el archivo:\n{str(e)}\n\n"
                            f"Puedes abrirlo manualmente desde:\n{self._ultimo_pdf}",
                        )
        else:
            QMessageBox.warning(self, "Aviso", "No hay ningún PDF generado todavía.")

    def _abrir_carpeta_reports(self):
        """Abre la carpeta reports en el explorador de archivos."""
        ruta = _ruta_reports_vista()
        if sys.platform == "win32":
            os.startfile(ruta)
        elif sys.platform == "darwin":
            subprocess.run(["open", ruta])
        else:
            subprocess.run(["xdg-open", ruta])
