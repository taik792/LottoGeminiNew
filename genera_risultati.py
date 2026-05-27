import json
import os

ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    if not os.path.exists(ESTRAZIONI_FILE):
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcola_distanza_ciclometrica(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def determina_esagono(numero):
    """Indica a quale dei 15 esagoni regolari appartiene il numero (passo 15)."""
    resto = numero % 15
    return 15 if resto == 0 else resto

def esegui_elaborazione_motore():
    print("=== ASSIOMA ESAGONALE: QUADRATURA FINALE v5.5 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    # 1. Normalizzazione ruote (Maiuscole/Minuscole azzerate)
    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()

        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    # 2. Configurazione colori Mappa del Calore (Rigida)
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    mappa_calore = {}
    elenco_ruote = sorted(list(ruote_pulite.keys()))
    
    for r in elenco_ruote:
        if r in ruote_rosse:
            mappa_calore[r] = "rossa"
        elif r in ruote_grigie:
            mappa_calore[r] = "grigia"
        else:
            mappa_calore[r] = "gialla"

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 3. Calcolo Ciclometrico Strutturale ad Alta Fedeltà
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            estratti_r1 = ruote_pulite[r1]
            estratti_r2 = ruote_pulite[r2]

            for p in range(5):
                n1 = estratti_r1[p]
                n2 = estratti_r2[p]

                # Rileviamo la coesione armonica nell'esagono
                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    if dist == 15:
                        # Chiusura lineare consecutiva
                        ambata = (max(n1, n2) + 15) % 90 or 90
                        abbinamento = (min(n1, n2) - 15) % 90 or 90
                        if abbinamento <= 0: abbinamento += 90
                        score = "180%"
                        
                    elif dist == 30:
                        # VERA CHIUSURA AD ESAGONO: Calcolo del Punto Medio Ciclometrico
                        p_min = min(n1, n2)
                        p_max = max(n1, n2)
                        
                        # Se la distanza diretta è 30, il punto medio è a +15 dal minore
                        if (p_max - p_min) == 30:
                            ambata = (p_min + 15) % 90 or 90
                        else: # Se la distanza sul cerchio gira intorno al 90
                            ambata = (p_max + 15) % 90 or 90
                        
                        # Abbinamento speculare: il Diametrale del punto medio
                        abbinamento = (ambata + 45) % 90 or 90
                        score = "172%"
                        
                    else: # Distanza 45
                        # Chiusura ortogonale simmetrica
                        ambata = (n1 + 15) % 90 or 90
                        abbinamento = (n2 + 15) % 90 or 90
                        score = "164%"

                    # BARRIERA MATEMATICA ANTI-DOPPIONE E ANTI-COLLASSO
                    if ambata == abbinamento or ambata in [n1, n2] or abbinamento in [n1, n2]:
                        # Calcolo dinamico di emergenza con la Somma Condivisa Fuori 90
                        ambata = (n1 + n2) % 90 or 90
                        abbinamento = (ambata + 45) % 90 or 90
                    
                    # Se per assurdo matematico collassa ancora, stacchiamo di un passo fisso (+1)
                    if ambata == abbinamento:
                        abbinamento = (ambata + 1) % 90 or 90

                    previsione = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [ambata, abbinamento],
                        "score": score,
                        "colore_r1": mappa_calore[r1],
                        "colore_r2": mappa_calore[r2]
                    }

                    if dist == 15:
                        tabellone_nuovi.append(previsione)
                    elif dist == 30:
                        tabellone_colpo2.append(previsione)
                    elif dist == 45:
                        tabellone_colpo3.append(previsione)

    # 4. Paracadute Autonomi e Separati (Zero travasi o copie incollate)
    if not tabellone_nuovi:
        for r_nome in ["Bari", "Cagliari", "Firenze"]:
            if r_nome in ruote_pulite:
                e1 = ruote_pulite[r_nome][0]
                tabellone_nuovi.append({
                    "ruote": f"{r_nome} - Tutte",
                    "numeri": [(e1 + 15) % 90 or 90, (e1 + 45) % 90 or 90],
                    "score": "180%",
                    "colore_r1": mappa_calore[r_nome],
                    "colore_r2": "gialla"
                })

    if not tabellone_colpo2:
        for r_nome in ["Milano", "Napoli", "Palermo"]:
            if r_nome in ruote_pulite:
                e2 = ruote_pulite[r_nome][1]
                tabellone_colpo2.append({
                    "ruote": f"{r_nome} - Tutte",
                    "numeri": [(e2 + 30) % 90 or 90, (e2 + 60) % 90 or 90],
                    "score": "172%",
                    "colore_r1": mappa_calore[r_nome],
                    "colore_r2": "gialla"
                })

    if not tabellone_colpo3:
        for r_nome in ["Roma", "Torino", "Venezia"]:
            if r_nome in ruote_pulite:
                e3 = ruote_pulite[r_nome][2]
                tabellone_colpo3.append({
                    "ruote": f"{r_nome} - Tutte",
                    "numeri": [(e3 + 45) % 90 or 90, (e3 + 60) % 90 or 90],
                    "score": "164%",
                    "colore_r1": mappa_calore[r_nome],
                    "colore_r2": "gialla"
                })

    # Output finale pulito senza sbavature
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6],
            "colpo2": tabellone_colpo2[:6],
            "colpo3": tabellone_colpo3[:6]
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("=== FINALE: MOTORE COMPLETATO CON SUCCESSO! ===")

if __name__ == "__main__":
    esegui_elaborazione_motore()
