import os
import json
from typing import Dict, List, Any
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class SimulatorePioppicoltura:
    def __init__(self, ditta: Any, parametri: Any):
        self.ditta = ditta
        self.parametri = parametri  
        self.dati_cloni: Dict[str, Any] = {}
        
        self.stats_globali = {
            "tagli_strutturali_saltati": 0,
            "tagli_biologici_saltati": 0,
            "lavorazioni_generiche_saltate": 0
        }
                
        self._carica_configurazione_cloni()

    def _carica_configurazione_cloni(self):
        percorso_json = os.path.join(os.path.dirname(__file__), "cloni.json")
        with open(percorso_json, "r", encoding="utf-8") as f:
            self.dati_cloni = json.load(f)

    def _get_chiave_fase(self, eta_anno: int) -> str:
        if eta_anno == 0:
            return 0
        elif eta_anno == 1:
            return 1
        elif 2 <= eta_anno <= 4:  # La fase giovane si ferma a 4 anni per liberare la cartiera a 5
            return "Fase_Crescita_Giovane"
        else:
            return "Fase_Mantenimento_Tardo"

    def prevedi_domanda_stagionale(self, is_esecuzione: bool = False) -> List[Dict[str, Any]]:
        stagione = self.parametri.stagione_corrente
        interventi = []
        
        for lotto in self.parametri.collezione_lotti:
            if not hasattr(lotto, "dati_correnti") or not lotto.dati_correnti:
                profilo = self.dati_cloni[lotto.clone_assegnato]
                lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
            
            # --- FIX 2: PROIEZIONE FUTURA DEL COMPLEANNO ---
            # Se siamo nella fase di pianificazione invernale (UI), la biologia non è ancora scattata.
            # Simuliamo l'età e il diametro che la pianta avrà tra pochi secondi quando premerai Esegui.
            eta_originale = lotto.eta
            diametro_originale = getattr(lotto, "diametro_medio_fusto", 0.0)
            
            if stagione == "Inverno" and not is_esecuzione:
                if (lotto.eta == 0 and lotto.numero_piante_vive > 0) or lotto.numero_piante_vive > 5:
                    eta_futura = lotto.eta + 1
                    profilo = self.dati_cloni[lotto.clone_assegnato]
                    dati_futuri = lotto.simula_accrescimento(profilo, eta_futura)
                    
                    lotto.eta = eta_futura
                    lotto.diametro_medio_fusto = dati_futuri.get("dbh_reale_cm", 0.0)

            is_maturo = lotto.verifica_maturita_raccolta()
            
            # Ripristino immediato dello stato originale per non corrompere la simulazione
            lotto.eta = eta_originale
            lotto.diametro_medio_fusto = diametro_originale
            # ------------------------------------------------
            
            filiera = STRUTTURA_LAVORAZIONI.get(lotto.destinazione_uso, STRUTTURA_LAVORAZIONI["OPERA"])
            
            if is_maturo or getattr(lotto, "tagliato", False):
                ops = filiera["Raccolta"][stagione] if stagione == "Inverno" else []
                is_raccolta = (stagione == "Inverno")
            else:
                chiave_fase = self._get_chiave_fase(lotto.eta)
                ops = filiera.get(chiave_fase, {}).get(stagione, []) if chiave_fase is not None else []
                is_raccolta = False
            
            for op in ops:
                id_univoco = op.get("id_operazione", "OP_GEN")
                descrizione_ui = op.get("descrizione", "Operazione Generica")
                
                macrocategoria = op.get("macrocategoria", "lavorazione_trattore")
                
                # --- FIX: Valutazione disponibilità totale (Proprietà + Nolo) per il preventivo ---
                if is_raccolta: 
                    harvester_noleggiabili = getattr(self.ditta, "limiti_noli_stagionali", {}).get("harvester", 0)
                    harvester_totali_disponibili = self.ditta.harvester_abbattitori + harvester_noleggiabili
                    macrocategoria = "raccolta_avanzata" if harvester_totali_disponibili > 0 else "raccolta_tradizionale"
                
                # Calcolo proporzionale superficie per raccolta
                if is_raccolta:
                    piante_teoriche_max = lotto.superficie_ettari * lotto.densita_iniziale
                    rapporto_sopravvivenza = lotto.dati_correnti.get("piante_attive", 0) / max(1, piante_teoriche_max)
                    unita = lotto.superficie_ettari * rapporto_sopravvivenza
                else:
                    unita = lotto.superficie_ettari
                
                ore_unitarie = op.get("ore_ha", 1.0)
                squadra = op.get("risorse", {})
                
                spec = self.ditta.calcola_specifiche_richiesta_cantiere(
                    tipo_cantiere=macrocategoria, 
                    unita_lavoro=unita, 
                    ore_unitarie=ore_unitarie,
                    composizione_squadra=squadra,
                    indice_attrito=getattr(lotto, "indice_attrito_spaziale", 0)
                )
                
                if spec:
                    interventi.append({
                        "lotto": lotto, 
                        "id_operazione": id_univoco,
                        "operazione": descrizione_ui,
                        "priorita": op.get("priorita", 4), 
                        "tipo_cantiere_chiave": macrocategoria, 
                        "specifiche_richiesta": spec, 
                        "is_raccolta": is_raccolta
                    })
        
        return sorted(interventi, key=lambda x: x["priorita"])

    def ottieni_previsione_impatto_stagione(self) -> Dict[str, float]:
        giorni_utili = 55
        ore_uomo_base = ((self.ditta.operai_grado_A + self.ditta.operai_grado_B) * 8 * giorni_utili) * self.ditta.coefficiente_iufro
        
        lista_interventi = self.prevedi_domanda_stagionale()
        domanda_ore_totali = sum(
            intervento.get("specifiche_richiesta", {}).get("grado_A", 0.0) + 
            intervento.get("specifiche_richiesta", {}).get("grado_B", 0.0)
            for intervento in lista_interventi
        )

        ore_extra_necessarie = max(0.0, domanda_ore_totali - ore_uomo_base)
        ore_interne_utilizzate = min(ore_uomo_base, domanda_ore_totali)

        return {
            "capacita_stabile_disponibile": round(ore_uomo_base, 2),
            "ore_interne_impegnate": round(ore_interne_utilizzate, 2),
            "ore_extra_da_noleggiare": round(ore_extra_necessarie, 2)
        }

    def esegui_fase_lavorazioni_stagionali(self) -> Dict[str, Any]:
        stagione_attiva = self.parametri.stagione_corrente
        giorni_utili_stagione = 55 
        self.ditta.inizializza_serbatoi_stagionali(giorni_utili_stagione)
        
        # Snapshot di inizio stagione per calcolo B.I. differenziale
        serbatoi_iniziali = self.ditta.serbatoi_ore.copy()
        extra_iniziali = self.ditta.registro_extra_anno.copy()
        
        report_stagionale = {
            "dettaglio_operazioni": [], 
            "tagli_effettuati": []
        }
    
        lista_interventi_richiesti = self.prevedi_domanda_stagionale(is_esecuzione=True)
    
        for intervento in lista_interventi_richiesti:
            lotto_target = intervento["lotto"]
            spec = intervento["specifiche_richiesta"]
            tipo_cantiere_chiave = intervento["tipo_cantiere_chiave"]
            
            if not hasattr(lotto_target, "malus_colturale_accumulato"): lotto_target.malus_colturale_accumulato = 0.0
            if not hasattr(lotto_target, "anni_ritardo_taglio"): lotto_target.anni_ritardo_taglio = 0
            if not hasattr(lotto_target, "dati_correnti") or not lotto_target.dati_correnti:
                profilo = self.dati_cloni[lotto_target.clone_assegnato]
                lotto_target.dati_correnti = lotto_target.simula_accrescimento(profilo, lotto_target.eta)
    
            percentuale_completamento = self.ditta.verifica_e_consuma_risorse(spec)
    
            if not intervento["is_raccolta"]:
                if percentuale_completamento >= 0.99:
                    stato_execution = "Eseguito"
                    if "impianto" in tipo_cantiere_chiave or "astoni" in intervento["operazione"].lower():
                        lotto_target.immissione_effettuata = True
                    
                    if tipo_cantiere_chiave == "impianto" and lotto_target.numero_piante_vive == 0:
                        lotto_target.numero_piante_vive = int(lotto_target.superficie_ettari * lotto_target.densita_iniziale)
                        lotto_target.dati_correnti["piante_attive"] = lotto_target.numero_piante_vive
                        
                elif percentuale_completamento > 0.0:
                    self.stats_globali["lavorazioni_generiche_saltate"] += 1
                    stato_execution = f"Eseguito Parziale ({int(percentuale_completamento * 100)}%)"
                    lotto_target.registra_fallimento_intervento(intervento["operazione"], stagione_attiva, self.parametri.anno_corrente)
                else:
                    self.stats_globali["lavorazioni_generiche_saltate"] += 1
                    stato_execution = "Bloccato (Risorse Insufficienti)"
                    lotto_target.registra_fallimento_intervento(intervento["operazione"], stagione_attiva, self.parametri.anno_corrente)
                    sensibilita = self.dati_cloni[lotto_target.clone_assegnato]["esigenze_trattamenti"]["sensibilita_marsonina"]
                    if intervento["priorita"] == 2:
                        mult_danno = 1.3 if sensibilita == "Alta" else (0.5 if "bassa" in sensibilita.lower() else 1.0)
                        lotto_target.malus_colturale_accumulato += (0.08 * mult_danno)
                    elif intervento["priorita"] == 3: lotto_target.malus_colturale_accumulato += 0.05
                    elif intervento["priorita"] == 4: lotto_target.malus_colturale_accumulato += 0.03

                ore_lavoro_puro_cantiere = spec.get("meta_lavoro_puro", 0.0) / self.ditta.coefficiente_rendimento_cantiere

                report_stagionale["dettaglio_operazioni"].append({
                    "lotto_id": lotto_target.id_lotto, 
                    "id_operazione": intervento["id_operazione"],
                    "priorita": intervento["priorita"], 
                    "durata_cantiere_h": round(spec.get("ore_richieste", 0.0), 2),
                    "ore_lavoro_totali": round(ore_lavoro_puro_cantiere, 2),
                    "squadre_attive": spec.get("meta_linee_attive", 1),
                    "stato": stato_execution
                })

            else:
                piante_totali = lotto_target.dati_correnti["piante_attive"]
                p_abbattute = int(piante_totali * percentuale_completamento) if percentuale_completamento < 0.98 else piante_totali
                
                if p_abbattute > 0:
                    rese = lotto_target.calcola_ripartizione_assortimenti(self.dati_cloni[lotto_target.clone_assegnato], p_abbattute)
                    self.parametri.totale_prodotto_opera_m3 += rese["opera_m3"]
                    self.parametri.totale_prodotto_cartiera_t += rese["cartiera_t"]
                    self.parametri.totale_prodotto_truciolato_t += rese["truciolato_t"]
        
                    lotto_target.numero_piante_vive = max(0, lotto_target.numero_piante_vive - p_abbattute)
                    lotto_target.dati_correnti["piante_attive"] = lotto_target.numero_piante_vive
                    
                    report_stagionale["tagli_effettuati"].append({
                        "lotto_id": lotto_target.id_lotto, 
                        "volume_raccolto_m3": round(lotto_target.dati_correnti.get("volume_singolo_m3", 0.0) * p_abbattute, 2), 
                        "rese": rese
                    })

                if lotto_target.numero_piante_vive <= 5 or p_abbattute >= piante_totali:
                    lotto_target.inizializza_nuovo_ciclo()
                    lotto_target.numero_piante_vive = 0 
                    lotto_target.tagliato = False
                    lotto_target.eta = 0 
                    
                    lotto_target.anni_ritardo_taglio = 0
                    lotto_target.malus_colturale_accumulato = 0.0
                    if hasattr(lotto_target, "cronistoria_lavorazioni_saltate"):
                        lotto_target.cronistoria_lavorazioni_saltate.clear()
                    if hasattr(lotto_target, "archivio_storico_lavorazioni_saltate"):
                        lotto_target.archivio_storico_lavorazioni_saltate.clear()
                    
                    lotto_target.dati_correnti = {
                        "dbh_reale_cm": 0.0, "altezza_m": 0.0, 
                        "volume_singolo_m3": 0.0, "piante_attive": 0, "volume_totale_m3": 0.0
                    }
                    stato_execution = "Eseguito (Taglio Completato - Reset Ciclo)"
                else:
                    self.stats_globali["tagli_strutturali_saltati"] += 1
                    if p_abbattute > 0: lotto_target.tagliato = True
                    lotto_target.anni_ritardo_taglio += 1
                    stato_execution = f"Eseguito Parziale (In piedi {lotto_target.numero_piante_vive} piante)"

                ore_lavoro_puro_cantiere = spec.get("meta_lavoro_puro", 0.0) / self.ditta.coefficiente_rendimento_cantiere

                report_stagionale["dettaglio_operazioni"].append({
                    "lotto_id": lotto_target.id_lotto, 
                    "id_operazione": intervento["id_operazione"], 
                    "durata_cantiere_h": round(spec.get("ore_richieste", 0.0), 2),
                    "ore_lavoro_totali": round(ore_lavoro_puro_cantiere, 2),
                    "squadre_attive": spec.get("meta_linee_attive", 1),
                    "stato": stato_execution
                })
    
        report_stagionale["risorse_umane_interne"] = {
            "disponibili_iniziali_A": round(serbatoi_iniziali.get("grado_A", 0.0), 2),
            "disponibili_iniziali_B": round(serbatoi_iniziali.get("grado_B", 0.0), 2),
            "consumate_A": round(serbatoi_iniziali.get("grado_A", 0.0) - self.ditta.serbatoi_ore.get("grado_A", 0.0), 2),
            "consumate_B": round(serbatoi_iniziali.get("grado_B", 0.0) - self.ditta.serbatoi_ore.get("grado_B", 0.0), 2)
        }

        report_stagionale["macchinari_interni_consumati"] = {
            "harvester": round(serbatoi_iniziali.get("harvester", 0.0) - self.ditta.serbatoi_ore.get("harvester", 0.0), 2),
            "forwarder": round(serbatoi_iniziali.get("forwarder", 0.0) - self.ditta.serbatoi_ore.get("forwarder", 0.0), 2),
            "trattori_alta": round(serbatoi_iniziali.get("trattori_alta", 0.0) - self.ditta.serbatoi_ore.get("trattori_alta", 0.0), 2),
            "trattori_media": round(serbatoi_iniziali.get("trattori_media", 0.0) - self.ditta.serbatoi_ore.get("trattori_media", 0.0), 2),
            "piattaforme": round(serbatoi_iniziali.get("piattaforme", 0.0) - self.ditta.serbatoi_ore.get("piattaforme", 0.0), 2)
        }

        report_stagionale["ricorso_terzi_e_noli"] = {
            chiave: round(self.ditta.registro_extra_anno.get(chiave, 0.0) - extra_iniziali.get(chiave, 0.0), 2)
            for chiave in ["grado_A", "grado_B", "trattori_alta", "trattori_media", "harvester", "forwarder", "piattaforme"]
        }

        return report_stagionale
        
    def avanza_passo_simulazione(self) -> Dict[str, Any]:
        
        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                profilo = self.dati_cloni[lotto.clone_assegnato]
                
                if lotto.eta == 0 and lotto.numero_piante_vive > 0:
                    lotto.eta = 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                elif lotto.numero_piante_vive > 5: 
                    lotto.eta += 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                
                lotto.diametro_medio_fusto = lotto.dati_correnti.get("dbh_reale_cm", 0.0)
                lotto.altezza_media_piante = lotto.dati_correnti.get("altezza_m", 0.0)
                if "piante_attive" in lotto.dati_correnti:
                    lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
                lotto.malus_colturale_accumulato = 0.0

        risultati_cantieri = self.esegui_fase_lavorazioni_stagionali()

        stato_lotti_istantaneo = {}
        for lotto in self.parametri.collezione_lotti:
            stato_lotti_istantaneo[lotto.id_lotto] = {
                "eta": lotto.eta, 
                "tagliato": lotto.tagliato,
                "biometria": lotto.dati_correnti.copy() if hasattr(lotto, "dati_correnti") and lotto.dati_correnti else {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, "volume_singolo_m3": 0.0, 
                    "piante_attive": lotto.numero_piante_vive, "volume_totale_m3": 0.0
                }
            }

        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                if lotto.eta > 0:
                    profilo = self.dati_cloni[lotto.clone_assegnato]
                    eta_rot = 5 if lotto.destinazione_uso == "INDUSTRIA" else 10
                    
                    if lotto.eta >= eta_rot and not lotto.verifica_maturita_raccolta():
                        self.stats_globali["tagli_biologici_saltati"] += 1
                        lotto.anni_ritardo_taglio = getattr(lotto, "anni_ritardo_taglio", 0) + 1

            chiave_anno_storico = f"Anno_{self.parametri.anno_corrente}_RisorseExtra"
            if hasattr(self.parametri, "storico_stagionale"):
                self.parametri.storico_stagionale[chiave_anno_storico] = self.ditta.registro_extra_anno.copy()
            for risorsa in self.ditta.registro_extra_anno:
                self.ditta.registro_extra_anno[risorsa] = 0.0

        quadro_stato = {
            "risultati_cantieri": risultati_cantieri,
            "stato_lotti": stato_lotti_istantaneo,  
            "produzione_cumulata": {
                "opera_m3": getattr(self.parametri, "totale_prodotto_opera_m3", 0.0),
                "cartiera_t": getattr(self.parametri, "totale_prodotto_cartiera_t", 0.0),
                "truciolato_t": getattr(self.parametri, "totale_prodotto_truciolato_t", 0.0)
            }
        }
        
        if hasattr(self.parametri, "registra_instantanea_stato_corrente"):
            self.parametri.registra_instantanea_stato_corrente(quadro_stato)
        
        dati_orologio = self.parametri.avanza_stagione()
        return {**dati_orologio, **quadro_stato}