# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'informe.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_InformesWidget(object):
    def setupUi(self, InformesWidget):
        if not InformesWidget.objectName():
            InformesWidget.setObjectName(u"InformesWidget")
        InformesWidget.resize(1000, 650)
        self.verticalLayout_main = QVBoxLayout(InformesWidget)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(InformesWidget)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(InformesWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.panel_controles = QFrame(self.splitter)
        self.panel_controles.setObjectName(u"panel_controles")
        self.panel_controles.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_controles = QVBoxLayout(self.panel_controles)
        self.verticalLayout_controles.setObjectName(u"verticalLayout_controles")
        self.lbl_selector = QLabel(self.panel_controles)
        self.lbl_selector.setObjectName(u"lbl_selector")

        self.verticalLayout_controles.addWidget(self.lbl_selector)

        self.combo_informe = QComboBox(self.panel_controles)
        self.combo_informe.addItem("")
        self.combo_informe.addItem("")
        self.combo_informe.addItem("")
        self.combo_informe.setObjectName(u"combo_informe")

        self.verticalLayout_controles.addWidget(self.combo_informe)

        self.lbl_descripcion = QLabel(self.panel_controles)
        self.lbl_descripcion.setObjectName(u"lbl_descripcion")
        self.lbl_descripcion.setWordWrap(True)

        self.verticalLayout_controles.addWidget(self.lbl_descripcion)

        self.grupo_filtros = QGroupBox(self.panel_controles)
        self.grupo_filtros.setObjectName(u"grupo_filtros")
        self.verticalLayout_filtros = QVBoxLayout(self.grupo_filtros)
        self.verticalLayout_filtros.setObjectName(u"verticalLayout_filtros")
        self.lbl_equipo = QLabel(self.grupo_filtros)
        self.lbl_equipo.setObjectName(u"lbl_equipo")

        self.verticalLayout_filtros.addWidget(self.lbl_equipo)

        self.combo_equipo = QComboBox(self.grupo_filtros)
        self.combo_equipo.setObjectName(u"combo_equipo")

        self.verticalLayout_filtros.addWidget(self.combo_equipo)

        self.lbl_eliminatoria = QLabel(self.grupo_filtros)
        self.lbl_eliminatoria.setObjectName(u"lbl_eliminatoria")

        self.verticalLayout_filtros.addWidget(self.lbl_eliminatoria)

        self.combo_eliminatoria = QComboBox(self.grupo_filtros)
        self.combo_eliminatoria.setObjectName(u"combo_eliminatoria")

        self.verticalLayout_filtros.addWidget(self.combo_eliminatoria)


        self.verticalLayout_controles.addWidget(self.grupo_filtros)

        self.grupo_ruta = QGroupBox(self.panel_controles)
        self.grupo_ruta.setObjectName(u"grupo_ruta")
        self.horizontalLayout_ruta = QHBoxLayout(self.grupo_ruta)
        self.horizontalLayout_ruta.setObjectName(u"horizontalLayout_ruta")
        self.txt_ruta = QLineEdit(self.grupo_ruta)
        self.txt_ruta.setObjectName(u"txt_ruta")
        self.txt_ruta.setReadOnly(True)

        self.horizontalLayout_ruta.addWidget(self.txt_ruta)

        self.btn_cambiar_ruta = QPushButton(self.grupo_ruta)
        self.btn_cambiar_ruta.setObjectName(u"btn_cambiar_ruta")

        self.horizontalLayout_ruta.addWidget(self.btn_cambiar_ruta)


        self.verticalLayout_controles.addWidget(self.grupo_ruta)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_controles.addItem(self.verticalSpacer)

        self.btn_generar = QPushButton(self.panel_controles)
        self.btn_generar.setObjectName(u"btn_generar")

        self.verticalLayout_controles.addWidget(self.btn_generar)

        self.btn_abrir_pdf = QPushButton(self.panel_controles)
        self.btn_abrir_pdf.setObjectName(u"btn_abrir_pdf")
        self.btn_abrir_pdf.setEnabled(False)

        self.verticalLayout_controles.addWidget(self.btn_abrir_pdf)

        self.btn_abrir_carpeta = QPushButton(self.panel_controles)
        self.btn_abrir_carpeta.setObjectName(u"btn_abrir_carpeta")

        self.verticalLayout_controles.addWidget(self.btn_abrir_carpeta)

        self.splitter.addWidget(self.panel_controles)
        self.panel_preview = QFrame(self.splitter)
        self.panel_preview.setObjectName(u"panel_preview")
        self.panel_preview.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_preview = QVBoxLayout(self.panel_preview)
        self.verticalLayout_preview.setObjectName(u"verticalLayout_preview")
        self.lbl_preview_titulo = QLabel(self.panel_preview)
        self.lbl_preview_titulo.setObjectName(u"lbl_preview_titulo")

        self.verticalLayout_preview.addWidget(self.lbl_preview_titulo)

        self.text_preview = QTextBrowser(self.panel_preview)
        self.text_preview.setObjectName(u"text_preview")

        self.verticalLayout_preview.addWidget(self.text_preview)

        self.lbl_estado = QLabel(self.panel_preview)
        self.lbl_estado.setObjectName(u"lbl_estado")

        self.verticalLayout_preview.addWidget(self.lbl_estado)

        self.splitter.addWidget(self.panel_preview)

        self.verticalLayout_main.addWidget(self.splitter)


        self.retranslateUi(InformesWidget)

        QMetaObject.connectSlotsByName(InformesWidget)
    # setupUi

    def retranslateUi(self, InformesWidget):
        InformesWidget.setWindowTitle(QCoreApplication.translate("InformesWidget", u"Informes del Torneo", None))
        self.lbl_titulo.setText(QCoreApplication.translate("InformesWidget", u"Informes del Torneo", None))
        self.lbl_selector.setText(QCoreApplication.translate("InformesWidget", u"Seleccionar Informe:", None))
        self.combo_informe.setItemText(0, QCoreApplication.translate("InformesWidget", u"Equipos y Jugadores", None))
        self.combo_informe.setItemText(1, QCoreApplication.translate("InformesWidget", u"Partidos y Resultados", None))
        self.combo_informe.setItemText(2, QCoreApplication.translate("InformesWidget", u"Clasificaci\u00f3n y Eliminatorias", None))

        self.lbl_descripcion.setText(QCoreApplication.translate("InformesWidget", u"Descripci\u00f3n del informe seleccionado", None))
        self.grupo_filtros.setTitle(QCoreApplication.translate("InformesWidget", u"Filtros", None))
        self.lbl_equipo.setText(QCoreApplication.translate("InformesWidget", u"Equipo:", None))
        self.lbl_eliminatoria.setText(QCoreApplication.translate("InformesWidget", u"Eliminatoria:", None))
        self.grupo_ruta.setTitle(QCoreApplication.translate("InformesWidget", u"Ruta de Guardado", None))
        self.txt_ruta.setPlaceholderText(QCoreApplication.translate("InformesWidget", u"Carpeta reports (por defecto)", None))
        self.btn_cambiar_ruta.setText(QCoreApplication.translate("InformesWidget", u"Cambiar", None))
        self.btn_generar.setText(QCoreApplication.translate("InformesWidget", u"Generar Informe PDF", None))
        self.btn_abrir_pdf.setText(QCoreApplication.translate("InformesWidget", u"Abrir \u00daltimo PDF", None))
        self.btn_abrir_carpeta.setText(QCoreApplication.translate("InformesWidget", u"Abrir Carpeta Reports", None))
        self.lbl_preview_titulo.setText(QCoreApplication.translate("InformesWidget", u"Vista Previa / Informaci\u00f3n", None))
        self.lbl_estado.setText(QCoreApplication.translate("InformesWidget", u"Listo. Selecciona un informe y pulsa Generar.", None))
    # retranslateUi

