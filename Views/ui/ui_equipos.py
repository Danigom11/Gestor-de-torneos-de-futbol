# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equipos.ui'
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class Ui_EquiposPage(object):
    def setupUi(self, EquiposPage):
        if not EquiposPage.objectName():
            EquiposPage.setObjectName("EquiposPage")
        EquiposPage.resize(1000, 700)

        self.verticalLayout_main = QVBoxLayout(EquiposPage)
        self.verticalLayout_main.setObjectName("verticalLayout_main")

        self.lbl_titulo = QLabel(EquiposPage)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(EquiposPage)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)

        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName("panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)
        self.panel_izquierdo.setFrameShadow(QFrame.Raised)

        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName("verticalLayout_izq")

        self.label_nombre = QLabel(self.panel_izquierdo)
        self.label_nombre.setObjectName("label_nombre")
        self.verticalLayout_izq.addWidget(self.label_nombre)

        self.txt_nombre = QLineEdit(self.panel_izquierdo)
        self.txt_nombre.setObjectName("txt_nombre")
        self.verticalLayout_izq.addWidget(self.txt_nombre)

        self.label_curso = QLabel(self.panel_izquierdo)
        self.label_curso.setObjectName("label_curso")
        self.verticalLayout_izq.addWidget(self.label_curso)

        self.combo_curso = QComboBox(self.panel_izquierdo)
        self.combo_curso.setObjectName("combo_curso")
        self.combo_curso.setEditable(True)
        self.verticalLayout_izq.addWidget(self.combo_curso)

        self.label_color = QLabel(self.panel_izquierdo)
        self.label_color.setObjectName("label_color")
        self.verticalLayout_izq.addWidget(self.label_color)

        self.btn_color = QPushButton(self.panel_izquierdo)
        self.btn_color.setObjectName("btn_color")
        self.verticalLayout_izq.addWidget(self.btn_color)

        self.label_escudo = QLabel(self.panel_izquierdo)
        self.label_escudo.setObjectName("label_escudo")
        self.verticalLayout_izq.addWidget(self.label_escudo)

        self.btn_escudo = QPushButton(self.panel_izquierdo)
        self.btn_escudo.setObjectName("btn_escudo")
        self.verticalLayout_izq.addWidget(self.btn_escudo)

        self.tarjeta_preview = QFrame(self.panel_izquierdo)
        self.tarjeta_preview.setObjectName("tarjeta_preview")
        self.tarjeta_preview.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_preview = QVBoxLayout(self.tarjeta_preview)
        self.verticalLayout_preview.setObjectName("verticalLayout_preview")

        self.lbl_preview_nombre = QLabel(self.tarjeta_preview)
        self.lbl_preview_nombre.setObjectName("lbl_preview_nombre")
        self.lbl_preview_nombre.setAlignment(Qt.AlignCenter)
        self.verticalLayout_preview.addWidget(self.lbl_preview_nombre)

        self.lbl_preview_curso = QLabel(self.tarjeta_preview)
        self.lbl_preview_curso.setObjectName("lbl_preview_curso")
        self.lbl_preview_curso.setAlignment(Qt.AlignCenter)
        self.verticalLayout_preview.addWidget(self.lbl_preview_curso)

        self.verticalLayout_izq.addWidget(self.tarjeta_preview)

        self.btn_registrar = QPushButton(self.panel_izquierdo)
        self.btn_registrar.setObjectName("btn_registrar")
        self.verticalLayout_izq.addWidget(self.btn_registrar)

        self.splitter.addWidget(self.panel_izquierdo)

        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName("panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)
        self.panel_derecho.setFrameShadow(QFrame.Raised)

        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName("verticalLayout_der")

        self.label_filtro = QLabel(self.panel_derecho)
        self.label_filtro.setObjectName("label_filtro")
        self.verticalLayout_der.addWidget(self.label_filtro)

        self.txt_filtro = QLineEdit(self.panel_derecho)
        self.txt_filtro.setObjectName("txt_filtro")
        self.verticalLayout_der.addWidget(self.txt_filtro)

        self.lista_equipos = QListWidget(self.panel_derecho)
        self.lista_equipos.setObjectName("lista_equipos")
        self.verticalLayout_der.addWidget(self.lista_equipos)

        self.splitter.addWidget(self.panel_derecho)
        self.verticalLayout_main.addWidget(self.splitter)

        self.retranslateUi(EquiposPage)
        QMetaObject.connectSlotsByName(EquiposPage)

    def retranslateUi(self, EquiposPage):
        EquiposPage.setWindowTitle(
            QCoreApplication.translate("EquiposPage", "Equipos", None)
        )
        self.lbl_titulo.setText(
            QCoreApplication.translate("EquiposPage", "Gesti\u00f3n de Equipos", None)
        )
        self.label_nombre.setText(
            QCoreApplication.translate("EquiposPage", "Nombre", None)
        )
        self.label_curso.setText(
            QCoreApplication.translate("EquiposPage", "Curso", None)
        )
        self.label_color.setText(
            QCoreApplication.translate("EquiposPage", "Color", None)
        )
        self.btn_color.setText(
            QCoreApplication.translate("EquiposPage", "Seleccionar Color", None)
        )
        self.label_escudo.setText(
            QCoreApplication.translate("EquiposPage", "Escudo", None)
        )
        self.btn_escudo.setText(
            QCoreApplication.translate("EquiposPage", "Seleccionar Escudo", None)
        )
        self.lbl_preview_nombre.setText(
            QCoreApplication.translate("EquiposPage", "Nombre del equipo", None)
        )
        self.lbl_preview_curso.setText(
            QCoreApplication.translate("EquiposPage", "Curso", None)
        )
        self.btn_registrar.setText(
            QCoreApplication.translate("EquiposPage", "Registrar", None)
        )
        self.label_filtro.setText(
            QCoreApplication.translate("EquiposPage", "Filtrar", None)
        )
