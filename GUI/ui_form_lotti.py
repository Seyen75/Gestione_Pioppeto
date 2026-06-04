# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_lotti.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTableWidget, QTableWidgetItem, QWidget)

class Ui_FormLotti(object):
    def setupUi(self, FormLotti):
        if not FormLotti.objectName():
            FormLotti.setObjectName(u"FormLotti")
        FormLotti.resize(647, 721)
        FormLotti.setMinimumSize(QSize(647, 720))
        FormLotti.setMaximumSize(QSize(647, 721))
        FormLotti.setStyleSheet(u"/* Sfondo applicato SOLO alla finestra principale della form */\n"
"QWidget#FormLotti {\n"
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
"    padding: 4px\n"
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
"}\n"
"\n"
"QTableWidget {\n"
"                    background-color: #1e2422;      /* Sfondo delle celle leggermente pi\u00f9 chiaro dello sfondo app */\n"
"                    gridline-color: #3a4743;          /* Il colore dei quadretti di separazione */\n"
"                    color: #ffffff;      "
                        "            /* Colore del testo delle celle */\n"
"                    font-size: 13px;\n"
"                    border: 1px solid #3a4743;\n"
"                }\n"
"                \n"
"                /* Stile dei titoli delle colonne in alto */\n"
"                QHeaderView::section {\n"
"                    background-color: #2d3835;       /* Sfondo dei titoli */\n"
"                    color: #a3b8b0;                  /* Testo dei titoli (verde oliva chiaro/grigio) */\n"
"                    padding: 6px;\n"
"                    font-weight: bold;\n"
"                    border: 1px solid #3a4743;       /* Confine dei titoli per allinearsi alla griglia */\n"
"                }\n"
"                \n"
"                /* Stile quando l'utente seleziona una riga */\n"
"                QTableWidget::item:selected {\n"
"                    background-color: #2e6b4e;       /* Colore verde foresta per la riga selezionata */\n"
"                    color: #ffffff;                  /* Testo bianco sulla selezion"
                        "e */\n"
"                }\n"
"")
        self.groupBox = QGroupBox(FormLotti)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 301, 241))
        self.groupBox.setFlat(False)
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 30, 271, 200))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.txt_id_lotto = QLineEdit(self.formLayoutWidget)
        self.txt_id_lotto.setObjectName(u"txt_id_lotto")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_id_lotto.sizePolicy().hasHeightForWidth())
        self.txt_id_lotto.setSizePolicy(sizePolicy)
        self.txt_id_lotto.setMinimumSize(QSize(135, 28))
        self.txt_id_lotto.setMaximumSize(QSize(135, 16777215))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txt_id_lotto)

        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.combo_destinazione = QComboBox(self.formLayoutWidget)
        self.combo_destinazione.setObjectName(u"combo_destinazione")
        self.combo_destinazione.setMinimumSize(QSize(145, 28))
        self.combo_destinazione.setMaximumSize(QSize(145, 16777215))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.combo_destinazione)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.spin_ettari = QDoubleSpinBox(self.formLayoutWidget)
        self.spin_ettari.setObjectName(u"spin_ettari")
        self.spin_ettari.setMinimumSize(QSize(90, 28))
        self.spin_ettari.setMaximumSize(QSize(90, 16777215))
        self.spin_ettari.setMinimum(1.000000000000000)
        self.spin_ettari.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spin_ettari)

        self.spin_eta_iniziale = QSpinBox(self.formLayoutWidget)
        self.spin_eta_iniziale.setObjectName(u"spin_eta_iniziale")
        self.spin_eta_iniziale.setMinimumSize(QSize(75, 0))
        self.spin_eta_iniziale.setMaximumSize(QSize(90, 16777215))
        self.spin_eta_iniziale.setMaximum(15)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spin_eta_iniziale)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.table_lotti = QTableWidget(FormLotti)
        if (self.table_lotti.columnCount() < 6):
            self.table_lotti.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_lotti.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_lotti.setObjectName(u"table_lotti")
        self.table_lotti.setGeometry(QRect(20, 330, 611, 371))
        self.table_lotti.setFrameShadow(QFrame.Shadow.Raised)
        self.table_lotti.setShowGrid(True)
        self.horizontalLayoutWidget = QWidget(FormLotti)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 260, 621, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.btn_azione_lotto = QPushButton(self.horizontalLayoutWidget)
        self.btn_azione_lotto.setObjectName(u"btn_azione_lotto")

        self.horizontalLayout.addWidget(self.btn_azione_lotto)

        self.btn_elimina_lotto = QPushButton(self.horizontalLayoutWidget)
        self.btn_elimina_lotto.setObjectName(u"btn_elimina_lotto")

        self.horizontalLayout.addWidget(self.btn_elimina_lotto)

        self.btn_randomizza = QPushButton(self.horizontalLayoutWidget)
        self.btn_randomizza.setObjectName(u"btn_randomizza")

        self.horizontalLayout.addWidget(self.btn_randomizza)

        self.btn_esci = QPushButton(self.horizontalLayoutWidget)
        self.btn_esci.setObjectName(u"btn_esci")

        self.horizontalLayout.addWidget(self.btn_esci)

        self.groupBox_2 = QGroupBox(FormLotti)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(330, 10, 301, 241))
        self.formLayoutWidget_2 = QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(9, 29, 281, 140))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.combo_clone = QComboBox(self.formLayoutWidget_2)
        self.combo_clone.setObjectName(u"combo_clone")
        self.combo_clone.setMinimumSize(QSize(140, 0))
        self.combo_clone.setMaximumSize(QSize(140, 16777215))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.combo_clone)

        self.label_5 = QLabel(self.formLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.combo_sesto_impianto = QComboBox(self.formLayoutWidget_2)
        self.combo_sesto_impianto.setObjectName(u"combo_sesto_impianto")
        self.combo_sesto_impianto.setMinimumSize(QSize(141, 0))
        self.combo_sesto_impianto.setMaximumSize(QSize(140, 16777215))

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.combo_sesto_impianto)

        self.label_7 = QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.spin_attrito = QSpinBox(self.formLayoutWidget_2)
        self.spin_attrito.setObjectName(u"spin_attrito")
        self.spin_attrito.setMaximumSize(QSize(90, 90))
        self.spin_attrito.setMaximum(10)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spin_attrito)

        self.label_6 = QLabel(self.formLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.spin_test_idrico = QDoubleSpinBox(self.formLayoutWidget_2)
        self.spin_test_idrico.setObjectName(u"spin_test_idrico")
        self.spin_test_idrico.setMinimumSize(QSize(90, 28))
        self.spin_test_idrico.setMaximumSize(QSize(90, 16777215))
        self.spin_test_idrico.setMinimum(-1.000000000000000)
        self.spin_test_idrico.setMaximum(1.000000000000000)
        self.spin_test_idrico.setSingleStep(0.100000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spin_test_idrico)

        self.lbl_avviso_clone = QLabel(self.groupBox_2)
        self.lbl_avviso_clone.setObjectName(u"lbl_avviso_clone")
        self.lbl_avviso_clone.setGeometry(QRect(10, 180, 271, 51))
        self.lbl_avviso_clone.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignTop)
        self.lbl_avviso_clone.setWordWrap(True)

        self.retranslateUi(FormLotti)

        QMetaObject.connectSlotsByName(FormLotti)
    # setupUi

    def retranslateUi(self, FormLotti):
        FormLotti.setWindowTitle(QCoreApplication.translate("FormLotti", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("FormLotti", u"Dati Lotto", None))
        self.label.setText(QCoreApplication.translate("FormLotti", u"ID Lotto", None))
        self.label_8.setText(QCoreApplication.translate("FormLotti", u"Tipologia Lotto", None))
        self.label_2.setText(QCoreApplication.translate("FormLotti", u"Estensione lotto", None))
        self.spin_ettari.setSuffix(QCoreApplication.translate("FormLotti", u" ha", None))
        self.spin_eta_iniziale.setSuffix(QCoreApplication.translate("FormLotti", u" anni", None))
        self.label_3.setText(QCoreApplication.translate("FormLotti", u"Et\u00e0 lotto", None))
        ___qtablewidgetitem = self.table_lotti.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FormLotti", u"ID Lotto", None))
        ___qtablewidgetitem1 = self.table_lotti.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FormLotti", u"Superficie", None))
        ___qtablewidgetitem2 = self.table_lotti.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FormLotti", u"Clone", None))
        ___qtablewidgetitem3 = self.table_lotti.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FormLotti", u"Sesto d'impianto", None))
        ___qtablewidgetitem4 = self.table_lotti.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FormLotti", u"Et\u00e0 Lotto", None))
        ___qtablewidgetitem5 = self.table_lotti.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FormLotti", u"Destinazione d'Uso", None))
        self.btn_azione_lotto.setText(QCoreApplication.translate("FormLotti", u"Aggiungi Lotto", None))
        self.btn_elimina_lotto.setText(QCoreApplication.translate("FormLotti", u"Svuota Lotto", None))
        self.btn_randomizza.setText(QCoreApplication.translate("FormLotti", u"Genera Lotto Random", None))
        self.btn_esci.setText(QCoreApplication.translate("FormLotti", u"Esci", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FormLotti", u"Dati Tipologia Impianto", None))
        self.label_4.setText(QCoreApplication.translate("FormLotti", u"Clone", None))
        self.label_5.setText(QCoreApplication.translate("FormLotti", u"Sesto d'impianto", None))
        self.label_7.setText(QCoreApplication.translate("FormLotti", u"Attrito spaziale", None))
        self.label_6.setText(QCoreApplication.translate("FormLotti", u"Stress idrico", None))
        self.lbl_avviso_clone.setText("")
    # retranslateUi

