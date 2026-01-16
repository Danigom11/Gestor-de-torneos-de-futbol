# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resultados.ui'
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class Ui_ResultadosPage(object):
    def setupUi(self, ResultadosPage):
        if not ResultadosPage.objectName():
            ResultadosPage.setObjectName("ResultadosPage")
        ResultadosPage.resize(1000, 700)

        self.verticalLayout_main = QVBoxLayout(ResultadosPage)
        self.verticalLayout_main.setObjectName("verticalLayout_main")

        self.lbl_titulo = QLabel(ResultadosPage)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(ResultadosPage)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)

        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName("panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName("verticalLayout_izq")

        self.label_partidos = QLabel(self.panel_izquierdo)
        self.label_partidos.setObjectName("label_partidos")
        self.verticalLayout_izq.addWidget(self.label_partidos)

        self.lista_partidos = QListWidget(self.panel_izquierdo)
        self.lista_partidos.setObjectName("lista_partidos")
        self.verticalLayout_izq.addWidget(self.lista_partidos)

        self.resumen = QLabel(self.panel_izquierdo)
        self.resumen.setObjectName("resumen")
        self.resumen.setWordWrap(True)
        self.verticalLayout_izq.addWidget(self.resumen)

        self.splitter.addWidget(self.panel_izquierdo)

        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName("panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName("verticalLayout_der")

        self.label_instruccion = QLabel(self.panel_derecho)
        self.label_instruccion.setObjectName("label_instruccion")
        self.label_instruccion.setAlignment(Qt.AlignCenter)
        self.verticalLayout_der.addWidget(self.label_instruccion)

        self.scroll_equipos = QScrollArea(self.panel_derecho)
        self.scroll_equipos.setObjectName("scroll_equipos")
        self.scroll_equipos.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.horizontalLayout_scroll = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_scroll.setObjectName("horizontalLayout_scroll")

        self.frame_local = QFrame(self.scrollAreaWidgetContents)
        self.frame_local.setObjectName("frame_local")
        self.frame_local.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_local = QVBoxLayout(self.frame_local)
        self.verticalLayout_local.setObjectName("verticalLayout_local")

        self.label_local = QLabel(self.frame_local)
        self.label_local.setObjectName("label_local")
        self.label_local.setAlignment(Qt.AlignCenter)
        self.verticalLayout_local.addWidget(self.label_local)

        self.horizontalLayout_scroll.addWidget(self.frame_local)

        self.frame_visitante = QFrame(self.scrollAreaWidgetContents)
        self.frame_visitante.setObjectName("frame_visitante")
        self.frame_visitante.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_visitante = QVBoxLayout(self.frame_visitante)
        self.verticalLayout_visitante.setObjectName("verticalLayout_visitante")

        self.label_visitante = QLabel(self.frame_visitante)
        self.label_visitante.setObjectName("label_visitante")
        self.label_visitante.setAlignment(Qt.AlignCenter)
        self.verticalLayout_visitante.addWidget(self.label_visitante)

        self.horizontalLayout_scroll.addWidget(self.frame_visitante)
        self.scroll_equipos.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_der.addWidget(self.scroll_equipos)

        self.btn_guardar = QPushButton(self.panel_derecho)
        self.btn_guardar.setObjectName("btn_guardar")
        self.verticalLayout_der.addWidget(self.btn_guardar)

        self.splitter.addWidget(self.panel_derecho)
        self.verticalLayout_main.addWidget(self.splitter)

        self.retranslateUi(ResultadosPage)
        QMetaObject.connectSlotsByName(ResultadosPage)

    def retranslateUi(self, ResultadosPage):
        ResultadosPage.setWindowTitle(
            QCoreApplication.translate("ResultadosPage", "Resultados", None)
        )
        self.lbl_titulo.setText(
            QCoreApplication.translate(
                "ResultadosPage", "Actualizaci\u00f3n de Resultados", None
            )
        )
        self.label_partidos.setText(
            QCoreApplication.translate("ResultadosPage", "Partidos", None)
        )
        self.resumen.setText(
            QCoreApplication.translate(
                "ResultadosPage", "(Resumen del partido aparecer\u00e1 aqu\u00ed)", None
            )
        )
        self.label_instruccion.setText(
            QCoreApplication.translate(
                "ResultadosPage", "Selecciona un partido de la lista", None
            )
        )
        self.label_local.setText(
            QCoreApplication.translate("ResultadosPage", "Equipo Local", None)
        )
        self.label_visitante.setText(
            QCoreApplication.translate("ResultadosPage", "Equipo Visitante", None)
        )
        self.btn_guardar.setText(
            QCoreApplication.translate("ResultadosPage", "Guardar Resultado", None)
        )
