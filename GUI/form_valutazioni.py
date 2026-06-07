# GUI/form_valutazioni.py
import os
from typing import Dict, Any, List

from PySide6.QtCore import Slot, Qt, QLocale
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QComboBox, QLabel, QPushButton, QTabWidget, QVBoxLayout, QHeaderView, QProgressBar, QTextEdit
from PySide6.QtGui import QScreen, QGuiApplication
from PySide6.QtGui import QColor, QFont
from PySide6.QtUiTools import QUiLoader

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class FormValutazioni(QWidget):
    def __init__(self, motore_simulazione, parent=None):
        super().__init__(parent)
        self.motore = motore_simulazione
        self.parametri = motore_simulazione.parametri

        # --- Inizializza QLocale per la formattazione italiana ---
        self.locale_it = QLocale(QLocale.Italian, QLocale.Italy)

        # 1. Caricamento UI e mappatura componenti
        self._carica_interfaccia()
        self._centra_finestra_su_schermo()
        self._mappa_componenti_ui()
        self._inizializza_canvas_grafico()
        self._tabelle_efficienza()
        self._connetti_segnali()
        
        # 2. Configurazione e popolamento iniziale dei dati
        self._configura_stato_iniziale_selettori()

    def _carica_interfaccia(self):
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_valutazioni.ui")
        self.ui = loader.load(percorso_ui, self)
        
        layout_principale = QVBoxLayout(self)
        layout_principale.addWidget(self.ui)
        layout_principale.setContentsMargins(15, 15, 15, 15)
        
        self.setWindowTitle("Report Finale e Statistiche Consuntive")
        
    def _centra_finestra_su_schermo(self):
        self.adjustSize()
        schermo: QScreen = QGuiApplication.primaryScreen()
        if self.parent() and self.parent().window():
            schermo = self.parent().window().screen()
            
        if schermo:
            geometria_schermo = schermo.geometry()
            larghezza_form = self.width() if self.width() > 100 else 1100
            altezza_form = self.height() if self.height() > 100 else 780
            x = (geometria_schermo.width() - larghezza_form) // 2
            y = (geometria_schermo.height() - altezza_form) // 2
            self.move(geometria_schermo.x() + x, geometria_schermo.y() + y)

    def _mappa_componenti_ui(self):
        self.tab_root = self.ui.findChild(QTabWidget, "tab_valutazioni_root")
        
        if self.tab_root:
            barra_tab = self.tab_root.tabBar()
            barra_tab.setExpanding(False)
        
        self.cmb_anno_report = self.ui.findChild(QComboBox, "cmb_anno_report")
        self.lbl_anno_selezionato = self.ui.findChild(QLabel, "lbl_anno_selezionato")
        self.widget_canvas_tab1 = self.ui.findChild(QWidget, "canvas_ripartizione_lotti")
        
        self.tbl_tagli_anno = self.ui.findChild(QTableWidget, "tbl_tagli_anno")
        if self.tbl_tagli_anno is None:
            tab_1 = self.ui.findChild(QWidget, "tab_consuntivo_annuale")
            if tab_1:
                self.tbl_tagli_anno = tab_1.findChild(QTableWidget, "tbl_tagli_anno")
        
        self.cmb_scelta_lotto = self.ui.findChild(QComboBox, "cmb_scelta_lotto")
        self.lbl_tipo_filiera_lotto = self.ui.findChild(QLabel, "lbl_tipo_filiera_lotto")
        self.lbl_titolo_lotto = self.ui.findChild(QLabel, "lbl_titolo_lotto")
        
        self.tbl_storico_lotto = self.ui.findChild(QTableWidget, "tbl_storico_lotto")
        if self.tbl_storico_lotto is None:
            tab_2 = self.ui.findChild(QWidget, "tab_storico_particella")
            if tab_2:
                self.tbl_storico_lotto = tab_2.findChild(QTableWidget, "tbl_storico_lotto")
                
        self.cmb_anno_report_capacita = self.ui.findChild(QComboBox, "cmb_anno_report_capacita")
        
        # --- Componenti Tab Anomalie ---
        self.tbl_log_anomalie = self.ui.findChild(QTableWidget, "tbl_log_anomalie")
        self.lbl_stato_dettaglio = self.ui.findChild(QLabel, "lbl_stato_dettaglio")
        self.pb_avanzamento_cantiere = self.ui.findChild(QProgressBar, "pb_avanzamento_cantiere")
        self.tbl_bilancio_risorse = self.ui.findChild(QTableWidget, "tbl_bilancio_risorse")
        self.txt_diagnostica = self.ui.findChild(QTextEdit, "txt_diagnostica")
        self.btn_vai_allo_storico = self.ui.findChild(QPushButton, "btn_vai_allo_storico")
        
        self.btn_esci = self.ui.findChild(QPushButton, "btn_esci")

    def _tabelle_efficienza(self):
        # --- Setup Tabella 1: Saturazione Interna ---
        if hasattr(self.ui, 'tbl_saturazione'):
            col_sat = ["Risorsa", "Stagione", "Ore\nDisponibili", "Ore\nLavorate", "%\nSaturaz."]
            self.ui.tbl_saturazione.setColumnCount(len(col_sat))
            self.ui.tbl_saturazione.setHorizontalHeaderLabels(col_sat)
            header_sat = self.ui.tbl_saturazione.horizontalHeader()
            header_sat.setMinimumHeight(45)
            header_sat.setSectionResizeMode(QHeaderView.ResizeToContents)
            header_sat.setSectionResizeMode(0, QHeaderView.Stretch)
            header_sat.setStretchLastSection(False)
        
        # --- Setup Tabella 2: Stress Test Noli ---
        if hasattr(self.ui, 'tbl_stagionali_noli'):
            col_stress = ["Risorsa", "Stagione", "Ore Extra\n(Noli)", "Tetto Max\nMercato", "%\nEsaurim.", "Ore Sforate\n(Criticità)"]
            self.ui.tbl_stagionali_noli.setColumnCount(len(col_stress))
            self.ui.tbl_stagionali_noli.setHorizontalHeaderLabels(col_stress)
            header_stress = self.ui.tbl_stagionali_noli.horizontalHeader()
            header_stress.setMinimumHeight(45)
            header_stress.setSectionResizeMode(QHeaderView.ResizeToContents)
            header_stress.setSectionResizeMode(0, QHeaderView.Stretch)
            header_stress.setStretchLastSection(False)
            
        # --- Setup Tabelle Anomalie ---
        if hasattr(self, 'tbl_log_anomalie') and self.tbl_log_anomalie:
            col_anomalie = ["Anno", "Stagione", "Lotto ID", "Operazione", "Stato / Anomalia"]
            self.tbl_log_anomalie.setColumnCount(len(col_anomalie))
            self.tbl_log_anomalie.setHorizontalHeaderLabels(col_anomalie)
            
            # Dimensionamento corretto delle colonne
            header_anom = self.tbl_log_anomalie.horizontalHeader()
            header_anom.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header_anom.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header_anom.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header_anom.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header_anom.setSectionResizeMode(4, QHeaderView.Stretch)
            
        if hasattr(self, 'tbl_bilancio_risorse') and self.tbl_bilancio_risorse:
            # Intestazioni inequivocabili
            col_bil = ["Risorsa", "Fabbisogno Tot.", "Ore Lavorate", "Ore Mancanti"]
            self.tbl_bilancio_risorse.setColumnCount(len(col_bil))
            self.tbl_bilancio_risorse.setHorizontalHeaderLabels(col_bil)
            self.tbl_bilancio_risorse.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _inizializza_canvas_grafico(self):
        colore_sfondo_hex = "#141923"
        self.fig_ripartizione = Figure(figsize=(5, 3), facecolor=colore_sfondo_hex)
        self.canvas_ripartizione = FigureCanvas(self.fig_ripartizione)
        self.ax_ripartizione = self.fig_ripartizione.add_subplot(111)
        self.ax_ripartizione.set_facecolor(colore_sfondo_hex)
        
        if self.widget_canvas_tab1:
            layout_grafico = QVBoxLayout(self.widget_canvas_tab1)
            layout_grafico.addWidget(self.canvas_ripartizione)
            layout_grafico.setContentsMargins(0, 0, 0, 0)

    def _connetti_segnali(self):
        if self.btn_esci:
            self.btn_esci.clicked.connect(self.close)
        
        if hasattr(self, 'cmb_anno_report') and self.cmb_anno_report:
            self.cmb_anno_report.currentTextChanged.connect(self.slot_cambio_anno_combobox)
            
        if self.cmb_scelta_lotto:
            self.cmb_scelta_lotto.currentTextChanged.connect(self.slot_cambio_lotto_combobox)
            
        if hasattr(self, 'cmb_anno_report_capacita') and self.cmb_anno_report_capacita:
            self.cmb_anno_report_capacita.currentTextChanged.connect(self._aggiorna_tab_efficienza)
            
        # Connessioni per il Tab Anomalie
        if self.tbl_log_anomalie:
            self.tbl_log_anomalie.cellClicked.connect(self.on_riga_anomalia_selezionata)
            
        if self.btn_vai_allo_storico:
            self.btn_vai_allo_storico.clicked.connect(self.azione_vai_allo_storico)
            
        if self.tbl_log_anomalie:
            # Sostituito cellClicked con itemSelectionChanged per prendere anche il click sull'header
            self.tbl_log_anomalie.itemSelectionChanged.connect(self.on_riga_anomalia_selezionata)
        
    def _configura_stato_iniziale_selettori(self):
        anni_presenti = set()
        dizionario_storia = getattr(self.parametri, "storico_stagionale", {}) 
        
        for chiave_stagione in dizionario_storia.keys(): 
            if chiave_stagione.startswith("A"):
                try:
                    anno = int(chiave_stagione.split("_")[0][1:])
                    anni_presenti.add(anno)
                except ValueError:
                    continue
        
        self.anno_max = max(anni_presenti) if anni_presenti else 1
        lista_anni = [str(a) for a in range(1, self.anno_max + 1)]
        
        if hasattr(self, 'cmb_anno_report') and self.cmb_anno_report:
            self.cmb_anno_report.clear()
            self.cmb_anno_report.addItems(lista_anni)
        
        if self.cmb_scelta_lotto:
            self.cmb_scelta_lotto.clear()
            for lotto in self.parametri.collezione_lotti:
                self.cmb_scelta_lotto.addItem(lotto.id_lotto)

        if self.tbl_storico_lotto:
            header = self.tbl_storico_lotto.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setStretchLastSection(False)
        
        if hasattr(self, 'cmb_anno_report_capacita') and self.cmb_anno_report_capacita:
            self.cmb_anno_report_capacita.clear()
            self.cmb_anno_report_capacita.addItems(lista_anni)
        
        # Scateniamo i popolamenti iniziali
        if hasattr(self, 'slot_cambio_anno_combobox'):
            self.slot_cambio_anno_combobox("1")
            
        if hasattr(self, '_aggiorna_tab_efficienza'):
            self._aggiorna_tab_efficienza("1")
            
        if self.cmb_scelta_lotto and self.cmb_scelta_lotto.count() > 0:
            self.slot_cambio_lotto_combobox(self.cmb_scelta_lotto.currentText())
            
        # Popoliamo la tabella delle anomalie all'avvio
        self._popola_tabella_anomalie()
    
    def _costruisci_mappa_operazioni(self) -> dict:
        mappa = {}
        for destinazione, fasi in STRUTTURA_LAVORAZIONI.items():
            for fase, stagioni in fasi.items():
                for stagione, operazioni in stagioni.items():
                    for op in operazioni:
                        mappa[op["id_operazione"]] = op["descrizione"]
        return mappa

    @Slot(str)
    def slot_cambio_anno_combobox(self, testo_anno: str):
        if not testo_anno: 
            return
        anno_selezionato = int(testo_anno)
        
        if self.tbl_tagli_anno is None:
            return
        self.tbl_tagli_anno.setRowCount(0)

        tot_opera, tot_cartiera, tot_truciolato = 0.0, 0.0, 0.0
        tot_vol_raccolto, superficie_tagliata_anno = 0.0, 0.0
        dati_grafico_lotti = []

        dizionario_completo = getattr(self.parametri, "storico_stagionale", {})
        chiave_inverno = f"A{anno_selezionato}_Inverno"
        
        if chiave_inverno in dizionario_completo:
            istantanea = dizionario_completo[chiave_inverno]
            risultati_cantieri = istantanea.get("risultati_cantieri", {})
            tagli = risultati_cantieri.get("tagli_effettuati", []) if risultati_cantieri else []
            
            for t in tagli:
                id_lotto = t.get("lotto_id", "")
                volume_totale_cantiere = float(t.get("volume_raccolto_m3", 0.0))
                rese = t.get("rese", {})
                
                lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto), None)
                if not lotto_reale: continue
                    
                riga = self.tbl_tagli_anno.rowCount()
                self.tbl_tagli_anno.insertRow(riga)
                
                superficie = getattr(lotto_reale, "superficie_ettari", 5.0)
                destinazione = str(lotto_reale.destinazione_uso).strip().upper()
                
                vol_opera = float(rese.get("opera_m3", 0.0))
                massa_cartiera = float(rese.get("cartiera_t", 0.0))
                massa_truciolato = float(rese.get("truciolato_t", 0.0))
                
                resa_ha_opera = vol_opera / superficie if superficie > 0 else 0.0
                resa_ha_cartiera = massa_cartiera / superficie if superficie > 0 else 0.0
                resa_ha_truciolato = massa_truciolato / superficie if superficie > 0 else 0.0
                
                tot_opera += vol_opera
                tot_cartiera += massa_cartiera
                tot_truciolato += massa_truciolato
                tot_vol_raccolto += volume_totale_cantiere
                superficie_tagliata_anno += superficie
                
                dati_grafico_lotti.append({"id": id_lotto, "opera": vol_opera, "cartiera": massa_cartiera, "truciolato": massa_truciolato})
                
                self.tbl_tagli_anno.setItem(riga, 0, QTableWidgetItem(id_lotto))
                self.tbl_tagli_anno.setItem(riga, 1, QTableWidgetItem(destinazione))
                self.tbl_tagli_anno.setItem(riga, 2, QTableWidgetItem(self.locale_it.toString(float(superficie), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 3, QTableWidgetItem(self.locale_it.toString(float(volume_totale_cantiere), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 4, QTableWidgetItem(self.locale_it.toString(float(vol_opera), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 5, QTableWidgetItem(self.locale_it.toString(float(massa_cartiera), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 6, QTableWidgetItem(self.locale_it.toString(float(massa_truciolato), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 7, QTableWidgetItem(self.locale_it.toString(float(resa_ha_opera), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 8, QTableWidgetItem(self.locale_it.toString(float(resa_ha_cartiera), 'f', 2)))
                self.tbl_tagli_anno.setItem(riga, 9, QTableWidgetItem(self.locale_it.toString(float(resa_ha_truciolato), 'f', 2)))

                for c in range(10):
                    item = self.tbl_tagli_anno.item(riga, c)
                    if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        sup_opera = sum(getattr(l, "superficie_ettari", 0) for l in self.parametri.collezione_lotti if str(l.destinazione_uso).strip().upper() == "OPERA" and l.id_lotto in [d["id"] for d in dati_grafico_lotti])
        sup_industria = sum(getattr(l, "superficie_ettari", 0) for l in self.parametri.collezione_lotti if str(l.destinazione_uso).strip().upper() == "INDUSTRIA" and l.id_lotto in [d["id"] for d in dati_grafico_lotti])

        media_ha_opera = (tot_opera / sup_opera) if sup_opera > 0 else 0.0
        media_ha_cartiera = (tot_cartiera / sup_industria) if sup_industria > 0 else 0.0
        media_ha_truciolato = (tot_truciolato / sup_industria) if sup_industria > 0 else 0.0

        valori_colonne = {3: tot_vol_raccolto, 4: tot_opera, 5: tot_cartiera, 6: tot_truciolato, 7: media_ha_opera, 8: media_ha_cartiera, 9: media_ha_truciolato}

        for col, valore in valori_colonne.items():
            nome_obj = f"lbl_tot_{col}"
            label_obj = self.ui.findChild(QLabel, nome_obj)
            if label_obj:
                header_item = self.tbl_tagli_anno.horizontalHeaderItem(col)
                testo_header = header_item.text().replace('\n', ' ') if header_item else f"Colonna {col}"
                valore_formattato = self.locale_it.toString(float(valore), 'f', 2)
                label_obj.setText(f"Totale {testo_header}: {valore_formattato}")

        self._aggiorna_grafico_ripartizione(dati_grafico_lotti)

    @Slot(str)
    def slot_cambio_lotto_combobox(self, id_lotto_selezionato: str):
        if not id_lotto_selezionato or self.tbl_storico_lotto is None:
            return
        lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto_selezionato), None)
        if not lotto_reale: return
        if self.lbl_tipo_filiera_lotto:
            self.lbl_tipo_filiera_lotto.setText(f"Indirizzo Produttivo: Filiera da {lotto_reale.destinazione_uso} | Clone: {lotto_reale.clone_assegnato}")
        self._popola_tabella_lotto(lotto_reale)
        
    def _popola_tabella_lotto(self, lotto_reale):
        if self.tbl_storico_lotto is None: return
        self.tbl_storico_lotto.setRowCount(0)
        
        eta_rotazione_standard = 5 if lotto_reale.destinazione_uso == "INDUSTRIA" else 10
        diametro_target = 15.0 if lotto_reale.destinazione_uso == "INDUSTRIA" else 30.0
        
        dizionario_completo = getattr(self.parametri, "storico_stagionale", {})
        anni_rilevati = set()
        for k in dizionario_completo.keys():
            if k.startswith("A") and "_" in k and not k.endswith("RisorseExtra"):
                parte_anno = k.split("_")[0]
                if parte_anno[1:].isdigit():
                    anni_rilevati.add(int(parte_anno[1:]))
                    
        storia_lotto = {}
        
        for anno in sorted(list(anni_rilevati)):
            chiave_inverno = f"A{anno}_Inverno"
            if chiave_inverno not in dizionario_completo: continue
            
            istanza_inverno = dizionario_completo[chiave_inverno]
            stato_lotti = istanza_inverno.get("stato_lotti_pre", {})
            risultati = istanza_inverno.get("risultati_cantieri", {})
            dati_biometrici = stato_lotti.get(lotto_reale.id_lotto, {})
            
            record = {
                "eta": dati_biometrici.get("eta", 0),
                "piante": dati_biometrici.get("biometria", {}).get("piante_attive", 0),
                "dbh": dati_biometrici.get("biometria", {}).get("dbh_reale_cm", 0.0),
                "h": dati_biometrici.get("biometria", {}).get("altezza_m", 0.0),
                "stato_taglio": "NO",
                "rese": {"opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}
            }
            
            tagli_anno = risultati.get("tagli_effettuati", [])
            ops = risultati.get("dettaglio_operazioni", [])
            dati_taglio = next((t for t in tagli_anno if t.get("lotto_id") == lotto_reale.id_lotto), None)
            
            if dati_taglio:
                record["rese"] = dati_taglio.get("rese", record["rese"])
                stato_op = next((o.get("stato", "") for o in ops if o.get("lotto_id") == lotto_reale.id_lotto and "RAC" in o.get("id_operazione", "")), "Eseguito")
                record["stato_taglio"] = "PARZIALE" if "Parziale" in stato_op else "COMPLETATO"
                    
            storia_lotto[anno] = record

        for anno, dati in storia_lotto.items():
            riga = self.tbl_storico_lotto.rowCount()
            self.tbl_storico_lotto.insertRow(riga)
            
            is_pronto = False
            if dati["stato_taglio"] in ["COMPLETATO", "PARZIALE"]:
                is_pronto = True
            else:
                try:
                    if float(dati["eta"]) >= eta_rotazione_standard and float(dati["dbh"]) >= diametro_target:
                        is_pronto = True
                except (ValueError, TypeError): pass
                    
            pronto_al_taglio = "SÌ" if is_pronto else "NO"

            self.tbl_storico_lotto.setItem(riga, 0, QTableWidgetItem(f"Anno {anno}"))
            self.tbl_storico_lotto.setItem(riga, 1, QTableWidgetItem(f"{dati['eta']} anni"))
            self.tbl_storico_lotto.setItem(riga, 2, QTableWidgetItem(f"{self.locale_it.toString(float(dati['dbh']), 'f', 2)} cm"))
            self.tbl_storico_lotto.setItem(riga, 3, QTableWidgetItem(f"{self.locale_it.toString(float(dati['h']), 'f', 2)} m"))
            self.tbl_storico_lotto.setItem(riga, 4, QTableWidgetItem(f"{dati['piante']} fusti"))
            
            item_pronto = QTableWidgetItem(pronto_al_taglio)
            if pronto_al_taglio == "SÌ": item_pronto.setForeground(QColor("#00e676"))
            self.tbl_storico_lotto.setItem(riga, 5, item_pronto)
            
            item_tagliato = QTableWidgetItem(dati["stato_taglio"])
            if dati["stato_taglio"] == "COMPLETATO": item_tagliato.setForeground(QColor("#00b0ff")) 
            elif dati["stato_taglio"] == "PARZIALE": item_tagliato.setForeground(QColor("#ff9800")) 
            elif pronto_al_taglio == "SÌ" and dati["stato_taglio"] == "NO": item_tagliato.setForeground(QColor("#ff5252")) 
            self.tbl_storico_lotto.setItem(riga, 6, item_tagliato)
            
            self.tbl_storico_lotto.setItem(riga, 7, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('opera_m3', 0.0)), 'f', 2)} m³"))
            self.tbl_storico_lotto.setItem(riga, 8, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('cartiera_t', 0.0)), 'f', 2)} t"))
            self.tbl_storico_lotto.setItem(riga, 9, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('truciolato_t', 0.0)), 'f', 2)} t"))

            for c in range(10):
                item = self.tbl_storico_lotto.item(riga, c)
                if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
    def _aggiorna_grafico_ripartizione(self, dati_lotti: List[Dict[str, Any]]):
        if not hasattr(self, 'ax_ripartizione'): return
        self.ax_ripartizione.clear()
        
        if not dati_lotti:
            self.ax_ripartizione.text(0.5, 0.5, "Nessun cantiere di taglio concluso\nin questo anno di esercizio", color='#ff8a80', ha='center', va='center', fontsize=10, style='italic')
            self.ax_ripartizione.set_xticks([])
            self.ax_ripartizione.set_yticks([])
            self.canvas_ripartizione.draw()
            return

        nomi_lotti = [d["id"] for d in dati_lotti]
        opera = np.array([d["opera"] for d in dati_lotti])
        cartiera = np.array([d["cartiera"] for d in dati_lotti])
        truciolato = np.array([d["truciolato"] for d in dati_lotti])

        larghezza_colonna = 0.35 
        x_pos = np.arange(len(nomi_lotti))
        
        self.ax_ripartizione.bar(x_pos, opera, width=larghezza_colonna, label='Opera', color='#b71c1c')
        self.ax_ripartizione.bar(x_pos, cartiera, bottom=opera, width=larghezza_colonna, label='Cartiera', color='#e65100')
        self.ax_ripartizione.bar(x_pos, truciolato, bottom=opera+cartiera, width=larghezza_colonna, label='Truciolato', color='#ffca28')
                
        self.ax_ripartizione.set_xticks(x_pos)
        self.ax_ripartizione.set_xticklabels(nomi_lotti)

        min_slots = 4
        if len(nomi_lotti) < min_slots:
            margine = (min_slots - len(nomi_lotti)) / 2.0
            self.ax_ripartizione.set_xlim(-margine - 0.5, len(nomi_lotti) - 1 + margine + 0.5)

        self.ax_ripartizione.set_title("Ripartizione Assoluta Masse Raccolte", color='#ff8a80', fontsize=11, weight='bold', pad=30)
        self.ax_ripartizione.tick_params(colors='#e0e0e0', labelsize=8)
        self.ax_ripartizione.grid(True, color='#2b1d20', linestyle='--', alpha=0.5, axis='y')
        
        legenda = self.ax_ripartizione.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=3, facecolor='#141923', edgecolor='#3d2429', fontsize=8, framealpha=1.0)
        for text in legenda.get_texts(): text.set_color('#e0e0e0')

        self.fig_ripartizione.subplots_adjust(top=0.78, bottom=0.15, left=0.15, right=0.95)
        self.canvas_ripartizione.draw()
        
    def _aggiorna_tab_efficienza(self, testo_anno: str):
        if not testo_anno: return
        anno = int(testo_anno)
        self.ui.tbl_saturazione.setRowCount(0)
        self.ui.tbl_stagionali_noli.setRowCount(0)
        
        stagioni = ["Inverno", "Primavera", "Estate", "Autunno"]
        risorse = [
            ("Op. Spec.", "grado_A", "personale_spec"),
            ("Op. Generici", "grado_B", "personale_comune"),
            ("Harvester", "harvester", "harvester"),
            ("Forwarder", "forwarder", "forwarder"),
            ("Trattori Alta", "trattori_alta", "trattori_alta"),
            ("Trattori Media", "trattori_media", "trattori_media"),
            ("Piattaforme", "piattaforme", "piattaforme")
        ]
        
        mappa_attributi_ditta = {
            "grado_A": "operai_grado_A", "grado_B": "operai_grado_B", "harvester": "harvester_abbattitori",
            "forwarder": "forwarder_caricatori", "trattori_alta": "trattori_alta_potenza",
            "trattori_media": "trattori_media_potenza", "piattaforme": "piattaforme_aeree_semoventi"
        }
        
        giorni_utili = 55
        ore_base = giorni_utili * getattr(self.motore.ditta, "ore_giorno_standard", 8)
        limiti_noli = getattr(self.motore.ditta, "limiti_noli_stagionali", {})
        
        for nome_ui, chiave_interna, chiave_nolo in risorse:
            tot_disp, tot_lav, tot_noli, tot_mercato, tot_sforate = 0.0, 0.0, 0.0, 0.0, 0.0
            nome_reale = mappa_attributi_ditta.get(chiave_interna, chiave_interna)
            disp = getattr(self.motore.ditta, nome_reale, 0) * ore_base
            
            for stagione in stagioni:
                chiave_stato = f"A{anno}_{stagione}"
                dizionario_storico = getattr(self.parametri, "storico_stati", getattr(self.parametri, "storico_stagionale", {}))
                stato = dizionario_storico.get(chiave_stato, {})
                report_cantieri = stato.get("risultati_cantieri", {})
                
                umane = report_cantieri.get("risorse_umane_interne", {})
                macchine = report_cantieri.get("macchinari_interni_consumati", {})
                lav = umane.get(f"consumate_{chiave_interna[-1]}", 0.0) if "grado" in chiave_interna else macchine.get(chiave_interna, 0.0)
                
                terzi = report_cantieri.get("ricorso_terzi_e_noli", {})
                noli_usati = terzi.get(chiave_interna, 0.0)
                
                unita_max = limiti_noli.get(chiave_nolo, 0)
                tetto_mercato = unita_max * ore_base
                ore_sforate = max(0.0, noli_usati - tetto_mercato)
                
                tot_disp += disp; tot_lav += lav; tot_noli += noli_usati; tot_mercato += tetto_mercato; tot_sforate += ore_sforate
                
                self._inserisci_riga_saturazione(nome_ui, stagione, disp, lav)
                self._inserisci_riga_stress(nome_ui, stagione, noli_usati, tetto_mercato, ore_sforate)
            
            self._inserisci_riga_saturazione(nome_ui, "TOTALE", tot_disp, tot_lav, is_totale=True)
            self._inserisci_riga_stress(nome_ui, "TOTALE", tot_noli, tot_mercato, tot_sforate, is_totale=True)
            self.ui.tbl_saturazione.insertRow(self.ui.tbl_saturazione.rowCount())
            self.ui.tbl_stagionali_noli.insertRow(self.ui.tbl_stagionali_noli.rowCount())

        stats = getattr(self.motore, "stats_globali", {})
        if hasattr(self.ui, 'lbl_tagli_falliti'): self.ui.lbl_tagli_falliti.setText(f"Tagli Raso Saltati (Mancanza Risorse): {stats.get('tagli_strutturali_saltati', 0)}")
        if hasattr(self.ui, 'lbl_biologici_falliti'): self.ui.lbl_biologici_falliti.setText(f"Tagli Ritardati (Oltre Maturità): {stats.get('tagli_biologici_saltati', 0)}")
        if hasattr(self.ui, 'lbl_generici_falliti'): self.ui.lbl_generici_falliti.setText(f"Lavorazioni Agronomiche Saltate: {stats.get('lavorazioni_generiche_saltate', 0)}")
                    
    def _inserisci_riga_saturazione(self, nome, stagione, disp, lav, is_totale=False):
        r = self.ui.tbl_saturazione.rowCount()
        self.ui.tbl_saturazione.insertRow(r)
        sat_perc = (lav / disp * 100) if disp > 0 else 0.0
        
        self.ui.tbl_saturazione.setItem(r, 0, QTableWidgetItem(nome if not is_totale else ""))
        self.ui.tbl_saturazione.setItem(r, 1, QTableWidgetItem(stagione))
        self.ui.tbl_saturazione.setItem(r, 2, QTableWidgetItem(f"{self.locale_it.toString(float(disp), 'f', 1)} h"))
        self.ui.tbl_saturazione.setItem(r, 3, QTableWidgetItem(f"{self.locale_it.toString(float(lav), 'f', 1)} h"))
        
        item_sat = QTableWidgetItem(f"{self.locale_it.toString(float(sat_perc), 'f', 1)}%")
        if sat_perc < 25.0 and disp > 0: item_sat.setForeground(QColor("#ff5252"))
        elif sat_perc > 75.0: item_sat.setForeground(QColor("#00e676"))
        self.ui.tbl_saturazione.setItem(r, 4, item_sat)
        
        for c in range(5):
            item = self.ui.tbl_saturazione.item(r, c)
            if item:
                if is_totale:
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                    if c != 4: item.setForeground(QColor("#ffecb3"))
                elif c != 4: item.setForeground(QColor("#ffffff"))

    def _inserisci_riga_stress(self, nome, stagione, noli, tetto, sforate, is_totale=False):
        r = self.ui.tbl_stagionali_noli.rowCount()
        self.ui.tbl_stagionali_noli.insertRow(r)
        esaurimento_perc = (noli / tetto * 100) if tetto > 0 else (100.0 if noli > 0 else 0.0)
        
        self.ui.tbl_stagionali_noli.setItem(r, 0, QTableWidgetItem(nome if not is_totale else ""))
        self.ui.tbl_stagionali_noli.setItem(r, 1, QTableWidgetItem(stagione))
        self.ui.tbl_stagionali_noli.setItem(r, 2, QTableWidgetItem(f"{self.locale_it.toString(float(noli), 'f', 1)} h"))
        self.ui.tbl_stagionali_noli.setItem(r, 3, QTableWidgetItem(f"{self.locale_it.toString(float(tetto), 'f', 1)} h"))
        self.ui.tbl_stagionali_noli.setItem(r, 4, QTableWidgetItem(f"{self.locale_it.toString(float(esaurimento_perc), 'f', 1)}%"))
        
        item_sforate = QTableWidgetItem(f"{self.locale_it.toString(float(sforate), 'f', 1)} h")
        if sforate > 0: 
            item_sforate.setForeground(QColor("#ff5252"))
            item_sforate.setFont(QFont("Arial", 11, QFont.Bold))
        else: item_sforate.setForeground(QColor("#00e676"))
        self.ui.tbl_stagionali_noli.setItem(r, 5, item_sforate)
        
        for c in range(6):
            item = self.ui.tbl_stagionali_noli.item(r, c)
            if item:
                if is_totale:
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                    if c != 5: item.setForeground(QColor("#ffecb3"))
                elif c != 5: item.setForeground(QColor("#ffffff"))

    # =========================================================
    # TAB 4: DIAGNOSTICA ANOMALIE
    # =========================================================

    def _popola_tabella_anomalie(self):
        if not self.tbl_log_anomalie: return
        self.tbl_log_anomalie.setRowCount(0)
        
        mappa_op = self._costruisci_mappa_operazioni()
        storico = getattr(self.parametri, "storico_stagionale", {})
        
        for chiave_stagione, dati in storico.items():
            if "RisorseExtra" in chiave_stagione: continue
            
            risultati = dati.get("risultati_cantieri", {})
            operazioni = risultati.get("dettaglio_operazioni", [])
            tagli_effettuati = risultati.get("tagli_effettuati", [])
            
            try:
                parts = chiave_stagione.split("_")
                anno_str = parts[0].replace("A", "") 
                stagione = parts[1]
            except (IndexError, ValueError):
                continue
            
            # --- FASE 1: Rilevamento Anomalie Operative ---
            for op in operazioni:
                stato_originale = str(op.get("stato", "")).strip()
                stato_lower = stato_originale.lower()
                
                if stato_lower == "" or (stato_lower.startswith("eseguito") and "parziale" not in stato_lower):
                    continue
                
                id_op = op.get("id_operazione", "")
                desc_operazione = mappa_op.get(id_op, id_op) 
                    
                riga = self.tbl_log_anomalie.rowCount()
                self.tbl_log_anomalie.insertRow(riga)
                
                self.tbl_log_anomalie.setItem(riga, 0, QTableWidgetItem(f"Anno {anno_str}"))
                self.tbl_log_anomalie.setItem(riga, 1, QTableWidgetItem(stagione))
                self.tbl_log_anomalie.setItem(riga, 2, QTableWidgetItem(str(op.get("lotto_id", ""))))
                self.tbl_log_anomalie.setItem(riga, 3, QTableWidgetItem(desc_operazione)) 
                
                item_stato = QTableWidgetItem(stato_originale)
                if "parziale" in stato_lower: item_stato.setForeground(QColor("#ff9800"))
                else: item_stato.setForeground(QColor("#ff5252"))
                self.tbl_log_anomalie.setItem(riga, 4, item_stato) 

            # --- FASE 2: Rilevamento Ritardi Biologici / Omissioni ---
            if stagione == "Inverno":
                stato_pre = dati.get("stato_lotti_pre", {})
                lotti_tagliati_ids = [t.get("lotto_id") for t in tagli_effettuati]
                
                for lotto_id, info in stato_pre.items():
                    lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == lotto_id), None)
                    if not lotto_reale: continue
                        
                    eta = info.get("eta", 0)
                    dbh = info.get("biometria", {}).get("dbh_reale_cm", 0.0)
                    eta_rot = 5 if lotto_reale.destinazione_uso == "INDUSTRIA" else 10
                    target_dbh = 15.0 if lotto_reale.destinazione_uso == "INDUSTRIA" else 30.0
                    
                    if eta >= eta_rot and lotto_id not in lotti_tagliati_ids:
                        motivo = ""
                        desc_operazione = "Taglio Raso (Fine Turno)" 
                        
                        if dbh < target_dbh:
                            motivo = "Ritardo Biologico (Immaturo)"
                        else:
                            gia_loggato = any(op.get("lotto_id") == lotto_id and op.get("id_operazione", "").startswith("OP_RAC") for op in operazioni)
                            if not gia_loggato:
                                motivo = "Taglio Omesso (Zero Risorse)"
                                
                        if motivo:
                            riga = self.tbl_log_anomalie.rowCount()
                            self.tbl_log_anomalie.insertRow(riga)
                            
                            self.tbl_log_anomalie.setItem(riga, 0, QTableWidgetItem(f"Anno {anno_str}"))
                            self.tbl_log_anomalie.setItem(riga, 1, QTableWidgetItem(stagione))
                            self.tbl_log_anomalie.setItem(riga, 2, QTableWidgetItem(lotto_id))
                            self.tbl_log_anomalie.setItem(riga, 3, QTableWidgetItem(desc_operazione)) 
                            
                            item_stato = QTableWidgetItem(motivo)
                            item_stato.setForeground(QColor("#c2185b")) 
                            self.tbl_log_anomalie.setItem(riga, 4, item_stato) 
                            
                            
                            

    def _diagnostica_fallimento(self, chiave_stagione, id_lotto, operazione, stato, op_data, fabbisogno, lavorate, perc, piante_rimaste_txt):
        storico = getattr(self.parametri, "storico_stagionale", {})
        dati_stagione = storico.get(chiave_stagione, {})
        stato_pre = dati_stagione.get("stato_lotti_pre", {}).get(id_lotto, {})
        
        diagnosi = []
        
        if "Ritardo Biologico" in stato:
            dbh = stato_pre.get("biometria", {}).get("dbh_reale_cm", 0.0)
            eta = stato_pre.get("eta", 0)
            diagnosi.append(f"• Età Raggiunta: Il lotto ha {eta} anni (fine turno), ma non ha la maturità commerciale.")
            diagnosi.append(f"• Dettaglio Biometrico: Il diametro (DBH) rilevato è di {dbh:.2f} cm. Almeno un clone in questo lotto sta subendo stress pedoclimatici o competizione da sovradensità.")
            diagnosi.append("• Azione: Il cantiere non è stato pianificato per evitare perdite finanziarie.")
            return "\n\n".join(diagnosi)
            
        if "Omesso" in stato or "Zero Risorse" in stato:
            eta = stato_pre.get("eta", 0)
            diagnosi.append(f"• Analisi Logistica: Il lotto ha {eta} anni ed è pronto per la vendita.")
            diagnosi.append("• Problema: La capacità aziendale (ore interne + noli massimi concessi sul mercato) è collassata a causa di altri cantieri prioritari.")
            diagnosi.append("• Azione: Taglio rinviato all'Inverno successivo. Il capitale rimane bloccato in bosco.")
            return "\n\n".join(diagnosi)

        if op_data:
            priorita = op_data.get("priorita", "N/A")
            
            if "Parziale" in stato:
                diagnosi.append(f"• Diagnosi di Cantiere: L'operazione '{operazione}' (Priorità {priorita}) è stata avviata ma interrotta.")
                diagnosi.append(f"• Il Blocco: Il cantiere aveva un fabbisogno totale stimato di {fabbisogno:.1f}h per processare l'intero lotto, ma ha potuto lavorare solo per {lavorate:.1f}h ({perc}% del completamento). L'arresto è avvenuto per esaurimento del plafond orario disponibile.")
                if piante_rimaste_txt:
                    diagnosi.append(f"• Impatto Fisico: Il taglio parziale ha lasciato in piedi {piante_rimaste_txt} piante. Il cantiere dovrà essere riaperto nella prossima finestra utile.")
                else:
                    diagnosi.append("• Conseguenze: Il lotto subisce un malus colturale proporzionale alla parte di lavoro non eseguita.")
            else:
                diagnosi.append(f"• Diagnosi di Cantiere: L'operazione '{operazione}' (Priorità {priorita}) aveva un fabbisogno di {fabbisogno:.1f}h.")
                diagnosi.append("• Il Blocco: Il cantiere NON è partito. Le macchine sono state interamente assorbite da lotti prioritari.")
                
            return "\n\n".join(diagnosi)
            
        return "Nessuna informazione di dettaglio disponibile nel log storico."
    
    @Slot()
    def on_riga_anomalia_selezionata(self):
        if not hasattr(self, 'tbl_log_anomalie') or not self.tbl_log_anomalie: return
        
        row = self.tbl_log_anomalie.currentRow()
        if row < 0 or self.tbl_log_anomalie.item(row, 0) is None: return
            
        anno_txt = self.tbl_log_anomalie.item(row, 0).text().replace("Anno ", "")
        stagione = self.tbl_log_anomalie.item(row, 1).text()
        id_lotto = self.tbl_log_anomalie.item(row, 2).text()
        operazione = self.tbl_log_anomalie.item(row, 3).text()
        stato = self.tbl_log_anomalie.item(row, 4).text()
        chiave_stagione = f"A{anno_txt}_{stagione}"
        
        if hasattr(self, 'lbl_stato_dettaglio') and self.lbl_stato_dettaglio: 
            self.lbl_stato_dettaglio.setText(f"OPERAZIONE: {operazione} | STATO: {stato.upper()}")
        
        storico = getattr(self.parametri, "storico_stagionale", {})
        dati_stagione = storico.get(chiave_stagione, {})
        operazioni = dati_stagione.get("risultati_cantieri", {}).get("dettaglio_operazioni", [])
        op_data = next((op for op in operazioni if op.get("lotto_id") == id_lotto and stato in op.get("stato", "")), None)
        
        fabbisogno = 0.0
        lavorate = 0.0
        perc = 0
        piante_rimaste_txt = ""

        if self.tbl_bilancio_risorse:
            self.tbl_bilancio_risorse.setRowCount(0)
            if op_data:
                richieste_json = float(op_data.get("durata_cantiere_h", 0.0))
                lavorate = float(op_data.get("ore_lavoro_totali", 0.0))
                lotto_obj = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto), None)
                
                # RICALCOLO INTELLIGENTE DEL FABBISOGNO REALE
                if "Taglio" in operazione or "RAC" in op_data.get("id_operazione", ""):
                    tagli_eff = dati_stagione.get("risultati_cantieri", {}).get("tagli_effettuati", [])
                    taglio = next((t for t in tagli_eff if t.get("lotto_id") == id_lotto), None)
                    stato_pre = dati_stagione.get("stato_lotti_pre", {}).get(id_lotto, {})
                    vol_pre = float(stato_pre.get("biometria", {}).get("volume_totale_m3", 0.001))
                    piante_pre = int(stato_pre.get("biometria", {}).get("piante_attive", 0))

                    if taglio and vol_pre > 0:
                        vol_raccolto = float(taglio.get("volume_raccolto_m3", 0.0))
                        perc_reale = vol_raccolto / vol_pre
                        perc = int(perc_reale * 100)
                        
                        piante_tagliate = int(piante_pre * perc_reale)
                        piante_rimaste = piante_pre - piante_tagliate
                        if piante_rimaste > 0: piante_rimaste_txt = str(piante_rimaste)

                        if 0 < perc_reale < 1: fabbisogno = lavorate / perc_reale
                        else: fabbisogno = lavorate
                    else:
                        fabbisogno = lotto_obj.superficie_ettari * 30.0 if lotto_obj else lavorate * 2
                else:
                    if "Parziale" in stato and lavorate == richieste_json:
                        ore_ha = 4.5 if "Sarchiatura" in operazione else 8.0
                        fabbisogno = (lotto_obj.superficie_ettari * ore_ha) if lotto_obj else lavorate * 2
                        if fabbisogno > 0: perc = int((lavorate / fabbisogno) * 100)
                    else:
                        fabbisogno = richieste_json
                        if fabbisogno > 0: perc = int((lavorate / fabbisogno) * 100)

                if "Bloccato" in stato or lavorate == 0: perc = 0
                perc = max(0, min(perc, 100))
                fabbisogno = max(fabbisogno, lavorate)
                deficit = fabbisogno - lavorate
                
                if hasattr(self, 'pb_avanzamento_cantiere') and self.pb_avanzamento_cantiere: 
                    self.pb_avanzamento_cantiere.setValue(perc)
                
                riga_tab = self.tbl_bilancio_risorse.rowCount()
                self.tbl_bilancio_risorse.insertRow(riga_tab)
                
                macchina_str = "Harvester/Forwarder" if "Taglio" in operazione else "Squadra/Trattori"
                self.tbl_bilancio_risorse.setItem(riga_tab, 0, QTableWidgetItem(macchina_str))
                self.tbl_bilancio_risorse.setItem(riga_tab, 1, QTableWidgetItem(f"{fabbisogno:.1f} h"))
                self.tbl_bilancio_risorse.setItem(riga_tab, 2, QTableWidgetItem(f"{lavorate:.1f} h"))
                
                item_def = QTableWidgetItem(f"{deficit:.1f} h")
                if deficit > 0: item_def.setForeground(QColor("#ff5252")) 
                self.tbl_bilancio_risorse.setItem(riga_tab, 3, item_def)
            else:
                if hasattr(self, 'pb_avanzamento_cantiere') and self.pb_avanzamento_cantiere: 
                    self.pb_avanzamento_cantiere.setValue(0)
            
        if hasattr(self, 'txt_diagnostica') and self.txt_diagnostica:
            spiegazione = self._diagnostica_fallimento(chiave_stagione, id_lotto, operazione, stato, op_data, fabbisogno, lavorate, perc, piante_rimaste_txt)
            self.txt_diagnostica.setText(spiegazione)
            
        if hasattr(self, 'btn_vai_allo_storico') and self.btn_vai_allo_storico:
            self.btn_vai_allo_storico.setEnabled(True)
            self.btn_vai_allo_storico.setProperty("lotto_target", id_lotto)
            
            
    @Slot()
    def azione_vai_allo_storico(self):
        if not self.btn_vai_allo_storico: return
        id_lotto = self.btn_vai_allo_storico.property("lotto_target")
        
        if id_lotto and self.tab_root and self.cmb_scelta_lotto:
            self.tab_root.setCurrentIndex(1) # Ti porta al tab dello storico
            idx = self.cmb_scelta_lotto.findText(id_lotto)
            if idx >= 0:
                self.cmb_scelta_lotto.setCurrentIndex(idx)