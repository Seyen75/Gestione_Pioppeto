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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_FormValutazioni(object):
    def setupUi(self, FormValutazioni):
        if not FormValutazioni.objectName():
            FormValutazioni.setObjectName(u"FormValutazioni")
        FormValutazioni.resize(1150, 780)
        FormValutazioni.setMinimumSize(QSize(1150, 780))
        FormValutazioni.setMaximumSize(QSize(1150, 780))
        FormValutazioni.setStyleSheet(u"/* =========================================================================\n"
"   SFONDO DELLA FINESTRA E DEI PANNELLI (Nuovo tono caldo armonizzato)\n"
"   ========================================================================= */\n"
"QWidget#FormValutazioni, QTabWidget::pane {\n"
"    background-color: #1a1516; /* Antracite caldissimo con una punta di bordeaux/terra d'ombra */\n"
"}\n"
"\n"
"/* =========================================================================\n"
"   STILE RADICALE DELLE LINGUETTE (Ancoraggio forzato a sinistra)\n"
"   ========================================================================= */\n"
"QTabWidget::tab-bar {\n"
"    left: 0px; /* Spinge fisicamente l'inizio della barra al millimetro zero */\n"
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
" "
                        "   border: 1px solid #3d292c;\n"
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
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8a1c24, stop:1 #4f0e13);\n"
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
""
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
"QLabel#lbl_titolo_lotto, \n"
"QGroupBox {\n"
"    font-weight: bold !important;\n"
"    font-size: 13px !important;\n"
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
"/* =========================================================================\n"
"   TABE"
                        "LLE (QTableWidget) - Sintonizzate sui toni caldi\n"
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
"   ========================================================================= */\n"
"QPushButton {\n"
"    back"
                        "ground: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d1820, stop:1 #420f13);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"    min-height: 30px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
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
"\n"
"QComboBox { \n"
"                    background-color: #2d181b; \n"
"                    color: #ffffff; \n"
"                    border: 1px solid #3d2429; \n"
"                    border-radius: 4px; \n"
"                    padding: 4px 10px;\n"
"                }\n"
"         "
                        "       QComboBox::drop-down {\n"
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
"                    height: 6px; \n"
"                    border-radius: 3px; \n"
"                } \n"
"                QSlider::handle:horizontal { \n"
"                    background: #ff8a80; \n"
"                    width: 14px; \n"
"                    margin: -4px 0; \n"
"                    border-radiu"
                        "s: 7px; \n"
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

        self.horizontalLayout_3.addWidget(self.lbl_anno_selezionato)

        self.sld_anno_report = QSlider(self.tab_consuntivo_annuale)
        self.sld_anno_report.setObjectName(u"sld_anno_report")
        self.sld_anno_report.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.sld_anno_report)


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
        self.groupBox = QGroupBox(self.tab_consuntivo_annuale)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 150))
        self.groupBox.setMaximumSize(QSize(500, 300))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lbl_res_opera_anno = QLabel(self.groupBox)
        self.lbl_res_opera_anno.setObjectName(u"lbl_res_opera_anno")

        self.verticalLayout_5.addWidget(self.lbl_res_opera_anno)

        self.lbl_res_cartiera_anno = QLabel(self.groupBox)
        self.lbl_res_cartiera_anno.setObjectName(u"lbl_res_cartiera_anno")

        self.verticalLayout_5.addWidget(self.lbl_res_cartiera_anno)

        self.lbl_res_truciolato_anno = QLabel(self.groupBox)
        self.lbl_res_truciolato_anno.setObjectName(u"lbl_res_truciolato_anno")

        self.verticalLayout_5.addWidget(self.lbl_res_truciolato_anno)

        self.lbl_resa_ettaro_media_anno = QLabel(self.groupBox)
        self.lbl_resa_ettaro_media_anno.setObjectName(u"lbl_resa_ettaro_media_anno")

        self.verticalLayout_5.addWidget(self.lbl_resa_ettaro_media_anno)


        self.horizontalLayout_4.addWidget(self.groupBox)

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

        self.tab_valutazioni_root.setCurrentIndex(1)


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
        self.groupBox.setTitle(QCoreApplication.translate("FormValutazioni", u"Rese Totali Comprensoriali", None))
        self.lbl_res_opera_anno.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_res_cartiera_anno.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_res_truciolato_anno.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
        self.lbl_resa_ettaro_media_anno.setText(QCoreApplication.translate("FormValutazioni", u"TextLabel", None))
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
        self.btn_esci.setText(QCoreApplication.translate("FormValutazioni", u"Esci", None))
    # retranslateUi

