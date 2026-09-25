import json
import os

def fuori_90(numero):
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def calcola_diametrale(numero):
    if numero <= 45: return numero + 45
    return numero - 45

def super_ottimizzazione_globale():
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    archivio_pulito = {k.upper(): v for k, v in archivio.items() if isinstance(v, list) and len(v) > 0}
    ruote_disponibili = [r for r in archivio_pulito.keys() if r != "NAZIONALE"]
    
    if not ruote_disponibili:
        print("Nessuna ruota valida trovata nell'archivio.")
        return

    # CORREZIONE BUG CHIAVE: prendiamo correttamente il primo nome stringa della lista
    nome_prima_ruota = ruote_disponibili[0]
    tot_estrazioni = len(archivio_pulito[nome_prima_ruota])
    classifica_combinazioni = []

    print(f"🔬 SUPER OTTIMIZZAZIONE GLOBALE VELOCE SU {tot_estrazioni} ESTRAZIONI...")
    print("Analisi ottimizzata di tutte le coppie possibili in corso...")

    # Pre-calcoliamo le estrazioni come liste di interi per velocizzare i cicli di 4 volte
    database_numerico = {}
    for r in ruote_disponibili:
        database_numerico[r] = []
        for estrazione in archivio_pulito[r]:
            if isinstance(estrazione, list):
                database_numerico[r].append([int(n) for n in estrazione[:5]])
            else:
                database_numerico[r].append([])

    # Ciclo sulle coppie di ruote
    for r_base in ruote_disponibili:
        estrazioni_base = database_numerico[r_base]
        
        for r_recupero in ruote_disponibili:
            if r_base == r_recupero: continue
            estrazioni_recupero = database_numerico[r_recupero]
            
            for fisso in range(1, 91):
                vincite_ambata = 0
                vincite_ambo = 0
                totale_previsioni = 0

                # Ottimizzazione colpi
                for i in range(tot_estrazioni - 9):
                    if i >= len(estrazioni_base) or i >= len(estrazioni_recupero): break
                    if not estrazioni_base[i]: continue
                    
                    primo_numero = estrazioni_base[i][0]
                    ambata = fuori_90(primo_numero + fisso)
                    abbinamento = calcola_diametrale(ambata)
                    
                    totale_previsioni += 1
                    vinta_ambata = False
                    vinto_ambo = False

                    for colpo in range(1, 10):
                        idx = i + colpo
                        if idx >= tot_estrazioni or idx >= len(estrazioni_base) or idx >= len(estrazioni_recupero): break
                        
                        num_base_futuri = estrazioni_base[idx]
                        num_recu_futuri = estrazioni_recupero[idx]

                        if not num_base_futuri or not num_recu_futuri: continue

                        if not vinta_ambata and ((ambata in num_base_futuri) or (ambata in num_recu_futuri)):
                            vincite_ambata += 1
                            vinta_ambata = True

                        if not vinto_ambo:
                            if (ambata in num_base_futuri and abbinamento in num_base_futuri) or (ambata in num_recu_futuri and abbinamento in num_recu_futuri):
                                vincite_ambo += 1
                                vinto_ambo = True

                if totale_previsioni > 0 and vincite_ambo > 0:
                    classifica_combinazioni.append({
                        "ruota_1": r_base,
                        "ruota_2": r_recupero,
                        "fisso": fisso,
                        "perc_ambata": (vincite_ambata / totale_previsioni) * 100,
                        "perc_ambo": (vincite_ambo / totale_previsioni) * 100,
                        "ambi_totali": vincite_ambo
                    })

    classifica_combinazioni.sort(key=lambda x: x["perc_ambo"], reverse=True)
    top_5 = classifica_combinazioni[:5]

    print("=" * 70)
    print("🏆 CLASSIFICA ASSOLUTA TOP 5 - LOTTO INTELLIGENCE V8 🏆")
    print("=" * 70)
    for idx, combo in enumerate(top_5, 1):
        print(f"{idx}° POSTO: {combo['ruota_1']} - {combo['ruota_2']} | Fisso: +{combo['fisso']}")
        print(f"   Ambata: {combo['perc_ambata']:.2f}% | Ambi Vinti: {combo['ambi_totali']} ({combo['perc_ambo']:.2f}%)")
        print("-" * 70)

if __name__ == "__main__":
    super_ottimizzazione_globale()
