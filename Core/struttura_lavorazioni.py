
STRUTTURA_LAVORAZIONI = {
    # -------------------------------------------------------------
    # ANNO 0: PREPARAZIONE ED IMPIANTO
    # -------------------------------------------------------------
    0: {
        "Inverno": [
            {
                "operazione": "Messa a dimora astoni (Impianto meccanizzato)",
                "priorita": 1,
                "ore_ha": 25.0,
                "risorse": {"trattori_media": 1.0, "ore_grado_B": 2.0}
            }
        ],
        "Primavera": [
            {
                "operazione": "Controllo Infestanti Meccanico Interfilare",
                "priorita": 3,
                "ore_ha": 4.0,
                "risorse": {"trattori_media": 1.0, "attrezzature_agricole": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Estate": [
            {
                "operazione": "Irrigazione di soccorso giovanile",
                "priorita": 1,
                "ore_ha": 8.0,
                "risorse": {"cura": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Autunno": [
            {
                "operazione": "Scasso e Ripuntatura profonda preliminare",
                "priorita": 1, # Massima priorità per preparare il suolo asciutto
                "ore_ha": 12.0,
                "risorse": {"trattori_alta": 1.0, "attrezzature_agricole": 1.0, "ore_grado_A": 1.0}
            }
        ]
    },

    # -------------------------------------------------------------
    # ANNO 1: ATTECCHIMENTO
    # -------------------------------------------------------------
    1: {
        "Inverno": [
            {
                "operazione": "Spollonatura e prima potatura aste",
                "priorita": 3,
                "ore_ha": 10.0,
                "risorse": {"ore_grado_B": 1.0}
            }
        ],
        "Primavera": [
            {
                "operazione": "Trattamento Antiparassitario fogliare",
                "priorita": 2,
                "ore_ha": 5.0,
                "risorse": {"trattori_media": 1.0, "cura": 1.0, "ore_grado_B": 1.0}
            },
            {
                "operazione": "Ripulitura erbe infestanti",
                "priorita": 3,
                "ore_ha": 4.0,
                "risorse": {"trattori_media": 1.0, "attrezzature_agricole": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Estate": [
            {
                "operazione": "Irrigazione di soccorso",
                "priorita": 1,
                "ore_ha": 6.0,
                "risorse": {"cura": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Autunno": [
            {
                "operazione": "Trattamento rameico al tronco (Prevenzione Cancri)",
                "priorita": 2,
                "ore_ha": 4.0,
                "risorse": {"trattori_media": 1.0, "cura": 1.0, "ore_grado_B": 1.0}
            }
        ]
    },

    # -------------------------------------------------------------
    # ANNI DA 2 A 5: ACCRESCIMENTO GIOVANE
    # -------------------------------------------------------------
    "Fase_Crescita_Giovane": {
        "Inverno": [
            {
                "operazione": "Potatura di elevazione in quota (Nodi)",
                "priorita": 2,
                "ore_ha": 15.0,
                "risorse": {"piattaforme": 1.0, "ore_grado_A": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Primavera": [
            {
                "operazione": "Trattamento fitosanitario della chioma",
                "priorita": 2,
                "ore_ha": 6.0,
                "risorse": {"trattori_media": 1.0, "cura": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Estate": [
            {
                "operazione": "Trinciatura stocchi interfilare",
                "priorita": 4,
                "ore_ha": 3.0,
                "risorse": {"trattori_media": 1.0, "attrezzature_agricole": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Autunno": [
            {
                "operazione": "Trattamento antifungino protettivo del fusto",
                "priorita": 2,
                "ore_ha": 5.0, # Leggermente più lungo per fusti più grandi rispetto all'anno 1
                "risorse": {"trattori_media": 1.0, "cura": 1.0, "ore_grado_B": 1.0}
            }
        ]
    },

    # -------------------------------------------------------------
    # ANNI DA 6 AL TAGLIO (MANUTENZIONE TARDA)
    # -------------------------------------------------------------
    "Fase_Mantenimento_Tardo": {
        "Inverno": [],
        "Primavera": [
            {
                "operazione": "Trattamento fitosanitario chioma adulta",
                "priorita": 2,
                "ore_ha": 7.0,
                "risorse": {"trattori_media": 1.0, "cura": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Estate": [
            {
                "operazione": "Trinciatura e controllo vegetazione sottobosco",
                "priorita": 4,
                "ore_ha": 3.0,
                "risorse": {"trattori_media": 1.0, "attrezzature_agricole": 1.0, "ore_grado_B": 1.0}
            }
        ],
        "Autunno": [] # Sulle piante adulte la corteccia è spessa e suberificata, non serve il trattamento
    },

    # -------------------------------------------------------------
    # CANTIERE DI RACCOLTA FINALE
    # -------------------------------------------------------------
    "Raccolta": {
        "Inverno": [
            {
                "operazione": "Abbattimento, sramatura ed esbosco (Taglio)",
                "priorita": 1,
                "ore_ha": 40.0,
                "risorse": {"forestali_taglio": 2.0, "ore_grado_A": 2.0}
            }
        ],
        "Primavera": [],
        "Estate": [],
        "Autunno": []
    }
}