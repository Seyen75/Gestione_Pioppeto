# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pioppeto_main.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 768)
        MainWindow.setMinimumSize(QSize(1024, 768))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1000, 700))
        self.centralwidget.setStyleSheet(u"#centralwidget {\n"
"    border-image: url(:/sfondo_main.jpg) 0 0 0 0 stretch stretch;\n"
"}\n"
"\n"
"/* Stile elegante per tutti i pulsanti dell'interfaccia */\n"
"QPushButton {\n"
"background-color: rgba(26, 42, 58, 0.85); /* Blu scuro semi-trasparente */\n"
"    color: white;                             /* Testo bianco */\n"
"    border: 1px solid rgba(255, 255, 255, 0.2);\n"
"    border-radius: 10px;\n"
"    padding: 12px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Effetto quando si passa sopra con il mouse (Hover) */\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(\n"
"        x1: 0, y1: 0, \n"
"        x2: 0, y2: 1,\n"
"        stop: 0 rgba(215, 235, 255, 0.9),  /* Azzurro chiarissimo e cristallino in alto */\n"
"        stop: 1 rgba(175, 210, 245, 0.9)   /* Azzurro pastello leggermente pi\u00f9 profondo in basso */\n"
"    );\n"
"    border: 1px solid #0078d4;               /* Bordino azzurro istituzionale che definisce i contorni */\n"
"    color: #1a2a3a;\n"
"}\n"
"\n"
"/* Effetto"
                        " quando il pulsante viene cliccato */\n"
"QPushButton:pressed {\n"
"    background-color: rgba(230, 230, 230, 0.9);\n"
"}\n"
"\n"
"/* Stile specifico per il tasto Esci */\n"
"QPushButton#btn_esci, QPushButton[text=\"Esci\"] {\n"
"    background-color: rgba(217, 83, 79, 0.85);\n"
"    color: white;\n"
"    border: 1px solid rgba(217, 83, 79, 0.5);\n"
"}\n"
"\n"
"QPushButton#btn_esci:hover, QPushButton[text=\"Esci\"]:hover {\n"
"    background-color: rgba(217, 83, 79, 1.0);\n"
"}\n"
"\n"
"QLabel#label_titolo {\n"
"    font-family: \"Georgia\", \"Times New Roman\", serif; /* Un font elegante con le grazie come nella bozza */\n"
"    background: transparent;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* --- STATO DISABILITATO PER TUTTI I PULSANTI --- */\n"
"QPushButton:disabled {\n"
"    background-color: rgba(40, 50, 60, 0.4);   /* Grigio-blu molto scuro e quasi trasparente */\n"
"    color: rgba(255, 255, 255, 0.3);          /* Testo bianco fortemente opacizzato (spento) */\n"
"    border: 1px solid rgba(255, 255, 25"
                        "5, 0.1);/* Bordino quasi invisibile */\n"
"}\n"
"\n"
"/* IMPORTANTE: Disattiviamo l'effetto hover quando il tasto \u00e8 bloccato */\n"
"QPushButton:disabled:hover {\n"
"    background-color: rgba(40, 50, 60, 0.4);   /* Resta identico allo stato disabled */\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);/* Nessun cambio di bordo */\n"
"    color: rgba(255, 255, 255, 0.3);          /* Il testo non si illumina */\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #b0bec5;\n"
"    font-size: 10px;\n"
"    font-style: italic;\n"
"    padding: 5px;\n"
"}")
        self.btn_esci = QPushButton(self.centralwidget)
        self.btn_esci.setObjectName(u"btn_esci")
        self.btn_esci.setGeometry(QRect(860, 630, 120, 40))
        self.btn_esci.setMinimumSize(QSize(120, 40))
        self.btn_esci.setMaximumSize(QSize(120, 40))
        self.label_titolo = QLabel(self.centralwidget)
        self.label_titolo.setObjectName(u"label_titolo")
        self.label_titolo.setGeometry(QRect(37, 45, 931, 91))
        self.label_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 150, 951, 451))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_reset = QPushButton(self.layoutWidget)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setEnabled(True)
        icon = QIcon(QIcon.fromTheme(u"document-revert"))
        self.btn_reset.setIcon(icon)
        self.btn_reset.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_reset, 4, 3, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 3, 3, 1, 1)

        self.btn_gestione_lotti = QPushButton(self.layoutWidget)
        self.btn_gestione_lotti.setObjectName(u"btn_gestione_lotti")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_gestione_lotti.sizePolicy().hasHeightForWidth())
        self.btn_gestione_lotti.setSizePolicy(sizePolicy)
        icon1 = QIcon(QIcon.fromTheme(u"preferences-desktop-locale"))
        self.btn_gestione_lotti.setIcon(icon1)
        self.btn_gestione_lotti.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_gestione_lotti, 0, 1, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setWordWrap(True)

        self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 5, 3, 1, 1)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setWordWrap(True)

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.btn_valutazioni = QPushButton(self.layoutWidget)
        self.btn_valutazioni.setObjectName(u"btn_valutazioni")
        self.btn_valutazioni.setEnabled(False)
        icon2 = QIcon(QIcon.fromTheme(u"document-print"))
        self.btn_valutazioni.setIcon(icon2)
        self.btn_valutazioni.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_valutazioni, 4, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextFormat(Qt.TextFormat.RichText)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)

        self.btn_gestione_ditta = QPushButton(self.layoutWidget)
        self.btn_gestione_ditta.setObjectName(u"btn_gestione_ditta")
        sizePolicy.setHeightForWidth(self.btn_gestione_ditta.sizePolicy().hasHeightForWidth())
        self.btn_gestione_ditta.setSizePolicy(sizePolicy)
        icon3 = QIcon(QIcon.fromTheme(u"contact-new"))
        self.btn_gestione_ditta.setIcon(icon3)
        self.btn_gestione_ditta.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_gestione_ditta, 0, 0, 1, 1)

        self.btn_monitoraggio = QPushButton(self.layoutWidget)
        self.btn_monitoraggio.setObjectName(u"btn_monitoraggio")
        self.btn_monitoraggio.setEnabled(False)
        self.btn_monitoraggio.setIcon(icon2)
        self.btn_monitoraggio.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_monitoraggio, 4, 0, 1, 1)

        self.btn_simulazione = QPushButton(self.layoutWidget)
        self.btn_simulazione.setObjectName(u"btn_simulazione")
        self.btn_simulazione.setEnabled(False)
        icon4 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.btn_simulazione.setIcon(icon4)
        self.btn_simulazione.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.btn_simulazione, 0, 3, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_esci.setText(QCoreApplication.translate("MainWindow", u"Esci", None))
        self.label_titolo.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:36px; font-weight:700; color:#ffffff;\">Gestione Pioppicultura</span></p></body></html>", None))
        self.btn_reset.setText(QCoreApplication.translate("MainWindow", u"Reset Simulazione", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<b>Pannello Gestione Aziendale:</b><br>\n"
"Consente di strutturare le squadre e inventariare i mezzi meccanici reali della ditta.<br><br>\n"
"\u2022 Operai Specializzati (Grado A)<br>\n"
"\u2022 Manovali Comuni (Grado B)<br>\n"
"\u2022 Flotta: Trattori, Piattaforme, Harvester<br><br>\n"
"<i>I dati inseriti determineranno la capacit\u00e0 oraria operativa e i colli di bottiglia nei cantieri stagionali.</i>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<b>Motore del Tempo:</b><br>\n"
"Consolida i dati di input e avvia l'algoritmo di calcolo stocastico su base trimestrale.<br><br>\n"
"\u2022 Avanzamento per stagioni biologiche<br>\n"
"\u2022 Esecuzione cantieri e consumo ore<br>\n"
"\u2022 Chiusura automatica a ciclo concluso<br><br>\n"
"<i>La simulazione termina quando tutti i lotti raggiungono la maturit\u00e0 e vengono abbattuti.</i>", None))
        self.btn_gestione_lotti.setText(QCoreApplication.translate("MainWindow", u"Gestione e Creazione Lotti", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<b>Bilancio Consuntivo:</b><br>\n"
"Analisi e revisione scientifica dei risultati economici e forestali ottenuti a fine ciclo.<br><br>\n"
"\u2022 Cubature raccolte (m\u00b3) e Masse in fibra (t)<br>\n"
"\u2022 Confronto rese ettariali tra singoli lotti<br>\n"
"\u2022 Efficienza e saturazione del capitale meccanico<br><br>\n"
"<i>Fornisce la diagnostica finale sui colli di bottiglia e sui fallimenti colturali della ditta.</i>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<b>Reset Simulazione</b><br>\n"
"Viene cancellato ogni dato precedentemente inserito per permettere l'inserimento dei parametri di una nuova ditta e lotti<br><br>\n"
"\n"
"", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<b>Analisi Dinamica:</b><br>\n"
"Visualizzazione grafica in tempo reale dell'avanzamento dei cicli in campo.<br><br>\n"
"\u2022 Accrescimento dendrometrico (D_bh / H)<br>\n"
"\u2022 Saturazione dei serbatoi d'ore ditta<br>\n"
"\u2022 Insorgenza di stress idrici e anomalie<br><br>\n"
"<i>Permette di valutare visivamente la reattivit\u00e0 del sistema durante il loop temporale.</i>", None))
        self.btn_valutazioni.setText(QCoreApplication.translate("MainWindow", u"Report Finale e Statistiche Consuntive", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<b>Pannello Controllo Pioppeto:</b><br>\n"
"Consente la creazione e la pianificazione selvicolturale dei lotti a partire dall'Anno 0.<br><br>\n"
"\u2022 Parametrizzazione Cloni Padani<br>\n"
"\u2022 Vulnerabilit\u00e0 idrica e Attrito logistico<br>\n"
"\u2022 Indirizzo produttivo (Opera / Industria)<br><br>\n"
"<i>Dispone di un sistema a regole integrato per la verifica in tempo reale della coerenza colturale.</i>", None))
        self.btn_gestione_ditta.setText(QCoreApplication.translate("MainWindow", u"Configurazione Ditta Forestale", None))
        self.btn_monitoraggio.setText(QCoreApplication.translate("MainWindow", u"Monitoraggio Grafico Real-Time", None))
        self.btn_simulazione.setText(QCoreApplication.translate("MainWindow", u"Avvia Simulazione", None))
    # retranslateUi

