# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resultados.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QScrollArea,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)

class Ui_ResultadosPage(object):
    def setupUi(self, ResultadosPage):
        if not ResultadosPage.objectName():
            ResultadosPage.setObjectName(u"ResultadosPage")
        ResultadosPage.resize(1000, 700)
        self.verticalLayout_main = QVBoxLayout(ResultadosPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(ResultadosPage)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(ResultadosPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName(u"panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName(u"verticalLayout_izq")
        self.label_partidos = QLabel(self.panel_izquierdo)
        self.label_partidos.setObjectName(u"label_partidos")

        self.verticalLayout_izq.addWidget(self.label_partidos)

        self.lista_partidos = QListWidget(self.panel_izquierdo)
        self.lista_partidos.setObjectName(u"lista_partidos")

        self.verticalLayout_izq.addWidget(self.lista_partidos)

        self.resumen = QLabel(self.panel_izquierdo)
        self.resumen.setObjectName(u"resumen")
        self.resumen.setWordWrap(True)

        self.verticalLayout_izq.addWidget(self.resumen)

        self.splitter.addWidget(self.panel_izquierdo)
        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName(u"panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName(u"verticalLayout_der")
        self.label_instruccion = QLabel(self.panel_derecho)
        self.label_instruccion.setObjectName(u"label_instruccion")
        self.label_instruccion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_der.addWidget(self.label_instruccion)

        self.scroll_equipos = QScrollArea(self.panel_derecho)
        self.scroll_equipos.setObjectName(u"scroll_equipos")
        self.scroll_equipos.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.horizontalLayout_scroll = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_scroll.setObjectName(u"horizontalLayout_scroll")
        self.frame_local = QFrame(self.scrollAreaWidgetContents)
        self.frame_local.setObjectName(u"frame_local")
        self.frame_local.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_local = QVBoxLayout(self.frame_local)
        self.verticalLayout_local.setObjectName(u"verticalLayout_local")
        self.label_local = QLabel(self.frame_local)
        self.label_local.setObjectName(u"label_local")
        self.label_local.setAlignment(Qt.AlignCenter)

        self.verticalLayout_local.addWidget(self.label_local)


        self.horizontalLayout_scroll.addWidget(self.frame_local)

        self.frame_visitante = QFrame(self.scrollAreaWidgetContents)
        self.frame_visitante.setObjectName(u"frame_visitante")
        self.frame_visitante.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_visitante = QVBoxLayout(self.frame_visitante)
        self.verticalLayout_visitante.setObjectName(u"verticalLayout_visitante")
        self.label_visitante = QLabel(self.frame_visitante)
        self.label_visitante.setObjectName(u"label_visitante")
        self.label_visitante.setAlignment(Qt.AlignCenter)

        self.verticalLayout_visitante.addWidget(self.label_visitante)


        self.horizontalLayout_scroll.addWidget(self.frame_visitante)

        self.scroll_equipos.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_der.addWidget(self.scroll_equipos)

        self.btn_guardar = QPushButton(self.panel_derecho)
        self.btn_guardar.setObjectName(u"btn_guardar")

        self.verticalLayout_der.addWidget(self.btn_guardar)

        self.splitter.addWidget(self.panel_derecho)

        self.verticalLayout_main.addWidget(self.splitter)


        self.retranslateUi(ResultadosPage)

        QMetaObject.connectSlotsByName(ResultadosPage)
    # setupUi

    def retranslateUi(self, ResultadosPage):
        ResultadosPage.setWindowTitle(QCoreApplication.translate("ResultadosPage", u"Resultados", None))
        self.lbl_titulo.setText(QCoreApplication.translate("ResultadosPage", u"Actualizaci\u00f3n de Resultados", None))
        self.label_partidos.setText(QCoreApplication.translate("ResultadosPage", u"Partidos", None))
        self.resumen.setText(QCoreApplication.translate("ResultadosPage", u"(Resumen del partido aparecer\u00e1 aqu\u00ed)", None))
        self.label_instruccion.setText(QCoreApplication.translate("ResultadosPage", u"Selecciona un partido de la lista", None))
        self.label_local.setText(QCoreApplication.translate("ResultadosPage", u"Equipo Local", None))
        self.label_visitante.setText(QCoreApplication.translate("ResultadosPage", u"Equipo Visitante", None))
        self.btn_guardar.setText(QCoreApplication.translate("ResultadosPage", u"Guardar Resultado", None))
    # retranslateUi

