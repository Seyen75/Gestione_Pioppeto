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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_FormDitta(object):
    def setupUi(self, FormDitta):
        if not FormDitta.objectName():
            FormDitta.setObjectName(u"FormDitta")
        FormDitta.resize(686, 280)
        FormDitta.setMinimumSize(QSize(686, 280))
        FormDitta.setMaximumSize(QSize(16777215, 16777215))
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
"    color: #8cbfa4; /* Verde salvia chiaro coordinato */\n"
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
"/* Evidenziazione del "
                        "campo quando l'utente ci clicca dentro */\n"
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
        self.groupBox.setGeometry(QRect(12, 12, 323, 181))
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(13, 28, 301, 111))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.spin_operaio_A = QSpinBox(self.formLayoutWidget)
        self.spin_operaio_A.setObjectName(u"spin_operaio_A")
        self.spin_operaio_A.setMaximumSize(QSize(75, 16777215))
        self.spin_operaio_A.setMaximum(200)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spin_operaio_A)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.spin_operaio_B = QSpinBox(self.formLayoutWidget)
        self.spin_operaio_B.setObjectName(u"spin_operaio_B")
        self.spin_operaio_B.setMaximumSize(QSize(75, 16777215))
        self.spin_operaio_B.setMaximum(200)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_operaio_B)

        self.spin_durata_piano = QSpinBox(self.formLayoutWidget)
        self.spin_durata_piano.setObjectName(u"spin_durata_piano")
        self.spin_durata_piano.setMaximumSize(QSize(75, 16777215))
        self.spin_durata_piano.setMinimum(1)
        self.spin_durata_piano.setMaximum(50)
        self.spin_durata_piano.setSingleStep(10)
        self.spin_durata_piano.setValue(10)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spin_durata_piano)

        self.label_9 = QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.groupBox_2 = QGroupBox(FormDitta)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(351, 12, 323, 256))
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
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

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.spin_motoseghe = QSpinBox(self.groupBox_2)
        self.spin_motoseghe.setObjectName(u"spin_motoseghe")
        self.spin_motoseghe.setMaximumSize(QSize(75, 16777215))

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spin_motoseghe)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)


        self.gridLayout_2.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.widget = QWidget(FormDitta)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 210, 321, 51))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.btn_salva = QPushButton(self.widget)
        self.btn_salva.setObjectName(u"btn_salva")

        self.horizontalLayout.addWidget(self.btn_salva)

        self.btn_esci = QPushButton(self.widget)
        self.btn_esci.setObjectName(u"btn_esci")

        self.horizontalLayout.addWidget(self.btn_esci)


        self.retranslateUi(FormDitta)

        QMetaObject.connectSlotsByName(FormDitta)
    # setupUi

    def retranslateUi(self, FormDitta):
        FormDitta.setWindowTitle(QCoreApplication.translate("FormDitta", u"Gestione dati ditta", None))
        self.groupBox.setTitle(QCoreApplication.translate("FormDitta", u"Gestione Personale", None))
        self.label_2.setText(QCoreApplication.translate("FormDitta", u"Personale specializzato", None))
        self.label.setText(QCoreApplication.translate("FormDitta", u"Personale non specializzato", None))
        self.spin_durata_piano.setSuffix(QCoreApplication.translate("FormDitta", u" anni", None))
        self.label_9.setText(QCoreApplication.translate("FormDitta", u"Durata massima simulazione", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FormDitta", u"Mezzi e Attrezzature Meccaniche", None))
        self.label_4.setText(QCoreApplication.translate("FormDitta", u"Trattori Media Potenza", None))
        self.label_5.setText(QCoreApplication.translate("FormDitta", u"Piattaforme Aeree", None))
        self.label_6.setText(QCoreApplication.translate("FormDitta", u"Abbattitrici (Harvester)", None))
        self.label_7.setText(QCoreApplication.translate("FormDitta", u"Caricatori (Forwarder)", None))
        self.label_8.setText(QCoreApplication.translate("FormDitta", u"Motoseghe professionali", None))
        self.label_3.setText(QCoreApplication.translate("FormDitta", u"Trattori Alta Potenza", None))
        self.btn_salva.setText(QCoreApplication.translate("FormDitta", u"Salva Ditta", None))
        self.btn_esci.setText(QCoreApplication.translate("FormDitta", u"Esci", None))
    # retranslateUi

