
# GUI/form_ditta.py
# Modulo della form di configurazione delle risorse aziendali.
# Sincronizza i dati inseriti con la classe Ditta per impostare i parametri della simulazione.

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from GUI.utils import mostra_messaggio_stilizzato, centra_finestra

from Core.ditta import Ditta

class FormDitta(QWidget):
    def __init__(self, ditta_condivisa: Ditta, parametri_condivisi, parent=None):
        super().__init__()

        # Configurazione dei flag della finestra per agganciarla alla form chiamante
        if parent:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            # Forza la distruzione effettiva della memoria alla chiusura per attivare il segnale .destroyed
            self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Caricamento dinamico dell'interfaccia con QUiLoader
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_ditta.ui")
        self.ui_interfaccia = loader.load(percorso_ui, None)

        # Inserisce la UI dentro il QWidget principale
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui_interfaccia)
        layout.setContentsMargins(10, 10, 10, 10)
        self.DIM_W = 686
        self.DIM_H = 470

        # Salva il riferimento all'oggetto Ditta globale passato alla chiamata e necessario per la gestione dei dati
        self.ditta = ditta_condivisa
        self.parametri = parametri_condivisi # Salviamo il puntatore globale ai parametri della simulazione

        self.setWindowTitle("Inventario Forze di Produzione - Risorse e Flotta")

        # RECUPERO DEI PUNTATORI AI WIDGET

        # Comparto Risorse Umane dipendenti diretti
        self.spin_operaio_A = self.ui_interfaccia.findChild(object, "spin_operaio_A")
        self.spin_operaio_B = self.ui_interfaccia.findChild(object, "spin_operaio_B")

        # Comparto Flotta Trazione e Manutenzione di proprietà
        self.spin_trattori_alta = self.ui_interfaccia.findChild(object, "spin_trattori_alta")
        self.spin_trattori_media = self.ui_interfaccia.findChild(object, "spin_trattori_media")
        self.spin_piattaforme = self.ui_interfaccia.findChild(object, "spin_piattaforme")
        self.spin_harvester = self.ui_interfaccia.findChild(object, "spin_harvester")
        self.spin_forwarder = self.ui_interfaccia.findChild(object, "spin_forwarder")
        self.spin_cippatrici = self.ui_interfaccia.findChild(object, "spin_cippatrici")
        self.spin_durata_piano = self.ui_interfaccia.findChild(object, "spin_durata_piano")


        # Comparto Noli e Stagionali
        self.spin_operaio_A_noleggio = self.ui_interfaccia.findChild(object, "spin_operaio_A_noleggio")
        self.spin_operaio_B_noleggio = self.ui_interfaccia.findChild(object, "spin_operaio_B_noleggio")
        self.spin_trattori_alta_noleggio = self.ui_interfaccia.findChild(object, "spin_trattori_alta_noleggio")
        self.spin_trattori_media_noleggio = self.ui_interfaccia.findChild(object, "spin_trattori_media_noleggio")
        self.spin_piattaforme_noleggio = self.ui_interfaccia.findChild(object, "spin_piattaforme_noleggio")
        self.spin_harvester_noleggio = self.ui_interfaccia.findChild(object, "spin_harvester_noleggio")
        self.spin_forwarder_noleggio = self.ui_interfaccia.findChild(object, "spin_forwarder_noleggio")
        self.spin_cippatrici_noleggio = self.ui_interfaccia.findChild(object, "spin_cippatrici_noleggio")
        
        self.spin_tolleranza = self.ui_interfaccia.findChild(object, "spin_tolleranza")
        
        # Pulsanti di Comando
        self.btn_salva = self.ui_interfaccia.findChild(object, "btn_salva")
        self.btn_esci = self.ui_interfaccia.findChild(object, "btn_esci")

        # INTERFACCIA E SEGNALI
        
        # Pre-popola i widget grafici con i valori correnti salvati nell'oggetto ditta
        self.aggiorna_interfaccia_da_modello()

        if self.btn_salva:
            self.btn_salva.clicked.connect(self.salva_dati_in_modello)

        if self.btn_esci:
            self.btn_esci.clicked.connect(self.esci_form)


    def showEvent(self, event):
        super().showEvent(event)
        centra_finestra(self, self.DIM_W, self.DIM_H)

    
    def aggiorna_interfaccia_da_modello(self):
        '''Estrae i dati dell'oggetto Ditta e popola i controlli dell'interfaccia'''
        self.spin_operaio_A.setValue(self.ditta.operai_grado_A)
        self.spin_operaio_B.setValue(self.ditta.operai_grado_B)
        
        self.spin_trattori_alta.setValue(self.ditta.trattori_alta_potenza)
        self.spin_trattori_media.setValue(self.ditta.trattori_media_potenza)
        self.spin_piattaforme.setValue(self.ditta.piattaforme_aeree_semoventi)
        self.spin_harvester.setValue(self.ditta.harvester_abbattitori)
        self.spin_forwarder.setValue(self.ditta.forwarder_caricatori)
        self.spin_cippatrici.setValue(self.ditta.cippatrice)
        self.spin_durata_piano.setValue(self.parametri.anni_durata_target)

        # Recupera i datti dall'oggetto Ditta dal dizionario dei limiti dei noli stagionali ed aggiorna i controlli sull form 
        limiti = self.ditta.limiti_noli_stagionali
        self.spin_operaio_A_noleggio.setValue(limiti["personale_spec"])
        self.spin_operaio_B_noleggio.setValue(limiti["personale_comune"])
        self.spin_trattori_alta_noleggio.setValue(limiti["trattori_alta"])
        self.spin_trattori_media_noleggio.setValue(limiti["trattori_media"])
        self.spin_piattaforme_noleggio.setValue(limiti["piattaforme"])
        self.spin_harvester_noleggio.setValue(limiti["harvester"])
        self.spin_forwarder_noleggio.setValue(limiti["forwarder"])
        self.spin_cippatrici_noleggio.setValue(limiti["cippatrice"])
        
        tolleranza_taglio = self.ditta.tolleranza_taglio * 100 
        self.spin_tolleranza.setValue(tolleranza_taglio)
    

    def salva_dati_in_modello(self):
        '''Legge i valori impostati dall'utente e aggiorna l'istanza della ditta se i controlli di consistenza sono passati'''    
       
        # Effettua prima le verifiche di consistenza delle modifiche effettuate rispetto alla stabilità minima della ditta
        op_A = self.spin_operaio_A.value() 
        op_B = self.spin_operaio_B.value()
        trattori_media = self.spin_trattori_media.value()

        if ((op_A + op_B) == 0) or (trattori_media == 0):
            mostra_messaggio_stilizzato(
                            self, 
                            "Inconsistenza Organico", 
                            "Impossibile salvare: la ditta deve disporre di almeno un lavoratore e di un trattore per operare nei cantieri.", 
                            "avviso"
                        )
            return

        piattaforme = self.spin_piattaforme.value()
        piattaforme_noleggio = self.spin_piattaforme_noleggio.value()
        trattori_alta = self.spin_trattori_alta.value()
        trattori_alta_noleggio = self.spin_trattori_alta_noleggio.value()
        cippatrice = self.spin_cippatrici.value()
        cippatrice_noleggio = self.spin_cippatrici_noleggio.value()
        
        if ((piattaforme + piattaforme_noleggio) == 0) or ((trattori_alta + trattori_alta_noleggio) == 0) or ((cippatrice + cippatrice_noleggio) == 0):
            mostra_messaggio_stilizzato(
                            self, 
                            "Inconsistenza Flotta", 
                            "Impossibile salvare: la ditta deve disporre di almeno una piattaforma aerea o di un trattore ad alta potenza (di proprietà o a noleggio) per operare nei cantieri.", 
                            "avviso"
                        )
            return

        
        # Una volta che i controlli sono passati positivamente vengono aggiornati i valori dell'oggetto Ditta con i valori dei controlli della form
        self.ditta.operai_grado_A = op_A
        self.ditta.operai_grado_B = op_B
        
        self.ditta.trattori_alta_potenza = self.spin_trattori_alta.value()
        self.ditta.trattori_media_potenza = self.spin_trattori_media.value()
        self.ditta.piattaforme_aeree_semoventi = self.spin_piattaforme.value()
        self.ditta.harvester_abbattitori = self.spin_harvester.value()
        self.ditta.forwarder_caricatori = self.spin_forwarder.value()
        self.ditta.cippatrice = self.spin_cippatrici.value()    
        

        self.ditta.limiti_noli_stagionali["personale_spec"] = int(self.spin_operaio_A_noleggio.value())
        self.ditta.limiti_noli_stagionali["personale_comune"] = int(self.spin_operaio_B_noleggio.value())
        self.ditta.limiti_noli_stagionali["trattori_alta"] = int(self.spin_trattori_alta_noleggio.value())
        self.ditta.limiti_noli_stagionali["trattori_media"] = int(self.spin_trattori_media_noleggio.value())
        self.ditta.limiti_noli_stagionali["piattaforme"] = int(self.spin_piattaforme_noleggio.value())
        self.ditta.limiti_noli_stagionali["harvester"] = int(self.spin_harvester_noleggio.value())
        self.ditta.limiti_noli_stagionali["forwarder"] = int(self.spin_forwarder_noleggio.value())
        self.ditta.limiti_noli_stagionali["cippatrice"] = int(self.spin_cippatrici_noleggio.value())
        
        # Salva la durata default per la simulazione batch all'interno della configurazione globale parametri
        self.parametri.anni_durata_target = self.spin_durata_piano.value()
        tolleranza_taglio = float(self.spin_tolleranza.value())
        self.ditta.tolleranza_taglio = tolleranza_taglio/100

        # Sincronizzazione immediata del monte ore stagionale nominale con il nuovo organico salvato
        if hasattr(self.ditta, "inizializza_serbatoi_stagionali"):
            self.ditta.inizializza_serbatoi_stagionali(55)
        else:
            ore_ricalcolate = (self.ditta.operai_grado_A + self.ditta.operai_grado_B) * 450.0
            self.ditta.serbatoi_ore = {
                "Inverno": ore_ricalcolate, "Primavera": ore_ricalcolate, "Estate": ore_ricalcolate, "Autunno": ore_ricalcolate
            }

        self.close()


    def esci_form(self):
        self.close()