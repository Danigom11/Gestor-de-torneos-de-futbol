# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calendario.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QFrame, QLabel,
    QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem,
    QSplitter, QVBoxLayout, QWidget)

class Ui_CalendarioPage(object):
    def setupUi(self, CalendarioPage):
        if not CalendarioPage.objectName():
            CalendarioPage.setObjectName(u"CalendarioPage")
        CalendarioPage.resize(1000, 700)
        self.verticalLayout_main = QVBoxLayout(CalendarioPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(CalendarioPage)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(CalendarioPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName(u"panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName(u"verticalLayout_izq")
        self.label_calendario = QLabel(self.panel_izquierdo)
        self.label_calendario.setObjectName(u"label_calendario")

        self.verticalLayout_izq.addWidget(self.label_calendario)

        self.calendario = QCalendarWidget(self.panel_izquierdo)
        self.calendario.setObjectName(u"calendario")

        self.verticalLayout_izq.addWidget(self.calendario)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_izq.addItem(self.verticalSpacer)

        self.splitter.addWidget(self.panel_izquierdo)
        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName(u"panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName(u"verticalLayout_der")
        self.label_partidos = QLabel(self.panel_derecho)
        self.label_partidos.setObjectName(u"label_partidos")

        self.verticalLayout_der.addWidget(self.label_partidos)

        self.lista_partidos = QListWidget(self.panel_derecho)
        self.lista_partidos.setObjectName(u"lista_partidos")

        self.verticalLayout_der.addWidget(self.lista_partidos)

        self.splitter.addWidget(self.panel_derecho)

        self.verticalLayout_main.addWidget(self.splitter)


        self.retranslateUi(CalendarioPage)

        QMetaObject.connectSlotsByName(CalendarioPage)
    # setupUi

    def retranslateUi(self, CalendarioPage):
        CalendarioPage.setWindowTitle(QCoreApplication.translate("CalendarioPage", u"Calendario", None))
        self.lbl_titulo.setText(QCoreApplication.translate("CalendarioPage", u"Calendario de Partidos", None))
        self.label_calendario.setText(QCoreApplication.translate("CalendarioPage", u"Selecciona una fecha", None))
        self.label_partidos.setText(QCoreApplication.translate("CalendarioPage", u"Partidos", None))
    # retranslateUi

