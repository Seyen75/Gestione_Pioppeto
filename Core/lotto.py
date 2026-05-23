
# Modulo di rappresentazione del modello biologico e strutturale del singolo lotto.


class Lotto:
    def __init__(self, id_lotto: str, superficie: float):
        # PARAMETRI FISSI - Sono quelli che sono posizionati di default sulla form all'apertura o nel nuovo inserimento
        self.id_lotto: str = id_lotto
        self.superficie_ettari: float = superficie
        self.sesto_impianto: str = "6x6"
        self.densita_iniziale: int = 277        # Calcolato dal sesto di impianto default -> superficie / 36)
       
        # Scala da 0 a 10
        # Con 0 lotto estremamente comodo da raggiungere e lavorare. Massimo 10 con lotto estremamente complesso da lavorare e distante dagli altri. 
        self.indice_attrito_spaziale: int = 0   
        
        # Range da -1.0 (-100%) a +1.0 (+100%)
        # Indica la risposta del clone alla disponibilità di acqua nel terreno. 
        # Con valori sopra lo 0 si indica un terreno ottimo dove il pioppo cresce proporzionalmente ai suoi potenziali biometrici
        # Con il valore 0 si ha la condizione standard, mentre andando verso il -1 il terreno ha stress idrico sempre maggiore che incide sulla produttività finale del lotto
        self.indice_tendenza_idrica: float = 0.0 
        
        # Nome del clone scelto. Di default si è scelto quello più generico per il settore padano
        self.clone_assegnato: str = "I-214"

        # PARAMETRI DI INDIRIZZO E COERENZA PRODUTTIVA
        # Opzioni ammesse: "OPERA" (Sfoglia/Segheria) oppure "INDUSTRIA" (Cartiera/Biomassa). 
        # Il TRUCIOLATO, terzo output non viene specificato in quanto è diretto risultato degli scarti degli altri due e non è un prodotto base di produzione
        self.destinazione_uso: str = "OPERA"
        # Coefficiente di efficienza accoppiamento clone con resa (1.0 = ottimo, < 1.0 = malus)
        self.moltiplicatore_efficienza_clone: float = 1.0
        # Flag per il ciclo chiuso: True quando il lotto viene abbattuto e concluso
        self.tagliato: bool = False

        # VARIABILI DI STATO BIOLOGICHE DINAMICHE - Sono utilizzate dal motore di simulazione con i dati di crescita del lotto
        self.eta_lotto: int = 0
        self.numero_piante_vive: int = 0        # Popolazione reale corrente
        self.diametro_medio_fusto: float = 0.0   # Diametro della pianta a 1.30 metri
        self.altezza_media_piante: float = 0.0   # Altezza media piante
        self.metri_potatura_effettivi: float = 0.0
        self.stato_infestanti: float = 0.0      # Coefficiente relativo alla presenza di infestanti e problemi fitopatologici
        self.anni_ritardo_taglio: int = 0       # Registra il ritardo gestionale del lotto

        # REGISTRO EVENTI - tiene la lista, per il successimo report finale, se sono saltate lavorazioni per mancanza personale\mezzi
        self.cronistoria_lavorazioni_saltate: list = []

        # CONSUNTIVO FINALE DEL LOTTO
        self.report_resa_finale: dict = {}

    def presets_fallback_strutturale(self) -> dict:
        # Restituisce un dizionario minimo di emergenza se il passaggio dati con i dati della form fallisce
        return {
            "parametri_crescita": {
                "incremento_medio_annuo_ottimale": 25.0,
                "coefficiente_forma": 0.42
            },
            "proprieta_tecnologiche": {
                "densita_verde_t_m3": 0.85
            },
            "esigenze_trattamenti": {
                "sensibilita_marsonina": "Media"
            }
        }

    def inizializza_nuovo_ciclo(self):
        # Resetta le variabili biologiche all'atto dell'impianto
        self.eta_lotto = 0
        self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)
        self.diametro_medio_fusto = 0.0
        self.altezza_media_piante = 0.0
        self.metri_potatura_effettivi = 0.0
        self.stato_infestanti = 0.0
        self.anni_ritardo_taglio = 0
        self.tagliato = False
        self.cronistoria_lavorazioni_saltate = []
        self.report_resa_finale = {}

    def inizializza_lotto_preesistente(self, eta_iniziale: int, nome_clone: str, dizionario_globale_cloni: dict):

        # Funzione precedentemente fatta per un eventuale evoluzione del software. Attualmente non utilizzata
        # Inizializza lo stato biologico retroattivo usando i parametri strutturali estratti dal file JSON dei cloni attivi

        self.eta_lotto = eta_iniziale
        self.anni_ritardo_taglio = 0
        self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)
        self.tagliato = False

        # BLINDATURA DI SICUREZZA ANTICRASH
        if not dizionario_globale_cloni or nome_clone not in dizionario_globale_cloni:
            print(f"Warning Fitosanitario: Dati per '{nome_clone}' mancanti nel passaggio GUI. Fallback protettivo.")
            self.clone_assegnato = "I-214"
            dati_clone = self.presets_fallback_strutturale()
        else:
            self.clone_assegnato = nome_clone
            dati_clone = dizionario_globale_cloni[nome_clone]

        if self.eta_lotto > 0:
            # Estrazione parametri di crescita dal sotto-dizionario JSON
            parametri_crescita = dati_clone.get("parametri_crescita", {})

            # Converte l'incremento medio annuo ottimale da mm a cm (es. 25.0 mm -> 2.5 cm)
            inc_diametro_annuo = parametri_crescita.get("incremento_medio_annuo_ottimale", 25.0) / 10.0

            # Quota proporzionale per l'altezza basata sulla tipologia del clone
            if self.clone_assegnato == "I-214":
                inc_altezza_annuo = 2.4
            elif self.clone_assegnato == "Neva":
                inc_altezza_annuo = 2.5
            elif self.clone_assegnato == "Velasco":
                inc_altezza_annuo = 2.6
            else:
                inc_altezza_annuo = 2.2

            self.diametro_medio_fusto = float(self.eta_lotto * inc_diametro_annuo)
            self.altezza_media_piante = float(self.eta_lotto * inc_altezza_annuo)

            # Modello di mortalità cumulativa basato sulla sensibilità fitosanitaria del JSON
            esigenze = dati_clone.get("esigenze_trattamenti", {})
            sensibilita_malantie = esigenze.get("sensibilita_marsonina", "Media")

            tasso_mortalita = 0.015
            if sensibilita_malantie == "Molto Bassa":
                tasso_mortalita = 0.007
            elif sensibilita_malantie == "Bassa":
                tasso_mortalita = 0.010
            elif sensibilita_malantie == "Alta":
                tasso_mortalita = 0.020

            tasso_sopravvivenza = (1.0 - tasso_mortalita) ** self.eta_lotto
            self.numero_piante_vive = int(self.numero_piante_vive * tasso_sopravvivenza)

            # Allineamento storico potature in base all'altezza strutturale raggiunta
            if self.altezza_media_piante >= 12.0:
                self.metri_potatura_effettivi = 6.0
            elif self.altezza_media_piante >= 7.0:
                self.metri_potatura_effettivi = 3.0
            else:
                self.metri_potatura_effettivi = 0.0

    def genera_richiesta_oraria_lorda(self, ore_standard_ha: float) -> dict:
        
        # Prende le ore nette dalla richieste per singolo ettaro e restituisce
        # le ore di lavoro effettive e le ore di trasferta (influenzate dall'attrito spaziale).
        
        ore_lavoro_pure = ore_standard_ha * self.superficie_ettari
        # Se attrito è 10, le ore di trasferta equivalgono al 100% delle ore lavoro pure
        ore_trasferta_logistica = ore_lavoro_pure * (self.indice_attrito_spaziale / 10.0)

        return {
            "lavoro": ore_lavoro_pure,
            "trasferta": ore_trasferta_logistica
        }

    def registra_fallimento_intervento(self, operazione: str, stagione: str, anno: int):
        # Quando un lotto non riesce a fare un intervento si aggiorna il suo storico di degrado
        self.cronistoria_lavorazioni_saltate.append({
            "anno": anno,
            "stagione": stagione,
            "operazione": operazione
        })

    def verifica_maturita_raccolta(self, parametri_clone: dict) -> bool:
        # Controlla se il lotto ha raggiunto l'età minima e se il diametro medio soddisfa lo standard qualitativo commerciale del clone.
        
        # Se non ha ancora raggiunto l'età minima biologica, non è tagliabile
        if self.eta_lotto < parametri_clone.get("eta_rotazione_standard", 10):
            return False

        # Se ha l'età ma il diametro è inferiore all'obiettivo 
        # Per la destinazione INDUSTRIA questo controllo verrà bypassato dal simulatore in quanto non è un parametro essenziale
        diametro_target = parametri_clone.get("diametro_obiettivo_cm", 30.0)
        if self.destinazione_uso == "OPERA" and self.diametro_medio_fusto < diametro_target:
            self.anni_ritardo_taglio += 1
            return False

        return True

    def calcola_ripartizione_assortimenti(self, parametri_clone_selezionato: dict, diametro_obiettivo: float = 30.0) -> dict:
        
        # Calcola le rese reali prodotte per i 3 output richiesti:
        # - Opera: espresso in metri cubi (m3).
        # - Cartiera e Truciolato: espressi in tonnellate (t).

        # I calcoli utilizzano i coefficienti dendrometrici di forma e tecnologici
        # quale la densità del legno fresco che sono specifici per ciascun clone, estratti dal JSON.
        
        # Estrazione coefficienti specifici dal JSON con fallback di sicurezza
        param_crescita = parametri_clone_selezionato.get("parametri_crescita", {})
        param_tecnologici = parametri_clone_selezionato.get("proprieta_tecnologiche", {})

        coeff_forma = param_crescita.get("coefficiente_forma", 0.42)
        densita_verde = param_tecnologici.get("densita_verde_t_m3", 0.85)

        # Calcolo del volume totale teorico in piedi (m3) tramite formula di cubatura
        d_m = self.diametro_medio_fusto / 100.0  # Conversione cm -> metri
        volume_totale_m3 = (d_m ** 2) * self.altezza_media_piante * coeff_forma * self.numero_piante_vive

        # Applicazione del moltiplicatore di efficienza derivato dalla scelta del clone
        volume_totale_m3 = volume_totale_m3 * self.moltiplicatore_efficienza_clone

        resa_opera_m3 = 0.0
        resa_cartiera_ton = 0.0
        resa_truciolato_ton = 0.0

        if self.destinazione_uso == "OPERA":
            # Controllo fallimento target qualitativo (diametro sotto la soglia commerciale)
            if self.diametro_medio_fusto < diametro_obiettivo:
                # CASO DECLASSAMENTO: Tutto convertito in tonnellate di truciolato
                resa_truciolato_ton = volume_totale_m3 * densita_verde
            else:
                # CASO SUCCESSO: Ripartizione assortimenti standard
                resa_opera_m3 = volume_totale_m3 * 0.70
                # Gli scarti (15% cartiera e 15% truciolato) vengono pesati e convertiti in tonnellate
                resa_cartiera_ton = (volume_totale_m3 * 0.15) * densita_verde
                resa_truciolato_ton = (volume_totale_m3 * 0.15) * densita_verde

        elif self.destinazione_uso == "INDUSTRIA":
            # Tutto il materiale va a sminuzzamento industriale (90% cartiera, 10% truciolato) in tonnellate
            resa_cartiera_ton = (volume_totale_m3 * 0.90) * densita_verde
            resa_truciolato_ton = (volume_totale_m3 * 0.10) * densita_verde

        return {
            "opera_m3": round(resa_opera_m3, 2),
            "cartiera_t": round(resa_cartiera_ton, 2),
            "truciolato_t": round(resa_truciolato_ton, 2),
            "volume_originale_m3": round(volume_totale_m3, 2),
            "coefficiente_forma_applicato": coeff_forma,
            "densita_verde_applicata": densita_verde
        }