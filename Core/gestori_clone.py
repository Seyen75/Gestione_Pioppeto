
# Modulo Gestore del Database dei Cloni. Garantisce l'integrità dei dati selvicolturali all'avvio e previene crash da corruzione file.

import os
import json
import shutil

class GestoreCloni:
    def __init__(self):
        # Definizione dei percorsi dei due file
        self.cartella_radice = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Il file default (protetto) contenente i cloni base
        # Utilità eventualmente per una futura features che permette di implementare nuovi cloni dall'utente e pertanto prevenire cancellazioni pericolose
        self.percorso_master = os.path.join(self.cartella_radice, "Core", "cloni_default.json")

        # Il file di lavoro letto attivamente dal simulatore e dalle form
        self.percorso_utente = os.path.join(self.cartella_radice, "cloni.json")

    def inizializza_database(self):
        # Verifica la presenza e la validità del file cloni.json. Se manca o è corrotto, lo rigenera. Anche qui per futura features
        if not os.path.exists(self.percorso_utente):
            print("Log Sistema: 'cloni.json' non trovato. Generazione database di lavoro dal Master...")
            self.ripristina_valori_fabbrica()
            return

        # Se il file esiste, esegue un test di validità sintattica JSON per prevenire crash
        try:
            with open(self.percorso_utente, "r", encoding="utf-8") as f:
                json.load(f)
        except (json.JSONDecodeError, IOError):
            print("ATTENZIONE: Il file 'cloni.json' è corrotto! Ripristino automatico di emergenza dal Master...")
            self.ripristina_valori_fabbrica()

    def ripristina_valori_fabbrica(self):
        # Copia il file originale protetto (con i 4 cloni default) sopra quello di lavoro.
        try:
            shutil.copy2(self.percorso_master, self.percorso_utente)
            print("Log Sistema: Database cloni allineato ai valori scientifici di fabbrica.")
        except IOError as e:
            print(f"ERRORE CRITICO: Impossibile accedere al file Master delle risorse cloni! {e}")

    def carica_cloni(self) -> dict:
        # Carica i cloni correnti dal file di lavoro per popolare la form
        self.inizializza_database() # Controllo preventivo di sicurezza ad ogni chiamata
        with open(self.percorso_utente, "r", encoding="utf-8") as f:
            return json.load(f)

    def salva_nuovo_clone(self, sigla: str, dati_clone: dict) -> bool:
        # Aggiunge o modifica un clone nel file utente - Predisposto per futura eventuale aggiunta
        
        try:
            cloni_attuali = self.carica_cloni()
            cloni_attuali[sigla] = dati_clone

            # Scrittura su un file temporaneo di transito per evitare corruzioni se si interrompe il processo
            percorso_tmp = self.percorso_utente + ".tmp"
            with open(percorso_tmp, "w", encoding="utf-8") as f:
                json.dump(cloni_attuali, f, indent=4, ensure_ascii=False)

            # Sostituzione sul disco
            os.replace(percorso_tmp, self.percorso_utente)
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio o la modifica del clone: {e}")
            return False