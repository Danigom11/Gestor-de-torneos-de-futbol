# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equipos.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)

class Ui_EquiposPage(object):
    def setupUi(self, EquiposPage):
        if not EquiposPage.objectName():
            EquiposPage.setObjectName(u"EquiposPage")
        EquiposPage.resize(1000, 700)
        self.verticalLayout_main = QVBoxLayout(EquiposPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(EquiposPage)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(EquiposPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName(u"panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)
        self.panel_izquierdo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName(u"verticalLayout_izq")
        self.label_nombre = QLabel(self.panel_izquierdo)
        self.label_nombre.setObjectName(u"label_nombre")

        self.verticalLayout_izq.addWidget(self.label_nombre)

        self.txt_nombre = QLineEdit(self.panel_izquierdo)
        self.txt_nombre.setObjectName(u"txt_nombre")

        self.verticalLayout_izq.addWidget(self.txt_nombre)

        self.label_curso = QLabel(self.panel_izquierdo)
        self.label_curso.setObjectName(u"label_curso")

        self.verticalLayout_izq.addWidget(self.label_curso)

        self.combo_curso = QComboBox(self.panel_izquierdo)
        self.combo_curso.setObjectName(u"combo_curso")
        self.combo_curso.setEditable(True)

        self.verticalLayout_izq.addWidget(self.combo_curso)

        self.label_color = QLabel(self.panel_izquierdo)
        self.label_color.setObjectName(u"label_color")

        self.verticalLayout_izq.addWidget(self.label_color)

        self.btn_color = QPushButton(self.panel_izquierdo)
        self.btn_color.setObjectName(u"btn_color")

        self.verticalLayout_izq.addWidget(self.btn_color)

        self.label_escudo = QLabel(self.panel_izquierdo)
        self.label_escudo.setObjectName(u"label_escudo")

        self.verticalLayout_izq.addWidget(self.label_escudo)

        self.btn_escudo = QPushButton(self.panel_izquierdo)
        self.btn_escudo.setObjectName(u"btn_escudo")

        self.verticalLayout_izq.addWidget(self.btn_escudo)

        self.tarjeta_preview = QFrame(self.panel_izquierdo)
        self.tarjeta_preview.setObjectName(u"tarjeta_preview")
        self.tarjeta_preview.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_preview = QVBoxLayout(self.tarjeta_preview)
        self.verticalLayout_preview.setObjectName(u"verticalLayout_preview")
        self.lbl_preview_nombre = QLabel(self.tarjeta_preview)
        self.lbl_preview_nombre.setObjectName(u"lbl_preview_nombre")
        self.lbl_preview_nombre.setAlignment(Qt.AlignCenter)

        self.verticalLayout_preview.addWidget(self.lbl_preview_nombre)

        self.lbl_preview_curso = QLabel(self.tarjeta_preview)
        self.lbl_preview_curso.setObjectName(u"lbl_preview_curso")
        self.lbl_preview_curso.setAlignment(Qt.AlignCenter)

        self.verticalLayout_preview.addWidget(self.lbl_preview_curso)


        self.verticalLayout_izq.addWidget(self.tarjeta_preview)

        self.btn_registrar = QPushButton(self.panel_izquierdo)
        self.btn_registrar.setObjectName(u"btn_registrar")

        self.verticalLayout_izq.addWidget(self.btn_registrar)

        self.splitter.addWidget(self.panel_izquierdo)
        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName(u"panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)
        self.panel_derecho.setFrameShadow(QFrame.Raised)
        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName(u"verticalLayout_der")
        self.label_filtro = QLabel(self.panel_derecho)
        self.label_filtro.setObjectName(u"label_filtro")

        self.verticalLayout_der.addWidget(self.label_filtro)

        self.txt_filtro = QLineEdit(self.panel_derecho)
        self.txt_filtro.setObjectName(u"txt_filtro")

        self.verticalLayout_der.addWidget(self.txt_filtro)

        self.lista_equipos = QListWidget(self.panel_derecho)
        self.lista_equipos.setObjectName(u"lista_equipos")

        self.verticalLayout_der.addWidget(self.lista_equipos)

        self.splitter.addWidget(self.panel_derecho)

        self.verticalLayout_main.addWidget(self.splitter)


        self.retranslateUi(EquiposPage)

        QMetaObject.connectSlotsByName(EquiposPage)
    # setupUi

    def retranslateUi(self, EquiposPage):
        EquiposPage.setWindowTitle(QCoreApplication.translate("EquiposPage", u"Equipos", None))
        self.lbl_titulo.setText(QCoreApplication.translate("EquiposPage", u"Gesti\u00f3n de Equipos", None))
        self.label_nombre.setText(QCoreApplication.translate("EquiposPage", u"Nombre", None))
        self.label_curso.setText(QCoreApplication.translate("EquiposPage", u"Curso", None))
        self.label_color.setText(QCoreApplication.translate("EquiposPage", u"Color", None))
        self.btn_color.setText(QCoreApplication.translate("EquiposPage", u"Seleccionar Color", None))
        self.label_escudo.setText(QCoreApplication.translate("EquiposPage", u"Escudo", None))
        self.btn_escudo.setText(QCoreApplication.translate("EquiposPage", u"Seleccionar Escudo", None))
        self.lbl_preview_nombre.setText(QCoreApplication.translate("EquiposPage", u"Nombre del equipo", None))
        self.lbl_preview_curso.setText(QCoreApplication.translate("EquiposPage", u"Curso", None))
        self.btn_registrar.setText(QCoreApplication.translate("EquiposPage", u"Registrar", None))
        self.label_filtro.setText(QCoreApplication.translate("EquiposPage", u"Filtrar", None))
    # retranslateUi

