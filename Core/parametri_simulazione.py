
# Modulo Gestione dello stato globale della simulazione, del cronometro stagionale e dei registri di produzione consuntiva dei lotti.

from Core.lotto import Lotto

class ParametriSimulazione:
    def __init__(self):

        # ANAGRAFICA E CONFIGURAZIONE SCENARIO
        self.nome_azienda: str = "Azienda Pioppicola Padana"

        # BILANCIO E PRODUZIONE REALE REALIZZATA (CUMULATIVA DI TUTTA LA SIMULAZIONE)
        self.totale_prodotto_opera_m3: float = 0.0
        self.totale_prodotto_cartiera_t: float = 0.0
        self.totale_prodotto_truciolato_t: float = 0.0

        # CONFIGURAZIONE DEL TEMPO DI SIMULAZIONE
        self.anno_corrente: int = 1
        self.anni_durata_target: int = 10  # Orizzonte standard di default (es. Piano Assestamento)

        # Sequenza che fissa l'anno biologico (Inizia in Inverno col riposo vegetativo e gli impianti)
        self.ciclo_stagioni: list[str] = ["Inverno", "Primavera", "Estate", "Autunno"]
        self.indice_stagione_corrente: int = 0  # 0 = Inverno, 1 = Primavera, 2 = Estate, 3 = Autunno

        # COLLEZIONE DEI LOTTI
        self.collezione_lotti: list[Lotto] = []

        # REGISTRO STORICO PER I SUCCESSIVI GRAFICI DI VALUTAZIONE
        self.storico_stagionale: dict[str, dict] = {}

    @property
    def stagione_corrente(self) -> str:
        """Restituisce il nome della stagione attiva in questo momento."""
        return self.ciclo_stagioni[self.indice_stagione_corrente]

    def avanza_stagione(self) -> dict:
        """
        Fa scattare l'orologio della simulazione alla stagione successiva.
        Gestisce il passaggio all'anno successivo quando termina l'Autunno.
        Controlla se l'orizzonte degli anni target prefissati dall'utente è concluso.
        """
        cambio_anno = False

        # Avanza l'indice della stagione corrente
        self.indice_stagione_corrente += 1

        # Se si supera l'autunno torniamo all'inverno dell'anno successivo
        if self.indice_stagione_corrente >= len(self.ciclo_stagioni):
            self.indice_stagione_corrente = 0
            self.anno_corrente += 1
            cambio_anno = True

        # La simulazione termina quando l'anno corrente supera gli anni impostati per il test
        fine_simulazione = self.anno_corrente > self.anni_durata_target

        return {
            "stagione": self.stagione_corrente,
            "anno": min(self.anno_corrente, self.anni_durata_target), # Evita over-index estetici nei log
            "cambio_anno_rilevato": cambio_anno,
            "simulazione_terminata": fine_simulazione
        }

    def accumula_resa_lotto(self, rese_lotto: dict):
        """
        Riceve il report delle rese di un lotto appena tagliato e aggiorna
        i contatori cumulativi aziendali della produzione totale.
        """
        self.totale_prodotto_opera_m3 += rese_lotto.get("opera_m3", 0.0)
        self.totale_prodotto_cartiera_t += rese_lotto.get("cartiera_t", 0.0)
        self.totale_prodotto_truciolato_t += rese_lotto.get("truciolato_t", 0.0)

    def aggiungi_lotto_a_collezione(self, id_lotto: str, superficie: float) -> Lotto:
        """Permette alla form di popolare dinamicamente la lista dei lotti aziendali."""
        nuovo_lotto = Lotto(id_lotto, superficie)
        nuovo_lotto.inizializza_nuovo_ciclo() # Garantisce la partenza da Anno 0
        self.collezione_lotti.append(nuovo_lotto)
        return nuovo_lotto

    def reset_simulazione_globale(self):
        """Riporta l'orologio all'inverno dell'Anno 1 e azzera i registri cumulativi."""
        self.anno_corrente = 1
        self.indice_stagione_corrente = 0
        self.totale_prodotto_opera_m3 = 0.0
        self.totale_prodotto_cartiera_t = 0.0
        self.totale_prodotto_truciolato_t = 0.0
        self.storico_stagionale.clear()

        # Il reset completo non deve azzerare i lotti (altrimenti perdiamo la fustaia impostata)
        # ma deve riportarli al loro stato d'età e biometria iniziale programmato per il test.
        # Nota: l'inizializzazione specifica con le classi di età sfasate 
        # (0-9 anni) verrà iniettata dalla Dashboard prima di avviare il simulatore.

    def registra_instantanea_stato_corrente(self, dati_quadro: dict):
        """Salva i dati correnti per popolare i grafici."""
        chiave_tempo = f"A{self.anno_corrente}_{self.stagione_corrente}"
        self.storico_stagionale[chiave_tempo] = dati_quadro