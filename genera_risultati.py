import json
import datetime
from itertools import combinations

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

# ===== CARICAMENTO DATI =====
try:
    with open("estrazioni.json", encoding="utf-8") as f:
        estrazioni = json.load(f)
except FileNotFoundError:
    print("Errore: estrazioni.json non trovato.")
    exit()

# Caricamento risultati precedenti (Memoria)
try:
    with open("risultati.json", encoding="utf-8") as f:
        vecchi = json.load(f)
        v_ambi = {r: d["ambo"] for r, d in vecchi.get("ruote", {}).items()}
        v_count = {r: d.get("countdown", 5) for r, d in vecchi.get("ruote", {}).items()}
        v_ultime = {r: d.get("ultima", []) for r, d in vecchi.get("ruote", {}).items()}
except:
    v_ambi, v_count, v_ultime = {}, {}, {}

risultati = {
    "ultimo_aggiornamento": datetime.datetime.now().isoformat(),
    "ruote": {}, 
    "giocate": [], 
    "jolly": {}
}

# --- FUNZIONI TECNICHE ---
def vertibile(n):
    s = str(n).zfill(2)
    v = int(s[::-1])
    if v > 90: v = n 
    if n % 10 == n // 10:
        v = (n // 10) * 10 + 9 if (n // 10) < 9 else 89
    return v

def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

# --- ANALISI CORE V3.1 ---
for ruota in RUOTE:
    if ruota not in estrazioni: continue
    estr_r = estrazioni[ruota]
    ultime_estr = estr_r[-1] # L'estrazione più recente nel file JSON

    f_b = calcola_freq(estr_r[-18:])
    f_m = calcola_freq(estr_r[-540:])
    
    # Calcolo Score equilibrato
    score_num = {n: (f_b.get(n,0)*3.2 + f_m.get(n,0)*1.2) for n in range(1,91)}
    candidati = sorted([n for n in range(1, 91) if n not in ultime_estr], key=lambda x: score_num[x], reverse=True)[:20]
    
    # Selezione Ambo Top
    miglior_ambo = [candidati[0], candidati[1]]
    miglior_score = round(score_num[candidati[0]] + score_num[candidati[1]], 2)

    # --- LOGICA COUNTDOWN INTELLIGENTE ---
    vecchio_ambo = v_ambi.get(ruota, [])
    vecchia_ultima = v_ultime.get(ruota, [])
    countdown_attuale = v_count.get(ruota, 5)

    if miglior_ambo == vecchio_ambo:
        # Se l'ambo è lo stesso, controlla se l'estrazione è cambiata
        if ultime_estr != vecchia_ultima:
            # Nuova estrazione rilevata -> scalo di 1
            nuovo_count = max(0, countdown_attuale - 1)
        else:
            # Stessa estrazione -> mantengo il numero attuale
            nuovo_count = countdown_attuale
    else:
        # L'ambo è cambiato -> resetto a 5
        nuovo_count = 5

    risultati["ruote"][ruota] = {
        "ultima": ultime_estr, 
        "ambo": miglior_ambo, 
        "vertibili": [vertibile(miglior_ambo[0]), vertibile(miglior_ambo[1])],
        "score": miglior_score,
        "countdown": nuovo_count
    }

# Classifica per la Dashboard
top_s = sorted(risultati["ruote"].items(), key=lambda x: x[1]["score"], reverse=True)
for r, d in top_s[:3]:
    risultati["giocate"].append({"ruota": r, "ambo": d["ambo"]})

risultati["jolly"] = {"ruota": "Napoli", "ambo": top_s[0][1]["ambo"], "vert": top_s[0][1]["vertibili"]}

# Salvataggio
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print(f"✅ Analisi completata alle {datetime.datetime.now().strftime('%H:%M:%S')}")
