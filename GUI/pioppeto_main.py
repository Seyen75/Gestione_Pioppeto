
# Modulo Finestra principale (Dashboard) del simulatore di pioppicoltura.
import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGraphicsDropShadowEffect, QMessageBox, QApplication, QProgressDialog
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from GUI.utils import mostra_messaggio_stilizzato

from Core.gestori_clone import GestoreCloni
from Core.ditta import Ditta
from Core.parametri_simulazione import ParametriSimulazione
from Core.SimulatorePioppicultura import SimulatorePioppicoltura
from Core.lotto import Lotto

from GUI.form_ditta import FormDitta
from GUI.form_lotti import FormLotti
from GUI.form_monitoraggio import form_monitoraggio
import risorse.rc_risorse

class PioppetoMain(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "pioppeto_main.ui")
        ui_temporanea = loader.load(percorso_ui, None) 

        widget_centrale = ui_temporanea.centralWidget()
        self.setCentralWidget(widget_centrale)
        self.setWindowTitle("Gestione Advanced per Sistemi di Pioppicoltura")

        self.gestore_cloni = GestoreCloni()
        self.dizionario_cloni = self.gestore_cloni.carica_cloni() 

        self.ditta_attiva = Ditta()
        self.parametri_condivisi = ParametriSimulazione()
        
        self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)


        self.parametri_condivisi.storico_stagionale = {}
        
        self.simulazione_eseguita: bool = False

        self.ditta_attiva.operai_grado_A = 4         
        self.ditta_attiva.operai_grado_B = 2         
        
        self.ditta_attiva.trattori_alta_potenza = 1
        self.ditta_attiva.trattori_media_potenza = 3 
        self.ditta_attiva.piattaforme_aeree_semoventi = 1
        
        self.ditta_attiva.harvester_abbattitori = 1
        self.ditta_attiva.forwarder_caricatori = 1
        
        self.ditta_attiva.kit_motoseghe_professionali = 4
        self.ditta_attiva.coefficiente_iufro = 0.80 

        # Tetti massimi al ricorso del mercato (Noli stagionali)
        self.ditta_attiva.limiti_noli_stagionali = {
            "personale_spec": 6,   
            "personale_comune": 15, 
            "harvester": 1,        
            "forwarder": 1,
            "trattori_alta": 1,
            "trattori_media": 4,
            "piattaforme": 2
        }
        
        
        
        if hasattr(self.ditta_attiva, "inizializza_serbatoi_stagionali"):
            self.ditta_attiva.inizializza_serbatoi_stagionali(55)
        else:
            ore_standard = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) * 450.0
            self.ditta_attiva.serbatoi_ore = {
                "Primavera": ore_standard, "Estate": ore_standard, "Autunno": ore_standard, "Inverno": ore_standard
            }

        self.parametri_condivisi.anni_durata_target = 10

        configurazione_lotti_default = [
            # --- FILIERA OPERA (Ciclo 10 anni) - 20 Lotti ---
            # Taglio Imminente (Maturano l'anno prossimo)
            {"id": "LTI-001", "clone": "I-214",   "dest": "OPERA", "eta": 9, "superficie": 13.5, "idrico": 0.0},
            {"id": "LTI-002", "clone": "Neva",    "dest": "OPERA", "eta": 9, "superficie": 12.0, "idrico": 0.1},
            
            # Fase Tardo Mantenimento
            {"id": "LTI-003", "clone": "Velasco", "dest": "OPERA", "eta": 8, "superficie": 14.0, "idrico": 0.2},
            {"id": "LTI-004", "clone": "I-214",   "dest": "OPERA", "eta": 8, "superficie": 13.0, "idrico": -0.1},
            {"id": "LTI-005", "clone": "Neva",    "dest": "OPERA", "eta": 7, "superficie": 12.5, "idrico": 0.0},
            {"id": "LTI-006", "clone": "I-214",   "dest": "OPERA", "eta": 7, "superficie": 13.5, "idrico": -0.2},
            {"id": "LTI-007", "clone": "Velasco", "dest": "OPERA", "eta": 6, "superficie": 13.0, "idrico": 0.0},
            {"id": "LTI-008", "clone": "I-214",   "dest": "OPERA", "eta": 6, "superficie": 12.5, "idrico": 0.1},
            {"id": "LTI-009", "clone": "Neva",    "dest": "OPERA", "eta": 5, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-010", "clone": "I-214",   "dest": "OPERA", "eta": 5, "superficie": 12.0, "idrico": 0.0},
            
            # Fase Giovane (Potature in quota)
            {"id": "LTI-011", "clone": "Velasco", "dest": "OPERA", "eta": 4, "superficie": 13.5, "idrico": 0.2},
            {"id": "LTI-012", "clone": "Neva",    "dest": "OPERA", "eta": 4, "superficie": 13.0, "idrico": -0.1},
            {"id": "LTI-013", "clone": "I-214",   "dest": "OPERA", "eta": 3, "superficie": 12.0, "idrico": 0.0},
            {"id": "LTI-014", "clone": "Velasco", "dest": "OPERA", "eta": 3, "superficie": 14.0, "idrico": -0.1},
            {"id": "LTI-015", "clone": "I-214",   "dest": "OPERA", "eta": 2, "superficie": 13.5, "idrico": 0.1},
            {"id": "LTI-016", "clone": "Neva",    "dest": "OPERA", "eta": 2, "superficie": 12.5, "idrico": 0.0},
            
            # Nuovi Impianti (Lavorazioni a terra)
            {"id": "LTI-017", "clone": "I-214",   "dest": "OPERA", "eta": 1, "superficie": 14.0, "idrico": -0.2},
            {"id": "LTI-018", "clone": "Velasco", "dest": "OPERA", "eta": 1, "superficie": 13.0, "idrico": 0.0},
            {"id": "LTI-019", "clone": "I-214",   "dest": "OPERA", "eta": 0, "superficie": 12.5, "idrico": 0.1},
            {"id": "LTI-020", "clone": "Neva",    "dest": "OPERA", "eta": 0, "superficie": 13.5, "idrico": 0.0},

            # --- FILIERA INDUSTRIA (Ciclo 5 anni) - 10 Lotti ---
            {"id": "LTI-021", "clone": "AF2",     "dest": "INDUSTRIA", "eta": 4, "superficie": 15.0, "idrico": 0.1},
            {"id": "LTI-022", "clone": "I-45/51", "dest": "INDUSTRIA", "eta": 4, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-023", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 3, "superficie": 16.0, "idrico": -0.1},
            {"id": "LTI-024", "clone": "AF2",     "dest": "INDUSTRIA", "eta": 3, "superficie": 14.0, "idrico": 0.2},
            {"id": "LTI-025", "clone": "I-45/51", "dest": "INDUSTRIA", "eta": 2, "superficie": 15.5, "idrico": 0.0},
            {"id": "LTI-026", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 2, "superficie": 15.0, "idrico": -0.2},
            {"id": "LTI-027", "clone": "AF2",     "dest": "INDUSTRIA", "eta": 1, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-028", "clone": "I-45/51", "dest": "INDUSTRIA", "eta": 1, "superficie": 16.5, "idrico": 0.1},
            {"id": "LTI-029", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 0, "superficie": 15.0, "idrico": -0.1},
            {"id": "LTI-030", "clone": "AF2",     "dest": "INDUSTRIA", "eta": 0, "superficie": 14.0, "idrico": 0.2}
        ]
        
        
        # Inserimento dei lotti di default all'interno della struttura operativa con la creazione dei dati dinamici dei lotti già avanzati
        self.parametri_condivisi.collezione_lotti = []
        for conf in configurazione_lotti_default:
            lotto = Lotto(id_lotto=conf["id"], superficie=conf["superficie"])
            lotto.sesto_impianto = "6x6"
            lotto.clone_assegnato = conf["clone"]
            lotto.destinazione_uso = conf["dest"]
            lotto.indice_attrito_spaziale = 2
            lotto.indice_tendenza_idrica = conf["idrico"]
            
            lotto.eta = conf["eta"]  
            
            lotto.inizializza_nuovo_ciclo() 
            
            if lotto.eta > 0:
                profilo = self.motore_condiviso.dati_cloni[lotto.clone_assegnato]
                lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                lotto.diametro_medio_fusto = lotto.dati_correnti["dbh_reale_cm"]
                lotto.altezza_media_piante = lotto.dati_correnti["altezza_m"]
                lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
            else:
                # Inizializza i dati correnti anche per i lotti neonati
                lotto.dati_correnti = {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, 
                    "volume_singolo_m3": 0.0, "piante_attive": lotto.numero_piante_vive, 
                    "volume_totale_m3": 0.0
                }
            
            lotto.moltiplicatore_efficienza_clone = 1.0

            self.parametri_condivisi.collezione_lotti.append(lotto)

        btn_esci = widget_centrale.findChild(QPushButton, "btn_esci")
        self.btn_ditta = widget_centrale.findChild(QPushButton, "btn_gestione_ditta")
        self.btn_lotti = widget_centrale.findChild(QPushButton, "btn_gestione_lotti")
        self.btn_simulazione = widget_centrale.findChild(QPushButton, "btn_simulazione")
        self.btn_monitoraggio = widget_centrale.findChild(QPushButton, "btn_monitoraggio")
        self.btn_valutazioni = widget_centrale.findChild(QPushButton, "btn_valutazioni")
        self.btn_reset = widget_centrale.findChild(QPushButton, "btn_reset")

        if btn_esci: btn_esci.clicked.connect(QApplication.instance().quit)
        if self.btn_ditta: self.btn_ditta.clicked.connect(self.ditta)
        if self.btn_lotti: self.btn_lotti.clicked.connect(self.lotti)
        if self.btn_simulazione: self.btn_simulazione.clicked.connect(self.simulazione)
        if self.btn_monitoraggio: self.btn_monitoraggio.clicked.connect(self.monitoraggio)
        if self.btn_valutazioni: self.btn_valutazioni.clicked.connect(self.valutazione)
        if self.btn_reset: self.btn_reset.clicked.connect(self.ripristina_simulazione_globale)

        self.setStyleSheet("QMainWindow { border-image: url(:/sfondo_main.jpg) 0 0 0 0 stretch stretch; }")
        self.label_titolo = widget_centrale.findChild(QWidget, "label_titolo")
        if self.label_titolo:
            ombra = QGraphicsDropShadowEffect(self)
            ombra.setBlurRadius(8); ombra.setXOffset(3); ombra.setYOffset(3)
            ombra.setColor(QColor(0, 0, 0, 200))
            self.label_titolo.setGraphicsEffect(ombra)

        self.aggiorna_stato_interfaccia()
        self._centra_finestra()
        
    def _centra_finestra(self):
        """Centra la finestra principale esattamente in mezzo allo schermo."""
        # Forza Qt a calcolare le dimensioni reali della finestra
        self.adjustSize() 
        
        # Ottiene la risoluzione e lo spazio disponibile dello schermo principale
        schermo = QGuiApplication.primaryScreen().availableGeometry()
        
        # Ottiene le dimensioni e la posizione attuali della nostra finestra
        geometria_finestra = self.frameGeometry()
        
        # Sposta il centro del "rettangolo" della finestra al centro del "rettangolo" dello schermo
        geometria_finestra.moveCenter(schermo.center())
        
        # Muove fisicamente la finestra verso le nuove coordinate calcolate (in alto a sinistra)
        self.move(geometria_finestra.topLeft())

    def aggiorna_stato_interfaccia(self):
        ditta_pronta = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) > 0
        lotti_pronti = len(self.parametri_condivisi.collezione_lotti) > 0
    
        if not ditta_pronta or not lotti_pronti:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            if not ditta_pronta and not lotti_pronti:
                self.statusBar().showMessage("⚠️ Configurazione richiesta: inserire i dati della ditta e creare almeno un lotto.")
            elif not ditta_pronta:
                self.statusBar().showMessage("⚠️ Configurazione incompleta: configurare il personale ditta forestale.")
            else:
                self.statusBar().showMessage("⚠️ Configurazione incompleta: creare almeno un lotto colturale nel pioppeto.")
        elif ditta_pronta and lotti_pronti and not self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(True)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(True)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            self.statusBar().showMessage("✅ Sistema pronto. Scegliere 'Avvia Simulazione' (Batch) o 'Monitoraggio Real-Time' (Primavera -> Inverno).")
        elif self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(True)
            self.statusBar().showMessage("📊 Simulazione conclusa! Analisi diagnostica disponibili in 'Report Finale'.")

    def abilita_report_finale(self):
        self.simulazione_eseguita = True
        self.aggiorna_stato_interfaccia()

    def ripristina_simulazione_globale(self):
        risposta = mostra_messaggio_stilizzato(
            parent=self, titolo="Conferma Ripristino", testo="Sei sicuro di voler azzerare la simulazione corrente?\nI dati storici e le rese andranno persi.", tipo="domanda"
        )
        if risposta != QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage("🔄 Operazione di ripristino annullata.")
            return
    
        self.parametri_condivisi.reset_simulazione_globale()
        self.parametri_condivisi.storico_stagionale = {}
        
        # 1. Ricrea il motore pulito
        self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
        
        # 2. RICREA I LOTTI DA ZERO basandoti sulla configurazione iniziale
        configurazione_lotti_default = [
            {"id": "LTI-001", "clone": "I-214", "dest": "OPERA", "eta": 9, "superficie": 2.0, "idrico": 0.0},
            # ... (inserisci qui tutta la lista dei 15 lotti come nel tuo __init__) ...
        ]
        
        self.parametri_condivisi.collezione_lotti = []
        for conf in configurazione_lotti_default:
            lotto = Lotto(id_lotto=conf["id"], superficie=conf["superficie"])
            lotto.sesto_impianto = "6x6"
            lotto.clone_assegnato = conf["clone"]
            lotto.destinazione_uso = conf["dest"]
            lotto.indice_attrito_spaziale = 2
            lotto.indice_tendenza_idrica = conf["idrico"]
            lotto.eta = conf["eta"]  
            
            lato1, lato2 = [float(x) for x in lotto.sesto_impianto.split("x")]
            lotto.densita_iniziale = int(10000 / (lato1 * lato2))
            
            lotto.inizializza_nuovo_ciclo() 
            
            if lotto.eta > 0:
                profilo = self.motore_condiviso.dati_cloni[lotto.clone_assegnato]
                lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                lotto.diametro_medio_fusto = lotto.dati_correnti["dbh_reale_cm"]
                lotto.altezza_media_piante = lotto.dati_correnti["altezza_m"]
                lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
                
            self.parametri_condivisi.collezione_lotti.append(lotto)

        # 3. Reset dei serbatoi ditta
        if hasattr(self.ditta_attiva, "inizializza_serbatoi_stagionali"):
            self.ditta_attiva.inizializza_serbatoi_stagionali(55)

        self.simulazione_eseguita = False
        self.aggiorna_stato_interfaccia()
        self.statusBar().showMessage("🔄 Sistema resettato. Orologio forestale impostato su Primavera Anno 1.")

    def ditta(self):
        self.finestra_ditta = FormDitta(self.ditta_attiva, self.parametri_condivisi, self)
        self.finestra_ditta.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.finestra_ditta.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_ditta.show()

    def lotti(self):
        self.finestra_lotti = FormLotti(self.parametri_condivisi, self)
        self.finestra_lotti.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.finestra_lotti.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_lotti.show()

    def simulazione(self):
        """Simulazione veloce Batch."""
        self.statusBar().showMessage("Inizializzazione del calcolo forestale in corso...")
        self.parametri_condivisi.reset_simulazione_globale()
        self.parametri_condivisi.storico_stagionale = {} 

        progress = QProgressDialog("Inizializzazione del motore forestale...", "Annulla", 0, self.parametri_condivisi.anni_durata_target, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle("Elaborazione Scenario"); progress.setMinimumDuration(0); progress.setAutoClose(True)

        try:
            self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
            fine_scatto = False
            
            while not fine_scatto:
                if progress.wasCanceled():
                    self.statusBar().showMessage("🔄 Simulazione interrotta.")
                    self.motore_condiviso = None
                    return

                stato_tempo = self.motore_condiviso.avanza_passo_simulazione()
                fine_scatto = stato_tempo["simulazione_terminata"]
                
                anno = self.parametri_condivisi.anno_corrente
                stagione = self.parametri_condivisi.stagione_corrente
                
                progress.setLabelText(f"Elaborazione Anno {anno} - {stagione} | Assestamento continuo...")
                progress.setValue(min(anno, self.parametri_condivisi.anni_durata_target))
                QApplication.processEvents()

            self.simulazione_eseguita = True
            mostra_messaggio_stilizzato(parent=self, titolo="Simulazione Conclusa", testo=f"Il piano di assestamento su {self.parametri_condivisi.anni_durata_target} anni è stato completato.\nI tre output sono pronti.", tipo="info")
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Errore di Calcolo", f"Crash nel motore:\n{str(e)}")
            self.simulazione_eseguita = False
            self.motore_condiviso = None

        self.aggiorna_stato_interfaccia()

    def monitoraggio(self):
        """Simulazione passo-passo interattiva."""
        self.statusBar().showMessage("Inizializzazione della plancia di monitoraggio real-time...")
        self.parametri_condivisi.reset_simulazione_globale()
        self.parametri_condivisi.storico_stagionale = {} 
        try:
            self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
            
            self.finestra_monitoraggio = form_monitoraggio(self.motore_condiviso, self)
            self.finestra_monitoraggio.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.finestra_monitoraggio.setWindowFlags(Qt.Window) 
            self.finestra_monitoraggio.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.finestra_monitoraggio.closeEvent = lambda event: [self.aggiorna_stato_interfaccia(), event.accept()]
            self.finestra_monitoraggio.show()
            self.statusBar().showMessage("Plancia di monitoraggio active. Gestione passo-passo abilitata.")
        except Exception as e:
            QMessageBox.critical(self, "Errore di Inizializzazione", f"Impossibile avviare il monitoraggio:\n{str(e)}")
            self.statusBar().showMessage("❌ Errore durante l'apertura del monitoraggio.")
            self.motore_condiviso = None

    def valutazione(self):
        """Apertura report finale con ispezione ed esportazione in file .json dello storico completo."""
        import json  # Importiamo il modulo JSON nativo per l'esportazione su file
        
        print("\n" + "="*80)
        print(" DIAGNOSTICA MEMORIA INTERMEDIA - STORICO DELLA SIMULAZIONE COMPLETA")
        print("="*80)

        if not hasattr(self, "motore_condiviso") or self.motore_condiviso is None:
            print("[ATTENZIONE] self.motore_condiviso è NONE o non inizializzato!")
            print("="*80 + "\n")
            self.statusBar().showMessage("⚠️ Nessuna simulazione attiva in memoria.")
            return

        parametri = self.motore_condiviso.parametri
        dizionario_storia = getattr(parametri, "storico_stagionale", {})

        print(f"[OK] Riferimento motore trovato in memoria: {self.motore_condiviso}")
        print(f"[OK] Riferimento parametri trovato in memoria: {parametri}")
        print(f" -> Numero totale di passi stagionali registrati nella storia: {len(dizionario_storia)}")

        # =========================================================================
        # BLOCCO DI ESPORTAZIONE IN FILE DETTAGLIATO "storia.json" 
        # =========================================================================
        try:
            percorso_esportazione = os.path.join(os.path.dirname(__file__), "storia.json")
            with open(percorso_esportazione, "w", encoding="utf-8") as f_json:
                # dump converte l'intera mappa di dizionari in testo strutturato e leggibile
                json.dump(dizionario_storia, f_json, indent=4, ensure_ascii=False)
            print(f"[EXPORT OK] Struttura 'dizionario_storia' salvata con successo in:\n -> {percorso_esportazione}")
        except Exception as e_json:
            print(f"[EXPORT ERRORE] Impossibile scrivere il file storia.json: {str(e_json)}")
        # =========================================================================

        # if len(dizionario_storia) > 0:
        #     chiavi_ordinate = sorted(list(dizionario_storia.keys()))
        #     print(f" -> Prime 4 chiavi temporali salvate: {chiavi_ordinate[:4]}")
        #     print(f" -> Ultime 4 chiavi temporali salvate: {chiavi_ordinate[-4:]}")
            
        #     chiave_campione = chiavi_ordinate[-1]
        #     print(f"\n --- ANALISI CAMPIONE STRUTTURA DATI INTERNA (Chiave: '{chiave_campione}') ---")
        #     istanza_campione = dizionario_storia[chiave_campione]
        #     print(f"   • Sotto-chiavi di quadro_stato: {list(istanza_campione.keys())}")
            
        #     prod_cumulata = istanza_campione.get("produzione_cumulata", {})
        #     print(f"   • Production Cumulata rilevata nel record: {prod_cumulata}")
            
        #     stato_lotti = istanza_campione.get("stato_lotti", {})
        #     print(f"   • Numero di lotti tracciati in questa istantanea: {len(stato_lotti)}")
        #     if len(stato_lotti) > 0:
        #         primo_id_lotto = list(stato_lotti.keys())[0]
        #         print(f"     -> Dati biometrici salvati per lotto {primo_id_lotto}: {stato_lotti[primo_id_lotto]}")
        # else:
        #     print("[ALLARME] Il dizionario 'storico_stagionale' è vuoto! La simulazione non ha registrato passi.")

        # print("="*80 + "\n")

        try:
            from GUI.form_valutazioni import FormValutazioni
            self.finestra_valutazioni = FormValutazioni(self.motore_condiviso, self)
            self.finestra_valutazioni.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.finestra_valutazioni.setWindowFlags(Qt.Window)
            self.finestra_valutazioni.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.finestra_valutazioni.show()
        except Exception as e:
            QMessageBox.critical(self, "Errore Interfaccia", f"Impossibile aprire il modulo di reportistica:\n{str(e)}")