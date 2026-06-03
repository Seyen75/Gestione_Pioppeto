# GUI/form_valutazioni.py
import os
from typing import Dict, Any, List

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QComboBox, QSlider, QLabel, QPushButton, QTabWidget, QVBoxLayout, QHeaderView
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

        # 1. Caricamento UI e mappatura componenti
        self._carica_interfaccia()
        self._mappa_componenti_ui()
        self._inizializza_canvas_grafico()
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

    def _mappa_componenti_ui(self):
        self.tab_root = self.ui.findChild(QTabWidget, "tab_valutazioni_root")
        
        if self.tab_root:
            barra_tab = self.tab_root.tabBar()
            barra_tab.setExpanding(False)
        
        self.sld_anno = self.ui.findChild(QSlider, "sld_anno_report")
        self.lbl_anno_selezionato = self.ui.findChild(QLabel, "lbl_anno_selezionato")
        self.widget_canvas_tab1 = self.ui.findChild(QWidget, "canvas_ripartizione_lotti")
        
        self.tbl_tagli_anno = self.ui.findChild(QTableWidget, "tbl_tagli_anno")
        if self.tbl_tagli_anno is None:
            tab_1 = self.ui.findChild(QWidget, "tab_consuntivo_annuale")
            if tab_1:
                self.tbl_tagli_anno = tab_1.findChild(QTableWidget, "tbl_tagli_anno")
        
        self.lbl_res_opera_anno = self.ui.findChild(QLabel, "lbl_res_opera_anno")
        self.lbl_res_cartiera_anno = self.ui.findChild(QLabel, "lbl_res_cartiera_anno")
        self.lbl_res_truciolato_anno = self.ui.findChild(QLabel, "lbl_res_truciolato_anno")
        self.lbl_resa_ettaro_media_anno = self.ui.findChild(QLabel, "lbl_resa_ettaro_media_anno")

        self.cmb_scelta_lotto = self.ui.findChild(QComboBox, "cmb_scelta_lotto")
        self.lbl_tipo_filiera_lotto = self.ui.findChild(QLabel, "lbl_tipo_filiera_lotto")
        self.lbl_titolo_lotto = self.ui.findChild(QLabel, "lbl_titolo_lotto")
        
        # FIX 1: Riallineamento nome reale del componente rispetto al file .ui
        self.tbl_storico_lotto = self.ui.findChild(QTableWidget, "tbl_storico_lotto")
        if self.tbl_storico_lotto is None:
            tab_2 = self.ui.findChild(QWidget, "tab_storico_particella")
            if tab_2:
                self.tbl_storico_lotto = tab_2.findChild(QTableWidget, "tbl_storico_lotto")

        self.btn_esci = self.ui.findChild(QPushButton, "btn_esci")


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
        if self.sld_anno:
            self.sld_anno.valueChanged.connect(self.slot_cambio_anno_slider)
        if self.cmb_scelta_lotto:
            self.cmb_scelta_lotto.currentTextChanged.connect(self.slot_cambio_lotto_combobox)

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
        
        if self.sld_anno:
            self.sld_anno.setMinimum(1)
            self.sld_anno.setMaximum(self.anno_max)
            self.sld_anno.setValue(1) 
        
        if self.cmb_scelta_lotto:
            self.cmb_scelta_lotto.clear()
            for lotto in self.parametri.collezione_lotti:
                self.cmb_scelta_lotto.addItem(lotto.id_lotto)

        # --- FIX: Stop alla dilatazione dell'ultima colonna ---
        if self.tbl_storico_lotto:
            header = self.tbl_storico_lotto.horizontalHeader()
            # Tutte le colonne si adattano al loro contenuto (titolo o dato)
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            # Impedisce forzatamente a Qt di allargare l'ultima colonna fino al bordo destro
            header.setStretchLastSection(False) 

        # Innesco forzato iniziale controlli
        self.slot_cambio_anno_slider(1)
        if self.cmb_scelta_lotto and self.cmb_scelta_lotto.count() > 0:
            self.slot_cambio_lotto_combobox(self.cmb_scelta_lotto.currentText())
    
    def _costruisci_mappa_operazioni(self) -> dict:
        """Crea un dizionario piatto {ID_OPERAZIONE: DESCRIZIONE_ESTESA}"""
        mappa = {}
        for destinazione, fasi in STRUTTURA_LAVORAZIONI.items():
            for fase, stagioni in fasi.items():
                for stagione, operazioni in stagioni.items():
                    for op in operazioni:
                        mappa[op["id_operazione"]] = op["descrizione"]
        return mappa

    @Slot(int)
    def slot_cambio_anno_slider(self, anno_selezionato: int):
        """Estrae ed aggrega i cantieri conclusi nelle 4 stagioni dell'anno selezionato."""
        if self.lbl_anno_selezionato:
            self.lbl_anno_selezionato.setText(f"Visualizzazione Consuntivo Anno: {anno_selezionato}")
            
        if self.tbl_tagli_anno is None:
            return

        # --- FIX: Rimodellazione dinamica delle 10 colonne ---
        intestazioni = [
            "ID Lotto", 
            "Destinazione", 
            "Superficie\n(ha)", 
            "Vol. Raccolto\n(m³)", 
            "Resa Opera\n(m³)", 
            "Resa Cartiera\n(t)", 
            "Resa Truciolato\n(t)",
            "Resa/Ha Opera\n(m³/ha)", 
            "Resa/Ha Cartiera\n(t/ha)", 
            "Resa/Ha Truciolato\n(t/ha)"
        ]
        self.tbl_tagli_anno.setColumnCount(len(intestazioni))
        self.tbl_tagli_anno.setHorizontalHeaderLabels(intestazioni)
        self.tbl_tagli_anno.setRowCount(0)
        
        # Manteniamo l'adattamento automatico delle larghezze per non tagliare il testo
        header = self.tbl_tagli_anno.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        tot_opera = 0.0
        tot_cartiera = 0.0
        tot_truciolato = 0.0
        superficie_tagliata_anno = 0.0
        dati_grafico_lotti = []

        dizionario_completo = getattr(self.parametri, "storico_stagionale", {})
        stagioni_target = [f"A{anno_selezionato}_Primavera", f"A{anno_selezionato}_Estate", f"A{anno_selezionato}_Autunno", f"A{anno_selezionato}_Inverno"]
        
        for chiave_passo in stagioni_target:
            if chiave_passo not in dizionario_completo:
                continue
                
            istantanea = dizionario_completo[chiave_passo]
            risultati_cantieri = istantanea.get("risultati_cantieri", {})
            tagli = risultati_cantieri.get("tagli_effettuati", []) if risultati_cantieri else []
            
            for t in tagli:
                id_lotto = t.get("lotto_id", "")
                volume_totale_cantiere = t.get("volume_raccolto_m3", 0.0)
                rese = t.get("rese", {})
                
                lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto), None)
                if not lotto_reale:
                    continue
                    
                riga = self.tbl_tagli_anno.rowCount()
                self.tbl_tagli_anno.insertRow(riga)
                
                superficie = getattr(lotto_reale, "superficie_ettari", 5.0)
                destinazione = str(lotto_reale.destinazione_uso).strip().upper()
                
                vol_opera = rese.get("opera_m3", 0.0)
                massa_cartiera = rese.get("cartiera_t", 0.0)
                massa_truciolato = rese.get("truciolato_t", 0.0)
                
                # --- CALCOLO DELLE 3 RESE SPECIFICHE PER ETTARO ---
                resa_ha_opera = vol_opera / superficie if superficie > 0 else 0.0
                resa_ha_cartiera = massa_cartiera / superficie if superficie > 0 else 0.0
                resa_ha_truciolato = massa_truciolato / superficie if superficie > 0 else 0.0
                
                tot_opera += vol_opera
                tot_cartiera += massa_cartiera
                tot_truciolato += massa_truciolato
                superficie_tagliata_anno += superficie
                
                dati_grafico_lotti.append({
                    "id": id_lotto, "opera": vol_opera,
                    "cartiera": massa_cartiera, "truciolato": massa_truciolato
                })
                
                # --- POPOLAMENTO DELLE 10 COLONNE ---
                self.tbl_tagli_anno.setItem(riga, 0, QTableWidgetItem(id_lotto))
                self.tbl_tagli_anno.setItem(riga, 1, QTableWidgetItem(destinazione))
                self.tbl_tagli_anno.setItem(riga, 2, QTableWidgetItem(f"{superficie:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 3, QTableWidgetItem(f"{volume_totale_cantiere:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 4, QTableWidgetItem(f"{vol_opera:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 5, QTableWidgetItem(f"{massa_cartiera:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 6, QTableWidgetItem(f"{massa_truciolato:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 7, QTableWidgetItem(f"{resa_ha_opera:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 8, QTableWidgetItem(f"{resa_ha_cartiera:.2f}"))
                self.tbl_tagli_anno.setItem(riga, 9, QTableWidgetItem(f"{resa_ha_truciolato:.2f}"))

                for c in range(10):
                    item = self.tbl_tagli_anno.item(riga, c)
                    if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Aggiornamento delle Label in basso
        if self.lbl_res_opera_anno:
            self.lbl_res_opera_anno.setText(f"Tronchetti da Opera Totali: {tot_opera:.2f} m³")
        if self.lbl_res_cartiera_anno:
            self.lbl_res_cartiera_anno.setText(f"Legno da Cartiera Totale: {tot_cartiera:.2f} t")
        if self.lbl_res_truciolato_anno:
            self.lbl_res_truciolato_anno.setText(f"Fibra per Truciolato Totale: {tot_truciolato:.2f} t")
            
        resa_media_ha = ((tot_opera * 0.80) + tot_cartiera + tot_truciolato) / superficie_tagliata_anno if superficie_tagliata_anno > 0 else 0.0
        if self.lbl_resa_ettaro_media_anno:
            self.lbl_resa_ettaro_media_anno.setText(f"Resa Media Comprensoriale Equivalente: {resa_media_ha:.2f} t/ha")

        self._aggiorna_grafico_ripartizione(dati_grafico_lotti)

    @Slot(str)
    def slot_cambio_lotto_combobox(self, id_lotto_selezionato: str):
        """Gestisce l'evento di cambio selezione della combobox lotti."""
        if not id_lotto_selezionato or self.tbl_storico_lotto is None:
            return
            
        lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto_selezionato), None)
        if not lotto_reale:
            return
            
        if self.lbl_tipo_filiera_lotto:
            self.lbl_tipo_filiera_lotto.setText(f"Indirizzo Produttivo: Filiera da {lotto_reale.destinazione_uso} | Clone: {lotto_reale.clone_assegnato}")
            
        self._popola_tabella_lotto(lotto_reale)

    def _popola_tabella_lotto(self, lotto_reale):
        """Estrae i dati dal dizionario di memoria e compila le righe storiche."""
        if self.tbl_storico_lotto is None:
            return
            
        self.tbl_storico_lotto.setRowCount(0)
        
        if lotto_reale.destinazione_uso == "INDUSTRIA":
            eta_rotazione_standard = 5
            diametro_target = 15.0
        else:
            eta_rotazione_standard = 10
            diametro_target = 30.0
        
        dizionario_completo = getattr(self.parametri, "storico_stagionale", {})
        
        anni_rilevati = []
        for k in dizionario_completo.keys():
            if k.startswith("A") and "_" in k and not k.endswith("RisorseExtra"):
                parte_anno = k.split("_")[0]
                if parte_anno[1:].isdigit():
                    anni_rilevati.append(int(parte_anno[1:]))
                    
        anni_rilevati = sorted(list(set(anni_rilevati)))
        
        for num_anno in anni_rilevati:
            riga = self.tbl_storico_lotto.rowCount()
            self.tbl_storico_lotto.insertRow(riga)
            
            chiave_inverno = f"A{num_anno}_Inverno"
            
            è_tagliato = "NO"
            rese_effettive = {"opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}
            dati_congelati_taglio = {}

            if chiave_inverno in dizionario_completo:
                istanza_inverno = dizionario_completo[chiave_inverno]
                risultati_cantieri = istanza_inverno.get("risultati_cantieri", {})
                tagli_anno = risultati_cantieri.get("tagli_effettuati", []) if risultati_cantieri else []
                
                # Cerca il cantiere per questo specifico lotto
                for t in tagli_anno:
                    if t.get("lotto_id") == lotto_reale.id_lotto:
                        è_tagliato = "SÌ"
                        rese_effettive = t.get("rese", rese_effettive)
                        dati_congelati_taglio = t
                        break

                stato_lotti_anno = istanza_inverno.get("stato_lotti", {})
                dati_storici_lotto = stato_lotti_anno.get(lotto_reale.id_lotto, {})
                
                if è_tagliato == "SÌ":
                    eta_biologica = dati_congelati_taglio.get("eta_pre_taglio", eta_rotazione_standard)
                    piante_attive = dati_congelati_taglio.get("piante_pre_taglio", 0)
                    dbh_val = dati_congelati_taglio.get("dbh_pre_taglio", 0.0)
                    h_val = dati_congelati_taglio.get("altezza_pre_taglio", 0.0)
                else:
                    eta_biologica = dati_storici_lotto.get("eta", num_anno)
                    bio = dati_storici_lotto.get("biometria", {})
                    piante_attive = bio.get("piante_attive", 0)
                    dbh_val = bio.get("dbh_reale_cm", 0.0)
                    h_val = bio.get("altezza_m", 0.0)
            else:
                eta_biologica = num_anno
                piante_attive = lotto_reale.numero_piante_vive
                dbh_val, h_val = 0.0, 0.0
                è_tagliato = "NO"

            # --- VERIFICA DELLA MATURITÀ (Rispecchia fedelmente il motore) ---
            is_pronto = False
            if eta_biologica >= eta_rotazione_standard:
                if dbh_val >= diametro_target:
                    is_pronto = True
                elif è_tagliato == "SÌ": 
                    is_pronto = True

            pronto_al_taglio = "SÌ" if is_pronto else "NO"

            # --- POPOLAMENTO VISIVO ---
            self.tbl_storico_lotto.setItem(riga, 0, QTableWidgetItem(f"Anno {num_anno}"))
            self.tbl_storico_lotto.setItem(riga, 1, QTableWidgetItem(f"{eta_biologica} anni"))
            self.tbl_storico_lotto.setItem(riga, 2, QTableWidgetItem(f"{dbh_val:.2f} cm"))
            self.tbl_storico_lotto.setItem(riga, 3, QTableWidgetItem(f"{h_val:.2f} m"))
            self.tbl_storico_lotto.setItem(riga, 4, QTableWidgetItem(f"{piante_attive} fusti"))
            
            item_pronto = QTableWidgetItem(pronto_al_taglio)
            if pronto_al_taglio == "SÌ": item_pronto.setForeground(Qt.GlobalColor.green)
            self.tbl_storico_lotto.setItem(riga, 5, item_pronto)
            
            # Il nostro indicatore diagnostico
            item_tagliato = QTableWidgetItem(è_tagliato)
            if è_tagliato == "SÌ": 
                item_tagliato.setForeground(Qt.GlobalColor.yellow)
            elif pronto_al_taglio == "SÌ" and è_tagliato == "NO":
                # Opzionale: Colora di rosso il "NO" se l'albero era pronto ma è stato saltato (Ritardo Strutturale)
                item_tagliato.setForeground(Qt.GlobalColor.red)
                
            self.tbl_storico_lotto.setItem(riga, 6, item_tagliato)
            
            self.tbl_storico_lotto.setItem(riga, 7, QTableWidgetItem(f"{rese_effettive.get('opera_m3', 0.0):.2f} m³"))
            self.tbl_storico_lotto.setItem(riga, 8, QTableWidgetItem(f"{rese_effettive.get('cartiera_t', 0.0):.2f} t"))
            self.tbl_storico_lotto.setItem(riga, 9, QTableWidgetItem(f"{rese_effettive.get('truciolato_t', 0.0):.2f} t"))

            for c in range(10):
                item = self.tbl_storico_lotto.item(riga, c)
                if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
    def _aggiorna_grafico_ripartizione(self, dati_lotti: List[Dict[str, Any]]):
        if not hasattr(self, 'ax_ripartizione'):
            return
            
        self.ax_ripartizione.clear()
        
        if not dati_lotti:
            self.ax_ripartizione.text(0.5, 0.5, "Nessun cantiere di taglio concluso\nin questo anno di esercizio", 
                                     color='#ff8a80', ha='center', va='center', fontsize=10, style='italic')
            self.ax_ripartizione.set_xticks([])
            self.ax_ripartizione.set_yticks([])
            self.canvas_ripartizione.draw()
            return

        nomi_lotti = [d["id"] for d in dati_lotti]
        opera = np.array([d["opera"] for d in dati_lotti])
        cartiera = np.array([d["cartiera"] for d in dati_lotti])
        truciolato = np.array([d["truciolato"] for d in dati_lotti])

        # --- FIX 1: Larghezza colonna ridotta e fissa ---
        larghezza_colonna = 0.35 
        x_pos = np.arange(len(nomi_lotti))
        
        self.ax_ripartizione.bar(x_pos, opera, width=larghezza_colonna, label='Opera', color='#b71c1c')
        self.ax_ripartizione.bar(x_pos, cartiera, bottom=opera, width=larghezza_colonna, label='Cartiera', color='#e65100')
        self.ax_ripartizione.bar(x_pos, truciolato, bottom=opera+cartiera, width=larghezza_colonna, label='Truciolato', color='#ffca28')
                
        self.ax_ripartizione.set_xticks(x_pos)
        self.ax_ripartizione.set_xticklabels(nomi_lotti)

        # --- FIX 2: Trucco per impedire colonne dilatate ---
        # Garantiamo sempre una "finestra" visiva di almeno 6 spazi. 
        # Se c'è 1 solo lotto, lo metterà al centro senza ingrandirlo.
        min_slots = 4
        if len(nomi_lotti) < min_slots:
            margine = (min_slots - len(nomi_lotti)) / 2.0
            self.ax_ripartizione.set_xlim(-margine - 0.5, len(nomi_lotti) - 1 + margine + 0.5)

        # Solleviamo il titolo (pad=30) per fare spazio alla legenda
        self.ax_ripartizione.set_title("Ripartizione Assoluta Masse Raccolte", color='#ff8a80', fontsize=11, weight='bold', pad=30)
        self.ax_ripartizione.tick_params(colors='#e0e0e0', labelsize=8)
        
        # Mettiamo solo la griglia orizzontale (axis='y') per un look più pulito
        self.ax_ripartizione.grid(True, color='#2b1d20', linestyle='--', alpha=0.5, axis='y')
        
        # --- FIX 3: Legenda in alto orizzontale (ncol=3) fuori dal tracciato ---
        legenda = self.ax_ripartizione.legend(
            loc='lower center', 
            bbox_to_anchor=(0.5, 1.02), 
            ncol=3,
            facecolor='#141923', 
            edgecolor='#3d2429', 
            fontsize=8,
            framealpha=1.0
        )
        for text in legenda.get_texts():
            text.set_color('#e0e0e0')

        # Sostituiamo tight_layout con subplots_adjust per evitare che la legenda alta venga mozzata
        self.fig_ripartizione.subplots_adjust(top=0.78, bottom=0.15, left=0.15, right=0.95)
        self.canvas_ripartizione.draw()