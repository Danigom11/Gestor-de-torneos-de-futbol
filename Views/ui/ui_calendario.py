# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calendario.ui'
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QCalendarWidget,
    QFrame,
    QLabel,
    QListWidget,
    QSizePolicy,
    QSplitter,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_CalendarioPage(object):
    def setupUi(self, CalendarioPage):
        if not CalendarioPage.objectName():
            CalendarioPage.setObjectName("CalendarioPage")
        CalendarioPage.resize(1000, 700)

        self.verticalLayout_main = QVBoxLayout(CalendarioPage)
        self.verticalLayout_main.setObjectName("verticalLayout_main")

        self.lbl_titulo = QLabel(CalendarioPage)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(CalendarioPage)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)

        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName("panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName("verticalLayout_izq")

        self.label_calendario = QLabel(self.panel_izquierdo)
        self.label_calendario.setObjectName("label_calendario")
        self.verticalLayout_izq.addWidget(self.label_calendario)

        self.calendario = QCalendarWidget(self.panel_izquierdo)
        self.calendario.setObjectName("calendario")
        self.verticalLayout_izq.addWidget(self.calendario)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.verticalLayout_izq.addItem(self.verticalSpacer)

        self.splitter.addWidget(self.panel_izquierdo)

        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName("panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName("verticalLayout_der")

        self.label_partidos = QLabel(self.panel_derecho)
        self.label_partidos.setObjectName("label_partidos")
        self.verticalLayout_der.addWidget(self.label_partidos)

        self.lista_partidos = QListWidget(self.panel_derecho)
        self.lista_partidos.setObjectName("lista_partidos")
        self.verticalLayout_der.addWidget(self.lista_partidos)

        self.splitter.addWidget(self.panel_derecho)
        self.verticalLayout_main.addWidget(self.splitter)

        self.retranslateUi(CalendarioPage)
        QMetaObject.connectSlotsByName(CalendarioPage)

    def retranslateUi(self, CalendarioPage):
        CalendarioPage.setWindowTitle(
            QCoreApplication.translate("CalendarioPage", "Calendario", None)
        )
        self.lbl_titulo.setText(
            QCoreApplication.translate("CalendarioPage", "Calendario de Partidos", None)
        )
        self.label_calendario.setText(
            QCoreApplication.translate("CalendarioPage", "Selecciona una fecha", None)
        )
        self.label_partidos.setText(
            QCoreApplication.translate("CalendarioPage", "Partidos", None)
        )
