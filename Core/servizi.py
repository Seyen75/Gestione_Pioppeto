# Core/servizi.py

class ServizioSelvicolturale:
    
    @staticmethod
    def calcola_densita_iniziale(sesto_impianto: str) -> int:
        """Calcola la densità di piante per ettaro dato un sesto (es: '6x6')."""
        try:
            lati = [float(x) for x in sesto_impianto.split("x")]
            return int(10000 / (lati[0] * lati[1]))
        except (ValueError, ZeroDivisionError, IndexError):
            return 0

    @staticmethod
    def ottieni_messaggio_coerenza(clone_nome: str, destinazione: str, dati_clone: dict) -> dict:
        """
        Analizza la coerenza tra clone e destinazione.
        Restituisce un dizionario con 'testo' e 'stile' CSS.
        """
        attitudine_reale = dati_clone.get("attitudini", "OPERA").upper()
        destinazione_scelta = destinazione.upper().strip()

        # Definizioni filiere
        filiere_industriali = ["OPERA", "INDUSTRIA", "DUAL"]
        
        # Logica di compatibilità
        is_ottimale = False
        if attitudine_reale == "DUAL":
            is_ottimale = True
        elif attitudine_reale == destinazione_scelta:
            is_ottimale = True
        elif attitudine_reale in filiere_industriali and destinazione_scelta in filiere_industriali:
            # Questa condizione copre il caso in cui entrambi sono validi anche se non identici
            is_ottimale = True

        # Costruzione del messaggio
        if is_ottimale:
            if attitudine_reale == "DUAL":
                testo = f"✅ Abbinamento Ottimale: Il clone {clone_nome} è 'DUAL', flessibilità garantita per la filiera {destinazione_scelta}."
            else:
                testo = f"✅ Abbinamento Ottimale: Il clone {clone_nome} esprime il massimo potenziale per la filiera {destinazione_scelta}."
            
            return {
                "testo": testo,
                "stile": "color: #4CAF50; font-weight: bold; font-style: italic;"
            }
        
        else:
            if destinazione_scelta == "OPERA":
                testo = f"⚠️ Rischio Colturale: Il clone {clone_nome} è da {attitudine_reale}. Produrrà nodi diffusi inficiando la resa in sfoglia."
            else:
                testo = f"⚠️ Eccesso Qualitativo: Il clone {clone_nome} è per compensati di pregio (OPERA). Destinarlo a triturazione abbatte i margini."
            
            return {
                "testo": testo,
                "stile": "color: #FF9800; font-weight: bold; font-style: italic;"
            }
            