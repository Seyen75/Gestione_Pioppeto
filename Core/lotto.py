
import math, random

class Lotto:
    
    # ATTRIBUTI FISSI E INIZIALI
    
    def __init__(self, id_lotto: str, superficie: float, sesto_impianto: str = "6x6"):
        '''Inizializza un nuovo lotto con i parametri di base. Il sesto di impianto determina la densità iniziale di piante per ettaro.'''
        
        # PARAMETRI IDENTIFICATIVI E FISICI
        self.id_lotto: str = id_lotto
        self.superficie_ettari: float = superficie
        
        # Gestione dinamica del sesto (calcolata in base al sesto scelto)
        self.sesto_impianto: str = sesto_impianto
        self.densita_iniziale: int = self._calcola_densita(sesto_impianto)
        
        # PARAMETRI AMBIENTALI E CLONALI
        self.indice_attrito_spaziale: int = 0   
        self.indice_tendenza_idrica: float = 0.0 
        self.clone_assegnato: str = "I-214"
        self.destinazione_uso: str = "OPERA"

        # VARIABILI DI STATO BIOLOGICHE DINAMICHE
        self.eta: int = 0
        self.numero_piante_vive: int = int(self.superficie_ettari * self.densita_iniziale)
        self.diametro_medio_fusto: float = 0.0
        self.altezza_media_piante: float = 0.0
        self.anni_ritardo_taglio: int = 0
        self.tagliato: bool = False
        
        # VARIABILI DI STATO OPERATIVE
        self.immissione_effettuata: bool = False
        self.malus_colturale_accumulato: float = 0.0
        self.report_resa_finale: dict = {}

    # PROPERTIES DI ALIAS
    @property
    def clone_scelto(self): return self.clone_assegnato
    @clone_scelto.setter
    def clone_scelto(self, value): self.clone_assegnato = value

    @property
    def superficie(self) -> float: return self.superficie_ettari
    @superficie.setter
    def superficie(self, value: float): self.superficie_ettari = value

   
    def _calcola_densita(self, sesto: str) -> int:
        """
        Calcola dinamicamente la densità iniziale di piante per ettaro 
        in base alla stringa del sesto di impianto (es. "6x6", "3x2").
        
        Se la stringa non è valida o vuota, solleva un ValueError.
        """
       
        # Splitta la stringa (es. "6x6" diventa ["6", "6"])
        distanza_fila, distanza_interfila = map(float, sesto.lower().split('x'))
        
        # Calcola la superficie del modulo d'impianto
        superficie_pianta = distanza_fila * distanza_interfila
        
        if superficie_pianta <= 0:
            raise ValueError("Le dimensioni del sesto devono essere maggiori di zero.")
            
        # 10.000 mq / superficie singola pianta, arrotondato all'intero più vicino
        
        return round(10000 / superficie_pianta)
        

    def inizializza_nuovo_ciclo(self):
        """Resetta le variabili per un nuovo ciclo di vita del pioppeto."""
                
        # Reset operativo
        self.immissione_effettuata = False 
        self.malus_colturale_accumulato = 0.0
        self.anni_ritardo_taglio = 0
        self.tagliato = False
        self.report_resa_finale = {}
        
        # Reset Biometrico Incondizionato
        self.diametro_medio_fusto = 0.0
        self.altezza_media_piante = 0.0
        
        # Reset piante (calcolo base)
        self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)

        # RESET DELLA CACHE DEL SIMULATORE
        self.dati_correnti = {
            "dbh_reale_cm": 0.0, 
            "altezza_m": 0.0, 
            "volume_singolo_m3": 0.0, 
            "piante_attive": self.numero_piante_vive, 
            "volume_totale_m3": 0.0
        }


    def esegui_raccolta(self, piante_abbattute: int, clone_profilo: dict) -> tuple[dict, str]:
            '''Esegue la raccolta del lotto, calcolando le rese e aggiornando lo stato delle piante. Se il lotto è completamente abbattuto, viene resettato per un nuovo ciclo. 
            Restituisce un dizionario con le rese e una stringa con lo stato dell'esecuzione.'''
            
            # Calcolo rese differenzuate per la tipologia di assortimenti e la tipologia di clone che ha una densità di legname specifica
            rese = self.calcola_ripartizione_assortimenti(clone_profilo, piante_abbattute)
            
            # Aggiornamento del numero di piante vive nel lotto in caso di taglio parziale
            self.numero_piante_vive = max(0, self.numero_piante_vive - piante_abbattute)
            self.dati_correnti["piante_attive"] = self.numero_piante_vive
            
            # Logica di reset ciclo in caso taglio totale o parziale. In caso taglio totale viene avviato il nuovo ciclo del lotto
            if self.numero_piante_vive <= 5:
                self.inizializza_nuovo_ciclo()
                stato_esecuzione = "Eseguito (Taglio Completato - Reset Ciclo)"
            elif piante_abbattute > 0:
                self.tagliato = True
                self.anni_ritardo_taglio += 1
                stato_esecuzione = f"Eseguito Parziale (In piedi {self.numero_piante_vive} piante)"
            else:
                self.tagliato = False
                self.anni_ritardo_taglio += 1
                stato_esecuzione = f"Taglio bloccato"
            
            # ritorna una tupla con il dizionario dei quantitativi di rese calcolato ed una stringa sullo stato di esecuzione della raccolta    
            return rese, stato_esecuzione

    
    def applica_lavorazione(self, operazione: str, tipo_cantiere: str, percentuale: float, stagione: str, anno: int, profilo_clone: dict, priorita: int):
        """
        Aggiorna lo stato interno del lotto basandosi sull'esito di una lavorazione.
        Restituisce lo stato dell'esecuzione come stringa.
        """
        # Caso successo. Verifica se la lavorazione è quella dell'inserimento di astoni per impianto per aggiornare la variabile di riferimento
        if percentuale >= 0.99:
            if "impianto" in tipo_cantiere.lower() or "astoni" in operazione.lower():
                self.immissione_effettuata = True
            
            # se la lavorazione è quella di nuovo impianto ricalcola il numero di piante vive presenti ad inizio ciclo
            if tipo_cantiere == "impianto" and self.numero_piante_vive == 0:
                self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)
                self.dati_correnti["piante_attive"] = self.numero_piante_vive
            
            return "Eseguito"

        # Caso fallimento/parziale avvia la registrazione nel registro della lavorazione fallita o parzialmente eseguita
        stato = f"Eseguito Parziale ({int(percentuale * 100)}%)" if percentuale > 0.001 else "Bloccato"
        
        # Gestione Malus
        if percentuale <= 0.001:
            sensibilita = profilo_clone["esigenze_trattamenti"].get("sensibilita_marsonina", "Media")
            self.applica_malus_da_fallimento(operazione, tipo_cantiere, sensibilita, priorita)
            
        return stato
    
    
    def verifica_maturita_raccolta(self, tolleranza: float) -> bool:
        '''Funzione che verifica lo stato di maturità di un lotto per il taglio.
        La funzione ha una tolleranza sulla verifica del diametro medio delle piante in caso di raggiungimento dell'età di taglio.
        Tale tolleranza è data dal fatto che economicamente è meglio effettuare un taglio di un lotto che per pochi millimetri non ha raggiunto il diametro target
        che daranno una leggera minore resa, che rimandare il taglio all'anno successivo perdendo i ritorno economici nell'anno in corso.'''
        TOLLERANZA_PERCENTUALE = tolleranza
         # Differenzia a seconda della tipologia di resa del lotto i parametri per la valutazione
        if self.destinazione_uso == "OPERA":
            eta_minima_verifica = 10
            diametro_target = 35.0 
            limite_massimo_ritardo = 5
        else:
            eta_minima_verifica = 5
            diametro_target = 15.0
            limite_massimo_ritardo = 3

        if self.eta < eta_minima_verifica: 
            return False
        # calcola la soglia elestica del 90% del diametro target
        soglia_elastica = diametro_target * (1.0 - TOLLERANZA_PERCENTUALE)
        
        # verifica lo stato di maturità del lotto
        if self.diametro_medio_fusto >= soglia_elastica:
            return True
            
        if self.anni_ritardo_taglio >= limite_massimo_ritardo:
            return True
            
        return False


    def calcola_ripartizione_assortimenti(self, parametri_clone_selezionato: dict, piante_abbattute: int) -> dict:
        '''Calcola la ripartizione degli assortimenti (Opera, Cartiera, Truciolato) in base al profilo del clone, alla destinazione d'uso e al numero di piante abbattute. 
        Restituisce un dizionario con le rese per ogni tipologia.'''
        
        # Inizializzazione delle variabili locali di conteggio delle rese
        volume_cantiere_m3 = 0.0
        resa_opera_m3 = 0.0
        resa_cartiera_ton = 0.0
        resa_truciolato_ton = 0.0
        
        # Se non ci sono piante da abbattere ritorna una resa nulla
        if piante_abbattute <= 0:
            return {"volume_cantiere_m3": 0.0, "opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}

        # estrae i parametri specifici del clone di pioppo utilizzato nel lotto per il calcolo della resa
        param_crescita = parametri_clone_selezionato["parametri_crescita"]
        param_tecnologici = parametri_clone_selezionato["proprieta_tecnologiche"]
        
        # coefficiente di forma per l'applicazione del calcolo del volume di un albero. L'albero non è un cilindro perfetto ma ha una rastremazione 
        # verso la zona cimale che varia a seconda del clone scelto.
        coeff_forma = param_crescita["coefficiente_forma"]
        # ogni clone di pioppo ha una densità del legname diverso. Questo per il calcolo del peso è determinante ai fini della resa per Industria
        densita_verde = param_tecnologici["densita_verde_t_m3"]
        
        # Calcolo del volume lordo reale del lotto. Viene utilizzata la formula dendrometrica di calcolo del volume che applica 
         # Calcolo dell'area della sezione (g) = (pi * d^2) / 4
         
        d_m = self.diametro_medio_fusto / 100.0 
        area_sezione = (math.pi * (d_m ** 2)) / 4

        # Volume totale del cantiere
        volume_cantiere_m3 = area_sezione * self.altezza_media_piante * coeff_forma * piante_abbattute
        
        if self.destinazione_uso == "OPERA":
            # DESTINAZIONE OPERA (Mobilifici ed edilizia). Poichè non tutto l'albero è utilizzabile come resa per assi viene prima calcolato un Indice Qualità Legname
            # Un malus di 0.0 significa fusto perfetto (indice 1.0).
            # Un malus alto riduce linearmente la qualità (es. i nodi impediscono di fare l'Opera)
            # Tale malus viene recuperato dallo storico del lotto e che proviene dalle eventuali lavorazioni non effettuate durante gli anni che hanno reso il lotto di minore qualità
            malus_storico = self.malus_colturale_accumulato
            indice_qualita_fusto = max(0.60, 1.0 - (malus_storico * 0.4)) 
            
            # Si utilizza il valore medio standard del 62%. Questo rappresenta mediamente la parte di albero utile per la resa da Opera
            # Il valore è poi influenzato dall'indice precedentemente calcolato
            mu_opera = 0.62 * indice_qualita_fusto 
            
            # Viene applicata una minima randomizzazione, attraverso l'uso di una funzione di densità normale, con parametro di media quello calcolato precedentemente
            # e con una deviazione standard specifica per ogni quota di resa. Questo per evitare l'appiattimento matematico di una formula matematica troppo deterministica
            # e dare un minimo di variabilità.
            quota_opera = max(0.01, random.gauss(mu_opera, 0.04))
            quota_cartiera = max(0.01, random.gauss(0.20, 0.03))
            quota_truciolato = max(0.01, random.gauss(0.18, 0.03))

            # Viene effettuata una normalizzazione dei valori che escono dal precedente calcolo per evitare distorzioni di risultati
            somma_quote = quota_opera + quota_cartiera + quota_truciolato
            quota_opera /= somma_quote
            quota_cartiera /= somma_quote
            quota_truciolato /= somma_quote

            # La resa viene poi inserita nelle variabili finali suddivise per unità di misura. Opera direttamente in metri cubi 
            # Industria viene trasformata in peso (tonnellate) attraverso l'applicazione del parametro di densità del legname del clone selezionato
            resa_opera_m3 = volume_cantiere_m3 * quota_opera
            resa_cartiera_ton = (volume_cantiere_m3 * quota_cartiera) * densita_verde
            resa_truciolato_ton = (volume_cantiere_m3 * quota_truciolato) * densita_verde
        else:
            # DESTINAZIONE INDUSTRIA (Biomassa/Cartiera pura)
            # In tale calcolo non serve applicare l'indice di qualità del legname in quanto nelle rese da industria il legname viene triturato e sono utilizzabili anche alberi strutturalmente storti
            # Viene applicata anche qui una randomizzazione della quota principale con l'uso di una normale con parametro 0.88 (88%) ed una deviazione standard di 0.03
            # In questo caso la resa del truciolato è semplicemente la rimanenza della resa principale. Il tutto viene poi trasformato in tonnellate. 
            quota_cartiera = random.gauss(0.88, 0.03)
            quota_cartiera = max(0.75, min(0.95, quota_cartiera))
            quota_truciolato = 1.0 - quota_cartiera
            resa_cartiera_ton = (volume_cantiere_m3 * quota_cartiera) * densita_verde
            resa_truciolato_ton = (volume_cantiere_m3 * quota_truciolato) * densita_verde

        # Ritorna il dizionario della resa del lotto
        return {
            "volume_cantiere_m3": round(volume_cantiere_m3, 2),
            "opera_m3": round(resa_opera_m3, 2),
            "cartiera_t": round(resa_cartiera_ton, 2),
            "truciolato_t": round(resa_truciolato_ton, 2)
        }
    
  
    def calcola_moltiplicatore_idrico(self, profilo_clone: dict) -> float:
        '''Calcola un moltiplicatore incrociando l'andamento idrico del lotto 
        con l'adattabilità genetica del clone selezionato.'''

        # 1. Recupero dell'indice genetico del clone (dal JSON)
        idx_clone = profilo_clone["parametri_crescita"]["indice_tendenza_idrica_base"]
        
        # 2. Recupero dell'indice ambientale del lotto (attributo di istanza)
        idx_lotto = self.indice_tendenza_idrica
        
        # 3. Indice combinato finale (Interazione Genotipo-Ambiente)
        idx_combinato = idx_lotto + idx_clone
        
        # 4. Calcolo del moltiplicatore secondo le tue soglie
        if idx_combinato >= 0:
            # Bonus lineare: fino a un massimo del +10%
            # Usiamo min per evitare che un super bonus superi la soglia logica del programma
            return min(1.10, 1.0 + (0.10 * idx_combinato))
        else:
            # Malus lineare: fino a un massimo del -15% (limite inferiore 0.85)
            # Usiamo max per evitare che il malus distrugga completamente la pianta sotto lo 0.85
            return max(0.85, 1.0 - (0.15 * abs(idx_combinato)))


    def simula_accrescimento(self, profilo_clone: dict, eta_anno: int) -> dict:
        '''Simula l'accrescimento del lotto per un anno, restituendo un dizionario con i nuovi parametri biometrici e di resa.'''
        
        # Se siamo all'anno iniziale i valori del lotto sono azzerati
        if eta_anno == 0:
            return {
                "dbh_reale_cm": 0.0, 
                "altezza_m": 0.0, 
                "volume_singolo_m3": 0.0, 
                "piante_attive": self.numero_piante_vive, 
                "volume_totale_m3": 0.0
            }

        # Recupera i dati relativi al clone di pioppo del lotto
        param = profilo_clone["parametri_crescita"]
        
        # La destinazione d'uso influenza la curva di crescita: i lotti da INDUSTRIA, essendo più orientati alla produzione rapida,
        # hanno una crescita iniziale più veloce ma un plateau più basso, mentre quelli da OPERA crescono più lentamente ma raggiungono diametri maggiori.
        # Questi sono i parametri "A", "K" ed "p" che saranno poi utilizzati per la formula di accrescimento di Richards
        # il valore costante A che corrisponde all’asintoto orizzontale superiore del diametro
        # il valore costante K che rappresenta il tasso intrinseco di accrescimento (governa la "pendenza" della curva e la velocità con cui l'asintoto viene approcciato)
        # il valore costante p che rappresenta l'esponente allometrico o parametro di forma
        
        if self.destinazione_uso == "INDUSTRIA":
            A = param["incremento_medio_annuo_ottimale"] * 0.78
            eta_rot = 5
            k = 1.9 / eta_rot  
        else:
            A = param["incremento_medio_annuo_ottimale"] * 1.65
            eta_rot = param["eta_rotazione_standard"]
            k = 2.2 / eta_rot  

        parametri_irrigazione = profilo_clone["esigenze_trattamenti"]
        p = 1.02 if parametri_irrigazione["frequenza_irrigazione_anni_1_2"] == "Alta" else 1.05
        
        # Simula l'andamento meteo annuale (un numero casuale gaussiano centrato sullo 0 con deviazione standard del 5%)
        fluttuazione_stagionale = random.gauss(0.0, 0.05) 
        
        # Creazione degli Indici di Vitalità Biologica che vanno a modificare la formula di Richards
        # Moltiplicatore ambientale dinamico per lo stress idrico del clone applicato al lotto selezionato
        vocazione_terreno = self.calcola_moltiplicatore_idrico(profilo_clone)
        
        # Integrazione direttamente nel moltiplicatore reale di crescita (Indici di Vitalità Biologica - IVB)
        Ivb = vocazione_terreno - self.malus_colturale_accumulato + fluttuazione_stagionale
        Ivb = max(0.35, min(1.30,Ivb)) # Cap di sicurezza per evitare crescite o blocchi assurdi

        # Calcolo del DBH teorico attraverso l'applicazione della formula di Richards con l'inserimento del moltiplicatore dell'Indice di Vitalità Biologica (IVB)
        dbh_teorico = (A * ((1.0 - math.exp(-k * eta_anno)) ** p)) * Ivb
        
        # Salvaguardia biologica (il diametro non si restringe se l'anno è pessimo
        # gli alberi non tornano indietro, ma possono solo crescere o stagnare se i malus sono eccessivi)
        dbh_precedente = self.diametro_medio_fusto
        dbh = max(dbh_precedente, dbh_teorico)

        # Calcolo dell'altezza. Questa è più veloce nei primi 5 anni di vita in cui la pianta giovane tende a crescere rapidamente per la competizione sulla luce
        # Successivamente ha un tasso di crescita più graduale con questa che mediamente non superano i 32 metri di altezza per i pioppi
        # Alla parametro di crescita viene aggiunto o sottratto un piccolo valore randomico (rumore_allometrico) per rendere la crescita meno deterministica
        
        # Rumore fisiologico per simulare la variabilità naturale tra piante vicine (± 1.0 metro)
        rumore_allometrico = random.uniform(-1.0, 1.0)

        if eta_anno <= 5:
            # Fase Industria
            h_teorica = (dbh * 0.7) + 3.0 + rumore_allometrico
        else:
            # Fase Opera
            delta_dbh = max(0.0, dbh - 20.0)
            h_teorica = 17.0 + (math.sqrt(delta_dbh) * 2.45) + rumore_allometrico
            
        # Recupero dell'altezza precedente per il vincolo biologico (gli alberi non decrescono)
        # altezza_precedente = 0.0
        # if hasattr(self, "dati_correnti") and self.dati_correnti:
        altezza_precedente = self.dati_correnti.get("altezza_m", 0.0)
        # Verifica che l'albero non sia decresciuto e che non abbia superato l'altezza massima tipica dei pioppi coltivati in zona Padana
        h = max(altezza_precedente, min(32.0, h_teorica))
        
        
        
        # rumore_allometrico = random.uniform(-0.03, 0.03)
        # if eta_anno <= 5:
        #     h = (dbh * (0.6 + rumore_allometrico)) + 4.0
        # else:
        #     h = min(27.5, (17.0 + rumore_allometrico * 10) + (1.2 * (dbh - 20)))
        
        # Calcolo del volume dell'albero con applicazione della formula dell'Albero Modello e l'uso del coefficiente di forma tipico del clone selezionato
        vol_singolo = (math.pi * ((dbh / 200) ** 2)) * h * param["coefficiente_forma"]

        # CALCOLO MORTALITA' PIANTE
        # La mortalità in natura non è una quota fissa, risente di eventi locali casuali. 
        # Il tasso di mortalità è diverso fra il primo anno di vita dell'impianto, dove mediamente raggiunge il 7%, salvo che non si sia fatta la lavorazione di
        # reinnesto di astoni in sostituzione, che fa calare la mortalità mediamente al solo 0,7%
        if eta_anno == 1:
            immissione_fatta = self.immissione_effettuata
            tasso_base = 0.007 if immissione_fatta else 0.07
            # Si aggiunge un valore stocastico con la funzione random.uniform che aggiunge\sottrae un 2% al tasso base per dare variabilità casuale minima
            tasso_reale = max(0.002, tasso_base + random.uniform(-0.02, 0.02))
            piante_vive = int((self.superficie_ettari * self.densita_iniziale) * (1.0 - tasso_reale))
        else:
            # Dopo il primo anno il tasso di mortalità mediamente cresce all'aumetare dell'età delle piante
            tasso_base = 0.012 if eta_anno <= 5 else (0.018 if eta_anno <= 10 else 0.025)
            
            # Si aggiunge un valore aggiuntivo relativo all'eventuale malus colturale accumulato dal lotto. Più si saltano lavorazioni, maggiori sono i rischi di mortalità
            influenza_malus = self.malus_colturale_accumulato * 0.1
            # Si aggiunge un valore stocastico con la funzione random.uniform che aggiunge\sottrae un 0,5%/1% al tasso base per dare variabilità casuale minima
            tasso_reale = max(0.005, tasso_base + random.uniform(-0.005, 0.01) + influenza_malus)
            piante_vive = int(self.numero_piante_vive * (1.0 - tasso_reale))
        
        # Si ritorna il dizionario dello stato dinamico del lotto
        return {
            "dbh_reale_cm": round(dbh, 2), 
            "altezza_m": round(h, 2),
            "volume_singolo_m3": round(vol_singolo, 4), 
            "piante_attive": max(0, piante_vive),
            "volume_totale_m3": round(vol_singolo * max(0, piante_vive), 2)
        }

        
    def aggiorna_parametri_strutturali(self, nuova_superficie, nuovo_sesto):
        """
        Gestisce il ricalcolo delle piante e dei volumi al variare di superficie o sesto.
        """
        # Calcolo vecchia densità per il fattore scala
        vecchie_piante_teoriche = self.superficie_ettari * self.densita_iniziale
        
        # Aggiorna parametri fisici
        self.superficie_ettari = nuova_superficie
        self.sesto_impianto = nuovo_sesto
        
        # Ricalcola la densità basandosi sul nuovo sesto
        self._calcola_densita(self.sesto_impianto)
                
        # Ricalcolo piante in base alla nuova densità
        nuove_piante_teoriche = self.superficie_ettari * self.densita_iniziale
        
        if vecchie_piante_teoriche > 0:
            fattore_scala = nuove_piante_teoriche / vecchie_piante_teoriche
            self.numero_piante_vive = int(self.numero_piante_vive * fattore_scala)
            
            # Aggiorna se esiste la gestione dei dati dinamici
            if hasattr(self, "dati_correnti") and "volume_singolo_m3" in self.dati_correnti:
                self.dati_correnti["piante_attive"] = self.numero_piante_vive
                self.dati_correnti["volume_totale_m3"] = round(self.dati_correnti["volume_singolo_m3"] * self.numero_piante_vive, 2)
        else:
            # Fallback se il lotto era vuoto o appena creato
            self.numero_piante_vive = int(nuove_piante_teoriche)
    
    
    def get_fase_colturale(self) -> str:
        """Determina la fase di crescita in base all'età del lotto."""
        if self.eta == 0:
            return "0"
        elif self.eta == 1:
            return "1"
        elif 2 <= self.eta <= 4:
            return "Fase_Crescita_Giovane"
        else:
            return "Fase_Mantenimento_Tardo"
    
    
    def applica_malus_da_fallimento(self, operazione: str, tipo_cantiere: str, sensibilita: str, priorita: int):
        """
        Calcola e accumula il malus in base alla sensibilità del clone e alla priorità dell'intervento.
        Determina il danno in modo differenziato tra lotti da Opera e lotti da Industria.
        """
        # Calcolo del moltiplicatore di danno basato sulla sensibilità genetica del clone
        mult_danno = 1.3 if sensibilita == "Alta" else (0.5 if "bassa" in sensibilita.lower() else 1.0)
        
        # Calcolo del danno base in base alla priorità dell'operazione saltata
        danno_base = 0.0
        if priorita == 2:
            danno_base = 0.08 * mult_danno
        elif priorita == 3: 
            danno_base = 0.05
        elif priorita == 4: 
            danno_base = 0.03

        # AMMORTIZZATORE PER L'INDUSTRIA
        # Se il cantiere è finalizzato all'industria, le mancanze colturali pesano la metà (moltiplicatore 0.5)
        # perché la tolleranza del bosco a ciclo breve è nettamente superiore.
        if tipo_cantiere.strip().upper() == "INDUSTRIA":
            danno_base *= 0.5

        # Accumulo effettivo del malus sul lotto
        self.malus_colturale_accumulato += danno_base
        
    