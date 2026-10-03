import datetime

def calcola_regina_concentrato(primo_estratto_bari):
    """
    Algoritmo Regina Concentrato V8 - Configurazione Laboratorio Locale
    Ruota Unica: BARI | Configurazione: FISSO +31 | 3 Ambi Secchi Ottimizzati
    """
    # 1. Calcolo dell'Ambata Principale (Fisso +31 con Fuori 90)
    ambata = primo_estratto_bari + 31
    if ambata > 90:
        ambata -= 90
        
    # 2. Calcolo dei 3 Abbinamenti Storici Ottimizzati per Bari (+9, +20, +74)
    passi_abbinamenti = [9, 20, 74]
    ambi_secchi = []
    
    for passo in passi_abbinamenti:
        abbinamento = ambata + passo
        if abbinamento > 90:
            abbinamento -= 90
        # Nel caso assurdo in cui l'abbinamento coincida con l'ambata, applica un correttivo (+1)
        if abbinamento == ambata:
            abbinamento = (abbinamento + 1) if abbinamento < 90 else 1
        ambi_secchi.append((ambata, abbinamento))
        
    return ambata, ambi_secchi

if __name__ == "__main__":
    # Input dell'estrazione del 3 Ottobre 2026
    # Bari: 13 - 60 - 19 - 29 - 56 (Il primo estratto è 13)
    primo_estratto_bari_stasera = 13
    
    ambata_risultato, ambi_risultato = calcola_regina_concentrato(primo_estratto_bari_stasera)
    
    # Stampa del pannello di controllo del Laboratorio Locale
    print("=" * 60)
    print("         LOTTO INTELLIGENCE V8 - AMBIENTE LABORATORIO PC       ")
    print("             LOGICA AGGIORNATA: REGINA CONCENTRATO             ")
    print("=" * 60)
    print(f"Data Elaborazione: {datetime.date.today().strftime('%d/%m/%Y')}")
    print(f"Ruota Unica di Gioco: BARI")
    print(f"Input (1° Estratto Bari): {primo_estratto_bari_stasera}")
    print("-" * 60)
    print(f"🔥 AMBATA PRINCIPALE: {ambata_risultato}")
    print("-" * 60)
    print("🎯 I 3 AMBI SECCHI IN CORSO (SU BARI):")
    for i, ambo in enumerate(ambi_risultato, 1):
        print(f"   Ambo Secco {i}: {ambo[0]} - {ambo[1]}")
    print("-" * 60)
    print("🛡️  PROTOCOLLO: 1° Colpo (Martedì 06/10) solo STUDIO. NON GIOCARE.")
    print("   Ingresso Reale programmato al 2° Colpo (Giovedì 08/10).")
    print("=" * 60)
