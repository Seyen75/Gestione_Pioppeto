# GUI/form_valutazioni.py
import os
from typing import Dict, Any, List

# Importazioni PySide6 per la gestione dell'interfaccia grafica
from PySide6.QtCore import Slot, Qt, QLocale
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QComboBox, QLabel, QPushButton, QTabWidget, QVBoxLayout, QHeaderView, QProgressBar, QTextEdit, QScrollArea
from PySide6.QtGui import QScreen, QGuiApplication
from PySide6.QtGui import QColor, QFont
from PySide6.QtUiTools import QUiLoader

from GUI.utils import centra_finestra

# Importazioni Matplotlib per la visualizzazione dei grafici
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
from matplotlib.figure import Figure
import mplcursors

# Importazioni NumPy per eventuali calcoli numerici
import numpy as np

# Importazioni personalizzate per la gestione della struttura delle lavorazioni e dei dati del motore di simulazione
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class FormValutazioni(QWidget):
    def __init__(self, motore_simulazione, parent=None):
        super().__init__(parent)
        self.motore = motore_simulazione
        self.parametri = motore_simulazione.parametri

        # Inizializza il modulo QLocale per la formattazione italiana dei dati numerici e delle date, garantendo la corretta visualizzazione dei valori con separatori decimali e migliaia secondo le convenzioni locali
        self.locale_it = QLocale(QLocale.Italian, QLocale.Italy)

        self.DIM_W = 1150
        self.DIM_H = 790
        
        # Caricamento UI e mappatura componenti
        self._carica_interfaccia()
        self._mappa_componenti_ui()
        self._inizializza_canvas_dei_grafici()
        self._inzializza_impostazioni_tabelle()
        self._connetti_segnali()
        
        # Configurazione e popolamento iniziale dei dati
        self._configura_stato_iniziale_selettori()

    # --- FUNZIONI GESTORE GRAFICA FORM ---
    
    def showEvent(self, event):
        '''Gestisce l'evento Show per richiamare la funzione per centrare la finestra allo schermo'''
        super().showEvent(event)
        centra_finestra(self, self.DIM_W, self.DIM_H)
    
    
    def _carica_interfaccia(self):
        '''Carica l'interfaccia della form dal file .ui creato con Qt Design'''
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_valutazioni.ui")
        self.ui = loader.load(percorso_ui, self)
        
        layout_principale = QVBoxLayout(self)
        layout_principale.addWidget(self.ui)
        layout_principale.setContentsMargins(15, 15, 15, 15)
        
        self.setWindowTitle("Report Finale e Statistiche Consuntive")
        
  
    def _mappa_componenti_ui(self):
        '''Funzione che mappa i componenti principali dell'interfaccia grafica come attributi della classe, 
           facilitando l'accesso e la manipolazione dei dati nei vari slot e funzioni di aggiornamento'''
        
        # Componente Tab principale
        self.tab_root = self.ui.findChild(QTabWidget, "tab_valutazioni_root")
        
        if self.tab_root:
            barra_tab = self.tab_root.tabBar()
            barra_tab.setExpanding(False)
        
        # TAB 1 - Componenti Consuntivo annuale
        self.cmb_anno_report = self.ui.findChild(QComboBox, "cmb_anno_report")
        self.lbl_anno_selezionato = self.ui.findChild(QLabel, "lbl_anno_selezionato")
        self.widget_canvas_tab1 = self.ui.findChild(QWidget, "canvas_ripartizione_lotti")
        
        self.tbl_tagli_anno = self.ui.findChild(QTableWidget, "tbl_tagli_anno")
        if self.tbl_tagli_anno is None:
            tab_1 = self.ui.findChild(QWidget, "tab_consuntivo_annuale")
            if tab_1:
                self.tbl_tagli_anno = tab_1.findChild(QTableWidget, "tbl_tagli_anno")
        
        
        # TAB 2 - Componenti Fascicolo Storico Particella
        self.cmb_scelta_lotto = self.ui.findChild(QComboBox, "cmb_scelta_lotto")
        self.lbl_tipo_filiera_lotto = self.ui.findChild(QLabel, "lbl_tipo_filiera_lotto")
        self.lbl_titolo_lotto = self.ui.findChild(QLabel, "lbl_titolo_lotto")
        
        self.tbl_storico_lotto = self.ui.findChild(QTableWidget, "tbl_storico_lotto")
        if self.tbl_storico_lotto is None:
            tab_2 = self.ui.findChild(QWidget, "tab_storico_particella")
            if tab_2:
                self.tbl_storico_lotto = tab_2.findChild(QTableWidget, "tbl_storico_lotto")
        
        
        # TAB 3 - Capacità Operative        
        self.cmb_anno_report_capacita = self.ui.findChild(QComboBox, "cmb_anno_report_capacita")
        self.tbl_saturazione = self.ui.findChild(QTableWidget, "tbl_saturazione")
        self.tbl_stagionali_noli = self.ui.findChild(QTableWidget, "tbl_stagionali_noli")
        self.lbl_tagli_falliti = self.ui.findChild(QLabel, "lbl_tagli_falliti")
        self.lbl_biologici_falliti = self.ui.findChild(QLabel, "lbl_biologici_falliti")
        self.lbl_generici_falliti = self.ui.findChild(QLabel, "lbl_generici_falliti")
        
        
        # TAB 4 -  Registro dei Fallimenti Operativi
        self.tbl_log_anomalie = self.ui.findChild(QTableWidget, "tbl_log_anomalie")
        self.lbl_stato_dettaglio = self.ui.findChild(QLabel, "lbl_stato_dettaglio")
        self.pb_avanzamento_cantiere = self.ui.findChild(QProgressBar, "pb_avanzamento_cantiere")
        self.tbl_bilancio_risorse = self.ui.findChild(QTableWidget, "tbl_bilancio_risorse")
        self.txt_diagnostica = self.ui.findChild(QTextEdit, "txt_diagnostica")
        self.btn_vai_allo_storico = self.ui.findChild(QPushButton, "btn_vai_allo_storico")
        
        self.btn_esci = self.ui.findChild(QPushButton, "btn_esci")
        
   
    def _inizializza_canvas_dei_grafici(self):
        '''Funzione che inizializza il canvas dei tre grafici presenti nelle TAB colori e layout per integrarsi armoniosamente con il tema scuro dell'applicazione
           e garantire una visualizzazione chiara dei dati. Aggiunge la scroll Area per i grafici della Tab 2'''
        
        colore_sfondo_hex = "#141923"
        
        # Recuper il canvas del grafico della Tab 1 - Consuntivo annuale
        self.fig_ripartizione = Figure(figsize = (5, 3), facecolor = colore_sfondo_hex)
        self.canvas_ripartizione = FigureCanvas(self.fig_ripartizione)
        self.ax_ripartizione = self.fig_ripartizione.add_subplot(111)
        self.ax_ripartizione.set_facecolor(colore_sfondo_hex)
        
        if self.widget_canvas_tab1:
            layout_grafico = QVBoxLayout(self.widget_canvas_tab1)
            layout_grafico.addWidget(self.canvas_ripartizione)
            layout_grafico.setContentsMargins(0, 0, 0, 0)

        # Recupera i canvas dei grafici della TAB 2 - Fascicolo Storico Lotto
        grafico_diametri = self.ui.findChild(QWidget, "widget_canvas_crescita")
        grafico_tot_piante = self.ui.findChild(QWidget, "widget_canvas_piante")
        
        # Creazione Figure e Canvas
        self.fig_crescita = Figure(figsize = (5, 3), facecolor = colore_sfondo_hex)
        self.canvas_crescita = FigureCanvas(self.fig_crescita)
        
        self.fig_piante = Figure(figsize = (5, 3), facecolor = colore_sfondo_hex)
        self.canvas_piante = FigureCanvas(self.fig_piante)
        
        # Aggiunge la ScrollArea per entrambi i grafici
        for p, c in [(grafico_diametri, self.canvas_crescita), (grafico_tot_piante, self.canvas_piante)]:
            layout = QVBoxLayout(p)
            layout.setContentsMargins(0, 0, 0, 0)
            
            scroll = QScrollArea()
            scroll.setWidget(c)
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setStyleSheet("QScrollArea { border: none; background: #141923; }")
            layout.addWidget(scroll)
   
   
    def _inzializza_impostazioni_tabelle(self):
        '''Funzione che configura le tabelle delle Tab, impostando il numero di colonne, le intestazioni, 
           il dimensionamento e lo stile generale per garantire chiarezza e leggibilità dei dati presentati'''
       
        # Tab 1 - Tabella tagli
        if self.tbl_tagli_anno:
            colonne_labels = [
                "ID Lotto", "Destinazione", "Superficie", "Vol.\nRaccolto", 
                "Resa\nOpera", "Massa\nCartiera", "Massa\nTruciolato", 
                "Resa/Ha\nOpera", "Resa/Ha\nCartiera", "Resa/Ha\nTruciolato"
            ]
            self.tbl_tagli_anno.setColumnCount(len(colonne_labels))
            self.tbl_tagli_anno.setHorizontalHeaderLabels(colonne_labels)
            
            # Impostazione altezza header per accomodare il testo su due righe
            header_tagli = self.tbl_tagli_anno.horizontalHeader()
            header_tagli.setMinimumHeight(50) 
            header_tagli.setSectionResizeMode(QHeaderView.ResizeToContents)
            
       
        # Tab 2 - Tabella Storico Lotto
        self.tbl_storico_lotto.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tbl_storico_lotto.horizontalHeader().setStretchLastSection(False)
                   
        # Tab 3 - Capacità Operative
        # Setup Tabella Saturazione Interna Risorse
        col_sat = ["Risorsa", "Stagione", "Ore\nDisponibili", "Ore\nLavorate", "%\nSaturaz."]
        self.tbl_saturazione.setColumnCount(len(col_sat))
        self.tbl_saturazione.setHorizontalHeaderLabels(col_sat)
        header_sat = self.tbl_saturazione.horizontalHeader()
        header_sat.setMinimumHeight(45)
        header_sat.setSectionResizeMode(QHeaderView.ResizeToContents)
        header_sat.setSectionResizeMode(0, QHeaderView.Stretch)
        header_sat.setStretchLastSection(False)
        
        # Setup Tabella Stress Test Noli
        col_stress = ["Risorsa", "Stagione", "Ore Extra\n(Noli)", "Tetto Max\nMercato", "%\nEsaurim."]
        self.tbl_stagionali_noli.setColumnCount(len(col_stress))
        self.tbl_stagionali_noli.setHorizontalHeaderLabels(col_stress)
        header_stress = self.tbl_stagionali_noli.horizontalHeader()
        header_stress.setMinimumHeight(45)
        header_stress.setSectionResizeMode(QHeaderView.ResizeToContents)
        header_stress.setSectionResizeMode(0, QHeaderView.Stretch)
        header_stress.setStretchLastSection(False)
         
        # Tab 4 - Registro Fallimento
        # Setup Tabella Anomalie
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
            
        # Setup Tabella Bilancio Risorse Intestazioni colonne per il bilancio risorse, con testo su più righe per chiarezza
        col_bil = ["Risorsa", "Fabbisogno Tot.", "Ore Lavorate", "Ore Mancanti"]
        self.tbl_bilancio_risorse.setColumnCount(len(col_bil))
        self.tbl_bilancio_risorse.setHorizontalHeaderLabels(col_bil)
        self.tbl_bilancio_risorse.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
    def _connetti_segnali(self):
        '''Funzione che connette i segnali dei componenti interattivi della form (come combobox, tabelle e bottoni) ai rispettivi slot, 
           garantendo che le azioni dell'utente attivino le funzioni di aggiornamento e visualizzazione dei dati in modo coerente e reattivo'''
        if self.btn_esci:
            self.btn_esci.clicked.connect(self.close)
        
        if hasattr(self, 'cmb_anno_report') and self.cmb_anno_report:
            self.cmb_anno_report.currentTextChanged.connect(self.slot_cambio_anno_combobox)
            
        if self.cmb_scelta_lotto:
            self.cmb_scelta_lotto.currentTextChanged.connect(self.slot_cambio_lotto_combobox)
            
        if hasattr(self, 'cmb_anno_report_capacita') and self.cmb_anno_report_capacita:
            self.cmb_anno_report_capacita.currentTextChanged.connect(self.slot_aggiorna_tab_efficienza)
            
        if self.tbl_log_anomalie:
            self.tbl_log_anomalie.cellClicked.connect(self.on_riga_anomalia_selezionata)
            
        if self.btn_vai_allo_storico:
            self.btn_vai_allo_storico.clicked.connect(self.azione_vai_allo_storico)
            
        if self.tbl_log_anomalie:
            # Sostituito cellClicked con itemSelectionChanged per prendere anche il click sull'header
            self.tbl_log_anomalie.itemSelectionChanged.connect(self.on_riga_anomalia_selezionata)

        
    def _configura_stato_iniziale_selettori(self):
        '''Funzione che configura lo stato iniziale dei selettori (combobox) e delle tabelle, popolando i dati iniziali 
           in base alle informazioni presenti nei parametri del motore di simulazione'''
           
        dizionario_storia = getattr(self.parametri, "storico_stagionale", {}) 
        anni_presenti = set()
        
        # Scansione sicura delle chiavi per identificare gli anni presenti, evitando errori in caso di chiavi non conformi o dati mancanti
        for k in dizionario_storia.keys():
            if k.startswith("A") and "_" in k:
                parte_anno = k.split("_")[0][1:]
                # Verifica che sia effettivamente un numero prima di aggiungerlo al set degli anni presenti
                if parte_anno.isdigit(): 
                    anni_presenti.add(int(parte_anno))
                    
        # Calcolo del ultimo anno presente in simulazione e lista degli anni simulati
        self.anno_max = max(anni_presenti) if anni_presenti else 1
        lista_anni = [str(a) for a in range(1, self.anno_max + 1)]

        # Popolamento componenti
        self.cmb_anno_report.clear()
        self.cmb_anno_report.addItems(lista_anni)
        
        self.cmb_scelta_lotto.clear()
        self.cmb_scelta_lotto.addItems([lotto.id_lotto for lotto in self.parametri.collezione_lotti])

        self.cmb_anno_report_capacita.clear()
        self.cmb_anno_report_capacita.addItems(lista_anni)
        
        # Esecuzione popolamenti iniziali
        self.slot_cambio_anno_combobox("1")
        self.slot_aggiorna_tab_efficienza("1")
            
        if self.cmb_scelta_lotto.count() > 0:
            self.slot_cambio_lotto_combobox(self.cmb_scelta_lotto.currentText())
        
        # Avvia il popolamento delle tabelle    
        self._popola_tabella_anomalie()
    

    # --- FUNZIONALITA' FORM ---
    
    def _costruisci_mappa_operazioni(self) -> dict:
        '''Funzione che costruisce una mappa rapida tra ID operazione e descrizione, facilitando la visualizzazione dei dati di raccolta 
           lavorazione nei report e nelle tabelle di valutazione'''
        mappa = {}
        for destinazione, fasi in STRUTTURA_LAVORAZIONI.items():
            for fase, stagioni in fasi.items():
                for stagione, operazioni in stagioni.items():
                    for op in operazioni:
                        mappa[op["id_operazione"]] = op["descrizione"]
        return mappa

    # Gli Slot si attivano al cambio di anno nella combobox, aggiornando la tabella dei tagli effettuati nell'anno selezionato   
    # L'uso del decoratore @Slot garantisce una connessione efficiente e tipizzata tra il segnale di cambio testo della combobox e la funzione di aggiornamento,
    # migliorando le prestazioni e la reattività dell'interfaccia utente durante la selezione di anni diversi per l'analisi dei dati di raccolta e lavorazione
    # E' un metodo usato da Qt ed il modulo PySide6 per ottimizzare la gestione dei segnali e degli slot, consentendo una comunicazione più efficiente tra i componenti dell'interfaccia grafica e le funzioni di elaborazione dei dati 
    # soprattutto quando si lavora con grandi quantità di informazioni o operazioni complesse di aggiornamento della UI.
    
    # TAB 1 - Consuntivo Tagli
    
    @Slot(str)
    def slot_cambio_anno_combobox(self, testo_anno: str):
        '''Funzione che gestisce il cambiamento di selezione nel combobox della TAB 1 - Consuntivo Annuale'''
        if not testo_anno: 
            return
        
        anno_selezionato = int(testo_anno)

        # Azzera la tabella ed inizializza i dati per popolare la tabella 
        self.tbl_tagli_anno.setRowCount(0)

        tot_opera, tot_cartiera, tot_truciolato = 0.0, 0.0, 0.0
        tot_vol_raccolto, superficie_tagliata_anno = 0.0, 0.0
        dati_grafico_lotti = []

        # Carica il dizionario delle stagioni simulate
        dizionario_completo = self.parametri.storico_stagionale
        chiave_inverno = f"A{anno_selezionato}_Inverno"
        
        # Ricerca nel dizionario la stagione invernale dell'anno selezionato, l'unica che può avere eventuali rese da taglio
        if chiave_inverno in dizionario_completo:
            # Carica dal dizionario la parte relativa alla stagione invernale dell'anno selezionata e da questa recupera la lista dei tagli, se esiste
            istantanea = dizionario_completo[chiave_inverno]
            risultati_cantieri = istantanea["risultati_cantieri"]
            tagli = risultati_cantieri.get("tagli_effettuati", []) if risultati_cantieri else []
            
            # Cicla su tutti i tagli presenti in lista
            for t in tagli:
                # Recupera le informazioni contenute nella lista tagli fra le quali le rese con i valori distinti per tipologia
                id_lotto = t["lotto_id"]
                # Estrae dalla lista t (taglio) la sottolista delle rese
                rese = t["rese"]
                volume_totale_cantiere = float(rese["volume_cantiere_m3"])
                
                # Scorre la lista della collezione lotti dell'oggetto parametri e cerca il primo valore che abbia il valore di id_lotto
                # inserisce i valori del lotto trovato nella variabile lotto_reale
                lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto), None)
                if not lotto_reale: continue
                
                # Inserisce una nuova riga nella tabella    
                riga = self.tbl_tagli_anno.rowCount()
                self.tbl_tagli_anno.insertRow(riga)
                
                # Recupera i dati di superficie e destinazione d'uso del lotto rilevato
                superficie = lotto_reale.superficie_ettari
                destinazione = str(lotto_reale.destinazione_uso).strip().upper()
                
                # Estrae i dati delle rese
                vol_opera = float(rese.get("opera_m3", 0.0))
                massa_cartiera = float(rese.get("cartiera_t", 0.0))
                massa_truciolato = float(rese.get("truciolato_t", 0.0))
                
                # Calcola la resa per ettaro
                resa_ha_opera = vol_opera / superficie
                resa_ha_cartiera = massa_cartiera / superficie
                resa_ha_truciolato = massa_truciolato / superficie
                
                # Somma i valori per il totale delle rese annuali
                tot_opera += vol_opera
                tot_cartiera += massa_cartiera
                tot_truciolato += massa_truciolato
                tot_vol_raccolto += volume_totale_cantiere
                superficie_tagliata_anno += superficie
                
                # Aggiunge i valori nella lista dei dati del grafico
                dati_grafico_lotti.append({"id": id_lotto, "opera": vol_opera, "cartiera": massa_cartiera, "truciolato": massa_truciolato})
                
                # Inserimento dati in tabella e per le componenti numeriche le trasforna in stringhe con le unità di misura di ognuna
                self.tbl_tagli_anno.setItem(riga, 0, QTableWidgetItem(id_lotto))
                self.tbl_tagli_anno.setItem(riga, 1, QTableWidgetItem(destinazione))
                self.tbl_tagli_anno.setItem(riga, 2, QTableWidgetItem(f"{self.locale_it.toString(float(superficie), 'f', 2)} ha"))
                self.tbl_tagli_anno.setItem(riga, 3, QTableWidgetItem(f"{self.locale_it.toString(float(volume_totale_cantiere), 'f', 2)} m³"))
                self.tbl_tagli_anno.setItem(riga, 4, QTableWidgetItem(f"{self.locale_it.toString(float(vol_opera), 'f', 2)} m³"))
                self.tbl_tagli_anno.setItem(riga, 5, QTableWidgetItem(f"{self.locale_it.toString(float(massa_cartiera), 'f', 2)} t"))
                self.tbl_tagli_anno.setItem(riga, 6, QTableWidgetItem(f"{self.locale_it.toString(float(massa_truciolato), 'f', 2)} t"))
                self.tbl_tagli_anno.setItem(riga, 7, QTableWidgetItem(f"{self.locale_it.toString(float(resa_ha_opera), 'f', 2)} m³"))
                self.tbl_tagli_anno.setItem(riga, 8, QTableWidgetItem(f"{self.locale_it.toString(float(resa_ha_cartiera), 'f', 2)} t"))
                self.tbl_tagli_anno.setItem(riga, 9, QTableWidgetItem(f"{self.locale_it.toString(float(resa_ha_truciolato), 'f', 2)} t"))

                # Centra i valori delle celle
                for c in range(10):
                    item = self.tbl_tagli_anno.item(riga, c)
                    if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        id_validi = {d["id"] for d in dati_grafico_lotti}

        # Calcola le superfici accedendo direttamente agli attributi della collezione 
        # Sfrutta la funzione sum in cui è presente una Espressione che cicla dentro la collezione Lotti e recupera i dati da sommare 
        # solo se corrispondono ai valori della destinazione d'uso specifica e se sono i lotti all'interno della lista id_validi che contiene i lotti dei tagli dell'anno
        sup_opera = sum(
            l.superficie_ettari 
            for l in self.parametri.collezione_lotti 
            if str(l.destinazione_uso).strip().upper() == "OPERA" and l.id_lotto in id_validi
        )

        sup_industria = sum(
            l.superficie_ettari 
            for l in self.parametri.collezione_lotti 
            if str(l.destinazione_uso).strip().upper() == "INDUSTRIA" and l.id_lotto in id_validi
        )

        # Effettua la media ettaro per resa
        media_ha_opera = (tot_opera / sup_opera) if sup_opera > 0 else 0.0
        media_ha_cartiera = (tot_cartiera / sup_industria) if sup_industria > 0 else 0.0
        media_ha_truciolato = (tot_truciolato / sup_industria) if sup_industria > 0 else 0.0

        # Dizionario con i valori totali e mappatura delle relative unità di misura con simbolo speciale da inserire nelle celle di riferimento
        valori_colonne = {3: tot_vol_raccolto, 4: tot_opera, 5: tot_cartiera, 6: tot_truciolato, 7: media_ha_opera, 8: media_ha_cartiera, 9: media_ha_truciolato}
        unita_misura = {3: "m³", 4: "m³", 5: "t", 6: "t", 7: "m³", 8: "t", 9: "t"}

        # Aggiornamento delle etichette sottostanti la tabella
        for col, valore in valori_colonne.items():
            nome_obj = f"lbl_tot_{col}"
            label_obj = self.ui.findChild(QLabel, nome_obj)
            if label_obj:
                header_item = self.tbl_tagli_anno.horizontalHeaderItem(col)
                testo_header = header_item.text().replace('\n', ' ') if header_item else f"Colonna {col}"
                valore_formattato = self.locale_it.toString(float(valore), 'f', 2)
                unita = unita_misura.get(col, "")
                label_obj.setText(f"Totale {testo_header}: {valore_formattato} {unita}")

        self._aggiorna_grafico_ripartizione(dati_grafico_lotti)

            
    def _aggiorna_grafico_ripartizione(self, dati_lotti: List[Dict[str, Any]]):
        '''Funzione che aggiorna il grafico di ripartizione dei risultati dei tagli effettuati nell'anno selezionato, 
           visualizzando la distribuzione in termini di volume raccolto per opera, cartiera e truciolato
           per ogni lotto tagliato, con una formattazione chiara e coerente con il tema scuro dell'applicazione 
           con l'aggiunta di una legenda per facilitare l'interpretazione dei dati da parte dell'utente, evidenziando eventuali assenze'''
        
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

    # TAB 2  - Storico Lotto

    @Slot(str)
    def slot_cambio_lotto_combobox(self, id_lotto_selezionato: str):
        '''Slot che si attiva al cambio di lotto nella combobox, aggiornando la tabella dello storico del lotto selezionato con i dati di crescita, 
           biometria e tagli effettuati negli anni precedenti,'''
           
        if not id_lotto_selezionato or self.tbl_storico_lotto is None:
            return
        
        # Recupera dalla collezione dei lotti il lotto con id_lotto_selezionato e lo inserisce in una variabile locale
        lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == id_lotto_selezionato), None)
        if not lotto_reale: return
        
        # Modifica il testo che indica i dati principali del lotto selezionato
        if self.lbl_tipo_filiera_lotto:
            self.lbl_tipo_filiera_lotto.setText(f"Indirizzo Produttivo: Filiera da {lotto_reale.destinazione_uso} | Clone: {lotto_reale.clone_assegnato}")
        
        # Avvia la funzione per popolare la tabella con la storia del lotto selezionato
        self._popola_tabella_storico_lotto(lotto_reale)
    
    
    def _popola_tabella_storico_lotto(self, lotto_reale):
        '''Funzione che popola la tabella dello storico del lotto selezionato, estraendo i dati di crescita, biometria e tagli effettuati negli anni precedenti
           e valutando se il lotto era pronto al taglio in base a criteri di età, diametro e stato di taglio, evidenziando con colori e formattazione
           le condizioni di prontezza e i risultati dei tagli effettuati negli anni per facilitare l'analisi visiva da parte dell'utente'''
        
        if self.tbl_storico_lotto is None: return
        # Azzera la tabella
        self.tbl_storico_lotto.setRowCount(0)
        
        # Sincronizza i parametri con il motore di accrescimento per 
        eta_rotazione_standard = 5 if lotto_reale.destinazione_uso == "INDUSTRIA" else 10
        
        # inserisce nella variabile locale lo storico stagionale della simulazione
        dizionario_completo = self.parametri.storico_stagionale
        
        # crea la lista con gli anni rilevati
        anni_rilevati = set()

        # Aggiungi tutti i valori da 1 al numero totale di item inclusi presenti nella cmb_anno_report che contiene già la lista degli anni
        anni_rilevati.update(range(1, self.cmb_anno_report.count() + 1))
                    
        # Crea il dizionario con la storia del lotto
        storia_lotto = {}
        
        # Cicla fra tutti gli anni della simulazione
        for anno in sorted(list(anni_rilevati)):
            # Estrae dal dizionario le chiavi delle stagioni invernali di ogni anno
            chiave_inverno = f"A{anno}_Inverno"
            if chiave_inverno not in dizionario_completo: continue
            istanza_inverno = dizionario_completo[chiave_inverno]
            
            # Recupera i dizionari dello stato dei lotti e dei risultati dei cantieri, prendendo i dati biometrici del lotto selezionato
            stato_lotti = istanza_inverno.get("stato_lotti_pre", {})
            risultati = istanza_inverno.get("risultati_cantieri", {})
            dati_biometrici = stato_lotti.get(lotto_reale.id_lotto, {})
            fallimenti = risultati.get("fallimenti_lavorazioni", {})
            fallimenti_taglio = fallimenti.get("tagli", {})
            
            # Crea un dizionario temporaneo dove si inseriranno i dati che poi popoleranno la tabella 
            record = {
                "eta": dati_biometrici.get("eta", 0),
                "piante": dati_biometrici.get("biometria", {}).get("piante_attive", 0),
                "dbh": dati_biometrici.get("biometria", {}).get("dbh_reale_cm", 0.0),
                "h": dati_biometrici.get("biometria", {}).get("altezza_m", 0.0),
                "stato_taglio": "NO",
                "rese": {"opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}
            }
            
            # Estrae dal dizionario estratto i tagli effettuati ed il dettaglio delle operazioni
            tagli_anno = risultati.get("tagli_effettuati", [])
            ops = risultati.get("dettaglio_operazioni", [])
            # Recupera i dati di interesse solo per il lotto selezionato
            dati_taglio = next((t for t in tagli_anno if t.get("lotto_id") == lotto_reale.id_lotto), None)
            
            # Verifica dal dizionario del taglio recuperato come questo si è concluso, se con taglio totale o parziale
            if dati_taglio:
                record["rese"] = dati_taglio.get("rese", record["rese"])
                stato_op = next((o.get("stato", "") for o in ops if o.get("lotto_id") == lotto_reale.id_lotto and "RAC" in o.get("id_operazione", "")), "Eseguito")
                record["stato_taglio"] = "PARZIALE" if "Parziale" in stato_op else "COMPLETATO"
                    
            # Aggiunge il dizionario dell'anno nella dizionario dello storico del lotto
            storia_lotto[anno] = record

        # Cicla su tutti gli anni presenti nel dizionario storia_lotto prima costruito per popolare la tabella
        for anno, dati in storia_lotto.items():
            # Crea la nuova riga
            riga = self.tbl_storico_lotto.rowCount()
            self.tbl_storico_lotto.insertRow(riga)
            
            # Verifica se per l'età del lotto sarebbe pronto per il taglio in questo anno
            is_maturo_per_eta = float(dati["eta"]) >= eta_rotazione_standard

            pronto_al_taglio = "SÌ" if is_maturo_per_eta else "NO"
            
            # Verifica se il lotto è stato tagliato, pazialmente o completamente, nell'anno della maturità per scegliere cosa inserire
            # nelle caselle tagliato e pronto
            if dati["stato_taglio"] in ["COMPLETATO", "PARZIALE"]:
                testo_taglio = dati["stato_taglio"]
            elif fallimenti_taglio["saltati_risorse"] != 0 and pronto_al_taglio == "SÌ":
                testo_taglio = "NO RISORSE"
            elif pronto_al_taglio == "SÌ":
                testo_taglio = "NON MATURO"
            else:
                testo_taglio = "NO"

            # Popolamento celle standard
            self.tbl_storico_lotto.setItem(riga, 0, QTableWidgetItem(f"Anno {anno}"))
            self.tbl_storico_lotto.setItem(riga, 1, QTableWidgetItem(f"{dati['eta']} anni"))
            self.tbl_storico_lotto.setItem(riga, 2, QTableWidgetItem(f"{self.locale_it.toString(float(dati['dbh']), 'f', 2)} cm"))
            self.tbl_storico_lotto.setItem(riga, 3, QTableWidgetItem(f"{self.locale_it.toString(float(dati['h']), 'f', 2)} m"))
            self.tbl_storico_lotto.setItem(riga, 4, QTableWidgetItem(f"{dati['piante']} fusti"))
            
            # Colonna 5: Pronto al Taglio
            item_pronto = QTableWidgetItem(pronto_al_taglio)
            if pronto_al_taglio == "SÌ": 
                item_pronto.setForeground(QColor("#00e676")) # Verde acceso
            else:
                item_pronto.setForeground(QColor("#ff5252")) # Rosso se ha l'età ma non è pronto
            self.tbl_storico_lotto.setItem(riga, 5, item_pronto)
            
            # Colonna 6: Stato Taglio (Gestione dinamica dei colori)
            item_tagliato = QTableWidgetItem(testo_taglio)
            if testo_taglio == "COMPLETATO": 
                item_tagliato.setForeground(QColor("#00b0ff")) # Azzurro
            elif testo_taglio == "PARZIALE": 
                item_tagliato.setForeground(QColor("#ff9800")) # Arancione
            elif testo_taglio == "NON MATURO" or testo_taglio == "NO RISORSE":
                item_tagliato.setForeground(QColor("#ff5252")) # Rosso acceso (Segnale d'allarme biologico)
            elif pronto_al_taglio == "SÌ" and testo_taglio == "NO": 
                item_tagliato.setForeground(QColor("#ff9800")) # Arancione: pronto ma non ancora toccato dall'utente
            self.tbl_storico_lotto.setItem(riga, 6, item_tagliato)
            
            # Colonne Rese
            self.tbl_storico_lotto.setItem(riga, 7, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('opera_m3', 0.0)), 'f', 2)} m³"))
            self.tbl_storico_lotto.setItem(riga, 8, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('cartiera_t', 0.0)), 'f', 2)} t"))
            self.tbl_storico_lotto.setItem(riga, 9, QTableWidgetItem(f"{self.locale_it.toString(float(dati['rese'].get('truciolato_t', 0.0)), 'f', 2)} t"))

            # Centra il testo di tutte le celle 
            for c in range(10):
                item = self.tbl_storico_lotto.item(riga, c)
                if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
        # Aggiorna i grafici dei dati biologici e della densità delle piante
        self._aggiorna_grafici_storico_lotto(storia_lotto)
    
    
    def _aggiorna_grafici_storico_lotto(self, storia_lotto: dict):
        # 1. Pulizia totale delle figure (reset completo per ogni cambio lotto)
        self.fig_crescita.clf()
        self.fig_piante.clf()
        
        # 2. Ricreazione assi
        self.ax_crescita = self.fig_crescita.add_subplot(111)
        self.ax_piante = self.fig_piante.add_subplot(111)
        
        # Impostazione colori tema scuro
        self.ax_crescita.set_facecolor('#141923')
        self.ax_piante.set_facecolor('#141923')
        
        anni = sorted(storia_lotto.keys())
        num_anni = len(anni)
        
        # Logica per asse X: step 1 se pochi anni, step 2 se tanti (evita sovrapposizioni)
        passo_asse_x = 1 if num_anni <= 20 else 2
        
        # Larghezza dinamica del canvas (minimo 500px, 60px per anno)
        larghezza_totale = max(500, num_anni * 60)
        self.canvas_crescita.setMinimumWidth(larghezza_totale)
        self.canvas_piante.setMinimumWidth(larghezza_totale)
        
        # Estrazione dati
        diametri_cm = [storia_lotto[a]["dbh"] for a in anni]
        altezze_m = [storia_lotto[a]["h"] for a in anni]
        piante = [storia_lotto[a]["piante"] for a in anni]

        # --- Grafico 1: Crescita Dimensionale (Doppio Asse Y) ---
        color_dbh = '#ffca28' # Giallo
        color_h = '#00e676'   # Verde
        
        # Asse SX: Altezza
        linea_h, = self.ax_crescita.plot(anni, altezze_m, marker='s', linestyle='-', color=color_h, label='Altezza (m)')
        self.ax_crescita.set_ylabel('Altezza (m)', color=color_h)
        self.ax_crescita.tick_params(axis='y', colors=color_h)
        
        # Asse DX: Diametro
        ax2 = self.ax_crescita.twinx()
        linea_dbh, = ax2.plot(anni, diametri_cm, marker='o', linestyle='-', color=color_dbh, label='Diametro (cm)')
        ax2.set_ylabel('Diametro (cm)', color=color_dbh)
        ax2.tick_params(axis='y', colors=color_dbh)
        
        # Configurazione Asse X (Interi)
        for ax in [self.ax_crescita, self.ax_piante]:
            ax.xaxis.set_major_locator(MultipleLocator(passo_asse_x))
            ax.xaxis.set_major_formatter(lambda x, pos: f'{int(x)}')
            ax.tick_params(axis='x', colors='#e0e0e0')
        
        self.ax_crescita.grid(True, linestyle='--', alpha=0.3, color='#444')
        self.ax_crescita.set_title("Evoluzione Dimensionale", color='#e0e0e0', fontsize=10)
        
        # Inizializzazione Cursore Interattivo
        self.cursor_crescita = mplcursors.cursor([linea_h, linea_dbh], hover=True)

        # --- Grafico 2: Evoluzione Densità ---
        linea_p, = self.ax_piante.plot(anni, piante, marker='D', linestyle='-', color='#2196f3', label='Piante Vive')
        self.ax_piante.set_ylabel('N° Fusti', color='#e0e0e0')
        self.ax_piante.set_xlabel('Anno', color='#e0e0e0')
        self.ax_piante.tick_params(colors='#e0e0e0')
        self.ax_piante.grid(True, linestyle='--', alpha=0.3, color='#444')
        self.ax_piante.set_title("Evoluzione Densità", color='#e0e0e0', fontsize=10)
        
        # Inizializzazione Cursore Interattivo
        self.cursor_piante = mplcursors.cursor([linea_p], hover=True)

        # Finalizzazione
        self.fig_crescita.tight_layout()
        self.fig_piante.tight_layout()
        self.canvas_crescita.draw()
        self.canvas_piante.draw()
   
    # TAB 3 - Caapcità Operative
    
    @Slot(str)
    def slot_aggiorna_tab_efficienza(self, testo_anno: str):
        '''Funzione che aggiorna le tabelle di valutazione dell'efficienza delle risorse interne e del ricorso a noli stagionali,
           calcolando per ogni risorsa e stagione le ore disponibili, le ore lavorate, le ore ricorse a noli, i tetti massimi di mercato e le eventuali
           ore sforate, evidenziando con formattazione e colori le criticità e i risultati di saturazione ed esaurimento delle risorse per facilitare l'analisi da parte dell'utente'''
        
        if not testo_anno: return
        anno = int(testo_anno)
        
        # Inizializza la tabella
        self.tbl_saturazione.setRowCount(0)
        self.tbl_stagionali_noli.setRowCount(0)
        
        # Crea delle liste per mappare tutte le modalità usate per definire le risorse ed evitare errori di ricerca fra le chiavi
        stagioni = ["Inverno", "Primavera", "Estate", "Autunno"]
        risorse = [
            ("Op. Spec.", "grado_A", "personale_spec"),
            ("Op. Generici", "grado_B", "personale_comune"),
            ("Harvester", "harvester", "harvester"),
            ("Forwarder", "forwarder", "forwarder"),
            ("Trattori Alta", "trattori_alta", "trattori_alta"),
            ("Trattori Media", "trattori_media", "trattori_media"),
            ("Piattaforme", "piattaforme", "piattaforme"),
            ("Cippatrici", "cippatrice", "cippatrice")
        ]
        
        mappa_attributi_ditta = {
            "grado_A": "operai_grado_A", "grado_B": "operai_grado_B", "harvester": "harvester_abbattitori",
            "forwarder": "forwarder_caricatori", "trattori_alta": "trattori_alta_potenza",
            "trattori_media": "trattori_media_potenza", "piattaforme": "piattaforme_aeree_semoventi", "cippatrice": "cippatrice"
        }
        
        giorni_utili = 55
        ore_giorni_standard = 8
        ore_base = giorni_utili *  ore_giorni_standard
        limiti_noli = self.motore.ditta.limiti_noli_stagionali
        
        # Cicla su ogni risorsa possibile che sta nella lista risorse
        for nome_ui, chiave_interna, chiave_nolo in risorse:
            # resetta i totali del ciclo
            tot_disp, tot_lav, tot_noli, tot_mercato, tot_sforate = 0.0, 0.0, 0.0, 0.0, 0.0
            # estrae il nome corretto da ricercare per la risorsa e ricava la disponibilità oraria della risorsa specifica
            nome_reale = mappa_attributi_ditta.get(chiave_interna, chiave_interna)
            disp = getattr(self.motore.ditta, nome_reale, 0) * ore_base
            
            # Cicla sulla lista delle stagioni
            for stagione in stagioni:
                # recupera il dizionario e lo mette in una variabile locale
                chiave_stato = f"A{anno}_{stagione}"
                dizionario_storico = self.parametri.storico_stagionale
                # recupera dal dizionario_storico locale solo la stagione e l'anno cercato
                stato = dizionario_storico[chiave_stato]
                # recupera il dizionario della stagione dei risultati dei cantieri, delle risorse umane e dei macchinari interni alla ditta 
                report_cantieri = stato["risultati_cantieri"]
                umane = report_cantieri["risorse_umane_interne"]
                macchine = report_cantieri["macchinari_interni_consumati"]
                
                # Recupera le ore totale del personale e dei macchinari ricercati
                if "grado" in chiave_interna:
                    lav = umane[f"consumate_{chiave_interna[-1]}"]
                else:
                    lav = macchine[chiave_interna]
                
                # Effettuata la stessa cosa con i noli esterni dal dizionario specificio
                terzi = report_cantieri["ricorso_terzi_e_noli"]
                noli_usati = terzi[chiave_interna]
                
                # Verifica se ci sono stati sforamenti oltre le ore presenti nei serbatoi della ditta e dei noli
                unita_max = limiti_noli[chiave_nolo]
                tetto_mercato = unita_max * ore_base
                ore_sforate = max(0.0, noli_usati - tetto_mercato)

                # Accumulatori aggiornati 
                tot_disp += disp
                tot_lav += lav
                tot_noli += noli_usati
                tot_mercato += tetto_mercato
                tot_sforate += ore_sforate
                
                # Avvia le funzioni specifiche per l'inserimento della riga specifica nelle due tabelle
                self._inserisci_riga_saturazione(nome_ui, stagione, disp, lav)
                self._inserisci_riga_stress(nome_ui, stagione, noli_usati, tetto_mercato, ore_sforate)
            
            # Ad ogni fine ciclo sulla singola risorsa viene aggiunta una riga alla tabella con i totali della risorsa stessa
            self._inserisci_riga_saturazione(nome_ui, "TOTALE", tot_disp, tot_lav, is_totale=True)
            self._inserisci_riga_stress(nome_ui, "TOTALE", tot_noli, tot_mercato, tot_sforate, is_totale=True)
            self.tbl_saturazione.insertRow(self.tbl_saturazione.rowCount())
            self.tbl_stagionali_noli.insertRow(self.tbl_stagionali_noli.rowCount())

        # CALCOLO E AGGIORNAMENTO FALLIMENTI ANNUALI
        tot_tagli_risorse = 0
        tot_tagli_biologici = 0
        tot_lav_generiche = 0
        
        dizionario_storico = self.parametri.storico_stagionale
        
        # Somma i fallimenti registrati nelle 4 stagioni dell'anno selezionato
        for stagione in ["Inverno", "Primavera", "Estate", "Autunno"]:
            chiave_stato = f"A{anno}_{stagione}"
            if chiave_stato in dizionario_storico:
                # Recupera il dizionario dei fallimento
                fallimenti = dizionario_storico[chiave_stato]["risultati_cantieri"]["fallimenti_lavorazioni"]
                
                # Aggiorna i contatori di fallimenti
                tot_tagli_risorse += fallimenti["tagli"]["saltati_risorse"]
                tot_tagli_biologici += fallimenti["tagli"]["rinviati_maturita"]
                tot_lav_generiche += fallimenti["lavorazioni_generiche"]["saltate_risorse"]

        # Aggiornamento diretto delle etichette della GUI
        self.lbl_tagli_falliti.setText(f"Tagli Raso Saltati (Mancanza Risorse): {tot_tagli_risorse}")
        self.lbl_biologici_falliti.setText(f"Tagli Ritardati (Oltre Maturità): {tot_tagli_biologici}")
        self.lbl_generici_falliti.setText(f"Lavorazioni Agronomiche Saltate: {tot_lav_generiche}")
    
                  
    def _inserisci_riga_saturazione(self, nome, stagione, disp, lav, is_totale = False):
        '''Funzione che inserisce una riga nella tabella di saturazione delle risorse, formattando i dati di ore disponibili, ore lavorate e percentuale di saturazione
           evidenziando con colori le condizioni di saturazione critica o ottimale e formattando in grassetto le righe totali per facilitare l'analisi visiva da parte dell'utente, 
           con attenzione alla coerenza stilistica e alla chiarezza dei dati presentati'''
        
        r = self.tbl_saturazione.rowCount()
        self.tbl_saturazione.insertRow(r)
        # Effettua il calcolo percentuale sull'utilizzo della risorsa
        sat_perc = (lav / disp * 100) if disp > 0 else 0.0
        
        # Inserisce i valori nelle celle con i dati recuperati
        self.tbl_saturazione.setItem(r, 0, QTableWidgetItem(nome if not is_totale else ""))
        self.tbl_saturazione.setItem(r, 1, QTableWidgetItem(stagione))
        self.tbl_saturazione.setItem(r, 2, QTableWidgetItem(f"{self.locale_it.toString(float(disp), 'f', 1)} h"))
        self.tbl_saturazione.setItem(r, 3, QTableWidgetItem(f"{self.locale_it.toString(float(lav), 'f', 1)} h"))
        
        # Imposta il colore del testo per evidenziare la percentuale di utilizzo della risorsa
        item_sat = QTableWidgetItem(f"{self.locale_it.toString(float(sat_perc), 'f', 1)}%")
        if sat_perc <= 25.0 and disp > 0: item_sat.setForeground(QColor("#00e676"))
        elif sat_perc > 25.0 and sat_perc <= 99.0: item_sat.setForeground(QColor("#ecaf29"))
        else: item_sat.setForeground(QColor("#ff5252"))
        self.tbl_saturazione.setItem(r, 4, item_sat)
        
        # Imposta i colori per le righe che contengono i totali
        for c in range(5):
            item = self.tbl_saturazione.item(r, c)
            if item:
                if is_totale:
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                    if c != 4: item.setForeground(QColor("#ffecb3"))
                elif c != 4: item.setForeground(QColor("#ffffff"))

    
    def _inserisci_riga_stress(self, nome, stagione, noli, tetto, sforate, is_totale = False):
        '''Funzione che inserisce una riga nella tabella di stress da noli stagionali, formattando i dati di ore ricorse a noli, tetti di mercato e percentuale di esaurimento,
           evidenziando con colori le condizioni di esaurimento critico o sostenibile e formattando in grassetto le righe totali per facilitare l'analisi visiva da parte dell'utente, con attenzione alla coerenza stilistica e alla chiarezza dei dati presentati,
           con un focus particolare sulle ore sforate evidenziate in rosso per facilitare l'identificazione delle criticità legate al ricorso a noli stagionali'''
        
        r = self.tbl_stagionali_noli.rowCount()
        self.tbl_stagionali_noli.insertRow(r)
        # Effettua il calcolo percentuale sull'utilizzo della risorsa
        esaurimento_perc = (noli / tetto * 100) if tetto > 0 else (100.0 if noli > 0 else 0.0)
        esaurimento_perc = round(esaurimento_perc, 2)
        
        # Inserisce i valori nelle celle con i dati recuperati
        self.tbl_stagionali_noli.setItem(r, 0, QTableWidgetItem(nome if not is_totale else ""))
        self.tbl_stagionali_noli.setItem(r, 1, QTableWidgetItem(stagione))
        self.tbl_stagionali_noli.setItem(r, 2, QTableWidgetItem(f"{self.locale_it.toString(float(noli), 'f', 1)} h"))
        self.tbl_stagionali_noli.setItem(r, 3, QTableWidgetItem(f"{self.locale_it.toString(float(tetto), 'f', 1)} h"))
        item_perc = QTableWidgetItem(f"{self.locale_it.toString(float(esaurimento_perc), 'f', 1)}%")
        
        # Imposta il colore del testo per evidenziare la percentuale di utilizzo della risorsa
        if esaurimento_perc > 99.00:
            item_perc.setForeground(QColor("#ff5252")) 
            item_perc.setFont(QFont("Arial", 11, QFont.Bold))
        elif esaurimento_perc <= 99.00 and esaurimento_perc > 75.00:
            item_perc.setForeground(QColor("#ecaf29")) 
            item_perc.setFont(QFont("Arial", 11, QFont.Bold))
        else:
            item_perc.setForeground(QColor("#00e676")) 
        
        self.tbl_stagionali_noli.setItem(r, 4, item_perc)
        
         # Imposta i colori per le righe che contengono i totali
        for c in range(5):
            item = self.tbl_stagionali_noli.item(r, c)
        if item:
            if is_totale:
                item.setFont(QFont("Arial", 11, QFont.Bold))
                item.setForeground(QColor("#ffecb3"))
            elif not is_totale and c != 4: 
                item.setForeground(QColor("#ffffff"))

    # TAB 4 - Registro dei Fallimenti Operativi
    
    def _popola_tabella_anomalie(self):
        '''Funzione che popola la tabella delle anomalie operative e biologiche rilevate durante l'analisi dello storico stagionale, 
           evidenziando con formattazione e colori le condizioni di anomalia e i motivi di fallimento dei tagli, facilitando l'identificazione visiva delle criticità
           e dei pattern ricorrenti nelle operazioni di taglio e nelle condizioni biologiche dei lotti, con un focus particolare sui ritardi biologici
           e sulle omissioni di taglio evidenziati in rosso per facilitare l'analisi da parte dell'utente'''
        
        if not self.tbl_log_anomalie: return
        self.tbl_log_anomalie.setRowCount(0)
        
        # costruisce un mappa delle operazioni per i successivi filtri di ricerca
        mappa_op = self._costruisci_mappa_operazioni()
        # carica su variabile locale lo storico_stagionale
        storico = self.parametri.storico_stagionale
        
        # Cicla su ogni stagione registrata nello storico e sui relativi dati operativi
        for chiave_stagione, dati in storico.items():
            if "RisorseExtra" in chiave_stagione: continue
            
            # Estrae dal dizionario risultati dei cantieri, il dettaglio delle operazioni ed i tagli effettuati
            risultati = dati.get("risultati_cantieri", {})
            operazioni = risultati.get("dettaglio_operazioni", [])
            tagli_effettuati = risultati.get("tagli_effettuati", [])
            
            # Recupera anno e stagione 
            parts = chiave_stagione.split("_")
            anno_str = parts[0].replace("A", "") 
            stagione = parts[1]
                        
            # Rilevamento Anomalie Operative
            for op in operazioni:
                # verifica se nella chiave stato non è presente la parola eseguito
                stato_originale = str(op.get("stato", "")).strip()
                stato_lower = stato_originale.lower()
                
                if stato_lower == "" or (stato_lower.startswith("eseguito") and "parziale" not in stato_lower):
                    continue
                
                # Recupera i dati dell'operazione
                id_op = op["id_operazione"]
                desc_operazione = mappa_op.get(id_op, id_op) 
                    
                # Inserisce la riga nella tabella con i dati della lavorazione non effettuata
                riga = self.tbl_log_anomalie.rowCount()
                self.tbl_log_anomalie.insertRow(riga)
                
                self.tbl_log_anomalie.setItem(riga, 0, QTableWidgetItem(f"Anno {anno_str}"))
                self.tbl_log_anomalie.setItem(riga, 1, QTableWidgetItem(stagione))
                self.tbl_log_anomalie.setItem(riga, 2, QTableWidgetItem(str(op["lotto_id"])))
                self.tbl_log_anomalie.setItem(riga, 3, QTableWidgetItem(desc_operazione)) 
                
                # Differenzia il colore del carattere se l'operazione è stata fatta parzialmente o bloccata integralmente
                item_stato = QTableWidgetItem(stato_originale)
                if "parziale" in stato_lower: item_stato.setForeground(QColor("#ff9800"))
                else: item_stato.setForeground(QColor("#ff5252"))
                self.tbl_log_anomalie.setItem(riga, 4, item_stato) 

            # Rilevamento Ritardi Biologici / Omissioni
            if stagione == "Inverno":
                # Questo controllo viene fatto solo in inverno per verificare eventuali mancati tagli in anni previsti
                stato_pre = dati["stato_lotti_pre"]
                lotti_tagliati_ids = [t["lotto_id"] for t in tagli_effettuati]
                
                # Cicla nel dizionario dello stato_precedente dei lotti
                for lotto_id, info in stato_pre.items():
                    # Cerca il lotto che corrisponde a lotto_id nella collazione dei lotti
                    lotto_reale = next((l for l in self.parametri.collezione_lotti if l.id_lotto == lotto_id), None)
                    if not lotto_reale: continue
                    
                    # Recupera i dati biologici del lotto    
                    eta = info["eta"]
                    dbh = info.get("biometria", {}).get("dbh_reale_cm", 0.0)
                    # imposta i limiti target a seconda della destinazione d'uso del lotto
                    eta_rot = 5 if lotto_reale.destinazione_uso == "INDUSTRIA" else 10
                    target_dbh = 15.0 if lotto_reale.destinazione_uso == "INDUSTRIA" else 35.0
                    
                    # Applica la tolleranza prevista già in simulazione
                    TOLLERANZA = self.parametri.tolleranza_taglio
                    soglia_elastica = target_dbh * (1.0 - TOLLERANZA)
                    
                    # Effettua le verifiche sulla lista dei lotti tagliati per decidere il motivo della fallanza ed applica poi l'inserimento in tabella
                    if eta >= eta_rot and lotto_id not in lotti_tagliati_ids:
                        motivo = ""
                        desc_operazione = "Taglio Raso (Fine Turno)" 
                        
                        if dbh < soglia_elastica:
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
        '''Funzione che fornisce una diagnosi dettagliata del motivo di fallimento di un'operazione di taglio, analizzando lo storico stagionale del lotto e confrontando i dati biometrici, l'età, le condizioni operative e le risorse disponibili,
           per identificare se il fallimento è dovuto a ritardi biologici, omissioni di taglio per mancanza di risorse o interruzioni operative, fornendo una spiegazione chiara e dettagliata delle cause alla base del fallimento, con un focus particolare sui
           ritardi biologici evidenziati in rosso per facilitare l'identificazione delle criticità legate alla maturità dei lotti e alle condizioni di crescita, e sulle omissioni di taglio evidenziate in arancione per facilitare l'analisi delle criticità 
           legate alla pianificazione e alla gestione delle risorse nei cantieri di taglio'''
        
        # Carica il dizionario stagionale e lo mette in una variabile locale e ne estrae il dizionario dello stato dei lotti   
        storico = self.parametri.storico_stagionale
        dati_stagione = storico[chiave_stagione]
        stato_pre = dati_stagione["stato_lotti_pre"][id_lotto]
        
        # Inizializza la lista delle diagnosi
        diagnosi = []
        
        # Se lo stato è di ritardo biologico fornisce le informazioni del motivo, dando i parametri del lotto 
        if "Ritardo Biologico" in stato:
            dbh = stato_pre.get("biometria", {}).get("dbh_reale_cm", 0.0)
            eta = stato_pre.get("eta", 0)
            diagnosi.append(f"• Età Raggiunta: Il lotto ha {eta} anni (fine turno), ma non ha la maturità commerciale.")
            diagnosi.append(f"• Dettaglio Biometrico: Il diametro (DBH) rilevato è di {dbh:.2f} cm. Il lotto ha subito stress pedoclimatici o competizione da sovradensità.")
            diagnosi.append("• Azione: Il cantiere non è stato pianificato per evitare rese insufficienti.")
            return "\n\n".join(diagnosi)
            
        # Se lo stato è omesso o zero risorse vengono fornite le informazioni del motivo ricadenti in problemi strutturali della ditta
        if "Omesso" in stato or "Zero Risorse" in stato:
            eta = stato_pre.get("eta", 0)
            diagnosi.append(f"• Analisi Logistica: Il lotto ha {eta} anni ed è pronto per la vendita.")
            diagnosi.append("• Problema: La capacità aziendale (ore interne + noli massimi concessi sul mercato) è collassata a causa di altri cantieri prioritari.")
            diagnosi.append("• Azione: Taglio rinviato all'Inverno successivo. La resa dell'anno non sarà ottimale.")
            return "\n\n".join(diagnosi)

        if op_data:
            priorita = op_data.get("priorita", "N/A")
            
            # Specifica la motivazione di una operazione fallita parzialmente o totalmente dando i dati dell'operazione, la priorità, il fabbisogno
            # che non è stato soddisfatto, le piante eventualmente ancora in piedi per le operazioni di taglio.
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
        '''Slot che si attiva quando l'utente seleziona una riga nella tabella delle anomalie, mostrando una diagnosi dettagliata del motivo di fallimento dell'operazione di taglio associata all'anomalia selezionata, con un focus particolare sui ritardi biologici evidenziati in rosso e sulle omissioni di taglio evidenziate 
           in arancione per facilitare l'identificazione delle criticità legate alla maturità dei lotti e alla pianificazione delle risorse nei cantieri di taglio'''
        
        if not hasattr(self, 'tbl_log_anomalie') or not self.tbl_log_anomalie: return
        
        row = self.tbl_log_anomalie.currentRow()
        # Verifica la presenza di una riga
        if row < 0 or self.tbl_log_anomalie.item(row, 0) is None: return
        
        # Recupera i dati dell'anomalia selezionata    
        anno_txt = self.tbl_log_anomalie.item(row, 0).text().replace("Anno ", "")
        stagione = self.tbl_log_anomalie.item(row, 1).text()
        id_lotto = self.tbl_log_anomalie.item(row, 2).text()
        operazione = self.tbl_log_anomalie.item(row, 3).text()
        stato = self.tbl_log_anomalie.item(row, 4).text()
        
        # crea la chiave del dizionario della stagione 
        chiave_stagione = f"A{anno_txt}_{stagione}"
        
        if hasattr(self, 'lbl_stato_dettaglio') and self.lbl_stato_dettaglio: 
            self.lbl_stato_dettaglio.setText(f"OPERAZIONE: {operazione} | STATO: {stato.upper()}")
        
        # recupera il dizionario storico delle stagioni e le mette in una variabile locale
        storico = self.parametri.storico_stagionale
        
        # recupera il dizionario della stagione selezionata e successivamente il dizionario delle operazioni
        dati_stagione = storico.get(chiave_stagione, {})
        operazioni = dati_stagione["risultati_cantieri"]["dettaglio_operazioni"]
        
        # Recupera nel dizionario operazioni l'operazione specifica del lotto selezionato
        op_data = next((op for op in operazioni if op.get("lotto_id") == id_lotto and stato in op.get("stato", "")), None)
        
        # Variabili accomulatori
        fabbisogno = 0.0
        lavorate = 0.0
        perc = 0
        piante_rimaste_txt = ""

        if hasattr(self, 'tbl_bilancio_risorse') and self.tbl_bilancio_risorse:
            # Azzera la tabella
            self.tbl_bilancio_risorse.setRowCount(0)
            
            if op_data:
                # Lettura diretta dei dati corretti salvati dal simulatore
                fabbisogno = float(op_data.get("durata_cantiere_h", 0.0))
                lavorate = float(op_data.get("ore_lavoro_totali", 0.0))
                
                # Uso della chiave percentuale_completamento
                perc_json = float(op_data.get("percentuale_completamento", 0.0))
                
                perc = int(perc_json)                 # Per la progress bar (numero intero 0-100)
                fattore = perc_json / 100.0           # Per la matematica delle piante (scala 0.0 - 1.0)

                # Calcolo piante rimaste (solo per i cantieri di taglio parziali)
                if ("Taglio" in operazione or "RAC" in op_data.get("id_operazione", "")) and 0.0 < fattore < 1.0:
                    stato_pre = dati_stagione.get("stato_lotti_pre", {}).get(id_lotto, {})
                    piante_pre = int(stato_pre.get("biometria", {}).get("piante_attive", 0))
                    
                    if lavorate > 0 and piante_pre > 0:
                        piante_tagliate = int(piante_pre * fattore)
                        piante_rimaste = piante_pre - piante_tagliate
                        if piante_rimaste > 0: 
                            piante_rimaste_txt = str(piante_rimaste)

                # Regole restrittive in caso di blocco totale
                if "Bloccato" in stato or lavorate == 0: 
                    perc = 0
                    
                perc = max(0, min(perc, 100))
                deficit = max(0.0, fabbisogno - lavorate)
                
                # Aggiornamento UI della barra percentuale
                if hasattr(self, 'pb_avanzamento_cantiere') and self.pb_avanzamento_cantiere: 
                    self.pb_avanzamento_cantiere.setValue(perc)
                
                # Popolamento Tabella Risorse
                riga_tab = self.tbl_bilancio_risorse.rowCount()
                self.tbl_bilancio_risorse.insertRow(riga_tab)
                
                # inserisce nella riga la tipologia di macchinario usato per l'operazione specific
                macchina_str = "Harvester/Forwarder" if ("Taglio" in operazione or "RAC" in op_data.get("id_operazione", "")) else "Squadra/Trattori"
                self.tbl_bilancio_risorse.setItem(riga_tab, 0, QTableWidgetItem(macchina_str))
                self.tbl_bilancio_risorse.setItem(riga_tab, 1, QTableWidgetItem(f"{fabbisogno:.2f} h"))
                self.tbl_bilancio_risorse.setItem(riga_tab, 2, QTableWidgetItem(f"{lavorate:.2f} h"))
                
                item_def = QTableWidgetItem(f"{deficit:.2f} h")
                if deficit > 0: item_def.setForeground(QColor("#ff5252")) 
                self.tbl_bilancio_risorse.setItem(riga_tab, 3, item_def)
                
                # Centra i valori nella tabella
                for col in range(4):
                    self.tbl_bilancio_risorse.item(riga_tab, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            else:
                if hasattr(self, 'pb_avanzamento_cantiere') and self.pb_avanzamento_cantiere: 
                    self.pb_avanzamento_cantiere.setValue(0)
            
        # Aggiornamento del testo diagnostico
        if hasattr(self, 'txt_diagnostica') and self.txt_diagnostica:
            spiegazione = self._diagnostica_fallimento(chiave_stagione, id_lotto, operazione, stato, op_data, fabbisogno, lavorate, perc, piante_rimaste_txt)
            self.txt_diagnostica.setText(spiegazione)
            
        # Abilitazione del bottone di navigazione
        if hasattr(self, 'btn_vai_allo_storico') and self.btn_vai_allo_storico:
            self.btn_vai_allo_storico.setEnabled(True)
            self.btn_vai_allo_storico.setProperty("lotto_target", id_lotto)
            
    
    @Slot()
    def azione_vai_allo_storico(self):
        '''Slot che si attiva quando l'utente clicca sul pulsante "Vai allo Storico" dopo aver selezionato un'anomalia, portando l'utente al tab dello storico stagionale e selezionando automaticamente il lotto associato all'anomalia per facilitare l'analisi dettagliata dello storico del lotto e delle operazioni di taglio ad esso associate, con un focus particolare sui lotti con ritardi biologici evidenziati in rosso e sulle omissioni di taglio evidenziate in arancione 
           per facilitare l'identificazione delle criticità legate alla maturità dei lotti e alla pianificazione delle risorse nei cantieri di taglio'''
        if not self.btn_vai_allo_storico: return
        id_lotto = self.btn_vai_allo_storico.property("lotto_target")
        
        if id_lotto and self.tab_root and self.cmb_scelta_lotto:
            self.tab_root.setCurrentIndex(1) # Porta al tab dello storico
            idx = self.cmb_scelta_lotto.findText(id_lotto)
            if idx >= 0:
                self.cmb_scelta_lotto.setCurrentIndex(idx)