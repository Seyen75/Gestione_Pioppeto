# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_monitoraggio.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_form_monitoraggio(object):
    def setupUi(self, form_monitoraggio):
        if not form_monitoraggio.objectName():
            form_monitoraggio.setObjectName(u"form_monitoraggio")
        form_monitoraggio.resize(1100, 900)
        form_monitoraggio.setMinimumSize(QSize(1100, 900))
        form_monitoraggio.setMaximumSize(QSize(1100, 900))
        form_monitoraggio.setStyleSheet(u"/* Sfondo applicato SOLO alla finestra principale della form (Blu Notte Profondo) */\n"
"QWidget#form_monitoraggio {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
"                                      stop:0 #141923, stop:1 #0c0f15);\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* Stile dei contenitori di gruppo */\n"
"QGroupBox {\n"
"    background-color: rgba(255, 255, 255, 0.03);\n"
"    border: 1px solid rgba(255, 255, 255, 0.10);\n"
"    border-radius: 8px;\n"
"    margin-top: 15px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Titoli dei GroupBox (Azzurro Ciano Tecnologico) */\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 12px;\n"
"    color: #4fc3f7; /* Azzurro luminoso per staccare dal verde delle altre form */\n"
"    padding: 0 5px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #a0aec0; /* Grigio chiaro neutro per le label di descrizione */\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"/* FORZATURA STRUTTURALE: Stile specifico per "
                        "la Label dell'Anno */\n"
"QGroupBox QLabel#lbl_anno, QLabel#lbl_anno {\n"
"    color: #ffffff !important;          /* Bianco puro per massima leggibilit\u00e0 */\n"
"    font-size: 22px !important;         /* Molto grande */\n"
"    font-weight: bold !important;       /* Grassetto marcato */\n"
"    font-family: \"Courier New\", monospace !important; \n"
"}\n"
"\n"
"/* FORZATURA STRUTTURALE: Stile specifico per la Label della Stagione */\n"
"QGroupBox QLabel#lbl_stagione, QLabel#lbl_stagione {\n"
"    color: #00e5ff !important;          /* Azzurro Ciano Neon ad alta visibilit\u00e0 */\n"
"    font-size: 18px !important;         /* Evidente */\n"
"    font-weight: bold !important;       /* Grassetto */\n"
"    font-family: \"Courier New\", monospace !important;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"/* Pulsante Standard / Avanzamento Temporale (Azzurro di Comando) */\n"
"QPushButton {\n"
"    background-color: #0288d1;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    font-weigh"
                        "t: bold;\n"
"    min-height: 30px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #039be5;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #01579b;\n"
"}\n"
"\n"
"/* Variante per il Pulsante di Chiusura/Termina Sessione (Rosso Corallo) */\n"
"/* Nota: applicheremo questo objectName specifico nel Designer al tasto di interruzione */\n"
"QPushButton#btn_termina_sessione {\n"
"    background-color: #d32f2f;\n"
"}\n"
"\n"
"QPushButton#btn_termina_sessione:hover {\n"
"    background-color: #f44336;\n"
"}\n"
"\n"
"QPushButton#btn_termina_sessione:pressed {\n"
"    background-color: #b71c1c;\n"
"}\n"
"\n"
"/* Stile della Tabella Monitoraggio Lotti */\n"
"QTableWidget {\n"
"    background-color: #171e2c;       /* Sfondo celle coordinato col blu notte */\n"
"    gridline-color: #2b364a;         /* Quadretti di separazione blu scuro */\n"
"    color: #ffffff;\n"
"    font-size: 13px;\n"
"    border: 1px solid #2b364a;\n"
"}\n"
"\n"
"/* Stile dei titoli delle colonn"
                        "e in alto */\n"
"QHeaderView::section {\n"
"    background-color: #222c3e;       /* Sfondo dei titoli di colonna */\n"
"    color: #8ab4f8;                  /* Testo dei titoli in azzurro soft */\n"
"    padding: 6px;\n"
"    font-weight: bold;\n"
"    border: 1px solid #2b364a;\n"
"}\n"
"\n"
"/* Stile della riga selezionata (Evidenziazione Blu Cobalto) */\n"
"QTableWidget::item:selected {\n"
"    background-color: #1a5ab5;       \n"
"    color: #ffffff;\n"
"}")
        self.grp_controllo_tempo = QGroupBox(form_monitoraggio)
        self.grp_controllo_tempo.setObjectName(u"grp_controllo_tempo")
        self.grp_controllo_tempo.setGeometry(QRect(20, 10, 397, 122))
        self.gridLayout = QGridLayout(self.grp_controllo_tempo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbl_anno = QLabel(self.grp_controllo_tempo)
        self.lbl_anno.setObjectName(u"lbl_anno")

        self.gridLayout.addWidget(self.lbl_anno, 0, 0, 1, 1)

        self.lbl_stagione = QLabel(self.grp_controllo_tempo)
        self.lbl_stagione.setObjectName(u"lbl_stagione")

        self.gridLayout.addWidget(self.lbl_stagione, 0, 1, 1, 2)

        self.btn_prossimo_trimestre = QPushButton(self.grp_controllo_tempo)
        self.btn_prossimo_trimestre.setObjectName(u"btn_prossimo_trimestre")

        self.gridLayout.addWidget(self.btn_prossimo_trimestre, 1, 0, 1, 2)

        self.btn_termina_sessione = QPushButton(self.grp_controllo_tempo)
        self.btn_termina_sessione.setObjectName(u"btn_termina_sessione")

        self.gridLayout.addWidget(self.btn_termina_sessione, 1, 2, 1, 1)

        self.grp_risorse = QGroupBox(form_monitoraggio)
        self.grp_risorse.setObjectName(u"grp_risorse")
        self.grp_risorse.setGeometry(QRect(20, 140, 491, 381))
        self.verticalLayout = QVBoxLayout(self.grp_risorse)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.canvas_risorse = QWidget(self.grp_risorse)
        self.canvas_risorse.setObjectName(u"canvas_risorse")

        self.verticalLayout.addWidget(self.canvas_risorse)

        self.grp_rese = QGroupBox(form_monitoraggio)
        self.grp_rese.setObjectName(u"grp_rese")
        self.grp_rese.setGeometry(QRect(520, 140, 551, 381))
        self.verticalLayout_2 = QVBoxLayout(self.grp_rese)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.canvas_rese = QWidget(self.grp_rese)
        self.canvas_rese.setObjectName(u"canvas_rese")

        self.verticalLayout_2.addWidget(self.canvas_rese)

        self.tbl_monitoraggio = QTableWidget(form_monitoraggio)
        if (self.tbl_monitoraggio.columnCount() < 8):
            self.tbl_monitoraggio.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbl_monitoraggio.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tbl_monitoraggio.setObjectName(u"tbl_monitoraggio")
        self.tbl_monitoraggio.setGeometry(QRect(20, 540, 1051, 341))
        self.tbl_monitoraggio.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_monitoraggio.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl_monitoraggio.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.groupBox = QGroupBox(form_monitoraggio)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(430, 10, 641, 121))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lbl_tagli_saltati = QLabel(self.groupBox)
        self.lbl_tagli_saltati.setObjectName(u"lbl_tagli_saltati")
        self.lbl_tagli_saltati.setMinimumSize(QSize(500, 0))
        self.lbl_tagli_saltati.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_3.addWidget(self.lbl_tagli_saltati)

        self.lbl_turni_saltati = QLabel(self.groupBox)
        self.lbl_turni_saltati.setObjectName(u"lbl_turni_saltati")
        self.lbl_turni_saltati.setMinimumSize(QSize(500, 0))
        self.lbl_turni_saltati.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_3.addWidget(self.lbl_turni_saltati)

        self.lbl_lavori_saltati = QLabel(self.groupBox)
        self.lbl_lavori_saltati.setObjectName(u"lbl_lavori_saltati")
        self.lbl_lavori_saltati.setMinimumSize(QSize(500, 0))
        self.lbl_lavori_saltati.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_3.addWidget(self.lbl_lavori_saltati)


        self.retranslateUi(form_monitoraggio)

        QMetaObject.connectSlotsByName(form_monitoraggio)
    # setupUi

    def retranslateUi(self, form_monitoraggio):
        form_monitoraggio.setWindowTitle(QCoreApplication.translate("form_monitoraggio", u"Form", None))
        self.grp_controllo_tempo.setTitle(QCoreApplication.translate("form_monitoraggio", u"\U0001f4ca Stato Avanzamento Simulazione", None))
        self.lbl_anno.setText(QCoreApplication.translate("form_monitoraggio", u"Anno 1", None))
        self.lbl_stagione.setText(QCoreApplication.translate("form_monitoraggio", u"STAGIONE: INVERNO", None))
        self.btn_prossimo_trimestre.setText(QCoreApplication.translate("form_monitoraggio", u"Avanza Stagione \u27a1\ufe0f", None))
        self.btn_termina_sessione.setText(QCoreApplication.translate("form_monitoraggio", u"Termina e Genera Report \u23f9\ufe0f", None))
        self.grp_risorse.setTitle(QCoreApplication.translate("form_monitoraggio", u"\U0001f4ca Saturazione Capacit\U000000e0 Operativa Ditta", None))
        self.grp_rese.setTitle(QCoreApplication.translate("form_monitoraggio", u"\U0001f4c8 Progressione Rese Commerciali Cumulate", None))
        ___qtablewidgetitem = self.tbl_monitoraggio.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("form_monitoraggio", u"ID Particella", None))
        ___qtablewidgetitem1 = self.tbl_monitoraggio.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("form_monitoraggio", u"N\u00b0 Piante", None))
        ___qtablewidgetitem2 = self.tbl_monitoraggio.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("form_monitoraggio", u"Superficie", None))
        ___qtablewidgetitem3 = self.tbl_monitoraggio.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("form_monitoraggio", u"Destinazione d'Uso", None))
        ___qtablewidgetitem4 = self.tbl_monitoraggio.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("form_monitoraggio", u"Et\u00e0 Biologica", None))
        ___qtablewidgetitem5 = self.tbl_monitoraggio.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("form_monitoraggio", u"Diametro Medio", None))
        ___qtablewidgetitem6 = self.tbl_monitoraggio.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("form_monitoraggio", u"Altezza Stimata", None))
        ___qtablewidgetitem7 = self.tbl_monitoraggio.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("form_monitoraggio", u"Stato Cantiere", None))
        self.groupBox.setTitle(QCoreApplication.translate("form_monitoraggio", u"\U0001f4ca Rese totali per annualit\U000000e0", None))
        self.lbl_tagli_saltati.setText(QCoreApplication.translate("form_monitoraggio", u"\u26d4 Tagli Saltati (Carenza Mezzi):", None))
        self.lbl_turni_saltati.setText(QCoreApplication.translate("form_monitoraggio", u"\u23f3 Tagli Rinviati (Immaturit\u00e0 Biologica):", None))
        self.lbl_lavori_saltati.setText(QCoreApplication.translate("form_monitoraggio", u"\u26a0\ufe0f Lavorazioni Generiche Fallite:", None))
    # retranslateUi

