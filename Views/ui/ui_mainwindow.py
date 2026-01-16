# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QFrame,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        self.action_salir = QAction(MainWindow)
        self.action_salir.setObjectName("action_salir")
        self.action_ayuda = QAction(MainWindow)
        self.action_ayuda.setObjectName("action_ayuda")
        self.action_acerca_de = QAction(MainWindow)
        self.action_acerca_de.setObjectName("action_acerca_de")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_inicio = QWidget()
        self.page_inicio.setObjectName("page_inicio")

        self.verticalLayout_2 = QVBoxLayout(self.page_inicio)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.lbl_titulo = QLabel(self.page_inicio)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.lbl_titulo)

        self.frame_tarjetas = QFrame(self.page_inicio)
        self.frame_tarjetas.setObjectName("frame_tarjetas")
        self.frame_tarjetas.setFrameShape(QFrame.StyledPanel)
        self.frame_tarjetas.setFrameShadow(QFrame.Raised)

        self.gridLayout = QGridLayout(self.frame_tarjetas)
        self.gridLayout.setObjectName("gridLayout")

        self.btn_equipos = QPushButton(self.frame_tarjetas)
        self.btn_equipos.setObjectName("btn_equipos")
        self.gridLayout.addWidget(self.btn_equipos, 0, 0, 1, 1)

        self.btn_participantes = QPushButton(self.frame_tarjetas)
        self.btn_participantes.setObjectName("btn_participantes")
        self.gridLayout.addWidget(self.btn_participantes, 0, 1, 1, 1)

        self.btn_calendario = QPushButton(self.frame_tarjetas)
        self.btn_calendario.setObjectName("btn_calendario")
        self.gridLayout.addWidget(self.btn_calendario, 1, 0, 1, 1)

        self.btn_resultados = QPushButton(self.frame_tarjetas)
        self.btn_resultados.setObjectName("btn_resultados")
        self.gridLayout.addWidget(self.btn_resultados, 1, 1, 1, 1)

        self.btn_clasificacion = QPushButton(self.frame_tarjetas)
        self.btn_clasificacion.setObjectName("btn_clasificacion")
        self.gridLayout.addWidget(self.btn_clasificacion, 2, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.frame_tarjetas)
        self.stackedWidget.addWidget(self.page_inicio)
        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))

        self.menu_archivo = QMenu(self.menubar)
        self.menu_archivo.setObjectName("menu_archivo")

        self.menu_ayuda = QMenu(self.menubar)
        self.menu_ayuda.setObjectName("menu_ayuda")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_archivo.menuAction())
        self.menubar.addAction(self.menu_ayuda.menuAction())
        self.menu_archivo.addAction(self.action_salir)
        self.menu_ayuda.addAction(self.action_ayuda)
        self.menu_ayuda.addAction(self.action_acerca_de)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "Gesti\u00f3n de Torneo de F\u00fatbol", None
            )
        )
        self.action_salir.setText(
            QCoreApplication.translate("MainWindow", "Salir", None)
        )
        self.action_ayuda.setText(
            QCoreApplication.translate("MainWindow", "Ayuda", None)
        )
        self.action_acerca_de.setText(
            QCoreApplication.translate("MainWindow", "Acerca de", None)
        )
        self.lbl_titulo.setText(
            QCoreApplication.translate(
                "MainWindow", "Gesti\u00f3n de Torneo de F\u00fatbol", None
            )
        )
        self.btn_equipos.setText(
            QCoreApplication.translate("MainWindow", "Equipos", None)
        )
        self.btn_participantes.setText(
            QCoreApplication.translate("MainWindow", "Participantes", None)
        )
        self.btn_calendario.setText(
            QCoreApplication.translate("MainWindow", "Calendario", None)
        )
        self.btn_resultados.setText(
            QCoreApplication.translate("MainWindow", "Resultados", None)
        )
        self.btn_clasificacion.setText(
            QCoreApplication.translate("MainWindow", "Clasificaci\u00f3n", None)
        )
        self.menu_archivo.setTitle(
            QCoreApplication.translate("MainWindow", "Archivo", None)
        )
        self.menu_ayuda.setTitle(
            QCoreApplication.translate("MainWindow", "Ayuda", None)
        )
