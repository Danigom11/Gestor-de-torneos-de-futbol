"""Pantalla de Resultados - Gestión de Resultados de Partidos.

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python para hacerlo más escalable, mantenible y mejorable. Menos estático.

Lado izquierdo (1/3): Lista scrollable de partidos registrados.
Lado derecho (2/3): Al seleccionar un partido, muestra los equipos con sus jugadores y controles para registrar goles y tarjetas.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QDialog,
    QLineEdit,
    QGridLayout,
    QFileDialog,
)
from PySide6.QtGui import QPixmap

from Models.equipo import Equipo
from Models.gol import Gol
from Models.partido import Partido
from Models.tarjeta import Tarjeta
from Views.base_page import BasePage
from Views.utils import obtener_ruta_recurso


class ResultadosPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Actualización de Resultados", parent)

        # Inicializar diccionario de inputs antes de crear la UI
        self._inputs_jugadores = {}

        # Panel principal translúcido
        panel_principal = QFrame()
        panel_principal.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 12px;
            }
        """
        )

        layout_principal = QVBoxLayout(panel_principal)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setSpacing(10)

        # Splitter para dividir izquierda/derecha
        self.splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo: Lista de partidos (1/3)
        self.panel_izquierdo = self._crear_panel_izquierdo()
        self.splitter.addWidget(self.panel_izquierdo)

        # Panel derecho: Edición de resultados (2/3)
        self.panel_derecho = self._crear_panel_derecho()
        self.splitter.addWidget(self.panel_derecho)

        # Proporciones 1:2
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        layout_principal.addWidget(self.splitter)
        self.contenido_layout.addWidget(panel_principal)

        self.partido_seleccionado = None

    def _crear_panel_izquierdo(self):
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: rgba(236, 240, 241, 0.95);
                border-radius: 8px;
            }
        """
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Título
        lbl_titulo = QLabel("Partidos Registrados")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet(
            """
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: white;
                padding: 8px;
                background-color: #34495e;
                border-radius: 6px;
            }
        """
        )
        layout.addWidget(lbl_titulo)

        # Botón de exportación CSV
        self.btn_exportar = QPushButton("📊 Exportar a CSV")
        self.btn_exportar.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """
        )
        self.btn_exportar.setMinimumHeight(35)
        self.btn_exportar.clicked.connect(self._exportar_csv)
        layout.addWidget(self.btn_exportar)

        # Lista de partidos
        self.lista_partidos = QListWidget()
        self.lista_partidos.setStyleSheet(
            """
            QListWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
            }
        """
        )
        self.lista_partidos.itemClicked.connect(self._seleccionar_partido)
        layout.addWidget(self.lista_partidos)

        return panel

    def _crear_panel_derecho(self):
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: rgba(236, 240, 241, 0.95);
                border-radius: 8px;
            }
        """
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Instrucción inicial
        self.lbl_instruccion = QLabel("Selecciona un partido de la lista")
        self.lbl_instruccion.setAlignment(Qt.AlignCenter)
        self.lbl_instruccion.setStyleSheet(
            """
            QLabel {
                font-size: 12pt;
                color: #7f8c8d;
                padding: 20px;
            }
        """
        )
        layout.addWidget(self.lbl_instruccion)

        # Contenedor scroll para equipos (inicialmente oculto)
        self.scroll_equipos = QScrollArea()
        self.scroll_equipos.setWidgetResizable(True)
        self.scroll_equipos.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )
        self.scroll_equipos.setVisible(False)

        self.widget_equipos = QWidget()
        self.layout_equipos = QHBoxLayout(self.widget_equipos)
        self.layout_equipos.setSpacing(15)

        self.scroll_equipos.setWidget(self.widget_equipos)
        layout.addWidget(self.scroll_equipos, 1)

        # Botón guardar (inicialmente oculto)
        self.btn_guardar = QPushButton("💾 Guardar Resultado")
        self.btn_guardar.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """
        )
        self.btn_guardar.setMinimumHeight(45)
        self.btn_guardar.setVisible(False)
        self.btn_guardar.clicked.connect(self._guardar_resultado)
        layout.addWidget(self.btn_guardar)

        return panel

    def on_show(self):
        """Llamado cuando se muestra la página."""
        self.cargar_partidos()

    def cargar_partidos(self):
        """Carga todos los partidos en la lista con escudos."""
        self.lista_partidos.clear()

        partidos = Partido.obtener_todos()
        if not partidos:
            item = QListWidgetItem("No hay partidos registrados")
            item.setFlags(Qt.ItemIsEnabled)
            self.lista_partidos.addItem(item)
            return

        for partido in partidos:
            e_local = Equipo.obtener_por_id(partido.equipo_local_id)
            e_vis = Equipo.obtener_por_id(partido.equipo_visitante_id)

            # Crear widget personalizado con escudos
            item_widget = self._crear_item_partido(partido, e_local, e_vis)

            item = QListWidgetItem()
            item.setData(Qt.UserRole, partido)
            item.setSizeHint(QSize(item_widget.sizeHint().width(), 50))
            self.lista_partidos.addItem(item)
            self.lista_partidos.setItemWidget(item, item_widget)

    def _crear_item_partido(self, partido: Partido, e_local: Equipo, e_vis: Equipo):
        """Crea un widget para mostrar un partido en la lista con escudos."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Escudo local
        if e_local and e_local.escudo:
            escudo_local = QLabel()
            ruta_escudo = obtener_ruta_recurso(
                f"Resources/img/escudos/{e_local.escudo}"
            )
            pixmap = QPixmap(ruta_escudo)
            if not pixmap.isNull():
                escudo_local.setPixmap(
                    pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            layout.addWidget(escudo_local)

        # Nombre local
        lbl_local = QLabel(e_local.nombre if e_local else "???")
        lbl_local.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl_local)

        # Marcador o VS
        if partido.jugado:
            lbl_marcador = QLabel(f"{partido.goles_local} - {partido.goles_visitante}")
            lbl_marcador.setStyleSheet(
                "color: #27ae60; font-weight: bold; font-size: 11pt;"
            )
        else:
            lbl_marcador = QLabel("vs")
            lbl_marcador.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(lbl_marcador)

        # Nombre visitante
        lbl_vis = QLabel(e_vis.nombre if e_vis else "???")
        lbl_vis.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl_vis)

        # Escudo visitante
        if e_vis and e_vis.escudo:
            escudo_vis = QLabel()
            ruta_escudo = obtener_ruta_recurso(f"Resources/img/escudos/{e_vis.escudo}")
            pixmap = QPixmap(ruta_escudo)
            if not pixmap.isNull():
                escudo_vis.setPixmap(
                    pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            layout.addWidget(escudo_vis)

        # Eliminatoria
        lbl_elim = QLabel(f"[{partido.eliminatoria}]")
        lbl_elim.setStyleSheet("color: #95a5a6; font-size: 9pt;")
        layout.addWidget(lbl_elim)

        layout.addStretch()
        return widget

    def _seleccionar_partido(self, item):
        """Maneja la selección de un partido."""
        partido = item.data(Qt.UserRole)
        if not partido:
            return

        self.partido_seleccionado = partido

        # Limpiar inputs anteriores para evitar referencias a widgets eliminados
        self._inputs_jugadores = {}

        # Ocultar instrucción
        self.lbl_instruccion.setVisible(False)

        # Mostrar scroll y botón
        self.scroll_equipos.setVisible(True)
        self.btn_guardar.setVisible(True)

        # Limpiar contenido anterior
        while self.layout_equipos.count():
            child = self.layout_equipos.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Obtener equipos
        e_local = Equipo.obtener_por_id(partido.equipo_local_id)
        e_vis = Equipo.obtener_por_id(partido.equipo_visitante_id)

        # Crear paneles de equipos
        if e_local:
            panel_local = self._crear_panel_equipo(e_local, partido, "local")
            self.layout_equipos.addWidget(panel_local)

        if e_vis:
            panel_vis = self._crear_panel_equipo(e_vis, partido, "visitante")
            self.layout_equipos.addWidget(panel_vis)

    def _crear_panel_equipo(self, equipo: Equipo, partido: Partido, lado: str):
        """Crea el panel de un equipo con sus jugadores."""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #dfe6e9;
                border-radius: 10px;
            }
        """
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Contenedor de título con escudo y nombre
        titulo_container = QWidget()
        titulo_layout = QHBoxLayout(titulo_container)
        titulo_layout.setContentsMargins(8, 6, 8, 6)
        titulo_layout.setSpacing(8)

        # Escudo del equipo
        if equipo.escudo:
            lbl_escudo = QLabel()
            ruta_escudo = obtener_ruta_recurso(f"Resources/img/escudos/{equipo.escudo}")
            pixmap = QPixmap(ruta_escudo)
            if not pixmap.isNull():
                lbl_escudo.setPixmap(
                    pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            titulo_layout.addWidget(lbl_escudo)

        # Nombre del equipo
        lbl_equipo = QLabel(equipo.nombre)
        lbl_equipo.setStyleSheet(
            """
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #2c3e50;
            }
        """
        )
        titulo_layout.addWidget(lbl_equipo, 1)

        titulo_container.setStyleSheet(
            """
            QWidget {
                background-color: #ecf0f1;
                border-radius: 6px;
            }
        """
        )
        layout.addWidget(titulo_container)

        # Cabecera de columnas
        cabecera = QWidget()
        layout_cabecera = QHBoxLayout(cabecera)
        layout_cabecera.setContentsMargins(5, 3, 5, 3)

        lbl_jugador = QLabel("Jugador")
        lbl_jugador.setStyleSheet("font-weight: bold; font-size: 10pt;")

        lbl_tarjetas = QLabel("Tarjetas")
        lbl_tarjetas.setAlignment(Qt.AlignCenter)
        lbl_tarjetas.setStyleSheet("font-weight: bold; font-size: 10pt;")

        lbl_goles = QLabel("Goles")
        lbl_goles.setAlignment(Qt.AlignCenter)
        lbl_goles.setStyleSheet("font-weight: bold; font-size: 10pt;")

        layout_cabecera.addWidget(lbl_jugador, 2)
        layout_cabecera.addWidget(lbl_tarjetas, 1)
        layout_cabecera.addWidget(lbl_goles, 1)

        layout.addWidget(cabecera)

        # Scroll con jugadores
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        contenedor_jugadores = QWidget()
        layout_jugadores = QVBoxLayout(contenedor_jugadores)
        layout_jugadores.setSpacing(5)
        layout_jugadores.setContentsMargins(0, 0, 0, 0)

        # Obtener jugadores
        jugadores = Equipo.obtener_jugadores(equipo.id)
        goles_actuales = Gol.obtener_por_partido(partido.id)
        tarjetas_actuales = Tarjeta.obtener_por_partido(partido.id)

        # Crear fila por cada jugador
        for jugador in jugadores:
            fila = self._crear_fila_jugador(
                jugador, goles_actuales, tarjetas_actuales, lado
            )
            layout_jugadores.addWidget(fila)

        layout_jugadores.addStretch()
        scroll.setWidget(contenedor_jugadores)
        layout.addWidget(scroll, 1)

        return panel

    def _crear_fila_jugador(
        self, jugador: dict, goles_actuales: list, tarjetas_actuales: list, lado: str
    ):
        """Crea una fila con los controles para un jugador."""
        fila = QFrame()
        fila.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 5px;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """
        )
        fila.setMinimumHeight(50)

        layout = QHBoxLayout(fila)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        # Nombre
        lbl_nombre = QLabel(jugador["nombre"])
        lbl_nombre.setStyleSheet("font-size: 10pt; color: #2c3e50;")
        layout.addWidget(lbl_nombre, 2)

        # Tarjetas - Cuadrados seleccionables
        widget_tarjetas = QWidget()
        layout_tarjetas = QHBoxLayout(widget_tarjetas)
        layout_tarjetas.setContentsMargins(0, 0, 0, 0)
        layout_tarjetas.setSpacing(5)
        layout_tarjetas.setAlignment(Qt.AlignCenter)

        # Cuadrado amarillo clickeable
        btn_amarilla = QPushButton()
        btn_amarilla.setCheckable(True)
        btn_amarilla.setFixedSize(30, 30)
        btn_amarilla.setStyleSheet(
            """
            QPushButton {
                background-color: #f1c40f;
                border: 2px solid #d4a506;
                border-radius: 3px;
            }
            QPushButton:checked {
                background-color: #d4a506;
                border: 3px solid #2c3e50;
            }
            QPushButton:hover {
                border: 3px solid #3498db;
            }
        """
        )

        # Cuadrado rojo clickeable
        btn_roja = QPushButton()
        btn_roja.setCheckable(True)
        btn_roja.setFixedSize(30, 30)
        btn_roja.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                border: 2px solid #c0392b;
                border-radius: 3px;
            }
            QPushButton:checked {
                background-color: #c0392b;
                border: 3px solid #2c3e50;
            }
            QPushButton:hover {
                border: 3px solid #3498db;
            }
        """
        )

        # Cargar estado actual
        for tarjeta in tarjetas_actuales:
            if tarjeta["jugador_id"] == jugador["id"]:
                if tarjeta["amarillas"] > 0:
                    btn_amarilla.setChecked(True)
                if tarjeta["rojas"] > 0:
                    btn_roja.setChecked(True)

        layout_tarjetas.addWidget(btn_amarilla)
        layout_tarjetas.addWidget(btn_roja)
        layout.addWidget(widget_tarjetas, 1)

        # Goles - QLineEdit simple
        txt_goles = QLineEdit()
        txt_goles.setPlaceholderText("0")
        txt_goles.setAlignment(Qt.AlignCenter)
        txt_goles.setMaxLength(2)
        txt_goles.setStyleSheet(
            """
            QLineEdit {
                font-size: 11pt;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #95a5a6;
            }
        """
        )
        txt_goles.setFixedWidth(55)

        # Cargar goles actuales
        for gol in goles_actuales:
            if gol["jugador_id"] == jugador["id"]:
                txt_goles.setText(str(gol["cantidad"]))
                break

        layout.addWidget(txt_goles, 1)

        # Guardar referencias
        self._inputs_jugadores[(lado, jugador["id"])] = {
            "amarilla": btn_amarilla,
            "roja": btn_roja,
            "goles": txt_goles,
        }

        return fila

    def _guardar_resultado(self):
        """Guarda el resultado del partido."""
        if not self.partido_seleccionado:
            return

        try:
            # Limpiar goles y tarjetas anteriores
            Gol.eliminar_por_partido(self.partido_seleccionado.id)
            Tarjeta.eliminar_por_partido(self.partido_seleccionado.id)

            total_local = 0
            total_visitante = 0

            # Procesar todos los inputs
            for (lado, jugador_id), controles in self._inputs_jugadores.items():
                # Obtener goles del QLineEdit
                texto_goles = controles["goles"].text().strip()
                goles = int(texto_goles) if texto_goles.isdigit() else 0

                # Registrar goles
                if goles > 0:
                    Gol.registrar_goles_partido(
                        self.partido_seleccionado.id, jugador_id, goles
                    )
                    if lado == "local":
                        total_local += goles
                    else:
                        total_visitante += goles

                # Registrar tarjetas
                if controles["amarilla"].isChecked():
                    Tarjeta.registrar_tarjetas_partido(
                        self.partido_seleccionado.id, jugador_id, amarillas=1
                    )
                if controles["roja"].isChecked():
                    Tarjeta.registrar_tarjetas_partido(
                        self.partido_seleccionado.id, jugador_id, rojas=1
                    )

            # Actualizar partido
            self.partido_seleccionado.goles_local = total_local
            self.partido_seleccionado.goles_visitante = total_visitante
            self.partido_seleccionado.jugado = True

            # Determinar ganador
            if total_local > total_visitante:
                self.partido_seleccionado.ganador_id = (
                    self.partido_seleccionado.equipo_local_id
                )
            elif total_visitante > total_local:
                self.partido_seleccionado.ganador_id = (
                    self.partido_seleccionado.equipo_visitante_id
                )
            else:
                self.partido_seleccionado.ganador_id = None  # Empate

            # Mostrar diálogo de confirmación deportivo
            e_local = Equipo.obtener_por_id(self.partido_seleccionado.equipo_local_id)
            e_vis = Equipo.obtener_por_id(self.partido_seleccionado.equipo_visitante_id)

            dialogo = DialogoConfirmacionResultado(
                self,
                e_local,
                e_vis,
                total_local,
                total_visitante,
                self._inputs_jugadores,
                self.partido_seleccionado,
            )

            if dialogo.exec() == QDialog.Accepted:
                # Guardar en BD
                self.partido_seleccionado.goles_local = total_local
                self.partido_seleccionado.goles_visitante = total_visitante
                self.partido_seleccionado.jugado = True

                if hasattr(self.partido_seleccionado, "actualizar"):
                    self.partido_seleccionado.actualizar()
                else:
                    self.partido_seleccionado.guardar()

                # Recargar lista
                self.cargar_partidos()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo guardar el resultado:\n{str(e)}"
            )

    def _exportar_csv(self):
        """Exporta todos los resultados de partidos a un archivo CSV."""
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Resultados como CSV",
            "resultados_partidos.csv",
            "Archivos CSV (*.csv)",
        )

        if ruta_archivo:
            if Partido.exportar_csv(ruta_archivo):
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Exportación exitosa")
                msg.setText(
                    f"Los resultados se han exportado correctamente a:\n{ruta_archivo}"
                )
                msg.setStyleSheet(
                    """
                    QMessageBox {
                        background-color: white;
                    }
                    QMessageBox QLabel {
                        color: #2c3e50;
                        background-color: transparent;
                    }
                    QMessageBox QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        min-width: 80px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #2980b9;
                    }
                    """
                )
                msg.exec()
            else:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error de exportación")
                msg.setText("No se pudo exportar los resultados. Intente nuevamente.")
                msg.setStyleSheet(
                    """
                    QMessageBox {
                        background-color: white;
                    }
                    QMessageBox QLabel {
                        color: #2c3e50;
                        background-color: transparent;
                    }
                    QMessageBox QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        min-width: 80px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #c0392b;
                    }
                    """
                )
                msg.exec()


class DialogoConfirmacionResultado(QDialog):
    """Diálogo grande tipo transmisión deportiva para confirmar resultado."""

    def __init__(
        self,
        parent,
        equipo_local,
        equipo_vis,
        goles_local,
        goles_vis,
        inputs_jugadores,
        partido,
    ):
        super().__init__(parent)
        self.setWindowTitle("Confirmación de Resultado")
        self.setModal(True)
        self.setMinimumSize(900, 700)

        # Fondo oscuro tipo pantalla deportiva
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        lbl_titulo = QLabel("RESUMEN DEL PARTIDO")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 24pt;
                font-weight: bold;
                padding: 10px;
                letter-spacing: 2px;
            }
        """
        )
        layout.addWidget(lbl_titulo)

        # Panel de resultado principal
        panel_resultado = self._crear_panel_resultado(
            equipo_local, equipo_vis, goles_local, goles_vis
        )
        layout.addWidget(panel_resultado)

        # Detalles (goleadores y tarjetas)
        panel_detalles = self._crear_panel_detalles(
            equipo_local, equipo_vis, inputs_jugadores, partido
        )
        layout.addWidget(panel_detalles, 1)

        # Botones
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(15)

        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("✅ Guardar y Confirmar")
        btn_guardar.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """
        )
        btn_guardar.clicked.connect(self.accept)

        layout_botones.addStretch()
        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)
        layout_botones.addStretch()

        layout.addLayout(layout_botones)

    def _crear_panel_resultado(self, e_local, e_vis, goles_local, goles_vis):
        """Crea el panel principal con equipos y marcador grande."""
        panel = QFrame()
        panel.setMinimumHeight(220)
        panel.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
            }
        """
        )

        layout = QHBoxLayout(panel)
        layout.setSpacing(30)

        # Equipo Local
        panel_local = QWidget()
        layout_local = QVBoxLayout(panel_local)
        layout_local.setSpacing(10)
        layout_local.setAlignment(Qt.AlignCenter)

        if e_local and e_local.escudo:
            escudo_local = QLabel()
            escudo_local.setMinimumSize(140, 140)
            ruta = obtener_ruta_recurso(f"Resources/img/escudos/{e_local.escudo}")
            pixmap = QPixmap(ruta)
            if not pixmap.isNull():
                escudo_local.setPixmap(
                    pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            escudo_local.setAlignment(Qt.AlignCenter)
            layout_local.addWidget(escudo_local)

        lbl_nombre_local = QLabel(e_local.nombre if e_local else "???")
        lbl_nombre_local.setAlignment(Qt.AlignCenter)
        lbl_nombre_local.setStyleSheet(
            """
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #2c3e50;
            }
        """
        )
        layout_local.addWidget(lbl_nombre_local)

        layout.addWidget(panel_local, 1)

        # Marcador
        panel_marcador = QWidget()
        layout_marcador = QVBoxLayout(panel_marcador)
        layout_marcador.setAlignment(Qt.AlignCenter)

        lbl_marcador = QLabel(f"{goles_local}  -  {goles_vis}")
        lbl_marcador.setAlignment(Qt.AlignCenter)
        lbl_marcador.setStyleSheet(
            """
            QLabel {
                font-size: 56pt;
                font-weight: bold;
                color: #27ae60;
                padding: 20px;
            }
        """
        )
        layout_marcador.addWidget(lbl_marcador)

        # Indicador resultado
        if goles_local > goles_vis:
            resultado_texto = f"Victoria {e_local.nombre}"
        elif goles_vis > goles_local:
            resultado_texto = f"Victoria {e_vis.nombre}"
        else:
            resultado_texto = "EMPATE"

        lbl_resultado = QLabel(resultado_texto)
        lbl_resultado.setAlignment(Qt.AlignCenter)
        lbl_resultado.setStyleSheet(
            """
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #7f8c8d;
            }
        """
        )
        layout_marcador.addWidget(lbl_resultado)

        layout.addWidget(panel_marcador)

        # Equipo Visitante
        panel_vis = QWidget()
        layout_vis = QVBoxLayout(panel_vis)
        layout_vis.setSpacing(10)
        layout_vis.setAlignment(Qt.AlignCenter)

        if e_vis and e_vis.escudo:
            escudo_vis = QLabel()
            escudo_vis.setMinimumSize(140, 140)
            ruta = obtener_ruta_recurso(f"Resources/img/escudos/{e_vis.escudo}")
            pixmap = QPixmap(ruta)
            if not pixmap.isNull():
                escudo_vis.setPixmap(
                    pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            escudo_vis.setAlignment(Qt.AlignCenter)
            layout_vis.addWidget(escudo_vis)

        lbl_nombre_vis = QLabel(e_vis.nombre if e_vis else "???")
        lbl_nombre_vis.setAlignment(Qt.AlignCenter)
        lbl_nombre_vis.setStyleSheet(
            """
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #2c3e50;
            }
        """
        )
        layout_vis.addWidget(lbl_nombre_vis)

        layout.addWidget(panel_vis, 1)

        return panel

    def _crear_panel_detalles(self, e_local, e_vis, inputs_jugadores, partido):
        """Crea el panel con goleadores y tarjetas."""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
            }
        """
        )

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # Columna Local
        col_local = self._crear_columna_detalles(
            "LOCAL", e_local, inputs_jugadores, "local"
        )
        layout.addWidget(col_local, 1)

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.VLine)
        separador.setStyleSheet("background-color: #bdc3c7;")
        separador.setFixedWidth(2)
        layout.addWidget(separador)

        # Columna Visitante
        col_vis = self._crear_columna_detalles(
            "VISITANTE", e_vis, inputs_jugadores, "visitante"
        )
        layout.addWidget(col_vis, 1)

        return panel

    def _crear_columna_detalles(self, titulo, equipo, inputs_jugadores, lado):
        """Crea una columna con goleadores y tarjetas de un equipo."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Título
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet(
            """
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #34495e;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 6px;
            }
        """
        )
        layout.addWidget(lbl_titulo)

        # Scroll con detalles
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        contenedor = QWidget()
        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setSpacing(8)

        # Buscar jugadores con goles o tarjetas
        jugadores = Equipo.obtener_jugadores(equipo.id)

        tiene_eventos = False
        for jugador in jugadores:
            key = (lado, jugador["id"])
            if key not in inputs_jugadores:
                continue

            controles = inputs_jugadores[key]
            texto_goles = controles["goles"].text().strip()
            goles = int(texto_goles) if texto_goles.isdigit() else 0
            tiene_amarilla = controles["amarilla"].isChecked()
            tiene_roja = controles["roja"].isChecked()

            if goles > 0 or tiene_amarilla or tiene_roja:
                tiene_eventos = True
                fila = self._crear_fila_detalle(
                    jugador["nombre"], goles, tiene_amarilla, tiene_roja
                )
                layout_contenedor.addWidget(fila)

        if not tiene_eventos:
            lbl_sin = QLabel("Sin eventos registrados")
            lbl_sin.setAlignment(Qt.AlignCenter)
            lbl_sin.setStyleSheet("color: #95a5a6; font-style: italic; padding: 20px;")
            layout_contenedor.addWidget(lbl_sin)

        layout_contenedor.addStretch()
        scroll.setWidget(contenedor)
        layout.addWidget(scroll, 1)

        return widget

    def _crear_fila_detalle(self, nombre, goles, amarilla, roja):
        """Crea una fila con los detalles de un jugador."""
        fila = QFrame()
        fila.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 8px;
            }
        """
        )

        layout = QHBoxLayout(fila)
        layout.setSpacing(10)

        # Nombre
        lbl_nombre = QLabel(nombre)
        lbl_nombre.setStyleSheet("font-size: 11pt; font-weight: bold; color: #2c3e50;")
        layout.addWidget(lbl_nombre, 1)

        # Goles
        if goles > 0:
            lbl_goles = QLabel(f"⚽ {goles}")
            lbl_goles.setStyleSheet(
                "font-size: 12pt; font-weight: bold; color: #27ae60;"
            )
            layout.addWidget(lbl_goles)

        # Tarjetas
        if amarilla:
            lbl_amarilla = QLabel("🟨")
            lbl_amarilla.setFixedSize(20, 20)
            lbl_amarilla.setStyleSheet("background-color: #f1c40f; border-radius: 3px;")
            layout.addWidget(lbl_amarilla)

        if roja:
            lbl_roja = QLabel("🟥")
            lbl_roja.setFixedSize(20, 20)
            lbl_roja.setStyleSheet("background-color: #e74c3c; border-radius: 3px;")
            layout.addWidget(lbl_roja)

        return fila
