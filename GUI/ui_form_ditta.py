# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_ditta.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_FormDitta(object):
    def setupUi(self, FormDitta):
        if not FormDitta.objectName():
            FormDitta.setObjectName(u"FormDitta")
        FormDitta.resize(686, 450)
        FormDitta.setMinimumSize(QSize(686, 450))
        FormDitta.setMaximumSize(QSize(686, 450))
        FormDitta.setStyleSheet(u"/* Sfondo applicato SOLO alla finestra principale della form */\n"
"QWidget#FormDitta {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"                                      stop:0 #1e2622, stop:1 #121715);\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* Stile dei contenitori di gruppo */\n"
"QGroupBox {\n"
"    background-color: rgba(255, 255, 255, 0.04);\n"
"    border: 1px solid rgba(255, 255, 255, 0.12);\n"
"    border-radius: 8px;\n"
"    margin-top: 15px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Titoli dei GroupBox */\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 12px;\n"
"    color: #8cbfa4; /* Verde salvia chiaro */\n"
"    padding: 0 5px;\n"
"}\n"
"\n"
"/* Campi numerici di inserimento */\n"
"QSpinBox {\n"
"    background-color: #2a332f;\n"
"    border: 1px solid #44544c;\n"
"    border-radius: 4px;\n"
"    padding: 4px;\n"
"    color: #ffffff;\n"
"    min-width: 65px;\n"
"}\n"
"\n"
"/* Evidenziazione del campo quand"
                        "o l'utente ci clicca dentro */\n"
"QSpinBox:focus {\n"
"    border: 1px solid #8cbfa4;\n"
"    background-color: #313c37;\n"
"}\n"
"\n"
"/* Etichette di testo statiche dentro la form */\n"
"QLabel {\n"
"    color: #e0e0e0;\n"
"}\n"
"\n"
"/* Pulsante di salvataggio finale */\n"
"QPushButton {\n"
"    background-color: #347a50;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"/* Effetto al passaggio del mouse sul pulsante */\n"
"QPushButton:hover {\n"
"    background-color: #419663;\n"
"}\n"
"\n"
"/* Effetto al click sul pulsante */\n"
"QPushButton:pressed {\n"
"    background-color: #245939;\n"
"}")
        self.groupBox = QGroupBox(FormDitta)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(12, 12, 641, 109))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.spin_operaio_A = QSpinBox(self.groupBox)
        self.spin_operaio_A.setObjectName(u"spin_operaio_A")
        self.spin_operaio_A.setMaximumSize(QSize(75, 16777215))
        self.spin_operaio_A.setMinimum(1)
        self.spin_operaio_A.setMaximum(200)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spin_operaio_A)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.spin_operaio_B = QSpinBox(self.groupBox)
        self.spin_operaio_B.setObjectName(u"spin_operaio_B")
        self.spin_operaio_B.setMaximumSize(QSize(75, 16777215))
        self.spin_operaio_B.setMinimum(1)
        self.spin_operaio_B.setMaximum(200)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_operaio_B)


        self.horizontalLayout_2.addLayout(self.formLayout)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_3.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.spin_operaio_A_noleggio = QSpinBox(self.groupBox)
        self.spin_operaio_A_noleggio.setObjectName(u"spin_operaio_A_noleggio")
        self.spin_operaio_A_noleggio.setMaximumSize(QSize(75, 16777215))
        self.spin_operaio_A_noleggio.setMaximum(100)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spin_operaio_A_noleggio)

        self.spin_operaio_B_noleggio = QSpinBox(self.groupBox)
        self.spin_operaio_B_noleggio.setObjectName(u"spin_operaio_B_noleggio")
        self.spin_operaio_B_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_operaio_B_noleggio)


        self.horizontalLayout_2.addLayout(self.formLayout_3)

        self.groupBox_2 = QGroupBox(FormDitta)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 140, 641, 231))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.spin_trattori_alta = QSpinBox(self.groupBox_2)
        self.spin_trattori_alta.setObjectName(u"spin_trattori_alta")
        self.spin_trattori_alta.setMaximumSize(QSize(75, 16777215))
        self.spin_trattori_alta.setMaximum(100)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spin_trattori_alta)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.spin_trattori_media = QSpinBox(self.groupBox_2)
        self.spin_trattori_media.setObjectName(u"spin_trattori_media")
        self.spin_trattori_media.setMaximumSize(QSize(75, 16777215))
        self.spin_trattori_media.setMinimum(1)
        self.spin_trattori_media.setMaximum(100)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_trattori_media)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.spin_piattaforme = QSpinBox(self.groupBox_2)
        self.spin_piattaforme.setObjectName(u"spin_piattaforme")
        self.spin_piattaforme.setMaximumSize(QSize(75, 16777215))
        self.spin_piattaforme.setMaximum(100)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spin_piattaforme)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.spin_harvester = QSpinBox(self.groupBox_2)
        self.spin_harvester.setObjectName(u"spin_harvester")
        self.spin_harvester.setMaximumSize(QSize(75, 16777215))

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spin_harvester)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.spin_forwarder = QSpinBox(self.groupBox_2)
        self.spin_forwarder.setObjectName(u"spin_forwarder")
        self.spin_forwarder.setMaximumSize(QSize(75, 16777215))

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spin_forwarder)


        self.horizontalLayout_3.addLayout(self.formLayout_2)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.spin_trattori_alta_noleggio = QSpinBox(self.groupBox_2)
        self.spin_trattori_alta_noleggio.setObjectName(u"spin_trattori_alta_noleggio")
        self.spin_trattori_alta_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spin_trattori_alta_noleggio)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.spin_trattori_media_noleggio = QSpinBox(self.groupBox_2)
        self.spin_trattori_media_noleggio.setObjectName(u"spin_trattori_media_noleggio")
        self.spin_trattori_media_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_trattori_media_noleggio)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.spin_piattaforme_noleggio = QSpinBox(self.groupBox_2)
        self.spin_piattaforme_noleggio.setObjectName(u"spin_piattaforme_noleggio")
        self.spin_piattaforme_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spin_piattaforme_noleggio)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.spin_harvester_noleggio = QSpinBox(self.groupBox_2)
        self.spin_harvester_noleggio.setObjectName(u"spin_harvester_noleggio")
        self.spin_harvester_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spin_harvester_noleggio)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.spin_forwarder_noleggio = QSpinBox(self.groupBox_2)
        self.spin_forwarder_noleggio.setObjectName(u"spin_forwarder_noleggio")
        self.spin_forwarder_noleggio.setMaximumSize(QSize(75, 16777215))

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spin_forwarder_noleggio)


        self.horizontalLayout_3.addLayout(self.formLayout_4)

        self.layoutWidget = QWidget(FormDitta)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 380, 321, 51))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.btn_salva = QPushButton(self.layoutWidget)
        self.btn_salva.setObjectName(u"btn_salva")

        self.horizontalLayout.addWidget(self.btn_salva)

        self.btn_esci = QPushButton(self.layoutWidget)
        self.btn_esci.setObjectName(u"btn_esci")

        self.horizontalLayout.addWidget(self.btn_esci)

        self.spin_durata_piano = QSpinBox(FormDitta)
        self.spin_durata_piano.setObjectName(u"spin_durata_piano")
        self.spin_durata_piano.setGeometry(QRect(560, 390, 75, 28))
        self.spin_durata_piano.setMaximumSize(QSize(75, 16777215))
        self.spin_durata_piano.setMinimum(10)
        self.spin_durata_piano.setMaximum(50)
        self.spin_durata_piano.setSingleStep(10)
        self.spin_durata_piano.setValue(10)
        self.label_9 = QLabel(FormDitta)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(359, 390, 201, 28))

        self.retranslateUi(FormDitta)

        QMetaObject.connectSlotsByName(FormDitta)
    # setupUi

    def retranslateUi(self, FormDitta):
        FormDitta.setWindowTitle(QCoreApplication.translate("FormDitta", u"Gestione dati ditta", None))
        self.groupBox.setTitle(QCoreApplication.translate("FormDitta", u"Gestione Personale dipendente e stagionale", None))
        self.label_2.setText(QCoreApplication.translate("FormDitta", u"Personale specializzato", None))
        self.label.setText(QCoreApplication.translate("FormDitta", u"Personale generico", None))
        self.label_10.setText(QCoreApplication.translate("FormDitta", u"Massimo Personale Specializzato Stagionale", None))
        self.label_11.setText(QCoreApplication.translate("FormDitta", u"Massimo Personale Generico Stagionale", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FormDitta", u"Mezzi e Attrezzature Meccaniche di propriet\u00e0 e noleggiabili", None))
        self.label_3.setText(QCoreApplication.translate("FormDitta", u"Trattori Alta Potenza", None))
        self.label_4.setText(QCoreApplication.translate("FormDitta", u"Trattori Media Potenza", None))
        self.label_5.setText(QCoreApplication.translate("FormDitta", u"Piattaforme Aeree", None))
        self.label_6.setText(QCoreApplication.translate("FormDitta", u"Abbattitrici (Harvester)", None))
        self.label_7.setText(QCoreApplication.translate("FormDitta", u"Caricatori (Forwarder)", None))
        self.label_12.setText(QCoreApplication.translate("FormDitta", u"Trattori Alta Potenza Noleggiabili", None))
        self.label_13.setText(QCoreApplication.translate("FormDitta", u"Trattori Media Potenza Noleggiabili", None))
        self.label_14.setText(QCoreApplication.translate("FormDitta", u"Piattaforme Aeree Noleggiabili", None))
        self.label_15.setText(QCoreApplication.translate("FormDitta", u"Abbattitrici (Harvester) Noleggiabili", None))
        self.label_16.setText(QCoreApplication.translate("FormDitta", u"Caricatori (Forwarder) Noleggiabili", None))
        self.btn_salva.setText(QCoreApplication.translate("FormDitta", u"Salva Ditta", None))
        self.btn_esci.setText(QCoreApplication.translate("FormDitta", u"Esci", None))
        self.spin_durata_piano.setSuffix(QCoreApplication.translate("FormDitta", u" anni", None))
        self.label_9.setText(QCoreApplication.translate("FormDitta", u"Durata  simulazione automatica", None))
    # retranslateUi

