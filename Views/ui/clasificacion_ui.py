# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clasificacion.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ClasificacionPage(object):
    def setupUi(self, ClasificacionPage):
        if not ClasificacionPage.objectName():
            ClasificacionPage.setObjectName(u"ClasificacionPage")
        ClasificacionPage.resize(1000, 700)
        self.verticalLayout_main = QVBoxLayout(ClasificacionPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(ClasificacionPage)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.frame_bracket = QFrame(ClasificacionPage)
        self.frame_bracket.setObjectName(u"frame_bracket")
        self.frame_bracket.setFrameShape(QFrame.StyledPanel)
        self.frame_bracket.setFrameShadow(QFrame.Raised)
        self.verticalLayout_bracket = QVBoxLayout(self.frame_bracket)
        self.verticalLayout_bracket.setObjectName(u"verticalLayout_bracket")
        self.label_bracket_info = QLabel(self.frame_bracket)
        self.label_bracket_info.setObjectName(u"label_bracket_info")
        self.label_bracket_info.setAlignment(Qt.AlignCenter)

        self.verticalLayout_bracket.addWidget(self.label_bracket_info)


        self.verticalLayout_main.addWidget(self.frame_bracket)

        self.btn_actualizar = QPushButton(ClasificacionPage)
        self.btn_actualizar.setObjectName(u"btn_actualizar")

        self.verticalLayout_main.addWidget(self.btn_actualizar)


        self.retranslateUi(ClasificacionPage)

        QMetaObject.connectSlotsByName(ClasificacionPage)
    # setupUi

    def retranslateUi(self, ClasificacionPage):
        ClasificacionPage.setWindowTitle(QCoreApplication.translate("ClasificacionPage", u"Clasificaci\u00f3n", None))
        self.lbl_titulo.setText(QCoreApplication.translate("ClasificacionPage", u"Cuadro de Clasificaci\u00f3n", None))
        self.label_bracket_info.setText(QCoreApplication.translate("ClasificacionPage", u"Bracket de eliminatorias (se dibujar\u00e1 din\u00e1micamente)", None))
        self.btn_actualizar.setText(QCoreApplication.translate("ClasificacionPage", u"Actualizar Clasificaci\u00f3n", None))
    # retranslateUi

