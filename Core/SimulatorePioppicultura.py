# Core/SimulatorePioppicultura.py
import os
import json
import math
from typing import Dict, List, Any
from Core.ditta import Ditta
from Core.lotto import Lotto
from Core.parametri_simulazione import ParametriSimulazione
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class SimulatorePioppicoltura:
    """
    Motore algoritmico e matematico per la simulazione del ciclo colturale del pioppo.
    Gestisce l'accrescimento biometrico mediante curve eco-fisiologiche guidate dai dati 
    del file JSON e calcola il bilancio di saturazione stagionale della ditta forestale.
    """
    def __init__(self, ditta: Ditta, parametri: ParametriSimulazione):
        self.ditta = ditta
        self.parametri = parametri  # Collegamento alla collezione lotti e all'orologio della GUI
        self.dati_cloni: Dict[str, Any] = {}
        # Solleva FileNotFoundError or json.JSONDecodeError bloccando l'esecuzione se il file fallisce
        self._carica_configurazione_cloni()

    def _carica_configurazione_cloni(self):
        """
        Carica i dati tecnologici ed ecofisiologici dei cloni dal file JSON originale.
        Se il file è assente o malformato, solleva un'eccezione bloccante.
        """
        percorso_json = os.path.join(os.path.dirname(__file__), "cloni.json")
        with open(percorso_json, "r", encoding="utf-8") as f:
            self.dati_cloni = json.load(f)

    def calcola_moltiplicatore_idrico(self, indice_idrico: float) -> float:
        """Sfrutta una funzione parabolica asimmetrica per calcolare lo stress ecofisiologico."""
        if indice_idrico >= 0:
            return 1.0 - (0.25 * (indice_idrico ** 2))
        else:
            return 1.0 - (0.30 * (abs(indice_idrico) ** 1.5))

    def _get_chiave_fase(self, eta_anno: int) -> str:
        """Determina la chiave di stringa corretta per mappare l'età sulla struttura lavorazioni."""
        if eta_anno == 0:
            return 0
        elif eta_anno == 1:
            return 1
        elif 2 <= eta_anno <= 5:
            return "Fase_Crescita_Giovane"
        else:
            return "Fase_Mantenimento_Tardo"

    def simula_accrescimento_lotto(self, lotto: Lotto, eta_anno: int) -> Dict[str, Any]:
        """
        Calcola la biometria reale del fusto in modo puramente matematico, deducendo 
        i parametri di crescita dalle proprietà qualitative e quantitative del tuo JSON.
        """
        if eta_anno == 0:
            return {"dbh_reale_cm": 0.0, "volume_totale_m3": 0.0, "piante_attive": lotto.densita_iniziale}

        # 1. Estrazione del profilo dal file cloni.json originale
        profilo_clone = self.dati_cloni[lotto.clone_assegnato]
        param_crescita = profilo_clone["parametri_crescita"]
        esigenze_trattamenti = profilo_clone["esigenze_trattamenti"]
        attitudine_suolo = profilo_clone["attitudine_suolo"]
        
        incremento_ottimale = param_crescita["incremento_medio_annuo_ottimale"]
        coeff_forma_json = param_crescita["coefficiente_forma"]
        eta_rotazione = param_crescita["eta_rotazione_standard"]

        # 2. TRADUZIONE SEMANTICA DELLE STRINGHE IN COEFFICIENTI BIOLOGICI REALI
        if "siccità" in attitudine_suolo.lower():
            indice_tolleranza_stress = 1.05  # Mitiga lo stress ambientale (cloni rustici)
        elif "falda" in attitudine_suolo.lower():
            indice_tolleranza_stress = 1.01
        else:
            indice_tolleranza_stress = 1.00  # Risposta standard

        # Penalizzazione extra per cloni iper-esigenti all'avvio in caso di stress idrico
        irrigazione_giovanile = esigenze_trattamenti.get("frequenza_irrigazione_anni_1_2", "Media")
        penalizzazione_esigenza_idrica = 0.92 if irrigazione_giovanile == "Alta" else 1.00

        # 3. DETERMINAZIONE DINAMICA DEI PARAMETRI DI CHAPMAN-RICHARDS (A, k, p)
        A = incremento_ottimale * 1.65 
        k = 1.5 / eta_rotazione
        p = 1.25 if esigenze_trattamenti.get("frequenza_irrigazione_anni_1_2", "Media") == "Alta" else 1.40

        # 4. CALCOLO DEI MOLTIPLICATORI AMBIENTALI E COLTURALI
        moltiplicatore = self.calcola_moltiplicatore_idrico(lotto.indice_tendenza_idrica)
        
        if moltiplicatore < 1.0:
            moltiplicatore = min(1.0, moltiplicatore * indice_tolleranza_stress)
            moltiplicatore *= penalizzazione_esigenza_idrica

        malus_colturale = getattr(lotto, "malus_colturale_accumulato", 0.0)
        moltiplicatore_reale = max(0.40, moltiplicatore - malus_colturale)

        # 5. ESECUZIONE DELLE EQUAZIONI BIOMETRICHE CON VINCOLO DI LIMITE DI SPECIE
        if eta_anno > 15:
            eta_calcolo = 15
            tasso_mortalita_annuo = 0.08  # 8% di piante morte all'anno dopo i 15 anni
        else:
            eta_calcolo = eta_anno
            tasso_mortalita_annuo = 0.005 # 0.5% standard

        dbh_potenziale = A * ((1.0 - math.exp(-k * eta_calcolo)) ** p)
        dbh_reale = dbh_potenziale * moltiplicatore_reale

        altezza_stimata = (1.15 * dbh_reale) + 1.2
        area_basale = math.pi * ((dbh_reale / 200) ** 2)
        volume_singolo = area_basale * altezza_stimata * coeff_forma_json

        # Calcolo della curva di mortalità reale accumulata nel tempo
        if eta_anno <= 15:
            sopravvivenza = (1.0 - tasso_mortalita_annuo) ** eta_anno
            piante_vive = int(lotto.superficie_ettari * lotto.densita_iniziale * sopravvivenza)
        else:
            sopravvivenza_15 = (1.0 - 0.005) ** 15
            piante_15 = int(lotto.superficie_ettari * lotto.densita_iniziale * sopravvivenza_15)
            anni_extra = eta_anno - 15
            piante_vive = int(piante_15 * ((1.0 - tasso_mortalita_annuo) ** anni_extra))
        
        return {
            "dbh_reale_cm": round(dbh_reale, 2),
            "altezza_m": round(altezza_stimata, 2),
            "volume_singolo_m3": round(volume_singolo, 4),
            "piante_attive": max(0, piante_vive),
            "volume_totale_m3": round(volume_singolo * max(0, piante_vive), 2)
        }

    def esegui_fase_lavorazioni_stagionali(self) -> Dict[str, Any]:
        """Scansiona i cantieri, li ordina per priorità, interroga la ditta e calcola i malus dal JSON."""
        stagione_attiva = self.parametri.stagione_corrente
        
        # Sincronizzazione dinamica trimestrale
        giorni_utili_stagione = 55 
        self.ditta.inizializza_serbatoi_stagionali(giorni_utili_stagione)
    
        report_stagionale = {
            "ore_disponibili_iniziali": round(self.ditta.serbatoi_ore["grado_A"] + self.ditta.serbatoi_ore["grado_B"], 2),
            "ore_risparmiate_o_mancanti": 0.0,
            "dettaglio_operazioni": [], 
            "tagli_effettuati": []
        }
    
        lista_interventi_richiesti = []
    
        # 1. Pianificazione teorica iniziale di tutte le operazioni del trimestre per ciascun lotto
        for lotto in self.parametri.collezione_lotti:
            if lotto.tagliato:
                continue
    
            eta_taglio = self.dati_cloni[lotto.clone_assegnato]["parametri_crescita"]["eta_rotazione_standard"]
            
            # BLINDATURA STRATEGICA: Il taglio si effettua ed esamina SOLO in inverno
            if lotto.eta_lotto >= eta_taglio:
                if stagione_attiva == "Inverno":
                    operazioni = STRUTTURA_LAVORAZIONI["Raccolta"][stagione_attiva]
                    is_raccolta = True
                else:
                    # In Primavera/Estate/Autunno il cantiere di taglio non viene riproposto
                    continue 
            else:
                fase_chiave = self._get_chiave_fase(lotto.eta_lotto)
                operazioni = STRUTTURA_LAVORAZIONI[fase_chiave].get(stagione_attiva, [])
                is_raccolta = False
    
            for op in operazioni:
                tipo_cantiere = op["operazione"].lower()
                if "trattamento" in tipo_cantiere or "fitosanitario" in tipo_cantiere:
                    tipo_cantiere = "trinciatura" 
                elif "potatura" in tipo_cantiere:
                    tipo_cantiere = "potatura"
                elif "impianto" in tipo_cantiere:
                    tipo_cantiere = "impianto"
                elif is_raccolta:
                    tipo_cantiere = "raccolta_avanzata" if self.ditta.harvester_abbattitori > 0 else "raccolta_tradizionale"
    
                # Assegnazione dell'unità di lavoro (numero piante reali per la raccolta, ettari per colture)
                if is_raccolta:
                    stato_bio = self.simula_accrescimento_lotto(lotto, lotto.eta_lotto)
                    unita_lavoro = stato_bio["piante_attive"]
                else:
                    unita_lavoro = lotto.superficie_ettari
    
                # Calcolo analitico specifico del fabbisogno per risorsa
                specifiche_richiesta = self.ditta.calcola_specifiche_richiesta_cantiere(
                    tipo_cantiere, unita_lavoro, lotto.indice_attrito_spaziale
                )
                
                if specifiche_richiesta:
                    lista_interventi_richiesti.append({
                        "lotto": lotto,
                        "operazione": op["operazione"],
                        "priorita": op["priorita"],
                        "specifiche_richiesta": specifiche_richiesta,
                        "is_raccolta": is_raccolta
                    })
    
        # 2. Ordinamento stabile basato sul livello di priorità (da 1 a 4)
        lista_interventi_richiesti.sort(key=lambda x: x["priorita"])
    
        # 3. Bilancio ed erogazione reale tramite macchina a stati a consumo proporzionale della Ditta
        for intervento in lista_interventi_richiesti:
            lotto_target = intervento["lotto"]
            specifiche = intervento["specifiche_richiesta"]
            
            if not hasattr(lotto_target, "malus_colturale_accumulato"):
                lotto_target.malus_colturale_accumulato = 0.0
    
            # CORREZIONE: Intercettiamo la percentuale float di completamento reale svolto (0.0 a 1.0)
            percentuale_completamento = self.ditta.verifica_e_consuma_risorse(specifiche)
    
            if percentuale_completamento >= 0.99:
                stato_esecuzione = "Eseguito"
            elif percentuale_completamento > 0.0:
                stato_esecuzione = f"Eseguito Parziale ({int(percentuale_completamento * 100)}%)"
            else:
                stato_esecuzione = "Bloccato (Risorse Insufficienti)"
                
                # Penalizzazione colturale applicata solo se il cantiere colturale salta del tutto
                if not intervento["is_raccolta"]:
                    sensibilita_marsonina = self.dati_cloni[lotto_target.clone_assegnato]["esigenze_trattamenti"]["sensibilita_marsonina"]
                    
                    if intervento["priorita"] == 2:  
                        moltiplicatore_danno = 1.3 if sensibilita_marsonina == "Alta" else (0.5 if "bassa" in sensibilita_marsonina.lower() else 1.0)
                        lotto_target.malus_colturale_accumulato += (0.08 * moltiplicatore_danno)
                    elif intervento["priorita"] == 3:  
                        lotto_target.malus_colturale_accumulato += 0.05
                    elif intervento["priorita"] == 4:  
                        lotto_target.malus_colturale_accumulato += 0.03
    
            report_stagionale["dettaglio_operazioni"].append({
                "lotto_id": lotto_target.id_lotto, 
                "operazione": intervento["operazione"],
                "priorita": intervento["priorita"],
                "ore_richieste": round(specifiche.get("ore_richieste", 0.0), 2),
                "stato": stato_esecuzione
            })
    
            # Processamento delle rese industriali eseguito SOLO se il cantiere di raccolta è completato al 100%
            if intervento["is_raccolta"] and percentuale_completamento >= 0.99:
                dati_biometrici = self.simula_accrescimento_lotto(lotto_target, lotto_target.eta_lotto) 
                vol_lotto_completo = dati_biometrici["volume_totale_m3"]
                densita_verde = self.dati_cloni[lotto_target.clone_assegnato]["proprieta_tecnologiche"]["densita_verde_t_m3"]
    
                # RIPARTIZIONE COMMERCIALE REALE DEI TRE OUTPUT IN BASE ALLA DESTINAZIONE D'USO
                destinazione_lotto = getattr(lotto_target, "destinazione_uso", "OPERA")
    
                if destinazione_lotto == "OPERA":
                    rese_lotto = {
                        "opera_m3": vol_lotto_completo * 0.70,        # 70% Tronco da opera di pregio
                        "cartiera_t": (vol_lotto_completo * 0.20) * densita_verde,  # 20% Ramaglie e sramatura alta
                        "truciolato_t": (vol_lotto_completo * 0.10) * densita_verde # 10% Scarti di ceppaia e nodi
                    }
                else:  # Destinazione INDUSTRIA (Cartiere/Biomassa - Rotazione Corta)
                    rese_lotto = {
                        "opera_m3": 0.0,                               # Nessun assortimento da segheria
                        "cartiera_t": (vol_lotto_completo * 0.90) * densita_verde,  # 90% Cippato e pasta meccanica
                        "truciolato_t": (vol_lotto_completo * 0.10) * densita_verde # 10% Scarti basali
                    }
                
                if hasattr(self.parametri, "accumula_resa_lotto"):
                    self.parametri.accumula_resa_lotto(rese_lotto)
                else:
                    self.parametri.totale_prodotto_opera_m3 = getattr(self.parametri, "totale_prodotto_opera_m3", 0.0) + rese_lotto["opera_m3"]
                    self.parametri.totale_prodotto_cartiera_t = getattr(self.parametri, "totale_prodotto_cartiera_t", 0.0) + rese_lotto["cartiera_t"]
                    self.parametri.totale_prodotto_truciolato_t = getattr(self.parametri, "totale_prodotto_truciolato_t", 0.0) + rese_lotto["truciolato_t"]
    
                # --- LINEA DI DIAGNOSTICA SUL TERMINALE PER VERIFICA TURNI ---
                print(f"🌲 [LOG MOTORE] -> Il {lotto_target.id_lotto} ({destinazione_lotto}) ha completato il ciclo colturale ed è stato interamente ABBATTUTO al termine dell'Anno {self.parametri.anno_corrente} (Stagione: {stagione_attiva}) all'età biometrica di {lotto_target.eta_lotto} anni.")
                
                # --- IL REIMPIANTO AUTOMATICO (CICLO CONTINUO ASINCRONO) ---
                lotto_target.eta_lotto = 0
                lotto_target.tagliato = False  # Il lotto si resetta e rientra in gioco per l'anno successivo
                lotto_target.malus_colturale_accumulato = 0.0
                
                report_stagionale["tagli_effettuati"].append({
                    "lotto_id": lotto_target.id_lotto, 
                    "volume_raccolto_m3": vol_lotto_completo,
                    "rese": rese_lotto
                })
                
            elif_trigger = intervento["is_raccolta"] and percentuale_completamento < 0.99
            if_fallimento_parziale = elif_trigger
            if if_fallimento_parziale:
                # Se la ditta non ha ore invernali sufficienti per abbattere l'intera particella,
                # il taglio slitta all'anno successivo per non falsare l'accumulo cumulativo delle rese
                lotto_target.tagliato = False
    
        # Restituisce il bilancio orario complessivo residuo della ditta
        ore_rimaste = self.ditta.serbatoi_ore["grado_A"] + self.ditta.serbatoi_ore["grado_B"]
        report_stagionale["ore_risparmiate_o_mancanti"] = round(ore_rimaste, 2)
    
        return report_stagionale

    def avanza_passo_simulazione(self) -> Dict[str, Any]:
        """Gestisce lo scatto del cronometro trimestrale, storicizza e aggiorna l'età biologica."""
        # 1. Esegui i cantieri previsti per questo trimestre
        risultati_cantieri = self.esegui_fase_lavorazioni_stagionali()

        # 2. L'accrescimento biologico e l'invecchiamento si consolidano solo in Autunno
        if self.parametri.stagione_corrente == "Autunno":
            for lotto in self.parametri.collezione_lotti:
                if not lotto.tagliato:
                    lotto.dati_correnti = self.simula_accrescimento_lotto(lotto, lotto.eta_lotto) 
                    lotto.eta_lotto += 1 
                    # Il malus colpisce lo sviluppo dell'anno corrente, poi il registro si svuota
                    lotto.malus_colturale_accumulato = 0.0

            # --- SEZIONE DIAGNOSTICA RESE DI FINE ANNO (TERMINALE) ---
            opera_tot = round(getattr(self.parametri, "totale_prodotto_opera_m3", 0.0), 2)
            cartiera_tot = round(getattr(self.parametri, "totale_prodotto_cartiera_t", 0.0), 2)
            truciolato_tot = round(getattr(self.parametri, "totale_prodotto_truciolato_t", 0.0), 2)
            
            print(f"\n=======================================================")
            print(f"📊 [CONSUNTIVO ANNUALE COMULATO] -> Fine Anno {self.parametri.anno_corrente}")
            print(f"-------------------------------------------------------")
            print(f" 🪵 Legname da OPERA (Sfoglia/Asse) : {opera_tot} m³")
            print(f" 🪵 Fibra da CARTIERA (Tranciatura): {cartiera_tot} t")
            print(f" 🪵 Scarti da TRUCIOLATO (Biomassa) : {truciolato_tot} t")
            print(f"=======================================================\n")

        # --- SEZIONE FOTOGRAFIA BIOMETRICA STAGIONALE (STRUTTURA PER GRAFICI) ---
        stato_lotti_istantaneo = {}
        for lotto in self.parametri.collezione_lotti:
            stato_lotti_istantaneo[lotto.id_lotto] = {
                "eta_lotto": lotto.eta_lotto,
                "tagliato": lotto.tagliato,
                "biometria": lotto.dati_correnti.copy() if hasattr(lotto, "dati_correnti") and lotto.dati_correnti else {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, "volume_singolo_m3": 0.0, "piante_attive": lotto.densita_iniziale, "volume_totale_m3": 0.0
                }
            }

        # 3. Costruzione del pacchetto di stato omnicomprensivo da inviare alla cronologia
        quadro_stato = {
            "risultati_cantieri": risultati_cantieri,
            "stato_lotti": stato_lotti_istantaneo,  # Memorizzato stabilmente per ogni trimestre!
            "produzione_cumulata": {
                "opera_m3": getattr(self.parametri, "totale_prodotto_opera_m3", 0.0),
                "cartiera_t": getattr(self.parametri, "totale_prodotto_cartiera_t", 0.0),
                "truciolato_t": getattr(self.parametri, "totale_prodotto_truciolato_t", 0.0)
            }
        }
        
        if hasattr(self.parametri, "registra_instantanea_stato_corrente"):
            self.parametri.registra_instantanea_stato_corrente(quadro_stato)
        
        # Avanzamento effettivo dell'orologio stagionale/annuo coordinato con la GUI
        dati_orologio = self.parametri.avanza_stagione() 
        
        return {**dati_orologio, **quadro_stato}