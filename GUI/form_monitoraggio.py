import os
from typing import Dict, Any

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QScreen, QGuiApplication

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class form_monitoraggio(QWidget):
    def __init__(self, motore_simulazione, parent=None):
        super().__init__(parent)
        self.motore = motore_simulazione
        self.parametri = motore_simulazione.parametri
        
        self.storico_trimestri: list[str] = []
        self.storico_opera: list[float] = []
        self.storico_cartiera: list[float] = []
        self.storico_truciolato: list[float] = []

        self._cumulato_opera_precedente = 0.0
        self._cumulato_cartiera_precedente = 0.0
        self._cumulato_truciolato_precedente = 0.0

        self._carica_interfaccia()
        self._inizializza_grafici()
        
        self.ui.btn_prossimo_trimestre.clicked.connect(self.slot_avanza_trimestre)
        self.ui.btn_termina_sessione.clicked.connect(self.slot_termina_simulazione)

        self._aggiorna_interfaccia_grafica(quadro_stato=None, iniziale=True)
        self._centra_finestra_su_schermo()

    def _carica_interfaccia(self):
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_monitoraggio.ui")
        self.ui = loader.load(percorso_ui, self)
        
        layout_principale = QVBoxLayout(self)
        layout_principale.addWidget(self.ui)
        layout_principale.setContentsMargins(0, 0, 0, 0)

    def _centra_finestra_su_schermo(self):
        schermo: QScreen = QGuiApplication.primaryScreen()
        if self.parent() and self.parent().window():
            schermo = self.parent().window().screen()
            
        if schermo:
            geometria_schermo = schermo.geometry()
            larghezza_form = self.width() if self.width() > 100 else 1100
            altezza_form = self.height() if self.height() > 100 else 750
            x = (geometria_schermo.width() - larghezza_form) // 2
            y = (geometria_schermo.height() - altezza_form) // 2
            self.move(geometria_schermo.x() + x, geometria_schermo.y() + y)

    def _formatta_numero_it(self, valore: float) -> str:
        stringa_base = f"{valore:,.1f}"
        stringa_it = stringa_base.replace(",", "X").replace(".", ",").replace("X", ".")
        return stringa_it


    # Inizializzazione dei grafici presenti nella form
    
    def _inizializza_grafici(self):
        colore_sfondo_hex = "#141923"

        self.fig_risorse = Figure(figsize=(6, 3), facecolor=colore_sfondo_hex)
        self.canvas_risorse = FigureCanvas(self.fig_risorse)
        self.ax_risorse = self.fig_risorse.add_subplot(111)
        self.ax_risorse.set_facecolor(colore_sfondo_hex)
        
        self.fig_risorse.subplots_adjust(top=0.80, bottom=0.20, left=0.12, right=0.95)
        
        layout_risorse = QVBoxLayout(self.ui.canvas_risorse)
        layout_risorse.addWidget(self.canvas_risorse)
        layout_risorse.setContentsMargins(0, 0, 0, 0)

        self.fig_rese = Figure(figsize=(5, 3), facecolor=colore_sfondo_hex)
        self.canvas_rese = FigureCanvas(self.fig_rese)
        
        self.ax_opera = self.fig_rese.add_subplot(211)  
        self.ax_industria = self.fig_rese.add_subplot(212, sharex=self.ax_opera) 
        
        self.ax_opera.set_facecolor(colore_sfondo_hex)
        self.ax_industria.set_facecolor(colore_sfondo_hex)
        
        self.fig_rese.subplots_adjust(top=0.78, bottom=0.22, left=0.16, right=0.95, hspace=0.65)
        
        layout_rese = QVBoxLayout(self.ui.canvas_rese)
        layout_rese.addWidget(self.canvas_rese)
        layout_rese.setContentsMargins(0, 0, 0, 0)


    # Funzione che terminata la simulazione di una stagione avvia le funzioni per aggiornare le tabelle ed i grafici
    
    def _aggiorna_interfaccia_grafica(self, quadro_stato: Dict[str, Any] = None, iniziale: bool = False):
        # Aggiorna le label con i dati dell'anno e della stagione corrente
        self.ui.lbl_anno.setText(f"ANNO {self.parametri.anno_corrente}")
        self.ui.lbl_stagione.setText(self.parametri.stagione_corrente.upper())

        # Avvia le funzioni di aggiornamento dei vari controlli e popola tabelle e grafici
        self._elabora_e_mostra_consuntivi(quadro_stato, iniziale)
        self._popola_tabella_particellare()
        self._rendiconta_e_disegna_previsione_risorse()
        self._ridisegna_grafico_rese_cumulate()


    # Funzione che 
    
    def _elabora_e_mostra_consuntivi(self, quadro_stato: Dict[str, Any], iniziale: bool):
        # Legge il registro del motore e se non esiste 
        stats = getattr(self.motore, "stats_globali", {
            "tagli_strutturali_saltati": 0, 
            "tagli_biologici_saltati": 0, 
            "lavorazioni_generiche_saltate": 0
        })
        
        t_strut = stats.get("tagli_strutturali_saltati", 0)
        t_bio = stats.get("tagli_biologici_saltati", 0)
        l_gen = stats.get("lavorazioni_generiche_saltate", 0)

        # Aggiorna le Label del Cruscotto Diagnostico con i dati recuperati dal dizionario generale nella chiava stats_globali

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
            
            # Prende i dati del lotto 
            destinazione = lotto.destinazione_uso
            eta = lotto.eta
            superficie = lotto.superficie_ettari
            
            if lotto.dati_correnti:
                piante_vive = lotto.dati_correnti["piante_attive"]
                dbh = lotto.dati_correnti["dbh_reale_cm"]
                altezza = lotto.dati_correnti["altezza_m"]
            else:
                piante_vive = lotto.numero_piante_vive
                dbh = lotto.diametro_medio_fusto
                altezza = lotto.altezza_media_piante

            # Verifica 
            # 1. Salva lo stato originale dei dati biologici del lotto
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

            filiera_lotto = STRUTTURA_LAVORAZIONI[lotto.destinazione_uso]
            
            if is_maturo or lotto.tagliato:
                if self.parametri.stagione_corrente == "Inverno":
                    stato_stringa = "Pianificato per la Raccolta (Taglio raso)"
                else:
                    stato_stringa = "In attesa dell'Inverno per Taglio"
            else:
                f_k = lotto.get_fase_colturale()
                ops_attive = filiera_lotto.get(f_k, {}).get(self.parametri.stagione_corrente, [])
                stato_stringa = " + ".join([o["descrizione"] for o in ops_attive]) if ops_attive else "Riposo vegetativo"

            # Setta i valori delle varie colonne della riga appena creata
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
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                
    # La funzione disegna il grafico delle uso delle risorse della ditta
    # La funzione per graficare le necessità delle risorse per la stagione in corso che deve ancora essere materialmente simulata
    # utilizza un dizionario "interventi_teorici" che lo riempie con i dati che il motore del simulatore avvia in maniera teorica

    def _rendiconta_e_disegna_previsione_risorse(self):
        giorni_utili_standard = 55
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

        # Avvia la simulazione in versione previsionale (non modifica i dati reali)
        interventi_teorici = self.motore.prevedi_domanda_stagionale()
        
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
        
        # Aggiunta la colonna separata nell'asse X
        categorie = ['Grado A\n(Spec.)', 'Grado B\n(Manov.)', 'Harvester', 'Forwarder', 'Trattori\nAlta', 'Trattori\nMedia', 'Piattaf.', 'Cippatrice']
        ore_totali_nominali = [quota_a_nominale, quota_b_nominale, quota_harv_nominale, quota_forw_nominale, quota_tratt_alta_nominale, quota_tratt_media_nominale, quota_piatt_nominale, quota_cipp_nominale]
        ore_domanda_effettiva = [ore_a_richieste, ore_b_richieste, ore_harv_richieste, ore_forw_richieste, ore_tratt_alta_richieste, ore_tratt_media_richieste, ore_piattaforma_richieste, ore_cippatrice_richieste]

        larghezza_barre = 0.45 

        self.ax_risorse.bar(categorie, ore_totali_nominali, label='Capacità Ditta Base', color='#222c3e', edgecolor='#3a4a63', linewidth=1.0, width=larghezza_barre)
        
        ore_interne = []
        ore_extra = []
        colori_extra = []
        
        chiave_risorsa_lista = ["grado_A", "grado_B", "harvester", "forwarder", "trattori_alta", "trattori_media", "piattaforme", "cippatrice"]
        
        for richiesta, limite, chiave in zip(ore_domanda_effettiva, ore_totali_nominali, chiave_risorsa_lista):
            cat_mercato = self.motore.ditta._ottieni_chiave_elasticita(chiave)
            
            unita_nolo_max = getattr(self.motore.ditta, "limiti_noli_stagionali", {}).get(cat_mercato, 1)
            ore_massime_mercato = unita_nolo_max * ore_base_stagione
            soffitto_reale = limite + ore_massime_mercato
            
            val_interno = min(richiesta, limite)
            val_extra = max(0.0, richiesta - limite)
            
            ore_interne.append(val_interno)
            ore_extra.append(val_extra)
            
            # --- LOGICA DEI COLORI MANTENUTA ---
            if richiesta > soffitto_reale and soffitto_reale > 0:
                colori_extra.append('#ff5252') # Sforamento totale (Rosso Corsa)
            else:
                colori_extra.append('#ffb74d') # Entro i limiti di nolo (Arancione)
                
        self.ax_risorse.bar(categorie, ore_interne, label='Richiesta (Personale/Mezzi Propri)', color='#0288d1', alpha=0.9, width=larghezza_barre)
        self.ax_risorse.bar(categorie, ore_extra, bottom=ore_interne, label='Richiesta (Stagionali/Noli)', color=colori_extra, alpha=0.9, width=larghezza_barre)

        self.ax_risorse.set_ylabel('Ore Lavoro (h)', color='#8ab4f8')
        
        # --- FIX 2: Adattamento dinamico scala (Addio linea verde) ---
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

    # Funzione che manda avanti una stagione alla volta della simulazione e si occupa di gestire gli aggiornamenti dei grafici

    @Slot()
    def slot_avanza_trimestre(self):
        # Tiene traccia delle stagione precedente
        stagione_appena_conclusa = self.parametri.stagione_corrente
        anno_appena_concluso = self.parametri.anno_corrente

        # 
        if "Avvio" in self.storico_trimestri:
            self.storico_trimestri.remove("Avvio")
            self.storico_opera.clear()
            self.storico_cartiera.clear()
            self.storico_truciolato.clear()

        quadro_stato = self.motore.avanza_passo_simulazione()

        # Solo l'Inverno chiude l'anno agricolo e aggiorna i grafici a barre delle rese
        if stagione_appena_conclusa == "Inverno":
            chiave_anno = f"Anno {anno_appena_concluso}"
            produzione_cumulata = quadro_stato.get("produzione_cumulata", {})
            
            cumulato_opera_attuale = produzione_cumulata.get("opera_m3", 0.0)
            cumulato_cartiera_attuale = produzione_cumulata.get("cartiera_t", 0.0)
            cumulato_truciolato_attuale = produzione_cumulata.get("truciolato_t", 0.0)

            netto_opera_anno = cumulato_opera_attuale - self._cumulato_opera_precedente
            netto_cartiera_anno = cumulato_cartiera_attuale - self._cumulato_cartiera_precedente
            netto_truciolato_anno = cumulato_truciolato_attuale - self._cumulato_truciolato_precedente

            if chiave_anno not in self.storico_trimestri:
                self.storico_trimestri.append(chiave_anno)
                self.storico_opera.append(max(0.0, netto_opera_anno))
                self.storico_cartiera.append(max(0.0, netto_cartiera_anno))
                self.storico_truciolato.append(max(0.0, netto_truciolato_anno))

                self._cumulato_opera_precedente = cumulato_opera_attuale
                self._cumulato_cartiera_precedente = cumulato_cartiera_attuale
                self._cumulato_truciolato_precedente = cumulato_truciolato_attuale

        self._aggiorna_interfaccia_grafica(quadro_stato=quadro_stato, iniziale=False)



    @Slot()
    def slot_termina_simulazione(self):
        if self.parent() and hasattr(self.parent(), "abilita_report_finale"):
            self.parent().abilita_report_finale()
        self.close()