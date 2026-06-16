
# Modulo Gestione dello stato globale della simulazione, del cronometro stagionale e dei registri di produzione consuntiva dei lotti.

import copy
from Core.lotto import Lotto

class ParametriSimulazione:
    def __init__(self):
        self.nome_azienda: str = "Azienda Pioppicola Padana"
        self.anno_corrente: int = 1
        self.anni_durata_target: int = 10  
        self.ciclo_stagioni: list[str] = ["Primavera", "Estate", "Autunno", "Inverno"]
        self.indice_stagione_corrente: int = 0  
        self.collezione_lotti: list[Lotto] = []
        self.storico_stagionale: dict[str, dict] = {}
        
        self.simulazione_avviata: bool = False

    @property
    def stagione_corrente(self) -> str:
        return self.ciclo_stagioni[self.indice_stagione_corrente]


    def avanza_stagione(self) -> dict:
        cambio_anno = False
        if self.stagione_corrente == "Inverno":
            self.indice_stagione_corrente = 0
            self.anno_corrente += 1
            cambio_anno = True
        else:
            self.indice_stagione_corrente += 1
            
        fine_simulazione = self.anno_corrente > self.anni_durata_target
        return {
            "stagione": self.stagione_corrente,
            "anno": min(self.anno_corrente, self.anni_durata_target),
            "cambio_anno_rilevato": cambio_anno,
            "simulazione_terminata": fine_simulazione
        }


    def reset_simulazione_globale(self):
        self.anno_corrente = 1
        self.indice_stagione_corrente = 0
        self.storico_stagionale.clear()


    def registra_instantanea_stato_corrente(self, dati_quadro: dict):
        chiave_tempo = f"A{self.anno_corrente}_{self.stagione_corrente}"
        # copy.deepcopy duplica l'intera struttura, scollegandola dalle modifiche future
        self.storico_stagionale[chiave_tempo] = copy.deepcopy(dati_quadro)