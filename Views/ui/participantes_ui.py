# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'participantes.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSplitter, QVBoxLayout, QWidget)

class Ui_ParticipantesPage(object):
    def setupUi(self, ParticipantesPage):
        if not ParticipantesPage.objectName():
            ParticipantesPage.setObjectName(u"ParticipantesPage")
        ParticipantesPage.resize(1000, 700)
        self.verticalLayout_main = QVBoxLayout(ParticipantesPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.lbl_titulo = QLabel(ParticipantesPage)
        self.lbl_titulo.setObjectName(u"lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.lbl_titulo)

        self.splitter = QSplitter(ParticipantesPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.panel_izquierdo = QFrame(self.splitter)
        self.panel_izquierdo.setObjectName(u"panel_izquierdo")
        self.panel_izquierdo.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_izq = QVBoxLayout(self.panel_izquierdo)
        self.verticalLayout_izq.setObjectName(u"verticalLayout_izq")
        self.label_nombre = QLabel(self.panel_izquierdo)
        self.label_nombre.setObjectName(u"label_nombre")

        self.verticalLayout_izq.addWidget(self.label_nombre)

        self.txt_nombre = QLineEdit(self.panel_izquierdo)
        self.txt_nombre.setObjectName(u"txt_nombre")

        self.verticalLayout_izq.addWidget(self.txt_nombre)

        self.label_fecha = QLabel(self.panel_izquierdo)
        self.label_fecha.setObjectName(u"label_fecha")

        self.verticalLayout_izq.addWidget(self.label_fecha)

        self.fecha = QDateEdit(self.panel_izquierdo)
        self.fecha.setObjectName(u"fecha")
        self.fecha.setCalendarPopup(True)

        self.verticalLayout_izq.addWidget(self.fecha)

        self.label_curso = QLabel(self.panel_izquierdo)
        self.label_curso.setObjectName(u"label_curso")

        self.verticalLayout_izq.addWidget(self.label_curso)

        self.combo_curso = QComboBox(self.panel_izquierdo)
        self.combo_curso.setObjectName(u"combo_curso")
        self.combo_curso.setEditable(True)

        self.verticalLayout_izq.addWidget(self.combo_curso)

        self.label_tipo = QLabel(self.panel_izquierdo)
        self.label_tipo.setObjectName(u"label_tipo")

        self.verticalLayout_izq.addWidget(self.label_tipo)

        self.rb_jugador = QRadioButton(self.panel_izquierdo)
        self.rb_jugador.setObjectName(u"rb_jugador")
        self.rb_jugador.setChecked(True)

        self.verticalLayout_izq.addWidget(self.rb_jugador)

        self.rb_arbitro = QRadioButton(self.panel_izquierdo)
        self.rb_arbitro.setObjectName(u"rb_arbitro")

        self.verticalLayout_izq.addWidget(self.rb_arbitro)

        self.rb_ambos = QRadioButton(self.panel_izquierdo)
        self.rb_ambos.setObjectName(u"rb_ambos")

        self.verticalLayout_izq.addWidget(self.rb_ambos)

        self.btn_continuar = QPushButton(self.panel_izquierdo)
        self.btn_continuar.setObjectName(u"btn_continuar")

        self.verticalLayout_izq.addWidget(self.btn_continuar)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_izq.addItem(self.verticalSpacer)

        self.splitter.addWidget(self.panel_izquierdo)
        self.panel_derecho = QFrame(self.splitter)
        self.panel_derecho.setObjectName(u"panel_derecho")
        self.panel_derecho.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_der = QVBoxLayout(self.panel_derecho)
        self.verticalLayout_der.setObjectName(u"verticalLayout_der")
        self.label_posicion = QLabel(self.panel_derecho)
        self.label_posicion.setObjectName(u"label_posicion")

        self.verticalLayout_der.addWidget(self.label_posicion)

        self.combo_posicion = QComboBox(self.panel_derecho)
        self.combo_posicion.setObjectName(u"combo_posicion")

        self.verticalLayout_der.addWidget(self.combo_posicion)

        self.label_lista = QLabel(self.panel_derecho)
        self.label_lista.setObjectName(u"label_lista")

        self.verticalLayout_der.addWidget(self.label_lista)

        self.lista_participantes = QListWidget(self.panel_derecho)
        self.lista_participantes.setObjectName(u"lista_participantes")

        self.verticalLayout_der.addWidget(self.lista_participantes)

        self.horizontalLayout_botones = QHBoxLayout()
        self.horizontalLayout_botones.setObjectName(u"horizontalLayout_botones")
        self.btn_volver = QPushButton(self.panel_derecho)
        self.btn_volver.setObjectName(u"btn_volver")

        self.horizontalLayout_botones.addWidget(self.btn_volver)

        self.btn_registrar = QPushButton(self.panel_derecho)
        self.btn_registrar.setObjectName(u"btn_registrar")

        self.horizontalLayout_botones.addWidget(self.btn_registrar)


        self.verticalLayout_der.addLayout(self.horizontalLayout_botones)

        self.splitter.addWidget(self.panel_derecho)

        self.verticalLayout_main.addWidget(self.splitter)


        self.retranslateUi(ParticipantesPage)

        QMetaObject.connectSlotsByName(ParticipantesPage)
    # setupUi

    def retranslateUi(self, ParticipantesPage):
        ParticipantesPage.setWindowTitle(QCoreApplication.translate("ParticipantesPage", u"Participantes", None))
        self.lbl_titulo.setText(QCoreApplication.translate("ParticipantesPage", u"Gesti\u00f3n de Participantes", None))
        self.label_nombre.setText(QCoreApplication.translate("ParticipantesPage", u"Nombre", None))
        self.label_fecha.setText(QCoreApplication.translate("ParticipantesPage", u"Fecha nacimiento", None))
        self.label_curso.setText(QCoreApplication.translate("ParticipantesPage", u"Curso", None))
        self.label_tipo.setText(QCoreApplication.translate("ParticipantesPage", u"Tipo", None))
        self.rb_jugador.setText(QCoreApplication.translate("ParticipantesPage", u"Jugador", None))
        self.rb_arbitro.setText(QCoreApplication.translate("ParticipantesPage", u"\u00c1rbitro", None))
        self.rb_ambos.setText(QCoreApplication.translate("ParticipantesPage", u"Ambos", None))
        self.btn_continuar.setText(QCoreApplication.translate("ParticipantesPage", u"Continuar", None))
        self.label_posicion.setText(QCoreApplication.translate("ParticipantesPage", u"Posici\u00f3n", None))
        self.label_lista.setText(QCoreApplication.translate("ParticipantesPage", u"Lista de Participantes", None))
        self.btn_volver.setText(QCoreApplication.translate("ParticipantesPage", u"Volver", None))
        self.btn_registrar.setText(QCoreApplication.translate("ParticipantesPage", u"Registrar", None))
    # retranslateUi

