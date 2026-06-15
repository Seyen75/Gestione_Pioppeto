import os
from typing import Dict, Any

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PySide6.QtUiTools import QUiLoader

from GUI.utils import centra_finestra

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class form_monitoraggio(QWidget):
    def __init__(self, motore_simulazione, parent=None):
        super().__init__(parent)
        # Istanzia l'oggetto della classe SimulatorePioppicoltura ed i parametri da essere utilizzato in tutta l'applicazione
        self.motore = motore_simulazione
        self.parametri = motore_simulazione.parametri
        
        # Liste con i dati della simulazione real time per poterli poi utilizzarli nel grafico rese
        self.storico_trimestri: list[str] = []
        self.storico_opera: list[float] = []
        self.storico_cartiera: list[float] = []
        self.storico_truciolato: list[float] = []

        self._cumulato_opera_precedente = 0.0
        self._cumulato_cartiera_precedente = 0.0
        self._cumulato_truciolato_precedente = 0.0
        
        # Dati per dimensioni della form
        self.DIM_W = 1100
        self.DIM_H = 900

        self._carica_interfaccia()
        self._inizializza_grafici()
        
        # Connessioni delle funzioni con l'evento click dei pulsanti nella form
        self.ui.btn_prossimo_trimestre.clicked.connect(self.slot_avanza_trimestre)
        self.ui.btn_termina_sessione.clicked.connect(self.slot_termina_simulazione)

        # Aggiornamento della form e dei controlli
        self._aggiorna_interfaccia_grafica(quadro_stato = None, iniziale = True)

    def showEvent(self, event):
        super().showEvent(event)
        centra_finestra(self, self.DIM_W, self.DIM_H)
    
    def _carica_interfaccia(self):
        '''Carico da parte del modulo di PySyde6 dell'interfaccia presente nel file .ui con la struttura della form'''
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_monitoraggio.ui")
        self.ui = loader.load(percorso_ui, self)
        
        layout_principale = QVBoxLayout(self)
        layout_principale.addWidget(self.ui)
        layout_principale.setContentsMargins(0, 0, 0, 0)


    def _formatta_numero_it(self, valore: float) -> str:
        '''funzione per formattare i numeri per visualizzazione italiana'''
        stringa_base = f"{valore:,.1f}"
        stringa_it = stringa_base.replace(",", "X").replace(".", ",").replace("X", ".")
        return stringa_it

    
    def _inizializza_grafici(self):
        '''Inizializza i due grafici all'interno della form, impostando colori, dimension e scale da utilizzare
           Il codice trasforma il grafico di matplotlib in un oggetto (Widget) che Qt può gestire.'''
        colore_sfondo_hex = "#141923"

        # Imposta il grafico a barre delle risorse
        self.fig_risorse = Figure(figsize=(6, 3), facecolor=colore_sfondo_hex)
        self.canvas_risorse = FigureCanvas(self.fig_risorse)
        self.ax_risorse = self.fig_risorse.add_subplot(111)
        self.ax_risorse.set_facecolor(colore_sfondo_hex)
        
        self.fig_risorse.subplots_adjust(top=0.80, bottom=0.20, left=0.12, right=0.95)
        
         # Crea un layout dinamico all'interno del widget canvas_risorse e vi "incolla" dentro il grafico
        layout_risorse = QVBoxLayout(self.ui.canvas_risorse)
        layout_risorse.addWidget(self.canvas_risorse)
        layout_risorse.setContentsMargins(0, 0, 0, 0)

        # Imposta il grafico a barre delle rese con l'uso di due subplot per diversificare le rese, avendo queste delle unità di misura differenti
        # Il subplot da opera ha dati in metri cubi, il subplot da industria (con le due resee) ha dati in tonnellate
        self.fig_rese = Figure(figsize=(5, 3), facecolor=colore_sfondo_hex)
        self.canvas_rese = FigureCanvas(self.fig_rese)
        
        self.ax_opera = self.fig_rese.add_subplot(211)  
        self.ax_industria = self.fig_rese.add_subplot(212, sharex=self.ax_opera) 
        
        self.ax_opera.set_facecolor(colore_sfondo_hex)
        self.ax_industria.set_facecolor(colore_sfondo_hex)
        
        self.fig_rese.subplots_adjust(top=0.78, bottom=0.22, left=0.16, right=0.95, hspace=0.65)
        
        # Crea un layout dinamico all'interno del widget canvas_risorse e vi "incolla" dentro il grafico
        layout_rese = QVBoxLayout(self.ui.canvas_rese)
        layout_rese.addWidget(self.canvas_rese)
        layout_rese.setContentsMargins(0, 0, 0, 0)

    @Slot()
    def slot_avanza_trimestre(self):
        '''Funzione che avvia la simulazione della stagione corrente tramite l'uso del motore di simulazione'''
        
        # Tiene traccia delle stagione precedente
        stagione_appena_conclusa = self.parametri.stagione_corrente
        anno_appena_concluso = self.parametri.anno_corrente

        # Se è l'avvio della form azzera le liste dello storico annuale delle rese
        if "Avvio" in self.storico_trimestri:
            self.storico_trimestri.remove("Avvio")
            self.storico_opera.clear()
            self.storico_cartiera.clear()
            self.storico_truciolato.clear()

        # Viene avviata la simulazione della stagione con la funzione dell'oggetto SimulatorePioppicultura istanziato ad inizio applicazione
        # La funzione restituisce un dizionario specifico di tutti gli eventi occorsi nella stagione corrente. 
        # Questo dizionaro il motore simulativo lo inserisce nel dizionario_storico_stagionale complessivo che sarà poi usato dalla parte di reportistica.
        quadro_stato = self.motore.avanza_passo_simulazione()

        # L'anno selvicolturale finisce con la stagoione invernale, quando vengono fatte le rese e si accumulano le informazioni da graficare.
        if stagione_appena_conclusa == "Inverno":
            chiave_anno = f"Anno {anno_appena_concluso}"
            # viene estratto il dizionario (con chiave "produzione_cumulata") presente nel dizionario stagionale che ha i valori delle rese complessive
            produzione_cumulata = quadro_stato["produzione_cumulata"]
            
            cumulato_opera_attuale = produzione_cumulata["opera_m3"]
            cumulato_cartiera_attuale = produzione_cumulata["cartiera_t"]
            cumulato_truciolato_attuale = produzione_cumulata["truciolato_t"]

            netto_opera_anno = round(cumulato_opera_attuale - self._cumulato_opera_precedente, 2)
            netto_cartiera_anno = round(cumulato_cartiera_attuale - self._cumulato_cartiera_precedente, 2)
            netto_truciolato_anno = round(cumulato_truciolato_attuale - self._cumulato_truciolato_precedente, 2)

            # I dati estratti vengono inseriti in un dizionario tampone utilizzato poi come base per il grafico delle rese
            #if chiave_anno not in self.storico_trimestri:
            self.storico_trimestri.append(chiave_anno)
            self.storico_opera.append(max(0.0, netto_opera_anno))
            self.storico_cartiera.append(max(0.0, netto_cartiera_anno))
            self.storico_truciolato.append(max(0.0, netto_truciolato_anno))

            self._cumulato_opera_precedente = cumulato_opera_attuale
            self._cumulato_cartiera_precedente = cumulato_cartiera_attuale
            self._cumulato_truciolato_precedente = cumulato_truciolato_attuale

        # Terminata la simulazione della stagione si avvia la funzione che si occupa di gestire gli aggiornamenti dei controlli e dei grafici
        self._aggiorna_interfaccia_grafica(quadro_stato = quadro_stato, iniziale = False)

    @Slot()
    def slot_termina_simulazione(self):
        '''Terminata la simulazione con la pressione del tasto si restituisce il controllo alla form padre segnalando che è possibile abilitare il tasto della Dashboard di reportistica'''
        self.parent().abilita_report_finale()
        self.close()

    
    def _aggiorna_interfaccia_grafica(self, quadro_stato: Dict[str, Any] = None, iniziale: bool = False):
        ''' Funzione richiamata al termine della simulazione della stagione
            Va a richiamare le varie funzioni di aggiornamento dei controlli, dei grafici e delle tabelle'''
        # Aggiorna le label con i dati dell'anno e della stagione corrente
        self.ui.lbl_anno.setText(f"ANNO {self.parametri.anno_corrente}")
        self.ui.lbl_stagione.setText(self.parametri.stagione_corrente.upper())

        # Avvia le funzioni di aggiornamento dei vari controlli e popola tabelle e grafici
        self._elabora_e_mostra_fallanze(quadro_stato, iniziale)
        self._popola_tabella_particellare()
        self._rendiconta_e_disegna_previsione_risorse()
        self._ridisegna_grafico_rese_cumulate()

    # Funzione che elabora i dati di consuntivo del trimestre appena concluso, aggiornando le label del cruscotto diagnostico con i dati di tagli saltati, 
    # turni rinviati e lavorazioni fallite, e inizializza lo storico per i grafici a barre se è la prima visualizzazione
    
    def _elabora_e_mostra_fallanze(self, quadro_stato: Dict[str, Any], iniziale: bool):
        '''Recupera i dati simulati nella stagione e ricerca i dizionari contenenti tutte le fallanze operative e biologiche occorse e le graficizza nei controlli di riferimento'''
        stats = self.motore.stats_globali
        
        # Estrae i valori relativi alle tre chiavi contenenti i dati delle fallanze
        t_strut = stats["tagli_strutturali_saltati"]
        t_bio = stats["tagli_biologici_saltati"]
        l_gen = stats["lavorazioni_generiche_saltate"]

        # Aggiorna le Label del Cruscotto Diagnostico con i dati recuperati dal dizionario generale nella chiava stats_globali
        # Le label vengono settate con colori differenti a qualora siano presenti o meno fallanze della categoria specifica

        self.ui.lbl_tagli_saltati.setText(f"⛔ Tagli Saltati (Carenza Mezzi): {t_strut}")
        self.ui.lbl_tagli_saltati.setVisible(True)
        self.ui.lbl_tagli_saltati.setStyleSheet("color: #ff5252; font-weight: bold;" if t_strut > 0 else "color: #00e676; font-weight: bold;")

        self.ui.lbl_turni_saltati.setText(f"⏳ Tagli Rinviati (Immaturità Biologica): {t_bio}")
        self.ui.lbl_turni_saltati.setVisible(True)
        self.ui.lbl_turni_saltati.setStyleSheet("color: #ffb74d; font-weight: bold;" if t_bio > 0 else "color: #00e676; font-weight: bold;")

        self.ui.lbl_lavori_saltati.setText(f"⚠️ Lavorazioni Fallite (Carenza Risorse): {l_gen}")
        self.ui.lbl_lavori_saltati.setVisible(True)
        self.ui.lbl_lavori_saltati.setStyleSheet("color: #ff5252; font-weight: bold;" if l_gen > 0 else "color: #00e676; font-weight: bold;")

        # Inizializzazione storico per i grafici a barre
        if not self.storico_trimestri:
            self.storico_trimestri.append("Avvio")
            self.storico_opera.append(0.0)
            self.storico_cartiera.append(0.0)
            self.storico_truciolato.append(0.0)

    # Funzione che recupera i dati dei lotti della collezione ed inserisce i dati nella tabella tbl_monitoraggio
    
    def _popola_tabella_particellare(self):
        '''Funzione che aggiorna la tabella tbl_monitoraggio con i dati di tutti i lotti
        ciclando su tutta la collezione dei lotti e recuperando per ogni lotto i dati di interesse sia statici che dinamici'''
        
        # azzera le righe se preesistenti
        self.ui.tbl_monitoraggio.setRowCount(0)
        
        # Imposta le labels della tabella e sistema le larghezze degli headers
        colonne_labels = ["ID Particella", "Destinazione d'Uso", "Superficie", "N° Piante", "Età Biologica", "Diametro Medio", "Altezza Stimata", "Stato Cantiere"]
        self.ui.tbl_monitoraggio.setColumnCount(len(colonne_labels))
        self.ui.tbl_monitoraggio.setHorizontalHeaderLabels(colonne_labels)
        self.ui.tbl_monitoraggio.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Cicla tutti i lotti presenti nella collezione ed inserisce le righe formattando i dati
        
        for lotto in self.parametri.collezione_lotti:
            # Inserisce la riga
            riga = self.ui.tbl_monitoraggio.rowCount()
            self.ui.tbl_monitoraggio.insertRow(riga)
            
            # Prende i dati statici del lotto
            destinazione = lotto.destinazione_uso
            eta = lotto.eta
            superficie = lotto.superficie_ettari
            
            # Prende i dati dinamici del lotto se già presenti, altrimenti inserisce i dati statici iniziali del lotto
            if lotto.dati_correnti:
                piante_vive = lotto.dati_correnti["piante_attive"]
                dbh = lotto.dati_correnti["dbh_reale_cm"]
                altezza = lotto.dati_correnti["altezza_m"]
            else:
                piante_vive = lotto.numero_piante_vive
                dbh = lotto.diametro_medio_fusto
                altezza = lotto.altezza_media_piante

            '''In questa parte della funzione viene effettuata una pre simulazione (che non comporta variazione dati) con la quale si verifica
                solo se siamo in Inverno (periodo di resa) se il lotto è maturo per età e dimensione per il taglio e salva l'informazione nella variabile booleana is_maturo
            '''
            eta_originale = lotto.eta
            diametro_originale = lotto.diametro_medio_fusto
            
            try:
                if self.parametri.stagione_corrente == "Inverno":
                    if (lotto.eta == 0 and lotto.numero_piante_vive > 0) or (lotto.numero_piante_vive > 5):
                        eta_futura = eta_originale + 1
                        profilo = self.motore.dati_cloni[lotto.clone_assegnato]
                        dati_futuri = lotto.simula_accrescimento(profilo, eta_futura)
                        
                        # Applica temporaneamente solo se necessario
                        lotto.eta = eta_futura
                        lotto.diametro_medio_fusto = dati_futuri["dbh_reale_cm"] # Accesso diretto
            
                is_maturo = lotto.verifica_maturita_raccolta()
            
            finally:
                # Ripristino in caso di errore nel blocco sopra
                lotto.eta = eta_originale
                lotto.diametro_medio_fusto = diametro_originale

            # Carica in filiea_lotto le lavorazioni necessarie per lo specifo lotto e la sua destinazione per la successiva simulazione
            filiera_lotto = STRUTTURA_LAVORAZIONI[lotto.destinazione_uso]
            
            # Verifica se il lotto è nell'anno del taglio e in che stagione la simulazione sta per diversificare il valore delal stringa che andrà nella tabella nella colonna "stato"
            if is_maturo or lotto.tagliato:
                if self.parametri.stagione_corrente == "Inverno":
                    stato_stringa = "Pianificato per la Raccolta (Taglio raso)"
                else:
                    stato_stringa = "In attesa dell'Inverno per Taglio"
            else:
                # Se non è maturo, interroga filiera_lotto specifico per la destinazione d'uso per trovare, 
                # in base alla fase colturale (f_k) e alla stagione, quali sono l'operazioni attive da inserire nella striga per la colonna "stato" della tabella
                f_k = lotto.get_fase_colturale()
                ops_attive = filiera_lotto.get(str(f_k), {}).get(self.parametri.stagione_corrente, [])
                stato_stringa = " + ".join([o["descrizione"] for o in ops_attive]) if ops_attive else "Riposo vegetativo"

            # Inserisce nella riga della tabella creata i valori sopra calcolati con le formattazioni del caso
            self.ui.tbl_monitoraggio.setItem(riga, 0, QTableWidgetItem(str(lotto.id_lotto)))
            self.ui.tbl_monitoraggio.setItem(riga, 1, QTableWidgetItem(str(destinazione)))
            self.ui.tbl_monitoraggio.setItem(riga, 2, QTableWidgetItem(f"{self._formatta_numero_it(superficie)} ha"))
            self.ui.tbl_monitoraggio.setItem(riga, 3, QTableWidgetItem(f"{int(piante_vive):,}".replace(",", ".")))
            self.ui.tbl_monitoraggio.setItem(riga, 4, QTableWidgetItem(f"{eta} anni"))
            self.ui.tbl_monitoraggio.setItem(riga, 5, QTableWidgetItem(f"{self._formatta_numero_it(dbh)} cm"))
            self.ui.tbl_monitoraggio.setItem(riga, 6, QTableWidgetItem(f"{self._formatta_numero_it(altezza)} m"))
            self.ui.tbl_monitoraggio.setItem(riga, 7, QTableWidgetItem(stato_stringa))

        # Dimensionamento dinamico e Centratura
        header = self.ui.tbl_monitoraggio.horizontalHeader()
        
        # Tutte le colonne si adattano esattamente alla larghezza del loro contenuto
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # L'ultima colonna ("Stato Cantiere") si allunga per occupare tutto lo spazio vuoto rimanente
        header.setStretchLastSection(True)

        # Ciclo per centrale i valori nelle celle della tabella
        for r in range(self.ui.tbl_monitoraggio.rowCount()):
            for c in range(self.ui.tbl_monitoraggio.columnCount()):
                item = self.ui.tbl_monitoraggio.item(r, c)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                            

    def _rendiconta_e_disegna_previsione_risorse(self):
        '''La funzione disegna il grafico delle uso delle risorse della ditta. 
           Per graficare le necessità delle risorse per la stagione in corso che deve ancora essere materialmente simulata
           utilizza un dizionario "interventi_teorici" che lo riempie con i dati che il motore del simulatore avvia in maniera teorica (non modifica i dati reali)'''
        giorni_utili_standard = 55
        
        # inizializza le variabili per il grafico con i valori considerando come base 55 giorni utili a stagione
        # Questo numero esprime mediamente quanti giorni, esclusi festivi, domeniche ci sono in una stagione di 3 mesi
        ore_base_stagione = giorni_utili_standard * self.motore.ditta.ore_giorno_standard
        
        quota_a_nominale = self.motore.ditta.operai_grado_A * ore_base_stagione
        quota_b_nominale = self.motore.ditta.operai_grado_B * ore_base_stagione
        quota_harv_nominale = self.motore.ditta.harvester_abbattitori * ore_base_stagione
        quota_forw_nominale = self.motore.ditta.forwarder_caricatori * ore_base_stagione

        quota_tratt_alta_nominale = self.motore.ditta.trattori_alta_potenza * ore_base_stagione
        quota_tratt_media_nominale = self.motore.ditta.trattori_media_potenza * ore_base_stagione
        
        quota_piatt_nominale = self.motore.ditta.piattaforme_aeree_semoventi * ore_base_stagione
        quota_cipp_nominale = self.motore.ditta.cippatrice * ore_base_stagione

        ore_a_richieste = 0.0
        ore_b_richieste = 0.0
        ore_harv_richieste = 0.0
        ore_forw_richieste = 0.0
        ore_tratt_alta_richieste = 0.0
        ore_tratt_media_richieste = 0.0
        ore_piattaforma_richieste = 0.0
        ore_cippatrice_richieste = 0.0

        # Avvia la simulazione in versione previsionale (non modifica i dati reali) ed ottiene la lista degli interventi che sarebbero preventivati per tutti i lotti nella stagione
        interventi_teorici = self.motore.prevedi_domanda_stagionale()
        
        # Cicla in tutti gl interventi previsti e calcola per ogni risorsa, personale o strumentazione, il totale di ore che sono necessarie
        for intervento in interventi_teorici:
            combi_squadra = intervento.get("specifiche_richiesta", {})
            
            ore_a_richieste += combi_squadra.get("grado_A", 0.0)
            ore_b_richieste += combi_squadra.get("grado_B", 0.0)
            ore_harv_richieste += combi_squadra.get("harvester", 0.0)
            ore_forw_richieste += combi_squadra.get("forwarder", 0.0)
            ore_tratt_alta_richieste += combi_squadra.get("trattori_alta", 0.0)
            ore_tratt_media_richieste += combi_squadra.get("trattori_media", 0.0)
            ore_piattaforma_richieste += combi_squadra.get("piattaforme", 0.0)
            ore_cippatrice_richieste += combi_squadra.get("cippatrice", 0.0)
        
        self.ax_risorse.clear()
        
        # Crea le liste con le tipologie di rese ed i valori che saranno passati al grafico per la visualizzazione
        categorie = ['Grado A\n(Spec.)', 'Grado B\n(Manov.)', 'Harvester', 'Forwarder', 'Trattori\nAlta', 'Trattori\nMedia', 'Piattaf.', 'Cippatrice']
        ore_totali_nominali = [quota_a_nominale, quota_b_nominale, quota_harv_nominale, quota_forw_nominale,
                               quota_tratt_alta_nominale, quota_tratt_media_nominale, quota_piatt_nominale, quota_cipp_nominale]
        ore_domanda_effettiva = [ore_a_richieste, ore_b_richieste, ore_harv_richieste, ore_forw_richieste, ore_tratt_alta_richieste, 
                                 ore_tratt_media_richieste, ore_piattaforma_richieste, ore_cippatrice_richieste]

        # imposta la larghezza delle barre
        larghezza_barre = 0.45 

        self.ax_risorse.bar(categorie, ore_totali_nominali, label='Capacità Ditta Base', color='#222c3e', edgecolor='#3a4a63', linewidth=1.0, width=larghezza_barre)
        
        ore_interne = []
        ore_extra = []
        colori_extra = []
        
        chiave_risorsa_lista = ["grado_A", "grado_B", "harvester", "forwarder", "trattori_alta", "trattori_media", "piattaforme", "cippatrice"]
        
        # Grafico a barre "impilate" (stacked bar chart) che permette di capire, a colpo d'occhio, se la ditta è in grado di coprire la domanda stagionale o se è in una situazione di crisi operativa
        # Il ciclo utilizza il comando zip, potente strumento di Python, che prende la prima riga di ogni colonna, le unisce in una tupla su cui ciclare
        for richiesta, limite, chiave in zip(ore_domanda_effettiva, ore_totali_nominali, chiave_risorsa_lista):
            # prende la tipologia della categoria presente nella lista chiave_risorsa_lista e la normalizza
            cat_mercato = self.motore.ditta._ottieni_chiave_elasticita(chiave)
            
            # acquisisce il valore massimo di unità presenti nella lista dei noli per la specifica categoria 
            unita_nolo_max = getattr(self.motore.ditta, "limiti_noli_stagionali", {}).get(cat_mercato, 1)
            # ottiene il limite massimo di ore da nolo e le somma alle ore massime impiegabili dalla ditta
            ore_massime_mercato = unita_nolo_max * ore_base_stagione
            limite_massimo = limite + ore_massime_mercato
            
            
            # imposta i valori che serviranno per creare il grafico a barre impilato
            val_interno = min(richiesta, limite)
            val_extra = max(0.0, richiesta - limite)
            
            ore_interne.append(val_interno)
            ore_extra.append(val_extra)
            
            # gestisce il colore della barra extra a rosso se le ore a disposizione non sono sufficienti, gialle se sono necessari i noleggi
            if richiesta > limite_massimo and limite_massimo > 0:
                colori_extra.append('#ff5252') # Sforamento totale (Rosso Corsa)
            else:
                colori_extra.append('#ffb74d') # Entro i limiti di nolo (Arancione)
        
        # imposta la le barre per vedere sovrapposte le ore interne e quelle dei noli        
        self.ax_risorse.bar(categorie, ore_interne, label = 'Richiesta (Propri)', color = '#0288d1', alpha = 0.9, width = larghezza_barre)
        self.ax_risorse.bar(categorie, ore_extra, bottom = ore_interne, label = 'Richiesta (Noli)', color = colori_extra, alpha = 0.9, width = larghezza_barre)

        self.ax_risorse.set_ylabel('Ore Lavoro (h)', color='#8ab4f8')
        
        # Il grafico si auto-scala basandosi solo sulla barra più alta visibile
        valore_massimo_grafico = max(max(ore_totali_nominali), max(ore_domanda_effettiva)) if ore_totali_nominali or ore_domanda_effettiva else 450
        self.ax_risorse.set_ylim(0, valore_massimo_grafico * 1.25)
        
        self.ax_risorse.tick_params(colors='#8ab4f8', labelsize=8)
        
        # Legenda espansa orizzontalmente e ripulita
        self.ax_risorse.legend(
            facecolor='#171e2c', edgecolor='none', labelcolor='#ffffff', 
            loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3, fontsize=8
        )
        
        self.ax_risorse.grid(axis='y', color='#2b364a', linestyle='--', alpha=0.4)
        self.canvas_risorse.draw()

    def _ridisegna_grafico_rese_cumulate(self):
        '''aggiornare visivamente i grafici delle rese produttive ogni volta che il simulatore avanza di un trimestre
           il grafico è suddiviso per le due tipologie di rese differenti opera ed industria'''
        self.ax_opera.clear()
        self.ax_industria.clear()
        
        step_visibili = self.storico_trimestri[-8:]  
        quanti_punti = len(step_visibili)
        
        if quanti_punti == 0:
            self.canvas_rese.draw()
            return
            
        indici_x = np.arange(quanti_punti)
        larghezza_colonna = 0.35

        self.ax_opera.bar(indici_x, self.storico_opera[-quanti_punti:], width=larghezza_colonna, color='#4fc3f7', label='Resa Opera (m³)')
        self.ax_opera.set_ylabel('Opera (m³/anno)', color='#4fc3f7', fontsize=8, fontweight='bold', labelpad=8)
        self.ax_opera.tick_params(axis='y', colors='#4fc3f7', labelsize=8)
        self.ax_opera.grid(axis='y', color='#2b364a', linestyle='--', alpha=0.25)
        self.ax_opera.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
        
        self.ax_opera.legend(
            facecolor='#171e2c', edgecolor='none', labelcolor='#ffffff', 
            loc='upper center', bbox_to_anchor=(0.5, 1.35), fontsize=8
        )

        self.ax_industria.bar(indici_x - (larghezza_colonna/2), self.storico_cartiera[-quanti_punti:], width=larghezza_colonna/2, color='#a8ffb2', label='Resa Cartiera (t)')
        self.ax_industria.bar(indici_x + (larghezza_colonna/2), self.storico_truciolato[-quanti_punti:], width=larghezza_colonna/2, color='#ffb74d', label='Resa Truciolato (t)')
        
        self.ax_industria.set_ylabel('Industria (t/anno)', color='#8ab4f8', fontsize=8, fontweight='bold', labelpad=8)
        self.ax_industria.tick_params(axis='y', colors='#8ab4f8', labelsize=8)
        self.ax_industria.grid(axis='y', color='#2b364a', linestyle='--', alpha=0.25)
        
        self.ax_industria.legend(
            facecolor='#171e2c', edgecolor='none', labelcolor='#ffffff', 
            loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=2, fontsize=8
        )

        self.ax_industria.set_xticks(indici_x)
        self.ax_industria.set_xticklabels(step_visibili)
        self.ax_industria.tick_params(axis='x', rotation=35, labelsize=7, colors='#8ab4f8')

        self.canvas_rese.draw()


    