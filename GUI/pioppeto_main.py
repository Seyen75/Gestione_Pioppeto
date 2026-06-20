
# Modulo Finestra principale (Dashboard) del simulatore di pioppicoltura.

import os
import time
import json

# Importazione di tutti i moduli di QT e PySide per la gestione grafica delle finestre e dei controlli
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGraphicsDropShadowEffect, QMessageBox, QApplication, QProgressDialog
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader

# Importazione della finestra di messaggi personalizzata
from GUI.utils import mostra_messaggio_stilizzato

#I Importazione dei moduli con le classi di gestione cloni, ditta, lotti, parametri e motore del simulatore
from Core.gestori_clone import GestoreCloni
from Core.ditta import Ditta
from Core.parametri_simulazione import ParametriSimulazione
from Core.SimulatorePioppicultura import SimulatorePioppicoltura
from Core.lotto import Lotto

# Importazioni classi per le form grafiche attivate dai pulsanti
from GUI.form_ditta import FormDitta
from GUI.form_lotti import FormLotti
from GUI.form_monitoraggio import form_monitoraggio
import risorse.rc_risorse

class PioppetoMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # Caricamento interfaccia grafica di PySide dal file .ui 
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "pioppeto_main.ui")
        
        # Nelle form QMainWindow si setta il riferimento al Widget centrale contenitore di tutti gli altri
        ui_temporanea = loader.load(percorso_ui, None) 
        widget_centrale = ui_temporanea.centralWidget()
        self.setCentralWidget(widget_centrale)
        
        self.setWindowTitle("Gestione di Sistemi di Pioppicoltura")

        # Si inizializza la classe che carica il file JSON dei cloni e lo si inserisce nel dizionario
        self.gestore_cloni = GestoreCloni()
        self.dizionario_cloni = self.gestore_cloni.carica_cloni() 

        # Inizializza la classe Ditta e ParametriSimulazione con i dati iniziali del costruttore e li inserisce nelle variabili della classe PioppetoMain per poi usarla a livello globale
        self.ditta_attiva = Ditta()
        
        # Questa variabile serve per passare alle form figlie i dati che provengono dalle simulazioni
        self.parametri_condivisi = ParametriSimulazione()
        
        # Inizializza il motore della simulazione
        self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)

        # Crea il dizioniario che conterrà i paramtri storici delle stagioni simulate
        self.parametri_condivisi.storico_stagionale = {}
        
        # Variabile booleana per segnalare che non è stata ancora avviata nessuna delle simulazioni (fase di partenza e reset)
        self.simulazione_eseguita: bool = False

       
        # INIZIALIZZA I DATI DELLA DITTA STANDARD
        # Personale fisso della ditta
        self.ditta_attiva.operai_grado_A = 4         
        self.ditta_attiva.operai_grado_B = 2         
        
        # Strumentazioni base della ditta
        self.ditta_attiva.trattori_alta_potenza = 1
        self.ditta_attiva.trattori_media_potenza = 3 
        self.ditta_attiva.piattaforme_aeree_semoventi = 1
        self.ditta_attiva.cippatrice = 1
        
        # Strumentazioni avanzate della ditta
        self.ditta_attiva.harvester_abbattitori = 1
        self.ditta_attiva.forwarder_caricatori = 1

        
        # Dichiarazione della variabile IUFRO (International Union of Forest Research Organizations)
        # Variabile che indica l'operatività media di un cantiere, pari all'80% delle ore disponibili totali
        # E' la quantità media di ore perse per attività di spostamento di persone e mezzi da e per i lotti
        self.ditta_attiva.coefficiente_iufro = 0.80 

        # Livelli standard di limite ricorso del mercato degli stagionali e dei Noli per la ditta standard
        self.ditta_attiva.limiti_noli_stagionali = {
            "personale_spec": 9,   
            "personale_comune": 50, 
            "harvester": 3,        
            "forwarder": 3,
            "trattori_alta": 3,
            "trattori_media": 5,
            "piattaforme": 3,
            "cippatrice": 3
        }
        
        # Iniziali i serbatoi stagionali con il parametro di 55 giorni lavorativi per stagione
        # Il numero 55 è dato dal conteggio medio (tolti sabati, domeniche e festivi) dei giorni lavorativi in un trimestre
            
        self.ditta_attiva.inizializza_serbatoi_stagionali(55)

        # Inizializza per la simulazione base la durata degli anni da simulare automaticamente
        self.parametri_condivisi.anni_durata_target = 10
        
        # Avvia la funzione che carica i lotti standard della ditta
        self._carica_lotti_iniziali()

        
        # Mappa i controlli Widget Form
        self.btn_esci = widget_centrale.findChild(QPushButton, "btn_esci")
        self.btn_ditta = widget_centrale.findChild(QPushButton, "btn_gestione_ditta")
        self.btn_lotti = widget_centrale.findChild(QPushButton, "btn_gestione_lotti")
        self.btn_simulazione = widget_centrale.findChild(QPushButton, "btn_simulazione")
        self.btn_monitoraggio = widget_centrale.findChild(QPushButton, "btn_monitoraggio")
        self.btn_valutazioni = widget_centrale.findChild(QPushButton, "btn_valutazioni")
        self.btn_reset = widget_centrale.findChild(QPushButton, "btn_reset")

        # Connettte le funzioni ai relativi pulsanti della form
        self.btn_esci.clicked.connect(QApplication.instance().quit)
        self.btn_ditta.clicked.connect(self.ditta)
        self.btn_lotti.clicked.connect(self.lotti)
        self.btn_simulazione.clicked.connect(self.simulazione)
        self.btn_monitoraggio.clicked.connect(self.monitoraggio)
        self.btn_valutazioni.clicked.connect(self.valutazione)
        self.btn_reset.clicked.connect(self.ripristina_simulazione_globale)

        # Aggiustamenti grafici della MainWindow, sfondo e grafica per il titolo
        self.setStyleSheet("QMainWindow { border-image: url(:/sfondo_main.jpg) 0 0 0 0 stretch stretch; }")
        self.label_titolo = widget_centrale.findChild(QWidget, "label_titolo")
        if self.label_titolo:
            ombra = QGraphicsDropShadowEffect(self)
            ombra.setBlurRadius(8); ombra.setXOffset(3); ombra.setYOffset(3)
            ombra.setColor(QColor(0, 0, 0, 200))
            self.label_titolo.setGraphicsEffect(ombra)
            
            # Assegnazione del testo dinamico
            self.label_titolo.setText(f"Gestione Pioppicultura\n{self.ditta_attiva.nome_ditta}")
        

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
        ''' Aggiorna l'interfaccia della form alla variazione dei dati della ditta e dei lotti
            aggiorna la status bar con i messaggi della situazione dell'applicazione'''
        
        # Verifica la presenza di lotti in collezione per permettere l'avvio della simulazione
        lotti_pronti = len(self.parametri_condivisi.collezione_lotti) > 0
    
        if not lotti_pronti:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            if not lotti_pronti:
                self.statusBar().showMessage("⚠️ Configurazione incompleta: creare almeno un lotto colturale nel pioppeto.")
        elif not self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(True)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(True)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            self.statusBar().showMessage("✅ Sistema pronto. Scegliere 'Avvia Simulazione' (Batch) o 'Monitoraggio Real-Time' (Primavera -> Inverno).")
        elif self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(True)
            self.statusBar().showMessage("📊 Simulazione conclusa! Analisi diagnostica disponibili in 'Report Finale'.")
       
    
    def _carica_lotti_iniziali(self):
        """Inizializza i 30 lotti di default (20 Opera, 10 Industria) allo stato zero."""
        configurazione_lotti_default = [
            # --- FILIERA OPERA (Ciclo 10 anni) - 20 Lotti ---
            {"id": "LTI-001", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 9, "superficie": 13.5, "idrico": 0.0},
            {"id": "LTI-002", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 9, "superficie": 12.0, "idrico": 0.1},
            {"id": "LTI-003", "clone": "Velasco", "dest": "OPERA", "sesto_impianto": "6x6", "eta": 8, "superficie": 14.0, "idrico": 0.2},
            {"id": "LTI-004", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 8, "superficie": 13.0, "idrico": -0.1},
            {"id": "LTI-005", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 7, "superficie": 12.5, "idrico": 0.0},
            {"id": "LTI-006", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 7, "superficie": 13.5, "idrico": -0.2},
            {"id": "LTI-007", "clone": "Velasco", "dest": "OPERA", "sesto_impianto": "6x6", "eta": 6, "superficie": 13.0, "idrico": 0.0},
            {"id": "LTI-008", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 6, "superficie": 12.5, "idrico": 0.1},
            {"id": "LTI-009", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 5, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-010", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 5, "superficie": 12.0, "idrico": 0.0},
            {"id": "LTI-011", "clone": "Velasco", "dest": "OPERA", "sesto_impianto": "6x6", "eta": 4, "superficie": 13.5, "idrico": 0.2},
            {"id": "LTI-012", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 4, "superficie": 13.0, "idrico": -0.1},
            {"id": "LTI-013", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 3, "superficie": 12.0, "idrico": 0.0},
            {"id": "LTI-014", "clone": "Velasco", "dest": "OPERA", "sesto_impianto": "6x6", "eta": 3, "superficie": 14.0, "idrico": -0.1},
            {"id": "LTI-015", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 2, "superficie": 13.5, "idrico": 0.1},
            {"id": "LTI-016", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 2, "superficie": 12.5, "idrico": 0.0},
            {"id": "LTI-017", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 1, "superficie": 14.0, "idrico": -0.2},
            {"id": "LTI-018", "clone": "Velasco", "dest": "OPERA", "sesto_impianto": "6x6", "eta": 1, "superficie": 13.0, "idrico": 0.0},
            {"id": "LTI-019", "clone": "I-214",   "dest": "OPERA", "sesto_impianto": "6x6", "eta": 0, "superficie": 12.5, "idrico": 0.1},
            {"id": "LTI-020", "clone": "Neva",    "dest": "OPERA", "sesto_impianto": "6x6", "eta": 0, "superficie": 13.5, "idrico": 0.0},

            # --- FILIERA INDUSTRIA (Ciclo 5 anni) - 10 Lotti ---
            {"id": "LTI-021", "clone": "AF2",     "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 4, "superficie": 15.0, "idrico": 0.1},
            {"id": "LTI-022", "clone": "I-45/51", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 4, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-023", "clone": "Velasco", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 3, "superficie": 16.0, "idrico": -0.1},
            {"id": "LTI-024", "clone": "AF2",     "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 3, "superficie": 14.0, "idrico": 0.2},
            {"id": "LTI-025", "clone": "I-45/51", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 2, "superficie": 15.5, "idrico": 0.0},
            {"id": "LTI-026", "clone": "Velasco", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 2, "superficie": 15.0, "idrico": -0.2},
            {"id": "LTI-027", "clone": "AF2",     "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 1, "superficie": 14.5, "idrico": 0.0},
            {"id": "LTI-028", "clone": "I-45/51", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 1, "superficie": 16.5, "idrico": 0.1},
            {"id": "LTI-029", "clone": "Velasco", "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 0, "superficie": 15.0, "idrico": -0.1},
            {"id": "LTI-030", "clone": "AF2",     "dest": "INDUSTRIA", "sesto_impianto": "3x3", "eta": 0, "superficie": 14.0, "idrico": 0.2}
        ]
        
        
        # Caricamento dei lotti nei parametri generali della simulazione
        self.parametri_condivisi.collezione_lotti = []
        for conf in configurazione_lotti_default:
            lotto = Lotto(id_lotto = conf["id"], superficie = conf["superficie"], sesto_impianto = conf["sesto_impianto"])
            lotto.clone_assegnato = conf["clone"]
            lotto.destinazione_uso = conf["dest"]

            lotto.sesto_impianto = conf["sesto_impianto"]
            lotto.indice_attrito_spaziale = 2
            lotto.indice_tendenza_idrico = conf["idrico"]
            lotto.eta = conf["eta"]  
            
            # inizializza il lotto           
            lotto.inizializza_nuovo_ciclo() 
            
            
            # Calcolo dei dati dinamici del lotto se ha un'età maggiore al primo impianto  per fornigli già una storia pregressa
            if lotto.eta > 0:
                profilo = self.motore_condiviso.dati_cloni[lotto.clone_assegnato]
                lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                lotto.diametro_medio_fusto = lotto.dati_correnti["dbh_reale_cm"]
                lotto.altezza_media_piante = lotto.dati_correnti["altezza_m"]
                lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
            else:
                lotto.dati_correnti = {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, 
                    "volume_singolo_m3": 0.0, "piante_attive": lotto.numero_piante_vive, 
                    "volume_totale_m3": 0.0
                }
            
            self.parametri_condivisi.collezione_lotti.append(lotto)

    
    def abilita_report_finale(self):
        '''Se la simulazione è stata effettuata abilita il bottone per accedere al report finale'''
        self.simulazione_eseguita = True
        self.aggiorna_stato_interfaccia()
  
  
    def ripristina_simulazione_globale(self):
        '''Resetta i dati della simulazione già effettuata per permettere una nuova simulazione'''
        risposta = mostra_messaggio_stilizzato(
            parent=self, 
            titolo="Conferma Ripristino", 
            testo="Sei sicuro di voler azzerare la simulazione corrente?\nI dati storici e le rese andranno persi.", 
            tipo="domanda"
        )
        if risposta != QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage("🔄 Operazione di ripristino annullata.")
            return
    
        # Reset del tempo e della cronologia stagionale
        self.parametri_condivisi.reset_simulazione_globale()
        self.parametri_condivisi.storico_stagionale = {}
        
        # Svuota anche l'eventuale dizionario storico_stati se presente
        if hasattr(self.parametri_condivisi, "storico_stati"):
            self.parametri_condivisi.storico_stati = {}
        
        # Ricrea un motore completamente pulito collegato alla ditta
        self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
        
        # Ripristina i lotti allo stato di default iniziale
        self._carica_lotti_iniziali()

        # Reset dei serbatoi ditta stagionali
        if hasattr(self.ditta_attiva, "inizializza_serbatoi_stagionali"):
            self.ditta_attiva.inizializza_serbatoi_stagionali(55)

        # Sblocca l'interfaccia (riattiva i due pulsanti di simulazione)
        self.simulazione_eseguita = False
        self.aggiorna_stato_interfaccia()
        self.statusBar().showMessage("🔄 Sistema resettato. Orologio forestale impostato su Primavera Anno 1.")


    def ditta(self):
        '''avvia la form per la configurazione e modifica dei parametri della ditta'''
        self.finestra_ditta = FormDitta(self.ditta_attiva, self.parametri_condivisi, self)
        self.finestra_ditta.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.finestra_ditta.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_ditta.show()


    def lotti(self):
        '''avvia la form per la configurazione e modifica dei parametri della collezione dei lotti della ditta'''
        self.finestra_lotti = FormLotti(self.parametri_condivisi, self.dizionario_cloni, self)
        self.finestra_lotti.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.finestra_lotti.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_lotti.show()
        
    
    def simulazione(self):
        '''Avvia la simulazione batch che cicla in automatico per un numero di anni presente nell'impostazione base
           Per dare una sensazione visiva viene usata una Dialog Progress con un leggero ritardo sulla velocità della simulazione'''
        
        # Inizializza la simulazione creando il dizionario storico che conterrà i dati della simulazione
        self.statusBar().showMessage("Inizializzazione del calcolo forestale in corso...")
        self.parametri_condivisi.reset_simulazione_globale()
        self.parametri_condivisi.storico_stagionale = {} 

        # Imposta la dialog per mostrare la progressione della simulazione usando la QProgressDialog di Qt
        progress = QProgressDialog("Inizializzazione del motore forestale...", "Annulla", 0, self.parametri_condivisi.anni_durata_target, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle("Elaborazione Scenario"); progress.setMinimumDuration(0); progress.setAutoClose(True)

        try:
            # Avvia l'oggetto simulatore fornendo i dati della ditta e dei parametri globali e la collezione dei lotti
            self.motore_condiviso = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
            fine_simulazione = False
            
            # Cicla fino a quando non si preme il tasto di interruzione oppure la simulazione batch non arriva al limite di anni imposto
            while not fine_simulazione:
                if progress.wasCanceled():
                    self.statusBar().showMessage("🔄 Simulazione interrotta.")
                    self.motore_condiviso = None
                    return

                # La simulazione avanza di stagione in stagione fino a quando la risposta non diventa simulazione_terminata
                stato_simulazione = self.motore_condiviso.avanza_passo_simulazione()
                fine_simulazione = stato_simulazione["simulazione_terminata"]
                
                anno = self.parametri_condivisi.anno_corrente
                stagione = self.parametri_condivisi.stagione_corrente
                
                # Aggiornamento della labe della Progress Dialog con i dati dell'anno e e della stagione simulata
                progress.setLabelText(f"Elaborazione Anno {anno} - {stagione} | Assestamento continuo...")
                time.sleep(0.05)
                progress.setValue(min(anno, self.parametri_condivisi.anni_durata_target))
                QApplication.processEvents()

            self.simulazione_eseguita = True
            # Si utilizza il messaggio personalizzato per indicare la fine della simulazione
            mostra_messaggio_stilizzato(parent = self, titolo = "Simulazione Conclusa", 
                                        testo = f"Il piano di assestamento su {self.parametri_condivisi.anni_durata_target} anni è stato completato.\nI tre output sono pronti.", tipo="info")
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Errore di Calcolo", f"Crash nel motore:\n{str(e)}")
            self.simulazione_eseguita = False
            self.motore_condiviso = None

        self.aggiorna_stato_interfaccia()
        
    
    def monitoraggio(self):
        '''Avvia la form del Monitoraggio Real Time inizializzando l'oggetto del simulatore'''
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
        '''Avvio form di Reportistica finale dopo che è stata effettuata la simulazione batch o quella Real-Time'''
        
        # Verifica che i risultati della simulazione è stata inizializzato o che non sia vuoto
        if not hasattr(self, "motore_condiviso") or self.motore_condiviso is None:
            print("[ATTENZIONE] self.motore_condiviso è NONE o non inizializzato!")
            print("="*80 + "\n")
            self.statusBar().showMessage("⚠️ Nessuna simulazione attiva in memoria.")
            return

        # instanzia l'oggetto per i parametri della simulazione
        parametri = self.motore_condiviso.parametri
        dizionario_storia = getattr(parametri, "storico_stagionale", {})

        try:
            # Viene creato il file storia.json dove viene salvato l'intero dizionario della storia della simulazione
            # File non necessario ai fini dell'applicazione, ma utile per vedere come è strutturato dentro il dizionario con i dati completi della simulazione
            percorso_esportazione = os.path.join(os.path.dirname(__file__), "storia.json")
            with open(percorso_esportazione, "w", encoding="utf-8") as f_json:
                json.dump(dizionario_storia, f_json, indent=4, ensure_ascii=False)
            print(f"[EXPORT OK] Struttura 'dizionario_storia' salvata con successo in:\n -> {percorso_esportazione}")
        except Exception as e_json:
            print(f"[EXPORT ERRORE] Impossibile scrivere il file storia.json: {str(e_json)}")
       
        try:
            from GUI.form_valutazioni import FormValutazioni
            # Avvia la form di Reportistica dei dati storici presenti in motore_condiviso
            self.finestra_valutazioni = FormValutazioni(self.motore_condiviso, self)
            self.finestra_valutazioni.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.finestra_valutazioni.setWindowFlags(Qt.Window)
            self.finestra_valutazioni.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.finestra_valutazioni.show()
        except Exception as e:
            QMessageBox.critical(self, "Errore Interfaccia", f"Impossibile aprire il modulo di reportistica:\n{str(e)}")