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

def aggrega_previsioni(lista_previsioni, score_base):
    """Fonde le previsioni con gli stessi numeri unendo le ruote ed eliminando i duplicati."""
    aggregato = {}
    for prev in lista_previsioni:
        # Ordina la coppia per identificare i duplicati speculari (es. 38-83 e 83-38)
        coppia_chiave = tuple(sorted(prev["numeri"]))
        ruote_correnti = [r.strip() for r in prev["ruote"].split("-")]
        
        if coppia_chiave not in aggregato:
            aggregato[coppia_chiave] = {
                "ruote_set": set(ruote_correnti),
                "numeri": list(coppia_chiave),
                "presenze": 1
            }
        else:
            aggregato[coppia_chiave]["ruote_set"].update(ruote_correnti)
            aggregato[coppia_chiave]["presenze"] += 1

    # Trasforma il dizionario aggregato nel formato finale per il JSON
    risultato_fuso = []
    for info in aggregato.values():
        lista_ruote_ordinate = sorted(list(info["ruote_set"]))
        stringa_ruote = " - ".join(lista_ruote_ordinate)
        
        # Calcolo del Peso Strutturale Dinamico in base alle convergenze reali
        valore_base = int(score_base.replace("%", ""))
        bonus_convergenza = (info["presenze"] - 1) * 2
        score_dinamico = f"{min(valore_base + bonus_convergenza, 185)}%"

        risultato_fuso.append({
            "ruote": stringa_ruote,
            "numeri": info["numeri"],
            "score": score_dinamico,
            "colore_r1": "rossa" if any(x in ["Palermo", "Roma", "Torino"] for x in lista_ruote_ordinate) else "gialla",
            "colore_r2": "grigia" if "Milano" in lista_ruote_ordinate else "gialla"
        })
        
    # Ordina per numero di presenze/convergenze (le più frequenti in alto)
    return sorted(risultato_fuso, key=lambda x: int(x["score"].replace("%", "")), reverse=True)

def esegui_elaborazione_motore():
    print("=== ASSIOMA ESAGONALE: COMPATTAZIONE CONVERGENZE v6.0 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    # 1. Normalizzazione ruote
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

    grezzo_nuovi = []
    grezzo_colpo2 = []

    # 3. Calcolo Ciclometrico Strutturale
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            estratti_r1 = ruote_pulite[r1]
            estratti_r2 = ruote_pulite[r2]

            for p in range(5):
                n1 = estratti_r1[p]
                n2 = estratti_r2[p]

                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    if dist == 15:
                        ambata = (max(n1, n2) + 15) % 90 or 90
                        abbinamento = (min(n1, n2) - 15) % 90 or 90
                        if abbinamento <= 0: abbinamento += 90
                        
                    elif dist == 30:
                        p_min = min(n1, n2)
                        p_max = max(n1, n2)
                        
                        if (p_max - p_min) == 30:
                            ambata = (p_min + 15) % 90 or 90
                        else:
                            ambata = (p_max + 15) % 90 or 90
                        
                        abbinamento = (ambata + 45) % 90 or 90
                    else:
                        continue # Salta distanza 45 (Ex Colpo 3)

                    # BARRIERA MATEMATICA ANTI-DOPPIONE
                    if ambata == abbinamento or ambata in [n1, n2] or abbinamento in [n1, n2]:
                        ambata = (n1 + n2) % 90 or 90
                        abbinamento = (ambata + 45) % 90 or 90
                    
                    if ambata == abbinamento:
                        abbinamento = (ambata + 1) % 90 or 90

                    previsione = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [ambata, abbinamento]
                    }

                    if dist == 15:
                        grezzo_nuovi.append(previsione)
                    elif dist == 30:
                        grezzo_colpo2.append(previsione)

    # 4. Fase di Aggregazione e Pulizia Duplicati
    tabellone_nuovi = aggrega_previsioni(grezzo_nuovi, "180%")
    tabellone_colpo2 = aggrega_previsioni(grezzo_colpo2, "172%")

    # 5. Paracadute di Emergenza (solo in caso di tabelloni vuoti)
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

    # Output finale pulito per risultati_v4.json (Colpo 3 eliminato dal dizionario)
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6],
            "colpo2": tabellone_colpo2[:6],
            "colpo3": []
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("=== FINALE: MOTORE FILTRATO E COMPATTATO! ===")

if __name__ == "__main__":
    esegui_elaborazione_motore()
