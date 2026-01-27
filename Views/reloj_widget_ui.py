# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reloj_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_lbl_tiempo(object):
    def setupUi(self, lbl_tiempo):
        if not lbl_tiempo.objectName():
            lbl_tiempo.setObjectName(u"lbl_tiempo")
        lbl_tiempo.resize(640, 480)
        self.label = QLabel(lbl_tiempo)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 180, 461, 101))
        font = QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(lbl_tiempo)

        QMetaObject.connectSlotsByName(lbl_tiempo)
    # setupUi

    def retranslateUi(self, lbl_tiempo):
        lbl_tiempo.setWindowTitle(QCoreApplication.translate("lbl_tiempo", u"Form", None))
        self.label.setText(QCoreApplication.translate("lbl_tiempo", u"TextLabel", None))
    # retranslateUi

