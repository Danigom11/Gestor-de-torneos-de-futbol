"""Pantalla de Participantes - Versión reorganizada.

Diseño hecho en ui con QTDesigner en resources/ui y mejorado con Python
para hacerlo más escalable, mantenible y mejorable. Menos estático.

Layout:
- Izquierda: Formulario completo de registro (campos básicos + condicionales según tipo)
- Derecha: Lista de todos los participantes con filtro y opciones de editar/eliminar
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from Models.participante import Participante
from Models.equipo import Equipo
from Models.partido import Partido
from Models.jugador_equipo import JugadorEquipo
from Views.base_page import BasePage


class _ParticipanteListItem(QWidget):
    """Widget personalizado para mostrar un participante en la lista con botones de editar y eliminar."""

    def __init__(self, participante: Participante, on_delete, on_edit, parent=None):
        super().__init__(parent)
        self.participante = participante

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Información del participante
        info = QVBoxLayout()
        info.setSpacing(2)

        # Nombre y tipo
        tipo_text = []
        if participante.es_jugador:
            tipo_text.append("⚽ Jugador")
        if participante.es_arbitro:
            tipo_text.append("🔴 Árbitro")
        tipo_str = " + ".join(tipo_text)

        nombre = QLabel(f"{participante.nombre} ({tipo_str})")
        nombre.setStyleSheet("font-weight: 800; color: #2c3e50; font-size: 11pt;")
        nombre.setWordWrap(False)

        # Detalles adicionales
        detalles = []
        if participante.curso:
            detalles.append(f"Curso: {participante.curso}")
        if participante.es_jugador and participante.posicion:
            detalles.append(f"Pos: {participante.posicion}")
            detalles.append(f"⚽ {participante.goles}")
            if participante.t_amarillas > 0 or participante.t_rojas > 0:
                detalles.append(
                    f"🟨 {participante.t_amarillas} 🟥 {participante.t_rojas}"
                )

        detalle_label = QLabel("   ".join(detalles))
        detalle_label.setStyleSheet("color: #34495e; font-size: 9pt;")
        detalle_label.setWordWrap(False)

        info.addWidget(nombre)
        info.addWidget(detalle_label)

        # Asignaciones (equipo/partido)
        asignaciones = []

        # Si es jugador, mostrar equipo asignado
        if participante.es_jugador:
            equipo_id = JugadorEquipo.obtener_equipo_de_jugador(participante.id)
            if equipo_id:
                equipo = Equipo.obtener_por_id(equipo_id)
                if equipo:
                    asignaciones.append(f"🏆 Equipo: {equipo.nombre}")
            else:
                asignaciones.append("🏆 Sin equipo")

        # Si es árbitro, buscar partido asignado
        if participante.es_arbitro:
            partidos = Partido.obtener_todos()
            partido_asignado = None
            for partido in partidos:
                if partido.arbitro_id == participante.id:
                    partido_asignado = partido
                    break

            if partido_asignado:
                equipo_local = Equipo.obtener_por_id(partido_asignado.equipo_local_id)
                equipo_visitante = Equipo.obtener_por_id(
                    partido_asignado.equipo_visitante_id
                )
                if equipo_local and equipo_visitante:
                    asignaciones.append(
                        f"⚖️ Partido: {equipo_local.nombre} vs {equipo_visitante.nombre}"
                    )
            else:
                asignaciones.append("⚖️ Sin partido")

        if asignaciones:
            asignacion_label = QLabel("   ".join(asignaciones))
            asignacion_label.setStyleSheet(
                "color: #7f8c8d; font-size: 9pt; font-style: italic;"
            )
            asignacion_label.setWordWrap(False)
            info.addWidget(asignacion_label)

        layout.addLayout(info, 1)

        # Botón de editar
        btn_edit = QPushButton("✎")
        btn_edit.setFixedSize(32, 32)
        btn_edit.setToolTip("Editar participante")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setStyleSheet(
            """
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white; 
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                font-family: 'Segoe UI', 'Arial';
                font-weight: normal; 
                font-size: 16pt;
                padding: 0px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: #21618c;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            """
        )
        btn_edit.clicked.connect(lambda: on_edit(participante))
        layout.addWidget(btn_edit, 0, Qt.AlignVCenter)

        # Botón de eliminar
        btn_del = QPushButton("×")
        btn_del.setFixedSize(32, 32)
        btn_del.setToolTip("Eliminar participante")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.setStyleSheet(
            """
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #ee5a6f);
                color: white; 
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                font-family: 'Segoe UI', 'Arial';
                font-weight: normal; 
                font-size: 20pt;
                padding: 0px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff5252, stop:1 #e53935);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: #c62828;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            """
        )
        btn_del.clicked.connect(lambda: on_delete(participante))
        layout.addWidget(btn_del, 0, Qt.AlignVCenter)

        # Estilo de fondo según tipo
        if participante.es_jugador and participante.es_arbitro:
            bg_color = "rgba(155, 89, 182, 0.15)"
            border_color = "rgba(155, 89, 182, 0.3)"
        elif participante.es_arbitro:
            bg_color = "rgba(231, 76, 60, 0.15)"
            border_color = "rgba(231, 76, 60, 0.3)"
        else:
            bg_color = "rgba(52, 152, 219, 0.15)"
            border_color = "rgba(52, 152, 219, 0.3)"

        self.setStyleSheet(
            f"""
            background-color: {bg_color};
            border-radius: 14px;
            border: 1px solid {border_color};
            """
        )


class ParticipantesPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Participantes", parent)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")
        self.contenido_layout.addWidget(splitter, 1)

        # ===================
        # PANEL IZQUIERDO: FORMULARIO DE REGISTRO
        # ===================
        self.panel_izq = QFrame()
        self.panel_izq.setObjectName("panel_izquierdo")
        self.panel_izq.setStyleSheet(
            """
            QFrame#panel_izquierdo {
                background-color: rgba(255, 255, 255, 210);
                border-radius: 12px;
                padding: 0px;
                margin: 5px;
            }
            QFrame#panel_izquierdo QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
        """
        )
        splitter.addWidget(self.panel_izq)

        # Layout principal del panel izquierdo
        panel_izq_layout = QVBoxLayout(self.panel_izq)
        panel_izq_layout.setContentsMargins(0, 0, 0, 0)
        panel_izq_layout.setSpacing(0)

        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: rgba(189, 195, 199, 0.3);
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(52, 152, 219, 0.6);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(52, 152, 219, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )
        panel_izq_layout.addWidget(scroll)

        # Widget contenedor del formulario
        form_widget = QWidget()
        scroll.setWidget(form_widget)

        izq = QVBoxLayout(form_widget)
        izq.setContentsMargins(15, 15, 15, 15)
        izq.setSpacing(10)

        # Título
        titulo = QLabel("Registro de Participante")
        titulo.setStyleSheet("font-size: 14pt; font-weight: 800; color: #2c3e50;")
        izq.addWidget(titulo)

        self._participante_actual: Participante | None = None

        # Campos básicos
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre completo")

        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDisplayFormat("yyyy-MM-dd")

        self.combo_curso = QComboBox()
        self.combo_curso.setEditable(True)
        self.combo_curso.addItems(
            ["1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bach", "2º Bach"]
        )
        self._aplicar_estilo_combo(self.combo_curso)

        izq.addWidget(QLabel("Nombre"))
        izq.addWidget(self.txt_nombre)
        izq.addWidget(QLabel("Fecha de nacimiento"))
        izq.addWidget(self.fecha)
        izq.addWidget(QLabel("Curso"))
        izq.addWidget(self.combo_curso)

        # Tipo de participante
        izq.addWidget(QLabel("Tipo de participante"))

        self.grp_tipo = QButtonGroup(self)
        self.rb_jugador = QRadioButton("Jugador")
        self.rb_arbitro = QRadioButton("Árbitro")
        self.rb_ambos = QRadioButton("Ambos")
        self.rb_jugador.setChecked(True)

        for rb in (self.rb_jugador, self.rb_arbitro, self.rb_ambos):
            self.grp_tipo.addButton(rb)
            rb.setStyleSheet(
                """
                QRadioButton { color: #2c3e50; font-weight: 700; }
                QRadioButton::indicator { width: 16px; height: 16px; border-radius: 8px; }
                QRadioButton::indicator:unchecked { border: 2px solid rgba(44,62,80,160); background: rgba(255,255,255,140); }
                QRadioButton::indicator:checked { border: 2px solid rgba(44,62,80,220); background: rgba(52,152,219,220); }
                """
            )
            rb.toggled.connect(self._sync_campos_visibles)

        fila_tipo = QHBoxLayout()
        fila_tipo.addWidget(self.rb_jugador)
        fila_tipo.addWidget(self.rb_arbitro)
        fila_tipo.addWidget(self.rb_ambos)
        izq.addLayout(fila_tipo)

        # ===== CAMPOS CONDICIONALES PARA JUGADOR =====
        self.widget_jugador = QWidget()
        layout_jugador = QVBoxLayout(self.widget_jugador)
        layout_jugador.setContentsMargins(0, 10, 0, 0)
        layout_jugador.setSpacing(10)

        # Separador visual
        separador_jugador = QLabel("— Datos de Jugador —")
        separador_jugador.setStyleSheet(
            "color: #3498db; font-weight: 800; font-size: 10pt; margin-top: 5px;"
        )
        separador_jugador.setAlignment(Qt.AlignCenter)
        layout_jugador.addWidget(separador_jugador)

        # Posición
        layout_jugador.addWidget(QLabel("Posición"))
        self.combo_posicion = QComboBox()
        self.combo_posicion.addItems(Participante.POSICIONES)
        self._aplicar_estilo_combo(self.combo_posicion)
        layout_jugador.addWidget(self.combo_posicion)

        # Tarjetas Amarillas
        layout_jugador.addWidget(QLabel("Tarjetas Amarillas"))
        self.spin_amarillas = QSpinBox()
        self.spin_amarillas.setMinimum(0)
        self.spin_amarillas.setMaximum(99)
        self.spin_amarillas.setValue(0)
        self._aplicar_estilo_spin(self.spin_amarillas)
        layout_jugador.addWidget(self.spin_amarillas)

        # Tarjetas Rojas
        layout_jugador.addWidget(QLabel("Tarjetas Rojas"))
        self.spin_rojas = QSpinBox()
        self.spin_rojas.setMinimum(0)
        self.spin_rojas.setMaximum(99)
        self.spin_rojas.setValue(0)
        self._aplicar_estilo_spin(self.spin_rojas)
        layout_jugador.addWidget(self.spin_rojas)

        # Goles
        layout_jugador.addWidget(QLabel("Goles"))
        self.spin_goles = QSpinBox()
        self.spin_goles.setMinimum(0)
        self.spin_goles.setMaximum(999)
        self.spin_goles.setValue(0)
        self._aplicar_estilo_spin(self.spin_goles)
        layout_jugador.addWidget(self.spin_goles)

        # Asignar a Equipo
        layout_jugador.addWidget(QLabel("Asignar a Equipo (opcional)"))
        self.combo_equipo = QComboBox()
        self._aplicar_estilo_combo(self.combo_equipo)
        layout_jugador.addWidget(self.combo_equipo)

        izq.addWidget(self.widget_jugador)

        # ===== CAMPOS CONDICIONALES PARA ÁRBITRO =====
        self.widget_arbitro = QWidget()
        layout_arbitro = QVBoxLayout(self.widget_arbitro)
        layout_arbitro.setContentsMargins(0, 10, 0, 0)
        layout_arbitro.setSpacing(10)

        # Separador visual
        separador_arbitro = QLabel("— Datos de Árbitro —")
        separador_arbitro.setStyleSheet(
            "color: #e74c3c; font-weight: 800; font-size: 10pt; margin-top: 5px;"
        )
        separador_arbitro.setAlignment(Qt.AlignCenter)
        layout_arbitro.addWidget(separador_arbitro)

        # Info
        lbl_arbitro_info = QLabel("Este participante será registrado como árbitro.")
        lbl_arbitro_info.setStyleSheet(
            "color: #2c3e50; font-size: 10pt; font-style: italic;"
        )
        lbl_arbitro_info.setWordWrap(True)
        layout_arbitro.addWidget(lbl_arbitro_info)

        # Asignar a Partido
        layout_arbitro.addWidget(QLabel("Asignar a Partido (opcional)"))
        self.combo_partido = QComboBox()
        self._aplicar_estilo_combo(self.combo_partido)
        layout_arbitro.addWidget(self.combo_partido)

        izq.addWidget(self.widget_arbitro)

        # Espaciador
        izq.addStretch(1)

        # Botones de acción
        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(10)

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setFixedHeight(40)
        self.btn_limpiar.setMinimumWidth(120)
        self.btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_limpiar.setStyleSheet(
            """
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QPushButton:pressed {
                background-color: #bdc3c7;
            }
            """
        )
        self.btn_limpiar.clicked.connect(self._limpiar_campos)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setFixedHeight(40)
        self.btn_guardar.setMinimumWidth(120)
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 700;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: #21618c;
            }
            """
        )
        self.btn_guardar.clicked.connect(self._guardar)

        fila_botones.addWidget(self.btn_limpiar)
        fila_botones.addStretch(1)
        fila_botones.addWidget(self.btn_guardar)

        izq.addLayout(fila_botones)

        # ===================
        # PANEL DERECHO: LISTA DE PARTICIPANTES
        # ===================
        self.panel_der = QFrame()
        self.panel_der.setObjectName("panel_derecho")
        self.panel_der.setStyleSheet(
            """
            QFrame#panel_derecho {
                background-color: rgba(255, 255, 255, 210);
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }
            QFrame#panel_derecho QLabel {
                color: #2c3e50;
                font-weight: 600;
            }
        """
        )
        splitter.addWidget(self.panel_der)

        der = QVBoxLayout(self.panel_der)
        der.setContentsMargins(15, 15, 15, 15)
        der.setSpacing(10)

        # Título
        titulo_der = QLabel("Lista de Participantes")
        titulo_der.setStyleSheet("font-size: 14pt; font-weight: 800; color: #2c3e50;")
        der.addWidget(titulo_der)

        # Filtro
        self.txt_filtro = QLineEdit()
        self.txt_filtro.setPlaceholderText("🔍 Buscar por nombre o curso...")
        self.txt_filtro.textChanged.connect(self._filtrar_participantes)
        der.addWidget(self.txt_filtro)

        # Lista
        self.lista_participantes = QListWidget()
        self.lista_participantes.setSpacing(5)
        self.lista_participantes.setStyleSheet(
            """
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: transparent;
                border: none;
            }
            """
        )
        der.addWidget(self.lista_participantes, 1)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        # Inicializar visibilidad de campos condicionales
        self._sync_campos_visibles()

        # Cargar datos iniciales
        self._cargar_equipos_y_partidos()
        self._refrescar_lista_participantes()

    def _aplicar_estilo_combo(self, combo: QComboBox):
        """Aplica el estilo consistente a un QComboBox."""
        combo.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px 8px;
                padding-right: 30px;
                font-size: 10pt;
                min-height: 24px;
            }
            QComboBox:hover {
                border-color: #95a5a6;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #2c3e50;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )

    def _aplicar_estilo_spin(self, spin: QSpinBox):
        """Aplica el estilo consistente a un QSpinBox."""
        spin.setStyleSheet(
            """
            QSpinBox {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 10pt;
                min-height: 24px;
            }
            QSpinBox:hover {
                border-color: #95a5a6;
            }
            QSpinBox:focus {
                border-color: #3498db;
            }
            """
        )

    def on_show(self):
        """Llamado cuando se muestra la página."""
        self._refrescar_lista_participantes()
        self._cargar_equipos_y_partidos()

    def _tipo(self):
        """Retorna el tipo de participante seleccionado como tupla (es_jugador, es_arbitro)."""
        if self.rb_ambos.isChecked():
            return True, True
        if self.rb_arbitro.isChecked():
            return False, True
        return True, False

    def _sync_campos_visibles(self):
        """Muestra u oculta los widgets condicionales según el tipo seleccionado."""
        es_jugador, es_arbitro = self._tipo()

        self.widget_jugador.setVisible(es_jugador)
        self.widget_arbitro.setVisible(es_arbitro and not es_jugador)

    def _cargar_equipos_y_partidos(self):
        """Carga los equipos y partidos disponibles en los combos."""
        # Cargar equipos
        self.combo_equipo.clear()
        self.combo_equipo.addItem("-- Sin asignar --", None)
        equipos = Equipo.obtener_todos()
        for equipo in equipos:
            self.combo_equipo.addItem(equipo.nombre, equipo.id)

        # Cargar partidos
        self.combo_partido.clear()
        self.combo_partido.addItem("-- Sin asignar --", None)
        partidos = Partido.obtener_todos()
        for partido in partidos:
            equipo_local = Equipo.obtener_por_id(partido.equipo_local_id)
            equipo_visitante = Equipo.obtener_por_id(partido.equipo_visitante_id)
            if equipo_local and equipo_visitante:
                texto = f"{equipo_local.nombre} vs {equipo_visitante.nombre} - {partido.fecha_hora[:10]}"
                self.combo_partido.addItem(texto, partido.id)

    def _refrescar_lista_participantes(self):
        """Refresca la lista de participantes aplicando el filtro actual."""
        self.lista_participantes.clear()

        filtro = self.txt_filtro.text().strip().lower()
        participantes = Participante.obtener_todos()

        for participante in participantes:
            # Aplicar filtro
            if filtro:
                if (
                    filtro not in participante.nombre.lower()
                    and filtro not in participante.curso.lower()
                ):
                    continue

            # Crear widget personalizado
            item_widget = _ParticipanteListItem(
                participante,
                on_delete=self._eliminar_participante,
                on_edit=self._editar_participante,
            )

            # Agregar a la lista
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.lista_participantes.addItem(item)
            self.lista_participantes.setItemWidget(item, item_widget)

    def _filtrar_participantes(self):
        """Filtra la lista de participantes según el texto ingresado."""
        self._refrescar_lista_participantes()

    def _editar_participante(self, participante: Participante):
        """Carga los datos del participante en el formulario para edición."""
        self._participante_actual = participante

        # Cargar datos básicos
        self.txt_nombre.setText(participante.nombre)

        # Fecha
        from PySide6.QtCore import QDate

        partes = participante.fecha_nacimiento.split("-")
        if len(partes) == 3:
            self.fecha.setDate(QDate(int(partes[0]), int(partes[1]), int(partes[2])))

        # Curso
        idx = self.combo_curso.findText(participante.curso)
        if idx >= 0:
            self.combo_curso.setCurrentIndex(idx)
        else:
            self.combo_curso.setEditText(participante.curso)

        # Tipo
        if participante.es_jugador and participante.es_arbitro:
            self.rb_ambos.setChecked(True)
        elif participante.es_arbitro:
            self.rb_arbitro.setChecked(True)
        else:
            self.rb_jugador.setChecked(True)

        # Datos de jugador
        if participante.es_jugador:
            idx = self.combo_posicion.findText(participante.posicion)
            if idx >= 0:
                self.combo_posicion.setCurrentIndex(idx)
            self.spin_amarillas.setValue(participante.t_amarillas)
            self.spin_rojas.setValue(participante.t_rojas)
            self.spin_goles.setValue(participante.goles)

            # Equipo actual
            equipo_id = JugadorEquipo.obtener_equipo_de_jugador(participante.id)
            if equipo_id:
                for i in range(self.combo_equipo.count()):
                    if self.combo_equipo.itemData(i) == equipo_id:
                        self.combo_equipo.setCurrentIndex(i)
                        break

        self._sync_campos_visibles()

        # Cambiar texto del botón
        self.btn_guardar.setText("Actualizar")

    def _eliminar_participante(self, participante: Participante):
        """Elimina un participante después de confirmación."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText(f"¿Estás seguro de eliminar a '{participante.nombre}'?")
        msg.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 10pt;
                font-weight: 600;
            }
            QMessageBox QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QMessageBox QPushButton:pressed {
                background-color: #bdc3c7;
            }
            """
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_si = msg.button(QMessageBox.Yes)
        btn_si.setText("Sí")
        btn_no = msg.button(QMessageBox.No)
        btn_no.setText("No")

        if msg.exec() == QMessageBox.Yes:
            if participante.eliminar():
                self._refrescar_lista_participantes()
                # Si estaba editando este participante, limpiar formulario
                if (
                    self._participante_actual
                    and self._participante_actual.id == participante.id
                ):
                    self._limpiar_campos()
            else:
                msg_error = QMessageBox(self)
                msg_error.setIcon(QMessageBox.Critical)
                msg_error.setWindowTitle("Error")
                msg_error.setText("No se pudo eliminar el participante.")
                msg_error.setStyleSheet(msg.styleSheet())
                msg_error.exec()

    def _limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self._participante_actual = None
        self.txt_nombre.clear()
        self.combo_curso.setCurrentIndex(0)
        self.rb_jugador.setChecked(True)
        self.combo_posicion.setCurrentIndex(0)
        self.spin_amarillas.setValue(0)
        self.spin_rojas.setValue(0)
        self.spin_goles.setValue(0)
        self.combo_equipo.setCurrentIndex(0)
        self.combo_partido.setCurrentIndex(0)
        self.btn_guardar.setText("Guardar")
        self._sync_campos_visibles()

    def _guardar(self):
        """Guarda o actualiza el participante en la base de datos."""
        nombre = self.txt_nombre.text().strip()
        curso = self.combo_curso.currentText().strip()
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        es_jugador, es_arbitro = self._tipo()

        # Validaciones
        if not nombre:
            self._mostrar_mensaje(
                "Datos incompletos", "El nombre es obligatorio.", QMessageBox.Warning
            )
            return

        if not curso:
            self._mostrar_mensaje(
                "Datos incompletos", "El curso es obligatorio.", QMessageBox.Warning
            )
            return

        # Obtener datos de jugador si aplica
        posicion = self.combo_posicion.currentText() if es_jugador else ""
        t_amarillas = self.spin_amarillas.value() if es_jugador else 0
        t_rojas = self.spin_rojas.value() if es_jugador else 0
        goles = self.spin_goles.value() if es_jugador else 0

        if self._participante_actual is None:
            # Crear nuevo participante
            p = Participante(
                nombre=nombre,
                fecha_nacimiento=fecha,
                curso=curso,
                es_jugador=es_jugador,
                es_arbitro=es_arbitro,
                posicion=posicion,
                t_amarillas=t_amarillas,
                t_rojas=t_rojas,
                goles=goles,
            )
        else:
            # Actualizar participante existente
            p = self._participante_actual
            p.nombre = nombre
            p.fecha_nacimiento = fecha
            p.curso = curso
            p.es_jugador = es_jugador
            p.es_arbitro = es_arbitro
            p.posicion = posicion if es_jugador else ""
            p.t_amarillas = t_amarillas
            p.t_rojas = t_rojas
            p.goles = goles

        if not p.guardar():
            self._mostrar_mensaje(
                "Error", "No se pudo guardar el participante.", QMessageBox.Critical
            )
            return

        # Asignar a equipo si es jugador y se seleccionó un equipo
        if es_jugador and self.combo_equipo.currentIndex() > 0:
            equipo_id = self.combo_equipo.currentData()
            if equipo_id:
                equipo_actual = JugadorEquipo.obtener_equipo_de_jugador(p.id)
                if equipo_actual and equipo_actual != equipo_id:
                    JugadorEquipo.desasignar_jugador(p.id, equipo_actual)
                if equipo_actual != equipo_id:
                    JugadorEquipo.asignar_jugador(p.id, equipo_id)

        # Asignar a partido si es árbitro y se seleccionó un partido
        if es_arbitro and self.combo_partido.currentIndex() > 0:
            partido_id = self.combo_partido.currentData()
            if partido_id:
                partido = Partido.obtener_por_id(partido_id)
                if partido:
                    partido.arbitro_id = p.id
                    partido.guardar()

        accion = "actualizado" if self._participante_actual else "registrado"
        self._mostrar_mensaje(
            "Éxito",
            f"Participante '{nombre}' {accion} correctamente.",
            QMessageBox.Information,
        )

        self._limpiar_campos()
        self._refrescar_lista_participantes()

    def _mostrar_mensaje(self, titulo: str, texto: str, icono):
        """Muestra un mensaje con estilo consistente."""
        msg = QMessageBox(self)
        msg.setIcon(icono)
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 10pt;
                font-weight: 600;
            }
            QMessageBox QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QMessageBox QPushButton:pressed {
                background-color: #bdc3c7;
            }
            """
        )
        msg.exec()
