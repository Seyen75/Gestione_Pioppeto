
# =====================================================================
# CATALOGO UNIVOCO DELLE OPERAZIONI AGRONOMICHE E FORESTALI
# =====================================================================

# --- PREPARAZIONE TERRENO E IMPIANTO ---

OP_CEP_01 = {"id_operazione": "OP_CEP_01", "descrizione": "Triturazione ceppaie e ripristino post-raccolta", 
             "macrocategoria": "preparazione_terreno", "priorita": 1, "ore_ha": 10.0, "risorse": {"trattori_alta": 1.0, "grado_A": 1.0}}
OP_SCA_01 = {"id_operazione": "OP_SCA_01", "descrizione": "Preparazione terreno e Scasso localizzato", 
             "macrocategoria": "preparazione_terreno", "priorita": 2, "ore_ha": 8.0, "risorse": {"trattori_alta": 1.0, "grado_A": 1.0}}
OP_ERP_01 = {"id_operazione": "OP_ERP_01", "descrizione": "Erpicatura profonda pre-impianto", "macrocategoria": "preparazione_terreno", 
             "priorita": 3, "ore_ha": 4.0, "risorse": {"trattori_alta": 1.0, "grado_A": 1.0}}

OP_IMP_01 = {"id_operazione": "OP_IMP_01", "descrizione": "Messa a dimora astoni/pioppelle", 
             "macrocategoria": "impianto", "priorita": 4, "ore_ha": 18.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0, "grado_B": 2.0}}
OP_IMP_02 = {"id_operazione": "OP_IMP_02", "descrizione": "Immissione nuovi astoni (Rimpiazzo fallanze)", 
             "macrocategoria": "impianto", "priorita": 4, "ore_ha": 3.0, "risorse": {"grado_B": 2.0}}

# --- LAVORAZIONI AL TRATTORE E MANUTENZIONE ---

OP_IRR_01 = {"id_operazione": "OP_IRR_01", "descrizione": "Irrigazione di soccorso giovanile", 
             "macrocategoria": "lavorazione_trattore", "priorita": 1, "ore_ha": 6.0, "risorse": {"trattori_media": 1.0, "grado_B": 1.0}}
OP_IRR_02 = {"id_operazione": "OP_IRR_02", "descrizione": "Irrigazione di soccorso standard", 
             "macrocategoria": "lavorazione_trattore", "priorita": 1, "ore_ha": 5.0, "risorse": {"trattori_media": 1.0, "grado_B": 1.0}}

OP_INF_01 = {"id_operazione": "OP_INF_01", "descrizione": "Controllo Infestanti Meccanico Interfilare", 
             "macrocategoria": "lavorazione_trattore", "priorita": 3, "ore_ha": 3.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_INF_02 = {"id_operazione": "OP_INF_02", "descrizione": "Ripulitura erbe infestanti", 
             "macrocategoria": "lavorazione_trattore", "priorita": 3, "ore_ha": 3.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRI_01 = {"id_operazione": "OP_TRI_01", "descrizione": "Trinciatura stocchi interfilare", 
             "macrocategoria": "lavorazione_trattore", "priorita": 4, "ore_ha": 2.5, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRI_02 = {"id_operazione": "OP_TRI_02", "descrizione": "Trinciatura e controllo sottobosco", 
             "macrocategoria": "lavorazione_trattore", "priorita": 4, "ore_ha": 2.5, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}

# --- TRATTAMENTI E ISPEZIONI ---

OP_TRA_01 = {"id_operazione": "OP_TRA_01", "descrizione": "Trattamento Antiparassitario fogliare", 
             "macrocategoria": "lavorazione_trattore", "priorita": 2, "ore_ha": 2.5, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRA_02 = {"id_operazione": "OP_TRA_02", "descrizione": "Trattamento rameico preventivo", 
             "macrocategoria": "lavorazione_trattore", "priorita": 2, "ore_ha": 2.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRA_03 = {"id_operazione": "OP_TRA_03", "descrizione": "Trattamento fitosanitario della chioma", 
             "macrocategoria": "lavorazione_trattore", "priorita": 2, "ore_ha": 2.5, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRA_04 = {"id_operazione": "OP_TRA_04", "descrizione": "Trattamento antifungino protettivo/fusto", 
             "macrocategoria": "lavorazione_trattore", "priorita": 2, "ore_ha": 2.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_TRA_05 = {"id_operazione": "OP_TRA_05", "descrizione": "Trattamento fitosanitario chioma adulta", 
             "macrocategoria": "lavorazione_trattore", "priorita": 2, "ore_ha": 3.0, "risorse": {"trattori_media": 1.0, "grado_A": 1.0}}
OP_MON_01 = {"id_operazione": "OP_MON_01", "descrizione": "Monitoraggio fitosanitario pre-raccolta", 
             "macrocategoria": "ispezione", "priorita": 2, "ore_ha": 1.5, "risorse": {"grado_A": 1.0}} 

# --- POTATURE (Manuali e Piattaforme) ---

OP_POT_01 = {"id_operazione": "OP_POT_01", "descrizione": "Spollonatura e prima potatura aste", 
             "macrocategoria": "potatura", "priorita": 3, "ore_ha": 10.0, "risorse": {"grado_B": 1.0}}
OP_POT_02 = {"id_operazione": "OP_POT_02", "descrizione": "Potatura di elevazione in quota (Nodi)", 
             "macrocategoria": "potatura", "priorita": 2, "ore_ha": 12.0, "risorse": {"piattaforme": 1.0, "grado_A": 1.0, "grado_B": 1.0}}
OP_POT_03 = {"id_operazione": "OP_POT_03", "descrizione": "Mondatura rami danneggiati post-eventi meteo", 
             "macrocategoria": "potatura", "priorita": 3, "ore_ha": 3.5, "risorse": {"piattaforme": 1.0, "grado_A": 1.0, "grado_B": 1.0}}

# --- RACCOLTA, ABBATTIMENTO E RECUPERO SCARTI ---

OP_RAC_01 = {"id_operazione": "OP_RAC_01", "descrizione": "Abbattimento ed esbosco avanzato Opera", 
             "macrocategoria": "raccolta", "priorita": 1, "ore_ha": 12.0, "risorse": {"grado_A": 2.0, "harvester": 1.0, "forwarder": 1.0}}
OP_RAC_02 = {"id_operazione": "OP_RAC_02", "descrizione": "Abbattimento e cippatura meccanizzata Cartiera", 
             "macrocategoria": "raccolta", "priorita": 1, "ore_ha": 9.0, "risorse": {"grado_A": 2.0, "harvester": 1.0, "forwarder": 1.0}}
OP_RAC_03 = {"id_operazione": "OP_RAC_03", "descrizione": "Abbattimento tradizionale (Motosega)", 
             "macrocategoria": "raccolta_tradizionale", "priorita": 1, "ore_ha": 30.0, "risorse": {"grado_A": 3.0, "trattori_media": 1.0}}
OP_CIP_01 = {"id_operazione": "OP_CIP_01", "descrizione": "Cippatura legname di scarto e ramaglie", 
             "macrocategoria": "recupero_biomassa", "priorita": 2, "ore_ha": 7.0, "risorse": {"cippatrice": 1.0, "grado_B": 1.0}}

# =========================================================
# CALENDARIO STRUTTURALE DELLE LAVORAZIONI
# =========================================================

STRUTTURA_LAVORAZIONI = {
    "OPERA": {
        "0": {
            "Inverno": [OP_CEP_01],
            "Primavera": [OP_SCA_01, OP_ERP_01, OP_IMP_01],
            "Estate": [OP_IRR_01],
            "Autunno": [OP_INF_01]
        },
        "1": {
            "Inverno": [OP_POT_01, OP_IMP_02],
            "Primavera": [OP_TRA_01, OP_INF_02],
            "Estate": [OP_IRR_02],
            "Autunno": [OP_TRA_02]
        },
        "Fase_Crescita_Giovane": { 
            "Inverno": [OP_POT_02],
            "Primavera": [OP_TRA_03, OP_POT_03],
            "Estate": [OP_TRI_01],
            "Autunno": [OP_TRA_04]
        },
        "Fase_Mantenimento_Tardo": { 
            "Inverno": [],
            "Primavera": [OP_TRA_05],
            "Estate": [OP_TRI_02],
            "Autunno": []
        },
        "Raccolta": {
            "Inverno": [OP_RAC_01, OP_CIP_01],
            "Primavera": [], "Estate": [], "Autunno": []
        },
        "Raccolta_tradizionale": {
            "Inverno": [OP_RAC_03, OP_CIP_01],
            "Primavera": [], "Estate": [], "Autunno": []
        }
    },
    "INDUSTRIA": {
        "0": {
            "Inverno": [OP_CEP_01],
            "Primavera": [OP_SCA_01, OP_ERP_01, OP_IMP_01],
            "Estate": [OP_IRR_01],
            "Autunno": [OP_INF_01]
        },
        "1": {
            "Inverno": [OP_IMP_02],
            "Primavera": [OP_TRA_01, OP_INF_02],
            "Estate": [OP_IRR_02],
            "Autunno": [OP_TRA_02]
        },
        "Fase_Crescita_Giovane": { 
            "Inverno": [], 
            "Primavera": [OP_TRA_03],
            "Estate": [OP_TRI_01],
            "Autunno": [OP_TRA_04]
        },
        "Fase_Mantenimento_Tardo": { 
            "Inverno": [],
            "Primavera": [OP_MON_01, OP_POT_03],
            "Estate": [OP_TRI_02],
            "Autunno": []
        },
        "Raccolta": {
            "Inverno": [OP_RAC_02], # Qui la cippatura è già integrata nell'Harvester
            "Primavera": [], "Estate": [], "Autunno": []
        },
        "Raccolta_tradizionale": {
            "Inverno": [OP_RAC_03, OP_CIP_01],
            "Primavera": [], "Estate": [], "Autunno": []
        }
    }
}