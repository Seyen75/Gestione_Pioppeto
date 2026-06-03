import os
from typing import Dict, Any, List

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

    def _aggiorna_interfaccia_grafica(self, quadro_stato: Dict[str, Any] = None, iniziale: bool = False):
        self.ui.lbl_anno.setText(f"ANNO {self.parametri.anno_corrente}")
        self.ui.lbl_stagione.setText(self.parametri.stagione_corrente.upper())

        self._elabora_e_mostra_consuntivi(quadro_stato, iniziale)
        self._popola_tabella_particellare()
        self._rendiconta_e_disegna_previsione_risorse()
        self._ridisegna_grafico_rese_cumulate()

    def _elabora_e_mostra_consuntivi(self, quadro_stato: Dict[str, Any], iniziale: bool):
        # 1. Leggiamo il registro All-Time dal motore (o usiamo zeri se appena avviato)
        stats = getattr(self.motore, "stats_globali", {
            "tagli_strutturali_saltati": 0, 
            "tagli_biologici_saltati": 0, 
            "lavorazioni_generiche_saltate": 0
        })
        
        t_strut = stats.get("tagli_strutturali_saltati", 0)
        t_bio = stats.get("tagli_biologici_saltati", 0)
        l_gen = stats.get("lavorazioni_generiche_saltate", 0)

        # 2. Aggiorniamo le tre Label del Cruscotto Diagnostico
        if hasattr(self.ui, "lbl_tagli_saltati"):
            self.ui.lbl_tagli_saltati.setText(f"⛔ Tagli Saltati (Carenza Mezzi): {t_strut}")
            self.ui.lbl_tagli_saltati.setVisible(True)
            self.ui.lbl_tagli_saltati.setStyleSheet("color: #ff5252; font-weight: bold;" if t_strut > 0 else "color: #00e676; font-weight: bold;")

        if hasattr(self.ui, "lbl_turni_saltati"):
            self.ui.lbl_turni_saltati.setText(f"⏳ Tagli Rinviati (Immaturità Biologica): {t_bio}")
            self.ui.lbl_turni_saltati.setVisible(True)
            self.ui.lbl_turni_saltati.setStyleSheet("color: #ffb74d; font-weight: bold;" if t_bio > 0 else "color: #00e676; font-weight: bold;")

        if hasattr(self.ui, "lbl_lavori_saltati"):
            self.ui.lbl_lavori_saltati.setText(f"⚠️ Lavorazioni Fallite (Carenza Risorse): {l_gen}")
            self.ui.lbl_lavori_saltati.setVisible(True)
            self.ui.lbl_lavori_saltati.setStyleSheet("color: #ff5252; font-weight: bold;" if l_gen > 0 else "color: #00e676; font-weight: bold;")

        # 3. Pulizia di sicurezza: Nascondiamo le vecchie etichette se sono ancora nel file .ui
        etichette_da_nascondere = ["lbl_opera_totale", "lbl_cartiera_totale", "lbl_truciolato_totale", "lbl_fallanze_totali"]
        for lbl in etichette_da_nascondere:
            if hasattr(self.ui, lbl):
                getattr(self.ui, lbl).setVisible(False)

        # 4. Inizializzazione storico per i grafici a barre inferiori
        if not self.storico_trimestri:
            self.storico_trimestri.append("Avvio")
            self.storico_opera.append(0.0)
            self.storico_cartiera.append(0.0)
            self.storico_truciolato.append(0.0)

    def _popola_tabella_particellare(self):
        self.ui.tbl_monitoraggio.setRowCount(0)
        colonne_labels = ["ID Particella", "Destinazione d'Uso", "Superficie", "N° Piante", "Età Biologica", "Diametro Medio", "Altezza Stimata", "Stato Cantiere"]
        self.ui.tbl_monitoraggio.setColumnCount(len(colonne_labels))
        self.ui.tbl_monitoraggio.setHorizontalHeaderLabels(colonne_labels)
        self.ui.tbl_monitoraggio.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        for lotto in self.parametri.collezione_lotti:
            riga = self.ui.tbl_monitoraggio.rowCount()
            self.ui.tbl_monitoraggio.insertRow(riga)

            destinazione = getattr(lotto, "destinazione_uso", "OPERA")
            eta = getattr(lotto, "eta", 0)  
            superficie = getattr(lotto, "superficie_ettari", 0.0)
            
            if hasattr(lotto, "dati_correnti") and lotto.dati_correnti:
                piante_vive = lotto.dati_correnti.get("piante_attive", getattr(lotto, "numero_piante_vive", 0))
                dbh = lotto.dati_correnti.get("dbh_reale_cm", 0.0)
                altezza = lotto.dati_correnti.get("altezza_m", 0.0)
            else:
                piante_vive = getattr(lotto, "numero_piante_vive", 0)
                dbh = getattr(lotto, "diametro_medio_fusto", 0.0)
                altezza = getattr(lotto, "altezza_media_piante", 0.0)
            
            is_maturo = lotto.verifica_maturita_raccolta()
            filiera_lotto = STRUTTURA_LAVORAZIONI.get(lotto.destinazione_uso, STRUTTURA_LAVORAZIONI["OPERA"])
            
            if is_maturo or getattr(lotto, "tagliato", False):
                if self.parametri.stagione_corrente == "Inverno":
                    stato_stringa = "Pianificato per la Raccolta (Taglio raso)"
                else:
                    stato_stringa = "In attesa dell'Inverno per Taglio"
            else:
                f_k = self.motore._get_chiave_fase(lotto.eta)
                ops_attive = filiera_lotto.get(f_k, {}).get(self.parametri.stagione_corrente, [])
                stato_stringa = " + ".join([o.get("descrizione", "") for o in ops_attive]) if ops_attive else "Riposo vegetativo"

            self.ui.tbl_monitoraggio.setItem(riga, 0, QTableWidgetItem(str(lotto.id_lotto)))
            self.ui.tbl_monitoraggio.setItem(riga, 1, QTableWidgetItem(str(destinazione)))
            self.ui.tbl_monitoraggio.setItem(riga, 2, QTableWidgetItem(f"{self._formatta_numero_it(superficie)} ha"))
            self.ui.tbl_monitoraggio.setItem(riga, 3, QTableWidgetItem(f"{int(piante_vive):,}".replace(",", ".")))
            self.ui.tbl_monitoraggio.setItem(riga, 4, QTableWidgetItem(f"{eta} anni"))
            self.ui.tbl_monitoraggio.setItem(riga, 5, QTableWidgetItem(f"{self._formatta_numero_it(dbh)} cm"))
            self.ui.tbl_monitoraggio.setItem(riga, 6, QTableWidgetItem(f"{self._formatta_numero_it(altezza)} m"))
            self.ui.tbl_monitoraggio.setItem(riga, 7, QTableWidgetItem(stato_stringa))

        header = self.ui.tbl_monitoraggio.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tbl_monitoraggio.setColumnWidth(0, 95)   
        self.ui.tbl_monitoraggio.setColumnWidth(1, 120)  
        self.ui.tbl_monitoraggio.setColumnWidth(2, 95)   
        self.ui.tbl_monitoraggio.setColumnWidth(3, 90)   
        self.ui.tbl_monitoraggio.setColumnWidth(4, 90)   
        self.ui.tbl_monitoraggio.setColumnWidth(5, 105)  
        self.ui.tbl_monitoraggio.setColumnWidth(6, 105)  
        header.setSectionResizeMode(7, QHeaderView.Stretch)  

        for r in range(self.ui.tbl_monitoraggio.rowCount()):
            for c in range(self.ui.tbl_monitoraggio.columnCount()):
                item = self.ui.tbl_monitoraggio.item(r, c)
                if item: item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def _rendiconta_e_disegna_previsione_risorse(self):
        giorni_utili_standard = 55
        ore_base_stagione = giorni_utili_standard * self.motore.ditta.ore_giorno_standard
        
        quota_a_nominale = self.motore.ditta.operai_grado_A * ore_base_stagione
        quota_b_nominale = self.motore.ditta.operai_grado_B * ore_base_stagione
        quota_harv_nominale = self.motore.ditta.harvester_abbattitori * ore_base_stagione
        quota_forw_nominale = self.motore.ditta.forwarder_caricatori * ore_base_stagione
        quota_tratt_nominale = self.motore.ditta.trattori_media_potenza * ore_base_stagione
        quota_piatt_nominale = self.motore.ditta.piattaforme_aeree_semoventi * ore_base_stagione

        ore_a_richieste = 0.0
        ore_b_richieste = 0.0
        ore_harv_richieste = 0.0
        ore_forw_richieste = 0.0
        ore_trattore_richieste = 0.0
        ore_piattaforma_richieste = 0.0

        interventi_teorici = self.motore.prevedi_domanda_stagionale()
        
        for intervento in interventi_teorici:
            combi_squadra = intervento.get("specifiche_richiesta", {})
            
            ore_a_richieste += combi_squadra.get("grado_A", 0.0)
            ore_b_richieste += combi_squadra.get("grado_B", 0.0)
            ore_harv_richieste += combi_squadra.get("harvester", 0.0)
            ore_forw_richieste += combi_squadra.get("forwarder", 0.0)
            ore_trattore_richieste += combi_squadra.get("trattori_alta", 0.0) + combi_squadra.get("trattori_media", 0.0)
            ore_piattaforma_richieste += combi_squadra.get("piattaforme", 0.0)

        self.ax_risorse.clear()
        categorie = ['Grado A\n(Spec.)', 'Grado B\n(Manov.)', 'Harvester', 'Forwarder', 'Trattori', 'Piattaf.']
        ore_totali_nominali = [quota_a_nominale, quota_b_nominale, quota_harv_nominale, quota_forw_nominale, quota_tratt_nominale, quota_piatt_nominale]
        ore_domanda_effettiva = [ore_a_richieste, ore_b_richieste, ore_harv_richieste, ore_forw_richieste, ore_trattore_richieste, ore_piattaforma_richieste]

        larghezza_barre = 0.45 

        self.ax_risorse.bar(categorie, ore_totali_nominali, label='Capacità Ditta Base', color='#222c3e', edgecolor='#3a4a63', linewidth=1.0, width=larghezza_barre)
        
        ore_interne = []
        ore_extra = []
        colori_extra = []
        tetti_massimi_elastici = []
        chiave_risorsa_lista = ["grado_A", "grado_B", "harvester", "forwarder", "trattori_media", "piattaforme"]
        
        for richiesta, limite, chiave in zip(ore_domanda_effettiva, ore_totali_nominali, chiave_risorsa_lista):
            cat_mercato = self.motore.ditta._ottieni_chiave_elasticita(chiave)
            moltiplicatore_attivo = self.motore.ditta.moltiplicatori_elasticita.get(cat_mercato, 2.0)
            soffitto_reale = limite * moltiplicatore_attivo
            tetti_massimi_elastici.append(soffitto_reale)
            
            val_interno = min(richiesta, limite)
            val_extra = max(0.0, richiesta - limite)
            
            ore_interne.append(val_interno)
            ore_extra.append(val_extra)
            
            if richiesta > soffitto_reale and soffitto_reale > 0:
                colori_extra.append('#ff5252') 
            else:
                colori_extra.append('#ffb74d') 
                
        self.ax_risorse.bar(categorie, ore_interne, label='Richiesta (Personale/Mezzi Propri)', color='#0288d1', alpha=0.9, width=larghezza_barre)
        self.ax_risorse.bar(categorie, ore_extra, bottom=ore_interne, label='Richiesta (Stagionali/Noli)', color=colori_extra, alpha=0.9, width=larghezza_barre)

        for i, soffitto in enumerate(tetti_massimi_elastici):
            if soffitto > 0:
                margine_linea = (larghezza_barre / 2) + 0.1
                self.ax_risorse.hlines(y=soffitto, xmin=i - margine_linea, xmax=i + margine_linea, colors='#00e676', linewidth=2.0, zorder=5)

        self.ax_risorse.set_ylabel('Ore Lavoro (h)', color='#8ab4f8')
        limite_g = max(max(tetti_massimi_elastici), max(ore_domanda_effettiva)) if ore_domanda_effettiva else 450
        self.ax_risorse.set_ylim(0, limite_g * 1.25)
        self.ax_risorse.tick_params(colors='#8ab4f8', labelsize=8)
        
        self.ax_risorse.plot([], [], color='#00e676', linewidth=2.0, label='Limite Max (con Noli)')
        
        self.ax_risorse.legend(
            facecolor='#171e2c', edgecolor='none', labelcolor='#ffffff', 
            loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, fontsize=8
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

    @Slot()
    def slot_avanza_trimestre(self):
        stagione_appena_conclusa = self.parametri.stagione_corrente
        anno_appena_concluso = self.parametri.anno_corrente

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