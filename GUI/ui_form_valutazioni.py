# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_valutazioni.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_FormValutazioni(object):
    def setupUi(self, FormValutazioni):
        if not FormValutazioni.objectName():
            FormValutazioni.setObjectName(u"FormValutazioni")
        FormValutazioni.resize(1150, 780)
        FormValutazioni.setMinimumSize(QSize(1150, 780))
        FormValutazioni.setMaximumSize(QSize(1150, 780))
        FormValutazioni.setStyleSheet(u"/* SFONDO DELLA FINESTRA E DEI PANNELLI (Nuovo tono caldo armonizzato) */\n"
"\n"
"QWidget#FormValutazioni, QTabWidget::pane {\n"
"    background-color: #1a1516;  /* Antracite */\n"
"}\n"
"\n"
"/* STILE RADICALE DELLE LINGUETTE (Ancoraggio forzato a sinistra) */\n"
"QTabWidget::tab-bar {\n"
"    left: 0px;\n"
"}\n"
"\n"
"QTabBar {\n"
"    alignment: left;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a1f21, stop:1 #1f1618);\n"
"    color: #b0a2a4; /* Grigio-rosa morbido per il testo inattivo */\n"
"    border: 1px solid #3d292c;\n"
"    border-bottom: none;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"    padding: 8px 20px; \n"
"    font-weight: bold;\n"
"    font-size: 11px;\n"
"    \n"
"    /* Usiamo width fisso anzich\u00e9 min-width per impedire a Qt qualsiasi ricalcolo */\n"
"    width: 200px; \n"
"}\n"
"\n"
"/* Tab Attivo (Selezionato) */\n"
"QTabBar::tab:selected {\n"
"    background: "
                        "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8a1c24, stop:1 #4f0e13);\n"
"    color: #ffffff;\n"
"    border: 1px solid #a8222d;\n"
"    border-bottom: 1px solid #1a1516; /* Si fonde con il nuovo sfondo caldo */\n"
"}\n"
"\n"
"QTabBar::tab:hover:!selected {\n"
"    background: #362528;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* =========================================================================\n"
"   ETICHETTE TESTUALI (QLabel - Tutto in Rosso Corallo Chiaro)\n"
"   ========================================================================= */\n"
"#FormValutazioni QLabel, \n"
"QGroupBox QLabel, \n"
"QTabWidget QLabel, \n"
"QLabel {\n"
"    color: #ff8a80 !important;\n"
"    font-size: 11px;\n"
"    font-weight: normal;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lbl_anno_selezionato,\n"
"QLabel#lbl_anno_selezionato_2,\n"
"QLabel#lbl_titolo_lotto, \n"
"QGroupBox {\n"
"    font-weight: bold !important;\n"
"    font-size: 11px !important;\n"
"}\n"
"\n"
"/* ---Label interne al GroupBox Rese Total"
                        "i --- */\n"
"QLabel#lbl_tot_3,\n"
"QLabel#lbl_tot_4,\n"
"QLabel#lbl_tot_5,\n"
"QLabel#lbl_tot_6,\n"
"QLabel#lbl_tot_7,\n"
"QLabel#lbl_tot_8,\n"
"QLabel#lbl_tot_9 {\n"
"    font-size: 13px;\n"
"    color: #ffecb3\n"
"}\n"
"\n"
"QGroupBox#GroupBoxReseTotali {\n"
"	color: #ff8a80 !important;\n"
"    font-size: 16px;\n"
"    font-weight: normal;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lbl_tipo_filiera_lotto {\n"
"    color: #ffca28 !important;         /* Un bellissimo Giallo Ambra/Oro luminoso */\n"
"    font-size: 16px !important;        /* Dimensione maggiorata per dominare la tabella */\n"
"    font-weight: bold !important;      /* Grassetto marcato */\n"
"    font-family: \"Georgia\", serif;     /* Font elegante coerente con il titolo main */\n"
"    padding-top: 10px;                 /* Distanza dal selettore sopra */\n"
"    padding-bottom: 5px;               /* Distanza dalla tabella sotto */\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* =================================================="
                        "=======================\n"
"   TABELLE (QTableWidget) - Sintonizzate sui toni caldi\n"
"   ========================================================================= */\n"
"QTableWidget {\n"
"    background-color: #151011; /* Celle scure calde */\n"
"    gridline-color: #2b1d20;\n"
"    color: #ffffff;\n"
"    border: 1px solid #3d2429;\n"
"    border-radius: 6px;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #5a151a;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d181b, stop:1 #1f1012);\n"
"    color: #ff8a80;\n"
"    padding: 6px;\n"
"    border: 1px solid #3d2429;\n"
"    font-weight: bold;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"/* =========================================================================\n"
"   PULSANTI GENERALI E DI USCITA\n"
"   ========================================================================"
                        "= */\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d1820, stop:1 #420f13);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"    min-height: 30px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9a2630, stop:1 #5e161b);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5e161b, stop:1 #2a0a0c);\n"
"}\n"
"\n"
"/* =========================================================================\n"
"   GROUPBOX INFORMATIVI\n"
"   ========================================================================= */\n"
"QGroupBox {\n"
"    border: 1px solid #4a282d;\n"
"    border-radius: 6px;\n"
"    margin-top: 15px;\n"
"    background-color: #1c1415;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 5px;\n"
"    left: 10px;\n"
"}\n"
""
                        "\n"
"QComboBox { \n"
"                    background-color: #2d181b; \n"
"                    color: #ffffff; \n"
"                    border: 1px solid #3d2429; \n"
"                    border-radius: 4px; \n"
"                    padding: 4px 10px;\n"
"                }\n"
"                QComboBox::drop-down {\n"
"                    subcontrol-origin: padding;\n"
"                    subcontrol-position: top right;\n"
"                    width: 20px;\n"
"                    border-left-width: 1px;\n"
"                    border-left-color: #3d2429;\n"
"                    border-left-style: solid;\n"
"                }\n"
"                QComboBox QAbstractItemView {\n"
"                    background-color: #151011;\n"
"                    color: #ffffff;\n"
"                    selection-background-color: #5a151a;\n"
"                    border: 1px solid #3d2429;\n"
"                }\n"
" \n"
"QSlider::groove:horizontal { \n"
"                    background: #2d181b; \n"
"                    height:"
                        " 6px; \n"
"                    border-radius: 3px; \n"
"                } \n"
"                QSlider::handle:horizontal { \n"
"                    background: #ff8a80; \n"
"                    width: 14px; \n"
"                    margin: -4px 0; \n"
"                    border-radius: 7px; \n"
"                }")
        self.verticalLayout_6 = QVBoxLayout(FormValutazioni)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(20, 20, 20, 20)
        self.tab_valutazioni_root = QTabWidget(FormValutazioni)
        self.tab_valutazioni_root.setObjectName(u"tab_valutazioni_root")
        self.tab_valutazioni_root.setMaximumSize(QSize(1100, 700))
        self.tab_valutazioni_root.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tab_valutazioni_root.setAutoFillBackground(False)
        self.tab_valutazioni_root.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_valutazioni_root.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_valutazioni_root.setElideMode(Qt.TextElideMode.ElideNone)
        self.tab_valutazioni_root.setUsesScrollButtons(True)
        self.tab_valutazioni_root.setDocumentMode(False)
        self.tab_valutazioni_root.setTabsClosable(False)
        self.tab_consuntivo_annuale = QWidget()
        self.tab_consuntivo_annuale.setObjectName(u"tab_consuntivo_annuale")
        self.verticalLayout_2 = QVBoxLayout(self.tab_consuntivo_annuale)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbl_anno_selezionato = QLabel(self.tab_consuntivo_annuale)
        self.lbl_anno_selezionato.setObjectName(u"lbl_anno_selezionato")
        self.lbl_anno_selezionato.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_3.addWidget(self.lbl_anno_selezionato)

        self.cmb_anno_report = QComboBox(self.tab_consuntivo_annuale)
        self.cmb_anno_report.setObjectName(u"cmb_anno_report")
        self.cmb_anno_report.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_3.addWidget(self.cmb_anno_report)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.tbl_tagli_anno = QTableWidget(self.tab_consuntivo_annuale)
        if (self.tbl_tagli_anno.columnCount() < 10):
            self.tbl_tagli_anno.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tbl_tagli_anno.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.tbl_tagli_anno.setObjectName(u"tbl_tagli_anno")
        self.tbl_tagli_anno.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.tbl_tagli_anno)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.GroupBoxReseTotali = QGroupBox(self.tab_consuntivo_annuale)
        self.GroupBoxReseTotali.setObjectName(u"GroupBoxReseTotali")
        self.GroupBoxReseTotali.setMinimumSize(QSize(0, 150))
        self.GroupBoxReseTotali.setMaximumSize(QSize(500, 300))
        self.verticalLayout_5 = QVBoxLayout(self.GroupBoxReseTotali)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lbl_tot_3 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_3.setObjectName(u"lbl_tot_3")

        self.verticalLayout_5.addWidget(self.lbl_tot_3)

        self.lbl_tot_4 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_4.setObjectName(u"lbl_tot_4")

        self.verticalLayout_5.addWidget(self.lbl_tot_4)

        self.lbl_tot_5 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_5.setObjectName(u"lbl_tot_5")

        self.verticalLayout_5.addWidget(self.lbl_tot_5)

        self.lbl_tot_6 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_6.setObjectName(u"lbl_tot_6")

        self.verticalLayout_5.addWidget(self.lbl_tot_6)

        self.lbl_tot_7 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_7.setObjectName(u"lbl_tot_7")

        self.verticalLayout_5.addWidget(self.lbl_tot_7)

        self.lbl_tot_8 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_8.setObjectName(u"lbl_tot_8")

        self.verticalLayout_5.addWidget(self.lbl_tot_8)

        self.lbl_tot_9 = QLabel(self.GroupBoxReseTotali)
        self.lbl_tot_9.setObjectName(u"lbl_tot_9")

        self.verticalLayout_5.addWidget(self.lbl_tot_9)


        self.horizontalLayout_4.addWidget(self.GroupBoxReseTotali)

        self.canvas_ripartizione_lotti = QWidget(self.tab_consuntivo_annuale)
        self.canvas_ripartizione_lotti.setObjectName(u"canvas_ripartizione_lotti")

        self.horizontalLayout_4.addWidget(self.canvas_ripartizione_lotti)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tab_valutazioni_root.addTab(self.tab_consuntivo_annuale, "")
        self.tab_storico_particella = QWidget()
        self.tab_storico_particella.setObjectName(u"tab_storico_particella")
        self.verticalLayout_4 = QVBoxLayout(self.tab_storico_particella)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lbl_titolo_lotto = QLabel(self.tab_storico_particella)
        self.lbl_titolo_lotto.setObjectName(u"lbl_titolo_lotto")

        self.horizontalLayout_5.addWidget(self.lbl_titolo_lotto)

        self.cmb_scelta_lotto = QComboBox(self.tab_storico_particella)
        self.cmb_scelta_lotto.setObjectName(u"cmb_scelta_lotto")
        self.cmb_scelta_lotto.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_5.addWidget(self.cmb_scelta_lotto)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lbl_tipo_filiera_lotto = QLabel(self.tab_storico_particella)
        self.lbl_tipo_filiera_lotto.setObjectName(u"lbl_tipo_filiera_lotto")

        self.horizontalLayout_6.addWidget(self.lbl_tipo_filiera_lotto)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.tbl_storico_lotto = QTableWidget(self.tab_storico_particella)
        if (self.tbl_storico_lotto.columnCount() < 10):
            self.tbl_storico_lotto.setColumnCount(10)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tbl_storico_lotto.setHorizontalHeaderItem(9, __qtablewidgetitem19)
        self.tbl_storico_lotto.setObjectName(u"tbl_storico_lotto")

        self.verticalLayout_4.addWidget(self.tbl_storico_lotto)

        self.tab_valutazioni_root.addTab(self.tab_storico_particella, "")
        self.tab_efficienza = QWidget()
        self.tab_efficienza.setObjectName(u"tab_efficienza")
        self.layoutWidget = QWidget(self.tab_efficienza)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 10, 1061, 30))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lbl_anno_selezionato_2 = QLabel(self.layoutWidget)
        self.lbl_anno_selezionato_2.setObjectName(u"lbl_anno_selezionato_2")
        self.lbl_anno_selezionato_2.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_7.addWidget(self.lbl_anno_selezionato_2)

        self.cmb_anno_report_capacita = QComboBox(self.layoutWidget)
        self.cmb_anno_report_capacita.setObjectName(u"cmb_anno_report_capacita")
        self.cmb_anno_report_capacita.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_7.addWidget(self.cmb_anno_report_capacita)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.groupBox = QGroupBox(self.tab_efficienza)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 530, 1061, 96))
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lbl_tagli_falliti = QLabel(self.groupBox)
        self.lbl_tagli_falliti.setObjectName(u"lbl_tagli_falliti")

        self.verticalLayout_7.addWidget(self.lbl_tagli_falliti)

        self.lbl_biologici_falliti = QLabel(self.groupBox)
        self.lbl_biologici_falliti.setObjectName(u"lbl_biologici_falliti")

        self.verticalLayout_7.addWidget(self.lbl_biologici_falliti)

        self.lbl_generici_falliti = QLabel(self.groupBox)
        self.lbl_generici_falliti.setObjectName(u"lbl_generici_falliti")

        self.verticalLayout_7.addWidget(self.lbl_generici_falliti)

        self.horizontalLayoutWidget = QWidget(self.tab_efficienza)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 40, 1061, 481))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.tbl_saturazione = QTableWidget(self.groupBox_2)
        if (self.tbl_saturazione.columnCount() < 5):
            self.tbl_saturazione.setColumnCount(5)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tbl_saturazione.setHorizontalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tbl_saturazione.setHorizontalHeaderItem(1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tbl_saturazione.setHorizontalHeaderItem(2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tbl_saturazione.setHorizontalHeaderItem(3, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tbl_saturazione.setHorizontalHeaderItem(4, __qtablewidgetitem24)
        self.tbl_saturazione.setObjectName(u"tbl_saturazione")

        self.verticalLayout_8.addWidget(self.tbl_saturazione)


        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.tbl_stagionali_noli = QTableWidget(self.groupBox_3)
        if (self.tbl_stagionali_noli.columnCount() < 4):
            self.tbl_stagionali_noli.setColumnCount(4)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tbl_stagionali_noli.setHorizontalHeaderItem(0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tbl_stagionali_noli.setHorizontalHeaderItem(1, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tbl_stagionali_noli.setHorizontalHeaderItem(2, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tbl_stagionali_noli.setHorizontalHeaderItem(3, __qtablewidgetitem28)
        self.tbl_stagionali_noli.setObjectName(u"tbl_stagionali_noli")

        self.verticalLayout_9.addWidget(self.tbl_stagionali_noli)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.tab_valutazioni_root.addTab(self.tab_efficienza, "")
        self.tab_anomalie = QWidget()
        self.tab_anomalie.setObjectName(u"tab_anomalie")
        self.verticalLayout_12 = QVBoxLayout(self.tab_anomalie)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_4 = QGroupBox(self.tab_anomalie)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.tbl_log_anomalie = QTableWidget(self.groupBox_4)
        if (self.tbl_log_anomalie.columnCount() < 5):
            self.tbl_log_anomalie.setColumnCount(5)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tbl_log_anomalie.setHorizontalHeaderItem(0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tbl_log_anomalie.setHorizontalHeaderItem(1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tbl_log_anomalie.setHorizontalHeaderItem(2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tbl_log_anomalie.setHorizontalHeaderItem(3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tbl_log_anomalie.setHorizontalHeaderItem(4, __qtablewidgetitem33)
        self.tbl_log_anomalie.setObjectName(u"tbl_log_anomalie")
        self.tbl_log_anomalie.setMaximumSize(QSize(16777203, 16777215))
        self.tbl_log_anomalie.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_10.addWidget(self.tbl_log_anomalie)


        self.verticalLayout_12.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_anomalie)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tbl_bilancio_risorse = QTableWidget(self.groupBox_5)
        if (self.tbl_bilancio_risorse.columnCount() < 4):
            self.tbl_bilancio_risorse.setColumnCount(4)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tbl_bilancio_risorse.setHorizontalHeaderItem(0, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tbl_bilancio_risorse.setHorizontalHeaderItem(1, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tbl_bilancio_risorse.setHorizontalHeaderItem(2, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tbl_bilancio_risorse.setHorizontalHeaderItem(3, __qtablewidgetitem37)
        self.tbl_bilancio_risorse.setObjectName(u"tbl_bilancio_risorse")

        self.gridLayout.addWidget(self.tbl_bilancio_risorse, 1, 0, 1, 1)

        self.lbl_stato_dettaglio = QLabel(self.groupBox_5)
        self.lbl_stato_dettaglio.setObjectName(u"lbl_stato_dettaglio")

        self.gridLayout.addWidget(self.lbl_stato_dettaglio, 0, 0, 1, 1)

        self.txt_diagnostica = QTextEdit(self.groupBox_5)
        self.txt_diagnostica.setObjectName(u"txt_diagnostica")

        self.gridLayout.addWidget(self.txt_diagnostica, 1, 1, 1, 1)

        self.pb_avanzamento_cantiere = QProgressBar(self.groupBox_5)
        self.pb_avanzamento_cantiere.setObjectName(u"pb_avanzamento_cantiere")
        self.pb_avanzamento_cantiere.setValue(0)

        self.gridLayout.addWidget(self.pb_avanzamento_cantiere, 0, 1, 1, 1)

        self.btn_vai_allo_storico = QPushButton(self.groupBox_5)
        self.btn_vai_allo_storico.setObjectName(u"btn_vai_allo_storico")
        self.btn_vai_allo_storico.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.btn_vai_allo_storico, 2, 0, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout)


        self.verticalLayout_12.addWidget(self.groupBox_5)

        self.tab_valutazioni_root.addTab(self.tab_anomalie, "")

        self.verticalLayout_6.addWidget(self.tab_valutazioni_root)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, -1, 10, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_esci = QPushButton(FormValutazioni)
        self.btn_esci.setObjectName(u"btn_esci")
        self.btn_esci.setMinimumSize(QSize(200, 42))

        self.horizontalLayout.addWidget(self.btn_esci)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.retranslateUi(FormValutazioni)

        self.tab_valutazioni_root.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(FormValutazioni)
    # setupUi

    def retranslateUi(self, FormValutazioni):
        FormValutazioni.setWindowTitle(QCoreApplication.translate("FormValutazioni", u"Reportistica Simulazione", None))
        self.lbl_anno_selezionato.setText(QCoreApplication.translate("FormValutazioni", u"Anno Simulazione", None))
        ___qtablewidgetitem = self.tbl_tagli_anno.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FormValutazioni", u"ID Lotto", None))
        ___qtablewidgetitem1 = self.tbl_tagli_anno.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FormValutazioni", u"Destinazione", None))
        ___qtablewidgetitem2 = self.tbl_tagli_anno.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FormValutazioni", u"Superficie", None))
        ___qtablewidgetitem3 = self.tbl_tagli_anno.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FormValutazioni", u"Vol. Raccolto", None))
        ___qtablewidgetitem4 = self.tbl_tagli_anno.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FormValutazioni", u"Resa Opera", None))
        ___qtablewidgetitem5 = self.tbl_tagli_anno.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FormValutazioni", u"Resa Cartiera", None))
        ___qtablewidgetitem6 = self.tbl_tagli_anno.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("FormValutazioni", u"Resa Truciolato", None))
        ___qtablewidgetitem7 = self.tbl_tagli_anno.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("FormValutazioni", u"Resa/Ha Opera", None))
        ___qtablewidgetitem8 = self.tbl_tagli_anno.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("FormValutazioni", u"Resa/Ha Cartiera", None))
        ___qtablewidgetitem9 = self.tbl_tagli_anno.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("FormValutazioni", u"Resa/Ha Truciolato", None))
        self.GroupBoxReseTotali.setTitle(QCoreApplication.translate("FormValutazioni", u"Rese Totali Comprensoriali", None))
        self.lbl_tot_3.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_4.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_5.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_6.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_7.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_8.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_tot_9.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.tab_valutazioni_root.setTabText(self.tab_valutazioni_root.indexOf(self.tab_consuntivo_annuale), QCoreApplication.translate("FormValutazioni", u"\U0001f4ca Consuntivo Annuale", None))
        self.lbl_titolo_lotto.setText(QCoreApplication.translate("FormValutazioni", u"Lotto Selezionato", None))
        self.lbl_tipo_filiera_lotto.setText(QCoreApplication.translate("FormValutazioni", u"Indirizzo Produttivo: Filiera da Opera", None))
        ___qtablewidgetitem10 = self.tbl_storico_lotto.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("FormValutazioni", u"Anno", None))
        ___qtablewidgetitem11 = self.tbl_storico_lotto.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("FormValutazioni", u"Et\u00e0", None))
        ___qtablewidgetitem12 = self.tbl_storico_lotto.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("FormValutazioni", u"Diametro", None))
        ___qtablewidgetitem13 = self.tbl_storico_lotto.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("FormValutazioni", u"Altezza", None))
        ___qtablewidgetitem14 = self.tbl_storico_lotto.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("FormValutazioni", u"Piante vive", None))
        ___qtablewidgetitem15 = self.tbl_storico_lotto.horizontalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("FormValutazioni", u"Pronto", None))
        ___qtablewidgetitem16 = self.tbl_storico_lotto.horizontalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("FormValutazioni", u"Tagliato", None))
        ___qtablewidgetitem17 = self.tbl_storico_lotto.horizontalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("FormValutazioni", u"Resa Opera", None))
        ___qtablewidgetitem18 = self.tbl_storico_lotto.horizontalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("FormValutazioni", u"Resa Cartiera", None))
        ___qtablewidgetitem19 = self.tbl_storico_lotto.horizontalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("FormValutazioni", u"Resa Truciolato", None))
        self.tab_valutazioni_root.setTabText(self.tab_valutazioni_root.indexOf(self.tab_storico_particella), QCoreApplication.translate("FormValutazioni", u"\U0001f332 Fascicolo Storico Particella", None))
        self.lbl_anno_selezionato_2.setText(QCoreApplication.translate("FormValutazioni", u"Anno Simulazione", None))
        self.groupBox.setTitle(QCoreApplication.translate("FormValutazioni", u"Fallimenti operativi e selvicolturali", None))
        self.lbl_tagli_falliti.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_biologici_falliti.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_generici_falliti.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FormValutazioni", u"Saturazione Asset Interni", None))
        ___qtablewidgetitem20 = self.tbl_saturazione.horizontalHeaderItem(0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("FormValutazioni", u"Risorsa", None))
        ___qtablewidgetitem21 = self.tbl_saturazione.horizontalHeaderItem(1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("FormValutazioni", u"Stagione", None))
        ___qtablewidgetitem22 = self.tbl_saturazione.horizontalHeaderItem(2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("FormValutazioni", u"Ore Disponibili", None))
        ___qtablewidgetitem23 = self.tbl_saturazione.horizontalHeaderItem(3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("FormValutazioni", u"New Column", None))
        ___qtablewidgetitem24 = self.tbl_saturazione.horizontalHeaderItem(4)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("FormValutazioni", u"% Saturazione", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("FormValutazioni", u"Utilizzi Stagionali e Noli", None))
        ___qtablewidgetitem25 = self.tbl_stagionali_noli.horizontalHeaderItem(0)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("FormValutazioni", u"Risorsa", None))
        ___qtablewidgetitem26 = self.tbl_stagionali_noli.horizontalHeaderItem(1)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("FormValutazioni", u"Stagione", None))
        ___qtablewidgetitem27 = self.tbl_stagionali_noli.horizontalHeaderItem(2)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("FormValutazioni", u"Ore Extra/Noli Usati", None))
        ___qtablewidgetitem28 = self.tbl_stagionali_noli.horizontalHeaderItem(3)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("FormValutazioni", u"Massimo Utilizzabile", None))
        self.tab_valutazioni_root.setTabText(self.tab_valutazioni_root.indexOf(self.tab_efficienza), QCoreApplication.translate("FormValutazioni", u"\u2699\ufe0f Capacit\u00e0 Operative", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("FormValutazioni", u"Lista Fallanze Operative", None))
        ___qtablewidgetitem29 = self.tbl_log_anomalie.horizontalHeaderItem(0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("FormValutazioni", u"Anno", None))
        ___qtablewidgetitem30 = self.tbl_log_anomalie.horizontalHeaderItem(1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("FormValutazioni", u"Stagione", None))
        ___qtablewidgetitem31 = self.tbl_log_anomalie.horizontalHeaderItem(2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("FormValutazioni", u"Lotto ID", None))
        ___qtablewidgetitem32 = self.tbl_log_anomalie.horizontalHeaderItem(3)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("FormValutazioni", u"Descrizione Lavorazione", None))
        ___qtablewidgetitem33 = self.tbl_log_anomalie.horizontalHeaderItem(4)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("FormValutazioni", u"Stato\\Anomalia", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("FormValutazioni", u"Descrizione Fallanza Lotto Selezionato", None))
        ___qtablewidgetitem34 = self.tbl_bilancio_risorse.horizontalHeaderItem(0)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("FormValutazioni", u"Risorsa", None))
        ___qtablewidgetitem35 = self.tbl_bilancio_risorse.horizontalHeaderItem(1)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("FormValutazioni", u"Fabbisogno", None))
        ___qtablewidgetitem36 = self.tbl_bilancio_risorse.horizontalHeaderItem(2)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("FormValutazioni", u"Ore Lavorate", None))
        ___qtablewidgetitem37 = self.tbl_bilancio_risorse.horizontalHeaderItem(3)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("FormValutazioni", u"Ore Mancanti", None))
        self.lbl_stato_dettaglio.setText(QCoreApplication.translate("FormValutazioni", u"STATO LOTTO", None))
        self.btn_vai_allo_storico.setText(QCoreApplication.translate("FormValutazioni", u"Controlla Storico Lotto", None))
        self.tab_valutazioni_root.setTabText(self.tab_valutazioni_root.indexOf(self.tab_anomalie), QCoreApplication.translate("FormValutazioni", u"\u26a0\ufe0f Registro dei Fallimenti Operativi", None))
        self.btn_esci.setText(QCoreApplication.translate("FormValutazioni", u"Esci", None))
    # retranslateUi

