"""Pantalla de Clasificación (bracket).

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

Bracket de eliminatorias real:
- Octavos de final (8 partidos)
- Cuartos de final (4 partidos)
- Semifinales (2 partidos)
- Final (1 partido) en el centro
- Líneas conectando las fases
- Resultados mostrados: ganador en verde, perdedor en rojo
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QRectF, QPointF, QSize
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QBrush, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtSvg import QSvgRenderer
import os

from Models.equipo import Equipo
from Models.partido import Partido
from Views.base_page import BasePage


class BracketWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tamaño fijo para que todo el bracket quepa sin márgenes
        self.setFixedSize(1050, 700)
        self._partidos = {
            "Octavos": [],
            "Cuartos": [],
            "Semifinales": [],
            "Final": None,
        }

    def set_data(self, partidos_dict):
        self._partidos = partidos_dict
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Dimensiones
        box_w = 126  # 30% más estrecho
        box_h = 70
        gap_y = 30
        col_spacing = 200

        # Función para dibujar un partido con resultados
        def draw_match(x, y, partido, fase=""):
            rect = QRectF(x, y, box_w, box_h)

            # Fondo de la caja
            painter.setPen(QPen(QColor(52, 152, 219), 2))
            painter.setBrush(QColor(255, 255, 255, 230))
            painter.drawRoundedRect(rect, 8, 8)

            if not partido:
                # Placeholder
                painter.setPen(QColor(150, 150, 150))
                font = QFont()
                font.setPointSize(9)
                painter.setFont(font)
                painter.drawText(rect, Qt.AlignCenter, "TBD")
                return rect

            # Obtener equipos y resultados
            e1 = Equipo.obtener_por_id(partido.equipo_local_id)
            e2 = Equipo.obtener_por_id(partido.equipo_visitante_id)

            nombre_local = e1.nombre if e1 else "—"
            nombre_vis = e2.nombre if e2 else "—"

            # Altura para cada equipo
            equipo_h = box_h / 2

            # Determinar ganador/perdedor si el partido está jugado
            ganador_local = False
            ganador_vis = False
            if partido.jugado:
                if partido.goles_local > partido.goles_visitante:
                    ganador_local = True
                elif partido.goles_visitante > partido.goles_local:
                    ganador_vis = True

            # Dibujar equipo local (mitad superior)
            rect_local = QRectF(x, y, box_w, equipo_h)
            if ganador_local:
                painter.setBrush(QColor(46, 204, 113, 180))  # Verde
            elif partido.jugado and ganador_vis:
                painter.setBrush(QColor(231, 76, 60, 180))  # Rojo
            else:
                painter.setBrush(QColor(255, 255, 255, 230))

            painter.setPen(QPen(QColor(52, 152, 219), 1))
            painter.drawRect(rect_local)

            # Escudo del equipo local
            escudo_max = 20
            escudo_x = x + 3
            escudo_y_base = y + equipo_h / 2

            if e1 and e1.escudo:
                ruta_escudo = os.path.join("Resources", "img", "escudos", e1.escudo)
                if os.path.exists(ruta_escudo):
                    if e1.escudo.endswith(".svg"):
                        renderer = QSvgRenderer(ruta_escudo)
                        svg_size = renderer.defaultSize()

                        # Calcular escala para que quepa en 20x20, limitando ambas dimensiones
                        scale_w = escudo_max / svg_size.width()
                        scale_h = escudo_max / svg_size.height()
                        scale = min(scale_w, scale_h)  # Usar la escala más restrictiva

                        # Calcular dimensiones finales
                        final_w = svg_size.width() * scale
                        final_h = svg_size.height() * scale

                        # Centrar en el espacio disponible
                        offset_x = (escudo_max - final_w) / 2
                        offset_y = -final_h / 2

                        renderer.render(
                            painter,
                            QRectF(
                                escudo_x + offset_x,
                                escudo_y_base + offset_y,
                                final_w,
                                final_h,
                            ),
                        )
                    else:
                        pixmap = QPixmap(ruta_escudo)
                        if not pixmap.isNull():
                            pixmap_scaled = pixmap.scaled(
                                escudo_max,
                                escudo_max,
                                Qt.KeepAspectRatio,
                                Qt.SmoothTransformation,
                            )
                            # Centrar el pixmap
                            offset_x = (escudo_max - pixmap_scaled.width()) / 2
                            offset_y = -pixmap_scaled.height() / 2
                            painter.drawPixmap(
                                int(escudo_x + offset_x),
                                int(escudo_y_base + offset_y),
                                pixmap_scaled,
                            )

            # Nombre del equipo local
            font = QFont()
            font.setPointSize(9)
            font.setBold(ganador_local)
            painter.setFont(font)
            painter.setPen(QColor(44, 62, 80))

            text_rect_local = rect_local.adjusted(26, 0, -35, 0)
            painter.drawText(
                text_rect_local, Qt.AlignVCenter | Qt.AlignLeft, nombre_local
            )

            # Goles del equipo local
            if partido.jugado:
                goles_rect_local = QRectF(x + box_w - 32, y + 2, 28, equipo_h - 4)
                painter.setBrush(QColor(52, 152, 219, 200))
                painter.drawRoundedRect(goles_rect_local, 4, 4)

                font.setPointSize(14)
                font.setBold(True)
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(
                    goles_rect_local, Qt.AlignCenter, str(partido.goles_local)
                )

            # Dibujar equipo visitante (mitad inferior)
            rect_vis = QRectF(x, y + equipo_h, box_w, equipo_h)
            if ganador_vis:
                painter.setBrush(QColor(46, 204, 113, 180))  # Verde
            elif partido.jugado and ganador_local:
                painter.setBrush(QColor(231, 76, 60, 180))  # Rojo
            else:
                painter.setBrush(QColor(255, 255, 255, 230))

            painter.setPen(QPen(QColor(52, 152, 219), 1))
            painter.drawRect(rect_vis)

            # Escudo del equipo visitante
            escudo_max = 20
            escudo_x = x + 3
            escudo_y_base = y + equipo_h + equipo_h / 2

            if e2 and e2.escudo:
                ruta_escudo = os.path.join("Resources", "img", "escudos", e2.escudo)
                if os.path.exists(ruta_escudo):
                    if e2.escudo.endswith(".svg"):
                        renderer = QSvgRenderer(ruta_escudo)
                        svg_size = renderer.defaultSize()

                        # Calcular escala para que quepa en 20x20, limitando ambas dimensiones
                        scale_w = escudo_max / svg_size.width()
                        scale_h = escudo_max / svg_size.height()
                        scale = min(scale_w, scale_h)  # Usar la escala más restrictiva

                        # Calcular dimensiones finales
                        final_w = svg_size.width() * scale
                        final_h = svg_size.height() * scale

                        # Centrar en el espacio disponible
                        offset_x = (escudo_max - final_w) / 2
                        offset_y = -final_h / 2

                        renderer.render(
                            painter,
                            QRectF(
                                escudo_x + offset_x,
                                escudo_y_base + offset_y,
                                final_w,
                                final_h,
                            ),
                        )
                    else:
                        pixmap = QPixmap(ruta_escudo)
                        if not pixmap.isNull():
                            pixmap_scaled = pixmap.scaled(
                                escudo_max,
                                escudo_max,
                                Qt.KeepAspectRatio,
                                Qt.SmoothTransformation,
                            )
                            # Centrar el pixmap
                            offset_x = (escudo_max - pixmap_scaled.width()) / 2
                            offset_y = -pixmap_scaled.height() / 2
                            painter.drawPixmap(
                                int(escudo_x + offset_x),
                                int(escudo_y_base + offset_y),
                                pixmap_scaled,
                            )

            # Nombre del equipo visitante
            font.setPointSize(9)
            font.setBold(ganador_vis)
            painter.setFont(font)
            painter.setPen(QColor(44, 62, 80))

            text_rect_vis = rect_vis.adjusted(26, 0, -35, 0)
            painter.drawText(text_rect_vis, Qt.AlignVCenter | Qt.AlignLeft, nombre_vis)

            # Goles del equipo visitante
            if partido.jugado:
                goles_rect_vis = QRectF(
                    x + box_w - 32, y + equipo_h + 2, 28, equipo_h - 4
                )
                painter.setBrush(QColor(52, 152, 219, 200))
                painter.drawRoundedRect(goles_rect_vis, 4, 4)

                font.setPointSize(14)
                font.setBold(True)
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(
                    goles_rect_vis, Qt.AlignCenter, str(partido.goles_visitante)
                )

            return rect

        # Calcular posiciones
        octavos = self._partidos.get("Octavos", [])
        cuartos = self._partidos.get("Cuartos", [])
        semis = self._partidos.get("Semifinales", [])
        final = self._partidos.get("Final", None)

        # Usar ancho fijo del widget
        w = 1050
        h = 700

        # Posiciones X para cada columna (bracket simétrico)
        col_spacing = 150  # Espaciado entre octavos-cuartos y cuartos-semifinales
        col_spacing_final = 10  # Separación mínima entre semifinales-final

        # Calcular desde el centro hacia afuera (final primero, luego semifinales simétricas)
        x_final = w // 2 - box_w // 2
        x_semis_izq = (
            x_final - box_w - col_spacing_final
        )  # Pegada a la izquierda de la final
        x_semis_der = (
            x_final + box_w + col_spacing_final
        )  # Pegada a la derecha de la final

        # Calcular el resto hacia los lados
        x_cuartos_izq = x_semis_izq - col_spacing
        x_octavos_izq = x_cuartos_izq - col_spacing
        x_cuartos_der = x_semis_der + col_spacing
        x_octavos_der = x_cuartos_der + col_spacing

        # OCTAVOS DE FINAL IZQUIERDA (4 partidos)
        y_start = 50
        rects_octavos_izq = []
        for i in range(4):
            p = octavos[i] if i < len(octavos) else None
            y = y_start + i * (box_h + gap_y)
            rect = draw_match(x_octavos_izq, y, p, "Octavos")
            rects_octavos_izq.append(rect)

        # OCTAVOS DE FINAL DERECHA (4 partidos)
        rects_octavos_der = []
        for i in range(4):
            p = octavos[i + 4] if (i + 4) < len(octavos) else None
            y = y_start + i * (box_h + gap_y)
            rect = draw_match(x_octavos_der, y, p, "Octavos")
            rects_octavos_der.append(rect)

        # CUARTOS DE FINAL IZQUIERDA (2 partidos)
        rects_cuartos_izq = []

        # Cuarto 1 izq (conecta octavos 0-1)
        y_cuarto_1_izq = (
            rects_octavos_izq[0].center().y()
            + (rects_octavos_izq[1].center().y() - rects_octavos_izq[0].center().y())
            / 2
            - box_h / 2
        )
        p_cuarto_1_izq = cuartos[0] if len(cuartos) > 0 else None
        rect_cuarto_1_izq = draw_match(
            x_cuartos_izq, y_cuarto_1_izq, p_cuarto_1_izq, "Cuartos"
        )
        rects_cuartos_izq.append(rect_cuarto_1_izq)

        # Cuarto 2 izq (conecta octavos 2-3)
        y_cuarto_2_izq = (
            rects_octavos_izq[2].center().y()
            + (rects_octavos_izq[3].center().y() - rects_octavos_izq[2].center().y())
            / 2
            - box_h / 2
        )
        p_cuarto_2_izq = cuartos[1] if len(cuartos) > 1 else None
        rect_cuarto_2_izq = draw_match(
            x_cuartos_izq, y_cuarto_2_izq, p_cuarto_2_izq, "Cuartos"
        )
        rects_cuartos_izq.append(rect_cuarto_2_izq)

        # CUARTOS DE FINAL DERECHA (2 partidos)
        rects_cuartos_der = []

        # Cuarto 1 der (conecta octavos 4-5)
        y_cuarto_1_der = (
            rects_octavos_der[0].center().y()
            + (rects_octavos_der[1].center().y() - rects_octavos_der[0].center().y())
            / 2
            - box_h / 2
        )
        p_cuarto_1_der = cuartos[2] if len(cuartos) > 2 else None
        rect_cuarto_1_der = draw_match(
            x_cuartos_der, y_cuarto_1_der, p_cuarto_1_der, "Cuartos"
        )
        rects_cuartos_der.append(rect_cuarto_1_der)

        # Cuarto 2 der (conecta octavos 6-7)
        y_cuarto_2_der = (
            rects_octavos_der[2].center().y()
            + (rects_octavos_der[3].center().y() - rects_octavos_der[2].center().y())
            / 2
            - box_h / 2
        )
        p_cuarto_2_der = cuartos[3] if len(cuartos) > 3 else None
        rect_cuarto_2_der = draw_match(
            x_cuartos_der, y_cuarto_2_der, p_cuarto_2_der, "Cuartos"
        )
        rects_cuartos_der.append(rect_cuarto_2_der)

        # SEMIFINAL IZQUIERDA (conecta cuartos izq 0-1)
        y_semi_izq = (
            rect_cuarto_1_izq.center().y()
            + (rect_cuarto_2_izq.center().y() - rect_cuarto_1_izq.center().y()) / 2
            - box_h / 2
        )
        p_semi_izq = semis[0] if len(semis) > 0 else None
        rect_semi_izq = draw_match(x_semis_izq, y_semi_izq, p_semi_izq, "Semifinal")

        # SEMIFINAL DERECHA (conecta cuartos der 0-1)
        y_semi_der = (
            rect_cuarto_1_der.center().y()
            + (rect_cuarto_2_der.center().y() - rect_cuarto_1_der.center().y()) / 2
            - box_h / 2
        )
        p_semi_der = semis[1] if len(semis) > 1 else None
        rect_semi_der = draw_match(x_semis_der, y_semi_der, p_semi_der, "Semifinal")

        # FINAL (centro, conecta ambas semifinales)
        y_final = (
            rect_semi_izq.center().y()
            + (rect_semi_der.center().y() - rect_semi_izq.center().y()) / 2
            - box_h / 2
        )
        rect_final = draw_match(x_final, y_final, final, "FINAL")

        # ====== LÍNEAS DE CONEXIÓN ======
        painter.setPen(QPen(QColor(52, 152, 219, 200), 2))

        # ===== LADO IZQUIERDO =====
        # Octavos izq -> Cuartos izq
        mid_x_oct_cuart_izq = (
            rects_octavos_izq[0].right() + rect_cuarto_1_izq.left()
        ) / 2

        # Octavos 0-1 -> Cuarto 1 izq
        for i in range(2):
            rect_oct = rects_octavos_izq[i]
            painter.drawLine(
                QPointF(rect_oct.right(), rect_oct.center().y()),
                QPointF(mid_x_oct_cuart_izq, rect_oct.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_izq, rects_octavos_izq[0].center().y()),
            QPointF(mid_x_oct_cuart_izq, rects_octavos_izq[1].center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_izq, rect_cuarto_1_izq.center().y()),
            QPointF(rect_cuarto_1_izq.left(), rect_cuarto_1_izq.center().y()),
        )

        # Octavos 2-3 -> Cuarto 2 izq
        for i in range(2, 4):
            rect_oct = rects_octavos_izq[i]
            painter.drawLine(
                QPointF(rect_oct.right(), rect_oct.center().y()),
                QPointF(mid_x_oct_cuart_izq, rect_oct.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_izq, rects_octavos_izq[2].center().y()),
            QPointF(mid_x_oct_cuart_izq, rects_octavos_izq[3].center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_izq, rect_cuarto_2_izq.center().y()),
            QPointF(rect_cuarto_2_izq.left(), rect_cuarto_2_izq.center().y()),
        )

        # Cuartos izq -> Semi izq
        mid_x_cuart_semi_izq = (rect_cuarto_1_izq.right() + rect_semi_izq.left()) / 2

        for rect_cuart in rects_cuartos_izq:
            painter.drawLine(
                QPointF(rect_cuart.right(), rect_cuart.center().y()),
                QPointF(mid_x_cuart_semi_izq, rect_cuart.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_cuart_semi_izq, rect_cuarto_1_izq.center().y()),
            QPointF(mid_x_cuart_semi_izq, rect_cuarto_2_izq.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_cuart_semi_izq, rect_semi_izq.center().y()),
            QPointF(rect_semi_izq.left(), rect_semi_izq.center().y()),
        )

        # Semi izq -> Final
        mid_x_semi_final_izq = (rect_semi_izq.right() + rect_final.left()) / 2
        painter.drawLine(
            QPointF(rect_semi_izq.right(), rect_semi_izq.center().y()),
            QPointF(mid_x_semi_final_izq, rect_semi_izq.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_semi_final_izq, rect_semi_izq.center().y()),
            QPointF(mid_x_semi_final_izq, rect_final.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_semi_final_izq, rect_final.center().y()),
            QPointF(rect_final.left(), rect_final.center().y()),
        )

        # ===== LADO DERECHO =====
        # Octavos der -> Cuartos der
        mid_x_oct_cuart_der = (
            rects_octavos_der[0].left() + rect_cuarto_1_der.right()
        ) / 2

        # Octavos 4-5 -> Cuarto 1 der
        for i in range(2):
            rect_oct = rects_octavos_der[i]
            painter.drawLine(
                QPointF(rect_oct.left(), rect_oct.center().y()),
                QPointF(mid_x_oct_cuart_der, rect_oct.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_der, rects_octavos_der[0].center().y()),
            QPointF(mid_x_oct_cuart_der, rects_octavos_der[1].center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_der, rect_cuarto_1_der.center().y()),
            QPointF(rect_cuarto_1_der.right(), rect_cuarto_1_der.center().y()),
        )

        # Octavos 6-7 -> Cuarto 2 der
        for i in range(2, 4):
            rect_oct = rects_octavos_der[i]
            painter.drawLine(
                QPointF(rect_oct.left(), rect_oct.center().y()),
                QPointF(mid_x_oct_cuart_der, rect_oct.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_der, rects_octavos_der[2].center().y()),
            QPointF(mid_x_oct_cuart_der, rects_octavos_der[3].center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_oct_cuart_der, rect_cuarto_2_der.center().y()),
            QPointF(rect_cuarto_2_der.right(), rect_cuarto_2_der.center().y()),
        )

        # Cuartos der -> Semi der
        mid_x_cuart_semi_der = (rect_cuarto_1_der.left() + rect_semi_der.right()) / 2

        for rect_cuart in rects_cuartos_der:
            painter.drawLine(
                QPointF(rect_cuart.left(), rect_cuart.center().y()),
                QPointF(mid_x_cuart_semi_der, rect_cuart.center().y()),
            )
        painter.drawLine(
            QPointF(mid_x_cuart_semi_der, rect_cuarto_1_der.center().y()),
            QPointF(mid_x_cuart_semi_der, rect_cuarto_2_der.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_cuart_semi_der, rect_semi_der.center().y()),
            QPointF(rect_semi_der.right(), rect_semi_der.center().y()),
        )

        # Semi der -> Final
        mid_x_semi_final_der = (rect_semi_der.left() + rect_final.right()) / 2
        painter.drawLine(
            QPointF(rect_semi_der.left(), rect_semi_der.center().y()),
            QPointF(mid_x_semi_final_der, rect_semi_der.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_semi_final_der, rect_semi_der.center().y()),
            QPointF(mid_x_semi_final_der, rect_final.center().y()),
        )
        painter.drawLine(
            QPointF(mid_x_semi_final_der, rect_final.center().y()),
            QPointF(rect_final.right(), rect_final.center().y()),
        )

        # Etiquetas de fase
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(52, 152, 219))

        painter.drawText(QRectF(x_octavos_izq, 5, box_w, 20), Qt.AlignCenter, "OCTAVOS")
        painter.drawText(QRectF(x_cuartos_izq, 5, box_w, 20), Qt.AlignCenter, "CUARTOS")
        painter.drawText(
            QRectF(x_semis_izq, 5, box_w, 20), Qt.AlignCenter, "SEMIFINALES"
        )
        painter.drawText(
            QRectF(x_final - 20, 5, box_w + 40, 20),
            Qt.AlignCenter,
            "★ FINAL ★",
        )
        painter.drawText(
            QRectF(x_semis_der, 5, box_w, 20), Qt.AlignCenter, "SEMIFINALES"
        )
        painter.drawText(QRectF(x_cuartos_der, 5, box_w, 20), Qt.AlignCenter, "CUARTOS")
        painter.drawText(QRectF(x_octavos_der, 5, box_w, 20), Qt.AlignCenter, "OCTAVOS")


class ClasificacionPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Clasificación", parent)

        cont = QFrame()
        cont.setObjectName("contenedor_translucido")
        cont.setStyleSheet(
            """
            QFrame#contenedor_translucido {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 12px;
                padding: 5px;
            }
        """
        )
        lay = QVBoxLayout(cont)
        lay.setContentsMargins(5, 10, 5, 10)
        lay.setSpacing(10)

        # Botón de exportación CSV
        self.btn_exportar = QPushButton("📊 Exportar Clasificación a CSV")
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
        self.btn_exportar.setMinimumHeight(40)
        self.btn_exportar.clicked.connect(self._exportar_csv)
        lay.addWidget(self.btn_exportar)

        # Bracket sin scroll (ya cabe todo en la ventana)
        self.bracket = BracketWidget()
        lay.addWidget(self.bracket, 1)

        self.contenido_layout.addWidget(cont, 1)
        self._refrescar()

    def _exportar_csv(self):
        """Exporta la clasificación a un archivo CSV."""
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Clasificación como CSV",
            "clasificacion.csv",
            "Archivos CSV (*.csv)",
        )

        if ruta_archivo:
            if Partido.exportar_clasificacion_csv(ruta_archivo):
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Exportación exitosa")
                msg.setText(
                    f"La clasificación se ha exportado correctamente a:\n{ruta_archivo}"
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
                msg.setText("No se pudo exportar la clasificación. Intente nuevamente.")
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

    def on_show(self):
        self._refrescar()

    def _refrescar(self):
        # Obtener todos los partidos y organizarlos por eliminatoria
        partidos = Partido.obtener_todos()

        partidos_dict = {"Octavos": [], "Cuartos": [], "Semifinales": [], "Final": None}

        for p in partidos:
            if p.eliminatoria == "Octavos":
                partidos_dict["Octavos"].append(p)
            elif p.eliminatoria == "Cuartos":
                partidos_dict["Cuartos"].append(p)
            elif p.eliminatoria == "Semifinales":
                partidos_dict["Semifinales"].append(p)
            elif p.eliminatoria == "Final":
                partidos_dict["Final"] = p

        # Asegurar que hay suficientes espacios (rellenar con None si es necesario)
        while len(partidos_dict["Octavos"]) < 8:
            partidos_dict["Octavos"].append(None)
        while len(partidos_dict["Cuartos"]) < 4:
            partidos_dict["Cuartos"].append(None)
        while len(partidos_dict["Semifinales"]) < 2:
            partidos_dict["Semifinales"].append(None)

        self.bracket.set_data(partidos_dict)
